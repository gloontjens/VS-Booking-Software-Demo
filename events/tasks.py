from .models import Event, Reminder, FormAutomatedEmail, FormHtml, Contact, Client, Global, Activity, MusicianEvent
from django.shortcuts import get_object_or_404
from datetime import datetime, date, timezone
from dateutil.relativedelta import relativedelta
from .form_dict import make_dict
from django.template import Template, Context
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from .views import add_action, process_due_dates, process_auto_reminders, process_update_flags, check_gcal
from io import BytesIO
from xhtml2pdf import pisa
import ftplib
import os
import struct
import socket
import select
from django.conf import settings



def internet_connected(to='8.8.8.8'):
    ping_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
    checksum = 49410
    header = struct.pack('!BBHHH', 8, 0, checksum, 0x123, 1)
    data = b'BCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwx'
    header = struct.pack(
        '!BBHHH', 8, 0, checksum, 0x123, 1
    )
    packet = header + data
    ping_socket.sendto(packet, (to, 1))
    inputready, _, _ = select.select([ping_socket], [], [], 1.0)
    if inputready == []:
        return False
    _, address = ping_socket.recvfrom(2048)
    return True


@db_periodic_task(crontab(minute='0,22', hour='7,8,9'))
def events_daily_automation():
    
    #if no internet connection then don't bother, and don't mark last_automated as today
    if not internet_connected():
        print("internet not connected")
        return
    else:
        print("internet connected")
    
    #if automation already run today, then don't run again until tomorrow
    today = date.today()
    this = Global.objects.get(pk=1)
    if this.last_automated == today:
        return
    else:
        this.last_automated = today
        this.save()
    
    #pull up each automatic reminder that's not done, not archived event,
    #    not past event, with reminder being in the range of 5dys ago to 5dys future.

    fivedayspast = today - relativedelta(days=5)
    fivedaysfuture = today + relativedelta(days=5)

    todos = Reminder.objects.filter(date__range=[fivedayspast, fivedaysfuture]).exclude(
                done=True).exclude(disb=True).exclude(
                event__date__lt=today).exclude(
                auto=False).exclude(
                event__event_archived=True).order_by('date')
                
    print(todos)
    
    #loop through each, determining what type (name) and doing appropriate code
    #    to send appropriate email or whatever needs to be done
    #    Then, set appropriate flags for each type (on assoc event), and also
    #    save a record of this in FormAutomatedEmail, and finally mark this reminder as done
    for todo in todos:
        event = get_object_or_404(Event, pk=todo.event_id)
        thisbody, subject, thissubject, to, pdf, action = '', '', '', '', '', ''
        sendnow, send_1, send_2, send_3 = False, False, False, False
        giveup, done, nothing, skip_send = False, False, False, False
        daysleft = (todo.date - date.today()).days
        atype = ""
        
        print(todo.name)
        print(todo.date)
        print(daysleft)
        
        if (todo.name == 'Send hold notice'):
            #easy, send one notice on actual date and nothing else.  Done.
            if daysleft <= 0:
                send_1 = True
                atype = "hold_initial"
                done = True
                action = "Hold notice was sent"
                #no assc flags need marking for a hold-sent reminder done
                #other types will require a flag or two to be marked when a reminder done
            else:
                nothing = True
                
        if (todo.name == 'Hold event indefinitely'):
            #send_1 3 days before (which is a actually 10 days before event's date)
            #send_2 1 day before (which is actually a week before event's date)
            #giveup when one day past.  never mark done here.
            if daysleft == 3 or daysleft == 2: #send_1
                send_1 = True
                atype = "hold_due_soon"
                action = "Hold-due-soon reminder sent"
            elif daysleft == 1 or daysleft == 0: #send_2
                send_2 = True
                atype = "hold_due_now"
                action = "Hold-due-now reminder sent"
            elif daysleft <= -1:
                giveup = True
                atype = "hold_giveup"
                action = "Hold-expired notice sent to Janie"
            else:
                nothing = True
            
        if (todo.name == 'Hold event until this date'):
            #send_1 3 days before, send_2 1 day before.
            #giveup when 1 day past.  never mark done here.
            if daysleft == 3 or daysleft == 2: #send_1
                send_1 = True
                atype = "hold_due_soon"
                action = "Hold-due-soon reminder sent"
            elif daysleft == 1 or daysleft == 0: #send_2
                send_2 = True
                atype = "hold_due_now"
                action = "Hold-due-now reminder sent"
            elif daysleft <= -1: #giveup
                giveup = True
                atype = "hold_giveup"
                action = "Hold-expired notice sent to Janie"
            else:
                nothing = True
            
        if (todo.name == 'Send Contract'):  #don't need to wait for due date       
            #send_1 now only, mark done
            if daysleft <= 1:
                send_1 = True
                atype = "contract_initial"
                done = True
                action = "Contract-signing request was sent"
                #assc flag need marking for a send-contract reminder done
                event.flag_contract_sent = True
                event.contract_sentdate = today
                event.event_reminders_done = False
                process_auto_reminders(event)
                process_due_dates(event)
                process_update_flags(event)
                event.event_reminders_done = True
                event.save()
                check_gcal(event, False)
            else:
                nothing = True
                
        if (todo.name == 'Receive signed contract'):
            #send_1 3 days before, send_2 1 day before.
            #giveup when 1 day past.  never mark done here.
            if daysleft == 3 or daysleft == 2: #send_1
                send_1 = True
                atype = "contract_due_soon"
                action = "Contract-due-soon reminder sent"
            elif daysleft == 1 or daysleft == 0: #send_2
                send_2 = True
                atype = "contract_due_now"
                action = "Contract-due-now reminder sent"
            elif daysleft <= -1: #giveup
                giveup = True
                atype = "contract_giveup"
                action = "Contract-expired notice sent to Janie"
            else:
                nothing = True
            
        if (todo.name == 'Send receipt for completed contract'):
            #this only runs if client sent in contract manually (rare case, if ever)
            #so if contract rcvd but not rcpt yet, send_1 now and mark done
            #can be done earlier than due date, that's fine
            if event.flag_contract_rcvd and not event.flag_contract_rcpt:
                send_1 = True
                atype = "contract_receipt"
                action = "Contract-completed receipt sent"
                done = True
                #assc flag need marking for a contract receipt done
                event.flag_contract_rcpt = True
                event.contract_rcptdate = today
                event.event_reminders_done = False
                process_auto_reminders(event)
                process_due_dates(event)
                process_update_flags(event)
                event.event_reminders_done = True
                event.save()
                check_gcal(event, False)
            else:
                nothing = True
            
        if (todo.name == 'Send Deposit request'): #dont need to wait for duedate, but
                                                    # do wait for contract request to be sent first
            #send_1 now only, mark done
            if (event.flag_contract_sent == True and event.contract_sentdate != today) or daysleft <= 0:
                #skip if client already marked sending check...
                if Client.objects.filter(event=event.id).exists():
                    client = get_object_or_404(Client, event=event.id)
                    if client.paid_deposit and (not client.paid_online):
                        skip_send = True
                send_1 = True
#                 if event.deposit_senddate == event.final_senddate:
#                     skip_send = True
                atype = "deposit_initial"
                done = True
                action = "Deposit request was sent"
                #assc flag need marking for a send-deposit reminder done
                event.flag_deposit_sent = True
                event.deposit_sentdate = today
                event.event_reminders_done = False
                process_auto_reminders(event)
                process_due_dates(event)
                process_update_flags(event)
                event.event_reminders_done = True
                event.save()
                check_gcal(event, False)
            else:
                nothing = True
            
        if (todo.name == 'Receive paid deposit'):
            #send_1 4 days before, send_2 1 day before.
            #giveup when 1 day past.  never mark done here.
            #if client marked on portal that they're sending a check, then
            #    don't actually send deposit_due_soon or deposit_due_now
            if Client.objects.filter(event=event.id).exists():
                client = get_object_or_404(Client, event=event.id)
                if client.paid_deposit and (not client.paid_online):
                    skip_send = True
            if daysleft == 4 or daysleft == 3: #send_1
                send_1 = True
                atype = "deposit_due_soon"
                action = "Deposit-due-soon reminder sent"
            elif daysleft == 1 or daysleft == 0: #send_2
                send_2 = True
                atype = "deposit_due_now"
                action = "Deposit-due-now reminder sent"
            elif daysleft <= -1: #giveup
                giveup = True
                skip_send = False
                atype = "deposit_giveup"
                action = "Deposit-past-due notice sent to Janie"
            else:
                nothing = True
            
        if (todo.name == 'Send receipt for paid deposit'):
            #if deposit rcvd but not rcpt yet, send_1 now and mark done
            #can be done earlier than due date, that's fine
            #if this is executed, it means event is automated but client paid by
            #    check (if automated & credit card, receipt will be done by client routines)
            #        (if not automated, existing email routines do the receipt pdf/ftp)
            #    so, in this case, we need to generate the pdf/ftp for client to
            #    review the receipt for their mailed check.  We'll do that down below
            if event.flag_deposit_rcvd and not event.flag_deposit_rcpt:
                send_1 = True
                atype = "deposit_receipt"
                action = "Deposit-received receipt sent"
                done = True
                #assc flag need marking for a deposit receipt done
                event.flag_deposit_rcpt = True
                event.deposit_rcptdate = today
                event.event_reminders_done = False
                process_auto_reminders(event)
                process_due_dates(event)
                process_update_flags(event)
                event.event_reminders_done = True
                event.save()
                check_gcal(event, False)
            else:
                nothing = True
            
        if (todo.name == 'Send Final Payment request'):
            #send_1 now only, mark done
            #if client marked on portal that they're sending a check FOR FULL PAY, then
            #    don't actually send final_payment_initial -- it'll be marked done that way
            #    but Janie will still mark rcvd reminder manually when she gets check, for
            #    both deposit and final (making up the total)
            if Client.objects.filter(event=event.id).exists():
                client = get_object_or_404(Client, event=event.id)
                if (client.paid_total or client.paid_final) and (not client.paid_online):
                    skip_send = True
            if daysleft <= 0:
                send_1 = True
                atype = "final_payment_initial"
                done = True
                action = "Final payment request was sent"
                #assc flag need marking for a send-finalpay reminder done
                event.flag_final_payment_sent = True
                event.final_sentdate = today
                event.event_reminders_done = False
                process_auto_reminders(event)
                process_due_dates(event)
                process_update_flags(event)
                event.event_reminders_done = True
                event.save()
                check_gcal(event, False)
            else:
                nothing = True
            
        if (todo.name == 'Receive paid final payment'):
            #send_1 4 days before, send_2 1 day before.
            #giveup when 1 day past.  never mark done here.
            #if client marked on portal that they're sending a check, then
            #    don't actually send final_payment_due_soon or final_payment_due_now
            if Client.objects.filter(event=event.id).exists():
                client = get_object_or_404(Client, event=event.id)
                if client.paid_final and (not client.paid_final_online):
                    skip_send = True
            if daysleft == 4 or daysleft == 3: #send_1
                send_1 = True
                atype = "final_payment_due_soon"
                action = "Final-payment-due-soon reminder sent"
            elif daysleft == 1 or daysleft == 0: #send_2
                send_2 = True
                atype = "final_payment_due_now"
                action = "Final-payment-due-now reminder sent"
            elif daysleft <= -1: #giveup
                giveup = True
                skip_send = False
                atype = "final_payment_giveup"
                action = "Final-payment-past-due notice sent to Janie"
            else:
                nothing = True
            
        if (todo.name == 'Send receipt for paid final payment'):
            #if final_payment rcvd but not rcpt yet, send_1 now and mark done
            #can be done earlier than due date, that's fine
            #if this is executed, it means event is automated but client paid by
            #    check (if automated & credit card, receipt will be done by client routines)
            #        (if not automated, existing email routines do the receipt pdf/ftp)
            #    so, in this case, we need to generate the pdf/ftp for client to
            #    review the receipt for their mailed check.  We'll do that down below
            if event.flag_final_payment_rcvd and not event.flag_final_payment_rcpt:
                send_1 = True
                atype = "final_payment_receipt"
                action = "Final-payment-received receipt sent"
                done = True
                #assc flag need marking for a contract receipt done
                event.flag_final_payment_rcpt = True
                event.final_rcptdate = today
                event.event_reminders_done = False
                process_auto_reminders(event)
                process_due_dates(event)
                process_update_flags(event)
                event.event_reminders_done = True
                event.save()
                check_gcal(event, False)
            else:
                nothing = True
            
        if (todo.name == 'Send request for music list'):
            #send_1 now only, mark done
            if daysleft <= 0:
                send_1 = True
                atype = "music_list_initial"
                done = True
                action = "Music List request was sent"
                #assc flag need marking for a send-musiclist reminder done
                event.flag_music_list_sent = True
                event.music_list_sentdate = today
                event.event_reminders_done = False
                process_auto_reminders(event)
                process_due_dates(event)
                process_update_flags(event)
                event.event_reminders_done = True
                event.save()
                check_gcal(event, False)
            else:
                nothing = True
            
        if (todo.name == 'Receive music list'):
            #send_1 3 days before, send_2 1 day before.
            #giveup when 1 day past.  never mark done here.
            if daysleft == 3 or daysleft == 2: #send_1
                send_1 = True
                atype = "music_list_due_soon"
                action = "Music-list-due-soon reminder sent"
            elif daysleft == 1 or daysleft == 0: #send_2
                send_2 = True
                atype = "music_list_due_now"
                action = "Music-list-due-now reminder sent"
            elif daysleft <= -1: #giveup
                giveup = True
                atype = "music_list_giveup"
                action = "Music-list-past-due notice sent to Janie"
            else:
                nothing = True
            
        if (todo.name == 'Send final confirmation of event'):
            #send_1 now only, mark done
            if daysleft <= 0:
                send_1 = True
                atype = "final_confirmation_initial"
                done = True
                action = "Final Event Confirmation request was sent"
                #assc flag need marking for a send-final-confirmation reminder done
                event.flag_final_confirmation_sent = True
                event.confirmation_sentdate = today
                event.event_reminders_done = False
                process_auto_reminders(event)
                process_due_dates(event)
                process_update_flags(event)
                event.event_reminders_done = True
                event.save()
                check_gcal(event, False)
            else:
                nothing = True
            
        if (todo.name == 'Receive reply to final confirmation'):
            #send_1 3 days before, send_2 1 day before.
            #giveup when 1 day past.  never mark done here.
            if daysleft == 3 or daysleft == 2: #send_1
                send_1 = True
                atype = "final_confirmation_due_soon"
                action = "Final-Confirmation-due-soon reminder sent"
            elif daysleft == 1 or daysleft == 0: #send_2
                send_2 = True
                atype = "final_confirmation_due_now"
                action = "Final-Confirmation-due-now reminder sent"
            elif daysleft <= -1: #giveup
                giveup = True
                atype = "final_confirmation_giveup"
                action = "Final-Confirmation-past-due notice sent to Janie"
            else:
                nothing = True
             
        if (todo.name == 'Wait for all musicians to confirm fact sheets'):
            #this one is tricky.  If not all replied, could we remind just one player?
            #or is it better/easier to just alert Janie when due date passed w/o all replies?
            #we can check MusicianEvent's gotit field to see who has responded
            numgotit = MusicianEvent.objects.filter(event=event, gotit=True).count()
            numplaying = event.ensemble_number
            if (event.flag_fact_sheets_rcvd) or (numgotit == numplaying):
                #got them all already, reminder will be marked as done by views.py process_auto_reminders next load
                #set reminder as done here too, and no email really necessary to Janie
                send_1 = True
                atype = "fact_sheets_received"
                action = "All musicians confirmed Fact Sheet"
                done = True
                event.flag_fact_sheets_rcvd = True
                event.fact_sheets_rcvddate = today
                event.event_reminders_done = False
                process_auto_reminders(event)
                process_due_dates(event)
                process_update_flags(event)
                event.event_reminders_done = True
                event.save()
                check_gcal(event, False)
            else:
                #got none or some.  Send_1 day-of.  Giveup when 1 day past.  Never mark done.
                #first, make list of musicians that have NOT responded gotit yet
                mlist=[]
                nlist=[]
                notgotits = MusicianEvent.objects.filter(event=event, placeholder=False, yes=True, no=False, gotit=False)
                for notgotit in notgotits:
                    mlist.append(notgotit.musician.email)
                    nlist.append(notgotit.musician.name)
                if daysleft == 1 or daysleft == 0:
                    send_1 = True
                    atype = "fact_sheets_reminder"
                    action = "Musician(s) were reminded to respond to Fact Sheet"
                elif daysleft <= -1: #giveup
                    giveup = True
                    atype = "fact_sheets_giveup"
                    nlist2 = ", ".join(nlist)
                    action = "Fact-Sheets-confirmation-past-due notice sent to Janie, no reply from " + nlist2
                else:
                    nothing = True
                    
                
        
        #process send_1, 2, 3, giveup, type...  if any done before, don't do again
        newtodo = get_object_or_404(Reminder, event_id= event.id, name = todo.name)
        if send_1 and not newtodo.send_1:
            newtodo.send_1 = True
            sendnow = True
        if send_2 and not newtodo.send_2:
            newtodo.send_2 = True
            sendnow = True
        if send_3 and not newtodo.send_3:
            newtodo.send_3 = True
            sendnow = True
        if giveup and not newtodo.giveup:
            newtodo.giveup = True
            sendnow = True
        if done:
            newtodo.done = True
        newtodo.save()
        
        #send appropriate email now.  if giveup type, it goes to Janie not client
        if atype and sendnow: #don't send anything if not required :)
            #the below three lines force an update so the due dates for things like deposit/final
            #    are properly calculated before we generate the emails that might include due dates
            #    **temp disabled, because it causes duplicate reminders to be saved
#             event.event_reminders_done = False
#             process_due_dates(event)
#             process_auto_reminders(event)
#             event.save()

            
            atype = 'automation_' + atype
            print(atype)
            if skip_send:
                print('skipped')
            else:
                print('sent!')
            formhtml = FormHtml.objects.get(name=atype)
            full_dict = make_dict(event)
            t = Template(formhtml.subject)
            c = Context(full_dict)
            thissubject = t.render(c)
            if event.contact:
                contact = get_object_or_404(Contact, name=event.contact)
                thisaddr = contact.email
            else:
                thisaddr = event.contact_email
            if 'giveup' in atype:
                thisaddr = settings.EMAIL_MAIN 
            t = Template(formhtml.body)
            c = Context(full_dict)
            thisbody = t.render(c)
            if atype == "automation_fact_sheets_giveup":
                thisbody = thisbody + "<br /><br />No response yet from " + nlist2 + "<br /><br />"
            subject, from_email, to = thissubject, settings.EMAIL_AUTO, thisaddr
            html_content = thisbody
            text_content = strip_tags(html_content)
            if atype != "automation_fact_sheets_reminder":
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to, settings.EMAIL_RECORDS])
            else:
                mlist.append('gclhome@gmail.com')
                msg = EmailMultiAlternatives(subject, text_content, from_email, mlist)
            msg.attach_alternative(html_content, "text/html")
            if (atype != "automation_fact_sheets_received") and (not skip_send):
                msg.send()
                #save to IMAP Sent folder!
                message = str(msg.message())
                imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP)
                imap.login(settings.EMAIL_HOST_IMAP_USER, settings.EMAIL_HOST_IMAP_PASSWORD)
                imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
                imap.logout() 
                
            #if deposit or finalpay receipt, save/upload pdf too, because if automation has to send receipt it
            #    means that event is automated but client paid via check so Janie marked rcvd manually, now receipt
            #    is being sent automatically for the first time
            if todo.name == 'Send receipt for paid deposit' or todo.name == 'Send receipt for paid final payment':
                t = Template(formhtml.pdf)
                c = Context(full_dict)
                pdf = t.render(c)
                if todo.name == 'Send receipt for paid deposit':
                    file_name = "Deposit-payment-receipt-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
                else:
                    if event.deposit_fee == 0 or event.deposit_fee == 0.00:
                        file_name = "Full-payment-receipt-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
                    else:
                        file_name = "Final-payment-receipt-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
                result = BytesIO()
                file = open(file_name, "wb")
                pdf = pisa.pisaDocument(BytesIO(pdf.encode("UTF-8")), file)
                file.close()
                file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "", file_name)
                session = ftplib.FTP_TLS(settings.FTP_ADDR, settings.FTP_LOGIN, settings.FTP_PWD)
                fileftp = open(file_path, 'rb')
                session.cwd('pdfs')
                session.storbinary('STOR ' + file_name, fileftp)
                fileftp.close()
                session.quit()
                
                
            
               
            #save record of what was sent
            if atype != "automation_fact_sheets_received" and (not skip_send):
                newform = FormAutomatedEmail(event = event)
                newform.sentdate = today
                newform.body = thisbody
                newform.subject = subject
                newform.addr = to
                newform.pdf = pdf
                newform.save()
                print('SENT: ' + atype + ' for ' + event.name)

            #now sent, so add activity,then mark done (if asked to) and save reminder changes
            if not skip_send:
                action = '[A] ' + action
                add_action(action, event, today)
            if nothing:
                nothing = True
#            todo.save()

        #    moved down here, because otherwise it causes duplicate reminders to be saved
#         event.event_reminders_done = False
#         process_due_dates(event)
#         process_auto_reminders(event)
#         event.event_reminders_done = True
#         event.save()



    
    
#also, we pre-process all upcoming events once a day
@db_periodic_task(crontab(minute='5', hour='6,7,8'))
def events_daily_automation_midnight():

    today = date.today()    
    events = Event.objects.filter(date__gte=today).exclude(
        event_archived=True).order_by('date','start_time')
        
    for event in events:
        process_due_dates(event)
        process_auto_reminders(event)
        process_update_flags(event)
        event.event_reminders_done = True
        event.save()
        check_gcal(event, False)

    #Also, each day, reset the sidecal calendar and main calendar to today's month
    this = Global.objects.get(pk=1)
    this.last_updated = today   
    year = datetime.now().year
    month = datetime.now().month
    this.mycal_year = year
    this.mycal_month = month
    this.sidecal_year = year
    this.sidecal_month = month
    this.auto_btn_side = False
    this.auto_btn = False
    this.save()

    
    
    
    
    
    
    