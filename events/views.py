from __future__ import print_function
from django.shortcuts import render, get_object_or_404
from .forms import TransitionForm, SearchForm, ESigForm, FormRateChart, ReminderFormAuto, AddForm, ActivityForm, VenueForm, ClientEmailForm, ClientForm, ContactForm, DayofcontactForm, SigForm, ReminderForm, FormEmailForm, FormHtmlForm, MusicianForm
from django.shortcuts import redirect
from _decimal import ROUND_HALF_UP
from django.utils import timezone
from django.utils.html import format_html, urlencode
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.core import mail
from django.template.loader import render_to_string, get_template
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.core.mail import EmailMultiAlternatives
from .models import BulkConvert, MusicList, FormAutomatedEmail, FormEmail, EventTemp, MusicRequest, Musician, Header, Client, MusicianEvent, MusicianInstrument, Event, Venue, Activity, EventType, FormHtml, Ensemble, Contact, DayofContact, RateChart, Reminder, Global
from .models import PaymentsReceived, PaymentsDue, ESig
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal
from phone_field.templatetags.phone import raw_phone, format_phone
from django.contrib import messages
from datetime import datetime, timedelta, date
import datetime
from datetime import time
import calendar
from dateutil.relativedelta import relativedelta
from django.forms.forms import Form
from django.core import serializers
from django.conf import settings
from .form_dict import make_dict
from django.template import Template, Context
from django.db.models import F 
from array import *
# from templated_email import send_templated_mail
import pickle
import os.path
import os
from dotenv import load_dotenv
from pyasn1.compat.octets import null
from encodings import undefined
#from builtins import True
#from builtins import None
# from events.tasks_code import result
load_dotenv()
from django.utils.html import format_html

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.oauth2.credentials
import google_auth_oauthlib.flow
import requests


from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
import re
from django.db.models import Q
from django.utils.html import conditional_escape as esc
from django.utils.safestring import mark_safe
from itertools import groupby
from calendar import HTMLCalendar
from calendar import day_abbr, month_name
from io import BytesIO
from xhtml2pdf import pisa
from django.views.generic import View
from urllib.request import quote
import urllib.parse
from events.utils import render_to_pdf, render_to_pdf_file
import ftplib
from urllib.parse import quote
from pip._internal import locations
from django.db.models.functions.window import Rank
from _hashlib import new
from ool import ConcurrentUpdate
import imaplib, time
from events import variables
import ssl










def fakeajax(request):
    if request.is_ajax():
        data = {'dummy':'dummy'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
    


def reports_calc(datetouse, future):
    today = datetouse
    pweek = today - relativedelta(days=7)
    nweek = today + relativedelta(days=7)
    pmonth = today - relativedelta(months=1)
    nmonth = today + relativedelta(months=1)
    p6months = today - relativedelta(months=6)
    n6months = today + relativedelta(months=6)
    pyear = today - relativedelta(years=1)
    nyear = today + relativedelta(years=1)
    thisyear = today.year
    if today.month < 9:
        seasonstart = date(thisyear - 1, 9, 1)
        seasonend = date(thisyear, 8, 31)
    else:
        seasonstart = date(thisyear, 9, 1)
        seasonend = date(thisyear + 1, 8, 31)
    
    
    
    
    periods = []                    #contains each of the search periods
                                    #prevweek, prevmonth,.......
                                    #newxtweek, nextmonth,.......
                                    
    periods.append(Event.objects.filter(date__range=[pweek, today]).exclude(event_archived=True).order_by('pk'))
    periods.append(Event.objects.filter(date__range=[pmonth, today]).exclude(event_archived=True).order_by('pk'))
    periods.append(Event.objects.filter(date__range=[p6months, today]).exclude(event_archived=True).order_by('pk'))
    periods.append(Event.objects.filter(date__range=[pyear, today]).exclude(event_archived=True).order_by('pk'))
    periods.append(Event.objects.filter(date__range=[seasonstart, today]).exclude(event_archived=True).order_by('pk'))
    #.....
    if future:
        periods.append(Event.objects.filter(date__range=[today, nweek]).exclude(event_archived=True).order_by('pk'))
        periods.append(Event.objects.filter(date__range=[today, nmonth]).exclude(event_archived=True).order_by('pk'))
        periods.append(Event.objects.filter(date__range=[today, n6months]).exclude(event_archived=True).order_by('pk'))
        periods.append(Event.objects.filter(date__range=[today, nyear]).exclude(event_archived=True).order_by('pk'))
        periods.append(Event.objects.filter(date__range=[today, seasonend]).exclude(event_archived=True).order_by('pk'))
        #.....
    
    report_events = []              #contains multiple 'each' records to correspond to time period
    
    for period in periods:
        
        each = 0                    #total
        each_lengths = [0,0,0,0,0]  #1hr, 2hr, 3hr, 4hr+, ?
        each_types = [0,0,0,0,0]    #solo, duo, trio, quartet+, ?
        for event in period:
            each += 1
            
            if event.end_time and event.start_time:
                tend = datetime.datetime.combine(today, event.end_time)
                tstart = datetime.datetime.combine(today, event.start_time)
                tdiff = tend - tstart
                duration = tdiff.total_seconds() / 3600
                if duration <= 1:
                    each_lengths[0] += 1
                elif duration <= 2:
                    each_lengths[1] += 1
                elif duration <= 3:
                    each_lengths[2] += 1
                else:
                    each_lengths[3] += 1
            else:
                each_lengths[4] += 1
            
            if event.ensemble_number == 0 or not event.ensemble_number:
                each_types[4] += 1
            elif event.ensemble_number == 1:
                each_types[0] += 1
            elif event.ensemble_number == 2:
                each_types[1] += 1
            elif event.ensemble_number == 3:
                each_types[2] += 1
            else:
                each_types[3] += 1
        
        report_events.append([each, each_lengths, each_types])
        

    report_fees = []              #contains multiple 'each' records to correspond to time period
    
    for period in periods:
        
        each_total = 0              #total $
        each_paid = 0               #paid to all musicians, w/o Glenn & Janie           
        each_profit = 0             #subtracted
        each_types = [0,0,0,0]       #glenn, janie, contracting, cash
        for event in period:
            if event.fee:
                each_total += event.fee
                each_profit += event.fee
            if event.musician_fee and event.ensemble_number:
                each_paid += event.musician_fee * event.ensemble_number
                each_profit -= event.musician_fee * event.ensemble_number
            if event.contracting_fee:
                each_types[2] += event.contracting_fee
            if event.cash_fee:
                each_types[3] += event.cash_fee
            playing = MusicianEvent.objects.filter(event_id=event.id, yes=True, no=False, placeholder=False).order_by('pk') 
            for player in playing:
                if "Janie Spangler" in player.musician.name:
                    if event.musician_fee:
                        each_types[1] += event.musician_fee
                        each_paid -= event.musician_fee
                        each_profit += event.musician_fee
                if "Glenn Loontjens" in player.musician.name:
                    if event.musician_fee:
                        each_types[0] += event.musician_fee
                        each_paid -= event.musician_fee
                        each_profit += event.musician_fee
        
        report_fees.append([each_total, each_paid, each_profit, each_types])
    
    
    return report_events, report_fees
    
def reports_calc_each_musician(datetouse, musician_id):
    today = datetouse
    pmonth = today - relativedelta(months=1)
    nmonth = today + relativedelta(months=1)
    p3months = today - relativedelta(months=3)
    n3months = today + relativedelta(months=3)
    p6months = today - relativedelta(months=6)
    n6months = today + relativedelta(months=6)
    pyear = today - relativedelta(years=1)
    nyear = today + relativedelta(years=1)
    thisyear = today.year
    if today.month < 9:
        seasonstart = date(thisyear - 1, 9, 1)
        seasonend = date(thisyear, 8, 31)
    else:
        seasonstart = date(thisyear, 9, 1)
        seasonend = date(thisyear + 1, 8, 31)
    
    
    periods = []                    #contains each of the search periods
                                    #prevweek, prevmonth,.......
                                    #newxtweek, nextmonth,.......
                                    
    periods.append(MusicianEvent.objects.filter(musician=musician_id).filter(event__date__range=[pmonth, today]).exclude(
        event__event_archived=True).exclude(yes=False).exclude(no=True).order_by('pk'))
    periods.append(MusicianEvent.objects.filter(musician=musician_id).filter(event__date__range=[p3months, today]).exclude(
        event__event_archived=True).exclude(yes=False).exclude(no=True).order_by('pk'))
    periods.append(MusicianEvent.objects.filter(musician=musician_id).filter(event__date__range=[p6months, today]).exclude(
        event__event_archived=True).exclude(yes=False).exclude(no=True).order_by('pk'))
    periods.append(MusicianEvent.objects.filter(musician=musician_id).filter(event__date__range=[pyear, today]).exclude(
        event__event_archived=True).exclude(yes=False).exclude(no=True).order_by('pk'))
    periods.append(MusicianEvent.objects.filter(musician=musician_id).filter(event__date__range=[seasonstart, today]).exclude(
        event__event_archived=True).exclude(yes=False).exclude(no=True).order_by('pk'))
    #......
    periods.append(MusicianEvent.objects.filter(musician=musician_id).filter(event__date__range=[today, nmonth]).exclude(
        event__event_archived=True).exclude(yes=False).exclude(no=True).order_by('pk'))
    periods.append(MusicianEvent.objects.filter(musician=musician_id).filter(event__date__range=[today, n3months]).exclude(
        event__event_archived=True).exclude(yes=False).exclude(no=True).order_by('pk'))
    periods.append(MusicianEvent.objects.filter(musician=musician_id).filter(event__date__range=[today, n6months]).exclude(
        event__event_archived=True).exclude(yes=False).exclude(no=True).order_by('pk'))
    periods.append(MusicianEvent.objects.filter(musician=musician_id).filter(event__date__range=[today, nyear]).exclude(
        event__event_archived=True).exclude(yes=False).exclude(no=True).order_by('pk'))
    periods.append(MusicianEvent.objects.filter(musician=musician_id).filter(event__date__range=[today, seasonend]).exclude(
        event__event_archived=True).exclude(yes=False).exclude(no=True).order_by('pk'))
    #......
    
    return periods


    
def reports_calc_musicians(datetouse):
    
    all_musicians = Musician.objects.all()
    report_musicians = []              #contains multiple musicians:
                                    #name, [[1m #, 1m $], [3m #, 3m $], [6m #, 6m $], etc...]
                                    #nextname, [1m #, 1m $], [3m #, 3m $], [6m #, 6m $], etc...]

    for musician in all_musicians:
        periods = reports_calc_each_musician(datetouse, musician.id)
        sumlist = []
        
        for period in periods:
            name = musician.name
            gigs = 0
            dollars = 0
            for musev in period:
                gigs = gigs + 1
                dollars = dollars + musev.event.musician_fee
            
            sumlist.append([gigs, dollars])
            
        if name != '----------':
            report_musicians.append([name, sumlist])
            
    return report_musicians
    

def reports(request):
    
    today = date.today()
    
    report_events_thisyear, report_fees_thisyear = reports_calc(today, True)
    
    oneyearago = date.today() - relativedelta(years=1)
     
    report_events_1yearago, report_fees_1yearago = reports_calc(oneyearago, False)
 
    twoyearago = date.today() - relativedelta(years=2)
     
    report_events_2yearago, report_fees_2yearago = reports_calc(twoyearago, False)

    report_musicians = reports_calc_musicians(today)
    
    

    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents,  pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()

    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])
        
    return render(request, 'events/reports.html', {'report_events':report_events_thisyear, 
                                                   'report_fees':report_fees_thisyear,
                                                    'report_events_1yearago':report_events_1yearago,
                                                    'report_fees_1yearago':report_fees_1yearago,
                                                    'report_events_2yearago':report_events_2yearago,
                                                    'report_fees_2yearago':report_fees_2yearago,
                                                    'report_musicians':report_musicians,
                                                'soonevents': soonevents, 'soonreminder': soonreminder, 
                                                'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal),
                                                'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount,
                                                'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents})





def sigtest(request):
    form = SigForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            nothing = 1
        else:
            nothing = 1   
            return redirect('/events/')  
    else:
        return render(request, 'events/sigtest.html', {'form': form})
    
def thankyou(request):
    
    
    today = date.today()
    sixtydaysago = today + relativedelta(days=-60)
    
#         
#         soonreminder = Reminder.objects.filter(date__range=[past182days, sevendays]).exclude(
#             done=True).exclude(disb=True).exclude(event__date__lt=today).exclude(name=booking2, date__range=[past182days, sevendays]).exclude(
#             name=booking1, date__range=[past182days, sevendays]).exclude(    
#             event__event_archived=True).order_by('event__pk', 'event__date', 'date')
#         
#         
    
#     oldrems = Reminder.objects.filter(event__date__lt=sixtydaysago)
#     
#     oldacts = Activity.objects.filter(event__date__lt=sixtydaysago)
#     
#     oldemails = FormEmail.objects.filter(event__date__lt=sixtydaysago)
#     print("**************************************************************************")
#     print(oldrems)
#     print("**************************************************************************")
#     print(oldacts)
#     print("**************************************************************************")
#     print(oldemails)
#     print("**************************************************************************")
#     
#     for oldrem in oldrems:
#         oldrem.delete()
#     
#     for oldact in oldacts:
#         oldact.delete()
#         
#     for oldemail in oldemails:
#         oldemail.delete()
# 
#     
    
    
    return HttpResponse('thank you!')

def process_music_list(request, event, cer = ''):
    background = str(request.POST.get('backgrounds'))
    dinner = str(request.POST.get('dinners'))
    reception = str(request.POST.get('receptions'))
    cocktail = str(request.POST.get('cocktails'))
    misc = str(request.POST.get('backgrounds'))
    parent = str(request.POST.get('parents'))
    groomsmen = str(request.POST.get('groomsmens'))
    bridesmaid = str(request.POST.get('bridesmaids'))
    bride = str(request.POST.get('brides'))
    ceremonymusic = str(request.POST.get('ceremonymusics'))
    ceremonymusic_type = str(request.POST.get('ceremonymusics_type'))
    ceremonymusic_when = str(request.POST.get('ceremonymusics_when'))
    recessional = str(request.POST.get('recessionals'))
    parent_custom = str(request.POST.get('parents_custom'))
    groomsmen_custom = str(request.POST.get('groomsmens_custom'))
    bridesmaid_custom = str(request.POST.get('bridesmaids_custom'))
    bride_custom = str(request.POST.get('brides_custom'))
    ceremonymusic_custom = str(request.POST.get('ceremonymusics_custom'))
    recessional_custom = str(request.POST.get('recessionals_custom'))
    recessional_cue = str(request.POST.get('recessionals_cue'))
    parent_custom_notinlist = str(request.POST.get('parents_custom_notinlist'))
    groomsmen_custom_notinlist = str(request.POST.get('groomsmens_custom_notinlist'))
    bridesmaid_custom_notinlist = str(request.POST.get('bridesmaids_custom_notinlist'))
    bride_custom_notinlist = str(request.POST.get('brides_custom_notinlist'))
    ceremonymusic_custom_notinlist = str(request.POST.get('ceremonymusics_custom_notinlist'))
    recessional_custom_notinlist = str(request.POST.get('recessionals_custom_notinlist'))

    if parent == "Other...":
        parent = ""
    if groomsmen == "Other...":
        groomsmen = ""
    if bridesmaid == "Other...":
        bridesmaid = ""
    if bride == "Other...":
        bride = ""
    if ceremonymusic == "Other...":
        ceremonymusic = ""
    if recessional == "Other...":
        recessional = ""
    
    if not event:
        etype = cer.lower()
    else:
        etype = event.event_type_name.lower()
    do_ceremony = do_cocktails = do_reception = do_dinner = do_background = do_misc = False
    if 'ceremony' in etype:
        do_ceremony = True
    if 'cocktail' in etype:
        do_cocktails = True
    if 'reception' in etype:
        do_reception = True
    if 'dinner' in etype:
        do_dinner = True
    if 'background' in etype:
        do_background = True
    if not do_ceremony and not do_cocktails and not do_reception and not do_dinner and not do_background:
        do_misc = True
    
    #assemble into nice format for emailing and pdf
    text = ""
    if do_ceremony:
        text += "<b>Parents: </b>" + parent + " " + parent_custom + " " + parent_custom_notinlist + "<br />"
        if not groomsmen.startswith('No music'):
            text += "<b>Groom/Groomsmen: </b>" + groomsmen + " " + groomsmen_custom + " " + groomsmen_custom_notinlist + "<br />"
        text += "<b>Bridal Party: </b>" + bridesmaid + " " + bridesmaid_custom + " " + bridesmaid_custom_notinlist + "<br />"
        text += "<b>Bride: </b>" + bride + " " + bride_custom + " " + bride_custom_notinlist + "<br />"
        if not ceremonymusic == 'No music needed':
            text += "<b>Ceremony Music: </b>" + ceremonymusic + " " + ceremonymusic_custom + " " + ceremonymusic_custom_notinlist + "&nbsp;&nbsp;"
            if ceremonymusic_type == '':
                ceremonymusic_type = 'no type given'
            if ceremonymusic_when == '':
                ceremonymusic_when = 'no timing given'
            text += "(" + ceremonymusic_type + ", " + ceremonymusic_when + ")<br />"
        text += "<b>Recessional: </b>" + recessional + " " + recessional_custom + " " + recessional_custom_notinlist + "<br />"
        if not recessional_cue:
            text += "<b>Cue for recessional: </b>" + "none given" + "<br />"
        else:
            text += "<b>Cue for recessional: </b>" + recessional_cue + "<br />"
    if do_cocktails:
        text += "<b>Cocktails: </b>" + cocktail + "<br />"
    if do_reception:
        text += "<b>Reception: </b>" + reception + "<br />"
    if do_dinner:
        text += "<b>Dinner: </b>" + dinner + "<br />"
    if do_background:
        text += "<b>Background: </b>" + background + "<br />"
    if do_misc:
        text += "<b>Event music: </b>" + misc + "<br />"
        
    return text


#from imp import reload  
#from .variables import refresh_musiclist

def check_accept_custom(request):
    if request.is_ajax():
        musiclist = request.GET['music_list']
        count = musiclist.count("$25")
        dollars = count * 25
        data = {'dollars':dollars}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")

def get_id_from_value(request):
    if request.is_ajax():
        item = request.GET['item']
        element = request.GET['element']
        
        if element == 'id_event_type_0':
            thisid = get_object_or_404(EventType, name=item).id
        elif element == 'id_ensemble_0':
            thisid = get_object_or_404(Ensemble, name=item).id
        elif element == 'id_location_0':
            thisid = get_object_or_404(Venue, name=item).id
        elif element == 'id_contact_0':
            thisid = get_object_or_404(Contact, name=item).id
        elif element == 'id_dayofcontact_0':
            thisid = get_object_or_404(DayofContact, name=item).id
        elif element == 'id_instrument':
            thisid = get_object_or_404(MusicianInstrument, instrument=item).id
        elif element == 'id_musician':
            thisid = get_object_or_404(Musician, name=item).id
        print(thisid)
        data = {'newid':thisid}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
    

def bulk_convert(request):
    bulktext = BulkConvert.objects.get(pk=1).bulktext
    btlines = bulktext.splitlines()
    
    #for musicians
#     for eachline in btlines:
#         fields = eachline.split("\t")
#         newmus = Musician(name=fields[0])
#         newmus.phone = fields[1]
#         newmus.email = fields[2]
#         newmus.instrument = fields[3]
#         newmus.instrument2 = fields[4]
#         newmus.order = fields[5]
#         newmus.save()   

    #for venues
#     for eachline in btlines:
#         fields = eachline.split("\t")
#         newmus = Venue(name=fields[0])
#         newmus.address = fields[1]
#         newmus.link = fields[2]
#         newmus.order = fields[3]
#         newmus.save()   

    #for contacts
#     for eachline in btlines:
#         fields = eachline.split("\t")
#         newmus = Contact(name=fields[0])
#         newmus.agency = fields[1]
#         newmus.phone = fields[2]
#         newmus.email = fields[3]
#         newmus.order = fields[4]
#         newmus.save()   

    #for dayof-contacts
    for eachline in btlines:
        fields = eachline.split("\t")
        newmus = DayofContact(name=fields[0])
        newmus.phone = fields[1]
        newmus.email = fields[2]
        newmus.order = fields[3]
        newmus.save()   

   
    return HttpResponse("Should be done! (I hope!)")


def check_music_list(request):
    if request.is_ajax():
        name = request.GET['name']
        if name in variables.currentmusiclist:
            onlist = True
        else:
            onlist = False
        data = {'onlist':onlist}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")

  
def client_home(request, eventnum, mode="reg"):
    if mode == 'admin':
        specialadmin = True
        mode = 'reg'
    else:
        specialadmin = False
    #refresh music list!
    listobject = MusicList.objects.get(pk=1)
    variables.currentmusiclist = listobject.list.splitlines()
    
    event = get_object_or_404(Event, pk=eventnum)
    pay_required = not event.waive_payment
    if event.contact:
        email = event.contact.email
    else:
        email = event.contact_email

    if Client.objects.filter(event=event.id).exists():
        client = get_object_or_404(Client, event=event.id)
    else:
        client = Client(event=event)
        client.save()
    if request.method == "POST":
        data = request.POST
        if "goto_event_details" in data:
            if event.ensemble_number == 1:
                musicianplural = "musician"
            else:
                musicianplural = "musicians"
            return render(request, 'events/client_show_details.html', {'event':event, 'musicianplural':musicianplural})
        elif "goto_questions" in data:
            form = ClientEmailForm()
            return render(request, 'events/client_questions.html', {'event':event, 'form':form, 'mode':mode})
        elif "goto_questions_contract" in data:
            form = ClientEmailForm()
            return render(request, 'events/client_questions_contract.html', {'event':event, 'form':form, 'mode':mode})
        elif "goto_questions_submit" in data:
            #process and send new email
            form = ClientEmailForm(request.POST)
            if form.is_valid():
                newclientemail = form.save(commit=True)
                newclientemail.subject = '[from client] ' + newclientemail.subject
                subject, from_email, to = newclientemail.subject, settings.EMAIL_MAIN, settings.EMAIL_MAIN
                html_content = '[from client portal for <a href="'+ settings.WEBSITE + \
                                str(event.id) + '/edit">this event</a>]<br /><br />' + \
                                '[MUST CHANGE REPLY ADDRESS to client email address, given as <b>' + newclientemail.from_email + '</b> !]'
                html_content = html_content + newclientemail.body
                html_content = html_content.replace('\n', '<br />')
                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=[settings.EMAIL_RECORDS])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                #save to IMAP Sent folder!
                message = str(msg.message())
                imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP)
                imap.starttls(ssl_context=ssl.create_default_context())
                imap.login(settings.EMAIL_HOST_IMAP_USER, settings.EMAIL_HOST_IMAP_PASSWORD)
                imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
                imap.logout() 
                
                message="Thank you, your message was sent to us!"
                senderror = False
                return render(request, 'events/client_questions_done.html', {'senderror':senderror, 'mode':mode, 'event':event, 'client':client, 'message':message})

            else:
                message="Sorry, there was an error.  Please try again..."
                senderror = True
                return render(request, 'events/client_questions_done.html', {'senderror':senderror, 'mode':mode, 'event':event, 'client':client, 'message':message})

            #return render(request, 'events/client_home.html', {'event':event, 'client':client, 'message':message}) 
        elif "goto_sign_contract" in data:
            etype = event.event_type_name.lower()
            do_ceremony = False
            if 'ceremony' in etype:
                do_ceremony = True
            if client.changedlist:
                changedlist = json.decoder.JSONDecoder().decode(client.changedlist)
            else:
                changedlist = ['nothing']
            return render(request, 'events/client_sign_contract_prep.html', {'event':event, 'client':client, 'pay_required':pay_required,
                                                                             'do_ceremony':do_ceremony, 'mode':mode, 'clist':changedlist}) 
        elif "goto_sign_contract_sign" in data:
            #we've posted the form data for contract, so make it and allow signing
            event.event_reminders_done = False
            changedlist = ['nothing']
            if request.POST.get('name'):
                new_action_save(['[A] Client added event name: ' + request.POST.get('name'),'dummy'], event)
                event.name = request.POST.get('name')
                changedlist.append('name')
            if request.POST.get('officiant_info'):
                new_action_save(['[A] Client added officiant info: ' + request.POST.get('officiant_info'),'dummy'], event)
                event.officiant_info = request.POST.get('officiant_info')
                changedlist.append('officiant_info')
            if request.POST.get('date'):
                new_action_save(['[A] Client added event date: ' + request.POST.get('date'),'dummy'], event)
                event.date = datetime.datetime.strptime(request.POST.get('date'), '%A %B %d, %Y')
                changedlist.append('date')
            if request.POST.get('start_time'):
                new_action_save(['[A] Client added start time: ' + request.POST.get('start_time'),'dummy'], event)
                event.start_time = datetime.datetime.strptime(request.POST.get('start_time'), '%H:%M %p')
                changedlist.append('start_time')
            if request.POST.get('end_time'):
                new_action_save(['[A] Client added end time: ' + request.POST.get('end_time'),'dummy'], event)
                event.end_time = datetime.datetime.strptime(request.POST.get('end_time'), '%H:%M %p')
                changedlist.append('end_time')
#             if request.POST.get('fee'):
#                 new_action_save(['Client added fee: ' + request.POST.get('fee'),'dummy'], event)
#                 event.fee = request.POST.get('fee')
#             if request.POST.get('deposit_fee'):
#                 new_action_save(['Client added deposit_fee: ' + request.POST.get('deposit_fee'),'dummy'], event)
#                 event.deposit_fee = request.POST.get('deposit_fee')
            if not event.location:
                if request.POST.get('location_name'):
                    new_action_save(['[A] Client added location name: ' + request.POST.get('location_name'),'dummy'], event)
                    event.location_name = request.POST.get('location_name')
                    changedlist.append('location_name')
                if request.POST.get('location_address'):    
                    new_action_save(['[A] Client added location address: ' + request.POST.get('location_address'),'dummy'], event)
                    event.location_address = request.POST.get('location_address')
                    changedlist.append('location_address')
            if request.POST.get('location_details'):        
                new_action_save(['[A] Client added location_details: ' + request.POST.get('location_details'),'dummy'], event)
                event.location_details = request.POST.get('location_details')
                changedlist.append('location_details')
            if request.POST.get('location_outdoors') == "True":
                location_outdoors_bool = True
            else:
                location_outdoors_bool = False
            if event.location_outdoors != location_outdoors_bool:    
                new_action_save(['[A] Client changed outdoors to ' + request.POST.get('location_outdoors'),'dummy'], event)
                event.location_outdoors = request.POST.get('location_outdoors')
                changedlist.append('location_outdoors')
            if not event.contact:
                if request.POST.get('contact_name'):
                    new_action_save(['[A] Client added contact name: ' + request.POST.get('contact_name'),'dummy'], event)
                    event.contact_name = request.POST.get('contact_name')
                    changedlist.append('contact_name')
                if request.POST.get('contact_email'):   
                    new_action_save(['[A] Client added contact email: ' + request.POST.get('contact_email'),'dummy'], event)
                    event.contact_email = request.POST.get('contact_email')
                    changedlist.append('contact_email')
                if request.POST.get('contact_phone'):    
                    new_action_save(['[A] Client added contact phone: ' + request.POST.get('contact_phone'),'dummy'], event)
                    event.contact_phone = request.POST.get('contact_phone')
                    changedlist.append('contact_phone')
            if not event.dayofcontact:
                if request.POST.get('dayofcontact_name'):
                    new_action_save(['[A] Client added planner name: ' + request.POST.get('dayofcontact_name'),'dummy'], event)
                    event.dayofcontact_name = request.POST.get('dayofcontact_name')
                    changedlist.append('dayofcontact_name')
                if request.POST.get('dayofcontact_phone'):    
                    new_action_save(['[A] Client added planner phone: ' + request.POST.get('dayofcontact_phone'),'dummy'], event)
                    event.dayofcontact_phone = request.POST.get('dayofcontact_phone')
                    changedlist.append('dayofcontact_phone')
                if request.POST.get('dayofcontact_email'):    
                    new_action_save(['[A] Client added planner email: ' + request.POST.get('dayofcontact_email'),'dummy'], event)
                    event.dayofcontact_email = request.POST.get('dayofcontact_email')
                    changedlist.append('dayofcontact_email')
            if request.POST.get('dayofcontact_alone_name'):
                new_action_save(['[A] Client added Day-of contact name: ' + request.POST.get('dayofcontact_alone_name'),'dummy'], event)
                event.dayofcontact_alone_name = request.POST.get('dayofcontact_alone_name')
                changedlist.append('dayofcontact_alone_name')
            if request.POST.get('dayofcontact_alone_phone'):
                new_action_save(['[A] Client added Day-of contact phone: ' + request.POST.get('dayofcontact_alone_phone'),'dummy'], event)
                event.dayofcontact_alone_phone = request.POST.get('dayofcontact_alone_phone')
                changedlist.append('dayofcontact_alone_phone')
            if request.POST.get('number_guests'):
                new_action_save(['[A] Client added Number of Guests: ' + request.POST.get('number_guests'),'dummy'], event)
                event.number_guests = request.POST.get('number_guests')
                changedlist.append('number_guests')
                  
            event.save()
            client.changedlist = json.dumps(changedlist)
            client.save()
            
            #prep version of contract for display and signing
            formhtml = FormHtml.objects.get(name='receipt_contract_auto')
            full_dict = make_dict(event)
            t = Template(formhtml.pdf)
            c = Context(full_dict)
            pdf = t.render(c)
            form = ClientForm(initial={'contract_pdf': pdf})
            today = date.today()
            return render(request, 'events/client_sign_contract_sign.html', {'event':event, 'client':client, 'pay_required':pay_required, 
                                                                             'form':form, 'today':today, 'mode':mode}) 
        
        elif "goto_sign_contract_complete" in data:
            # we've gotten the signed contract, so finish up, email it to them, etc...
            form = ClientForm(request.POST)
            if form.is_valid():
                #  IF they already submitted, then don't do the important stuff again!
                if client.did_sign and client.started and event.flag_contract_rcvd:
                    clientalreadysigned = True
                else:
                    clientalreadysigned = False
                    
                client.signature_name = request.POST.get('signature_name')
                client.signature = request.POST.get('signature')
                client.signature_date = request.POST.get('signature_date')
                client.contract_pdf = request.POST.get('contract_pdf')
                if event.contact:
                    client.signature_email = event.contact.email
                else:
                    client.signature_email = event.contact_email
                client.did_sign = True
                #this counts as getting started!
                client.started = True
                client.changedlist = ''
                client.save()
                # mark contract as signed
                event.event_reminders_done = False
                event.contract_rcvddate = date.today()
                event.flag_contract_rcvd = True
                event.flag_contract_rcpt = True
                event.contract_rcptdate = date.today()
                process_due_dates(event)
                process_auto_reminders(event)
                process_update_flags(event)              
                event.save()
                check_gcal(event, False)
                if not clientalreadysigned:
                    new_action_save(['[A] Client signed contract online','dummy'], event)
                    

                # generate a real pdf
                    #grab Janie's signature first
                glob = Global.objects.get(pk=1)
                janie_sig = glob.janie_sig
                
                pdf = client.contract_pdf
                pdf += '<br /><br /><br />Your Name:  &nbsp;<u>' + client.signature_name
                pdf += '</u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                pdf += 'Date Signed:  &nbsp;<u>' + client.signature_date + '</u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                pdf += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Signature:  &nbsp;'
                pdf += '<img width="400px" align="middle" src="' + client.signature + '"></img>'
                pdf += '<br />Vanderbilt Strings:  &nbsp;<u>Janie Spangler'
                pdf += '</u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                pdf += 'Date Signed:  &nbsp;<u>' + client.signature_date + '</u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                pdf += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Signature:  &nbsp;'
                pdf += '<img width="400px" align="middle" src="' + janie_sig + '"></img>'
                file_name = "Contract-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf"
                result = BytesIO()
                file = open(file_name, "wb")
                pdf = pisa.pisaDocument(BytesIO(pdf.encode("UTF-8")), file)
                file.close()
                file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "", file_name)
                    
                
                # render stuff for the confirmation email
                formhtml = FormHtml.objects.get(name='receipt_contract_auto')
                full_dict = make_dict(event)
                t = Template(formhtml.subject)
                c = Context(full_dict)
                subject = t.render(c)
                t = Template(formhtml.body)
                c = Context(full_dict)
                bodytext = t.render(c)
                
                    
                # send the confirmation email
                from_email, to = settings.EMAIL_MAIN, client.signature_email
                html_content = bodytext
                text_content = strip_tags(html_content) 
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=[settings.EMAIL_RECORDS])
                msg.attach_alternative(html_content, "text/html")
                attachment = open(file_path, 'rb')
                msg.attach(file_name, attachment.read() , 'text/csv')
                #msg.attach_file(file_path)
                if not clientalreadysigned:
                    msg.send()
                    #save to IMAP Sent folder!
                    message = str(msg.message())
                    imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP)
                    imap.starttls(ssl_context=ssl.create_default_context())
                    imap.login(settings.EMAIL_HOST_IMAP_USER, settings.EMAIL_HOST_IMAP_PASSWORD)
                    imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
                    imap.logout() 
                
                    
                #NEW:  email planner (dayofcontact, really) as well, if planner exists!
                if event.dayofcontact:
                    doc_email = event.dayofcontact.email
                else:
                    doc_email = event.dayofcontact_email
                if doc_email:
                    # render stuff for the confirmation email
                    formhtml = FormHtml.objects.get(name='receipt_contract_auto_planner')
                    full_dict = make_dict(event)
                    t = Template(formhtml.subject)
                    c = Context(full_dict)
                    subject = t.render(c)
                    t = Template(formhtml.body)
                    c = Context(full_dict)
                    bodytext = t.render(c)
                    
                    # send the confirmation email
                    from_email, to = settings.EMAIL_MAIN, doc_email
                    html_content = bodytext
                    text_content = strip_tags(html_content) 
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=[settings.EMAIL_RECORDS])
                    msg.attach_alternative(html_content, "text/html")
                    attachment = open(file_path, 'rb')
                    msg.attach(file_name, attachment.read() , 'text/csv')
                    #msg.attach_file(file_path)
                    if not clientalreadysigned:
                        print('email sent')
                        msg.send()
                        #save to IMAP Sent folder!
                        message = str(msg.message())
                        imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP)
                        imap.starttls(ssl_context=ssl.create_default_context())
                        imap.login(settings.EMAIL_HOST_IMAP_USER, settings.EMAIL_HOST_IMAP_PASSWORD)
                        imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
                        imap.logout()
                        new_action_save(['[A] Copy of Contract was sent to planner','dummy'], event) 
                #ENDNEW
                    
                
                # ftp the pdf to website space for user to see immediately
                if not os.environ.get("FTP_LOGIN"):
                    session = ftplib.FTP_TLS(settings.FTP_ADDR, settings.FTP_LOGIN, settings.FTP_PWD)
                else:
                    session = ftplib.FTP_TLS(settings.FTP_ADDR, os.environ.get("FTP_LOGIN"), os.environ.get("FTP_PWD"))
                fileftp = open(file_path, 'rb')
                session.cwd('requests')
                session.cwd('pdfs')
                session.storbinary('STOR ' + file_name, fileftp)
                fileftp.close()
                session.quit()
                ftp_file_path = settings.FTP_URL + file_name
                # in client_sign_contract_complete.html, offer to also download pdf
                
                if mode != "reg" and mode != "contract" and not pay_required and not clientalreadysigned:
                    send_email_for_login(event, client)
                    

                client_home_path = settings.WEBSITE + 'client_home/' + str(event.id) + "/"
                client_pin = event.date.strftime("%m%d")
                
                print(client_home_path)
                print(client_pin)
                
                return render(request, 'events/client_sign_contract_complete.html', {'event':event, 'client_home_path':client_home_path, 
                                                                                     'pdf': pdf, 'client_pin':client_pin,
                                                                                     'ftp_file_path': ftp_file_path,
                                                                                     'email': to, 'mode': mode,
                                                                                     'client':client, 'pay_required':pay_required})
            else:
                emessage = 'Sorry, there was an error.  Please try again or email janie@vanderbiltstrings.com.'
                etype = event.event_type_name.lower()
                do_ceremony = False
                if 'ceremony' in etype:
                    do_ceremony = True
                if client.changedlist:
                    changedlist = json.decoder.JSONDecoder().decode(client.changedlist)
                else:
                    changedlist = ['nothing']
                return render(request, 'events/client_sign_contract_prep.html', {'emessage':emessage, 'event':event, 'client':client, 'pay_required':pay_required,
                                                                                 'do_ceremony':do_ceremony, 'mode':mode, 'clist':changedlist}) 
        
        elif "goto_pay_full_paypal" in data:
            this_type = 'full'
            this_fee = event.paypal_full_fee
            this_fee_base = event.fee
            this_fee_fee = round(this_fee - float(this_fee_base),2)
            return render(request, 'events/client_pay_paypal.html', {'event':event, 'this_fee':this_fee, 'this_fee_fee':this_fee_fee,
                                                                     'this_type':this_type, 'this_fee_base':this_fee_base,
                                                                     'client':client, 'error':False, 'mode': mode}) 

        elif "goto_pay_deposit_paypal" in data:
            this_type = 'deposit'
            this_fee = event.paypal_deposit_fee
            this_fee_base = event.deposit_fee
            this_fee_fee = round(this_fee - float(this_fee_base),2)
            return render(request, 'events/client_pay_paypal.html', {'event':event, 'this_fee':this_fee, 'this_fee_fee':this_fee_fee,
                                                                     'this_type':this_type, 'this_fee_base':this_fee_base, 
                                                                     'client':client, 'error':False, 'mode':mode}) 

        elif "goto_pay_final_paypal" in data:
            this_type = 'final'
            this_fee = event.paypal_final_fee
            this_fee_base = event.final_fee
            this_fee_fee = round(this_fee - float(this_fee_base),2)
            return render(request, 'events/client_pay_paypal.html', {'event':event, 'this_fee':this_fee, 'this_fee_fee':this_fee_fee,
                                                                     'this_type':this_type, 'this_fee_base':this_fee_base, 
                                                                     'client':client, 'error':False, 'mode':mode}) 

        elif "goto_pay_extra_paypal" in data:
            this_type = 'extra'
            this_fee = event.paypal_extra_fee
            this_fee_base = event.extra_fee
            this_fee_fee = round(this_fee - float(this_fee_base),2)
            return render(request, 'events/client_pay_paypal.html', {'event':event, 'this_fee':this_fee, 'this_fee_fee':this_fee_fee,
                                                                     'this_type':this_type, 'this_fee_base':this_fee_base, 
                                                                     'client':client, 'error':False, 'mode':mode}) 

        elif "goto_pay_extra_mail" in data:
            this_type = 'extra'
            this_fee = event.extra_fee
            return render(request, 'events/client_pay_mail.html', {'event':event, 'this_fee':this_fee, 'email':email,
                                                                     'this_type':this_type, 'error':False, 'mode':mode}) 

        elif "goto_pay_full_mail" in data:
            this_type = 'full'
            this_fee = event.fee
            return render(request, 'events/client_pay_mail.html', {'event':event, 'this_fee':this_fee, 'email':email,
                                                                     'this_type':this_type, 'error':False, 'mode':mode}) 

        elif "goto_pay_deposit_mail" in data:
            this_type = 'deposit'
            this_fee = event.deposit_fee
            return render(request, 'events/client_pay_mail.html', {'event':event, 'this_fee':this_fee, 'email':email,
                                                                     'this_type':this_type, 'error':False, 'mode':mode}) 

        elif "goto_pay_final_mail" in data:
            this_type = 'final'
            this_fee = event.final_fee
            return render(request, 'events/client_pay_mail.html', {'event':event, 'this_fee':this_fee, 'email':email,
                                                                     'this_type':this_type, 'error':False, 'mode':mode}) 
                
        elif "goto_signout" in data:
            return render(request, 'events/client_signin.html', {'event':event,
                                                                     'error':False}) 
        
        elif "goto_submit_music_requests" in data:
            num = event.ensemble_number
            if num == 1:
                name = "solo"
            elif num == 2:
                name = "quartet"
            elif num == 3:
                name = "quartet"
            elif num == 4:
                name = "quartet"
            else:
                name = "quartet"
            #print(name)
            list_parents = get_object_or_404(MusicRequest, name=name, type="parents")
            list_groomsmens = get_object_or_404(MusicRequest, name=name, type="groomsmens")
            list_bridesmaids = get_object_or_404(MusicRequest, name=name, type="bridesmaids")
            list_brides = get_object_or_404(MusicRequest, name=name, type="brides")
            list_ceremonymusics = get_object_or_404(MusicRequest, name=name, type="ceremonymusics")
            list_recessionals = get_object_or_404(MusicRequest, name=name, type="recessionals")
            list_cocktails = get_object_or_404(MusicRequest, name=name, type="cocktails")
            list_dinners = get_object_or_404(MusicRequest, name=name, type="dinners")
            list_backgrounds = get_object_or_404(MusicRequest, name=name, type="backgrounds")
            
            parents = list_parents.list.splitlines()
            groomsmens = list_groomsmens.list.splitlines()
            bridesmaids = list_bridesmaids.list.splitlines()
            brides = list_brides.list.splitlines()
            ceremonymusics = list_ceremonymusics.list.splitlines()
            recessionals = list_recessionals.list.splitlines()
            cocktails = list_cocktails.list.splitlines()
            dinners = list_dinners.list.splitlines()
            backgrounds = list_backgrounds.list.splitlines()
            receptions = cocktails
            parents_num = event.number_parents
            bridesmaids_num = event.number_bridesmaids
            flowergirls = event.flowergirls
            
            etype = event.event_type_name.lower()
            do_ceremony = do_cocktails = do_reception = do_dinner = do_background = do_misc = False
            if 'ceremony' in etype:
                do_ceremony = True
            if 'cocktail' in etype:
                do_cocktails = True
            if 'reception' in etype:
                do_reception = True
            if 'dinner' in etype:
                do_dinner = True
            if 'background' in etype:
                do_background = True
            if not do_ceremony and not do_cocktails and not do_reception and not do_background and not do_dinner:
                do_misc = True
            
            
            
            return render(request, 'events/client_requests.html', {'event':event, 'mode':mode, 'groomsmens':groomsmens,
                                                                   'parents':parents, 'bridesmaids':bridesmaids,
                                                                   'brides':brides, 'ceremonymusics':ceremonymusics,
                                                                   'recessionals':recessionals,
                                                                   'cocktails':cocktails, 'dinners':dinners,
                                                                   'backgrounds':backgrounds,
                                                                   'receptions':receptions,
                                                                   'do_ceremony':do_ceremony, 
                                                                   'do_cocktails':do_cocktails,
                                                                   'do_reception':do_reception,
                                                                   'do_dinner':do_dinner,
                                                                   'do_background':do_background,
                                                                   'do_misc':do_misc, 'parents_num':parents_num,
                                                                   'bridesmaids_num':bridesmaids_num,
                                                                   'flowergirls':flowergirls,
                                                                     'error':False}) 

        elif "goto_requests_done" in data:
            #if already done, don't do important stuff again
            if client.did_music_list and event.flag_music_list_rcvd:
                clientalreadydidmusiclist = True
            else:
                clientalreadydidmusiclist = False
            #collect data from form into nice format
            html = process_music_list(request, event)
            
            #email to janie
            subject = "Music requests list received from " + event.name
            greeting = "The music list for the <a href='" + settings.WEBSITE
            greeting += str(event.id) + "/edit'>" + event.name + "</a>"
            greeting += " event (on " + event.date.strftime("%m-%d-%y") + ") "
            greeting += "has been submitted online & automatically recorded: <br /><br />"
            from_email, to = settings.EMAIL_AUTO, settings.EMAIL_MAIN
            html_content = greeting + html
            text_content = strip_tags(html_content)
            
            connection = mail.get_connection(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT, username=settings.EMAIL_HOST_USER_AUTO, 
                                             password=settings.EMAIL_HOST_PASSWORD_AUTO, use_tls=settings.EMAIL_USE_TLS)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=[settings.EMAIL_RECORDS,'gclhome@yahoo.com'], connection=connection)
            
            msg.attach_alternative(html_content, "text/html")
            if not clientalreadydidmusiclist:
                msg.send()
                #save to IMAP Sent folder!
                message = str(msg.message())
                imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP)
                imap.starttls(ssl_context=ssl.create_default_context())
                imap.login(settings.EMAIL_HOST_IMAP_USER, settings.EMAIL_HOST_IMAP_PASSWORD)
                imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
                imap.logout() 
            
            
            #insert into event database and mark flags
            event.event_reminders_done = False
            #if includes '$25)' then add reminder for janie to check custom requests
            customcount = html.count("$25")
            if customcount > 0 and not clientalreadydidmusiclist:
                register_reminder(settings.CHECK_MUSIC_LIST, date.today() + relativedelta(days=3), event)
            #-----------------to be added to ?
            
            if not clientalreadydidmusiclist:
                if event.music_list != "":
                    oldmusiclist = "<br /><br /><b>--Below was previously listed:--</b><br />" + event.music_list
                else:
                    oldmusiclist = "" 
            else:
                oldmusiclist = ""
            if "<b>Cue for recessional: </b>" in html:
                tempbeg = html.split("<b>Cue for recessional: </b>", 1)
                tempend = tempbeg[1].split("<br />", 1)
                html_cut = tempbeg[0] + tempend[1]
                event.music_list = html_cut + oldmusiclist
            else:
                event.music_list = html + oldmusiclist
            if not clientalreadydidmusiclist:
                event.flag_music_list_rcvd = True
                event.music_list_rcvddate = date.today()
                event.flag_music_list_sent = True #of course, if filled out, then mark as sent
                if not event.music_list_sentdate:
                    event.music_list_sentdate = date.today()
            if request.POST.get('recessionals_cue'):
                event.recessional_cue = request.POST.get('recessionals_cue')
            if request.POST.get('parents_num'):
                event.number_parents = request.POST.get('parents_num')
            if request.POST.get('bridesmaids_num'):
                event.number_bridesmaids = request.POST.get('bridesmaids_num')
            if request.POST.get('flowergirls') == 'Yes':
                event.flowergirls = True
            else:
                event.flowergirls = False
                
            temp = is_reminder_done(settings.SEND_MUSIC_LIST, event)
            process_due_dates(event)
            process_auto_reminders(event)
            process_update_flags(event)
            event.save()
            disable_reminder(settings.SEND_MUSIC_LIST, event, temp)
            check_gcal(event, False)
            client.did_music_list = True
            if not clientalreadydidmusiclist:
                client.music_list_date = date.today()
            client.save()
            if not clientalreadydidmusiclist:
                new_action_save(['[A] Client completed music list online','dummy'], event)
            

            
            #email to client
            # render stuff for the confirmation email
            formhtml = FormHtml.objects.get(name='music_request_confirmation')
            full_dict = make_dict(event)
            t = Template(formhtml.subject)
            c = Context(full_dict)
            subject = t.render(c)
            t = Template(formhtml.body)
            c = Context(full_dict)
            bodytext = t.render(c)
            
            if event.contact:
                clientemail = event.contact.email
            else:
                clientemail = event.contact_email
            from_email, to = settings.EMAIL_MAIN, clientemail
            html_content = bodytext
            text_content = strip_tags(html_content) 
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=[settings.EMAIL_RECORDS])
            msg.attach_alternative(html_content, "text/html")
            if not clientalreadydidmusiclist:
                msg.send()
            #save to IMAP Sent folder!
            message = str(msg.message())
            imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP)
            imap.starttls(ssl_context=ssl.create_default_context())
            imap.login(settings.EMAIL_HOST_IMAP_USER, settings.EMAIL_HOST_IMAP_PASSWORD)
            imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
            imap.logout() 
            
            #NEW:  email to planner too (if exists)
            # render stuff for the confirmation email
            formhtml = FormHtml.objects.get(name='music_request_confirmation_planner')
            full_dict = make_dict(event)
            t = Template(formhtml.subject)
            c = Context(full_dict)
            subject = t.render(c)
            t = Template(formhtml.body)
            c = Context(full_dict)
            bodytext = t.render(c)
            
            if event.dayofcontact:
                docemail = event.dayofcontact.email
            else:
                docemail = event.dayofcontact_email
            if docemail:
                from_email, to = settings.EMAIL_MAIN, docemail
                html_content = bodytext
                text_content = strip_tags(html_content) 
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=[settings.EMAIL_RECORDS])
                msg.attach_alternative(html_content, "text/html")
                if not clientalreadydidmusiclist:
                    msg.send()
                #save to IMAP Sent folder!
                message = str(msg.message())
                imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP)
                imap.starttls(ssl_context=ssl.create_default_context())
                imap.login(settings.EMAIL_HOST_IMAP_USER, settings.EMAIL_HOST_IMAP_PASSWORD)
                imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
                imap.logout() 
                new_action_save(['[A] Copy of Music List was sent to planner','dummy'], event)
            #ENDNEW
            
            
            
            #save as pdf, put onto ftp site for future reference
            pdf = '<div style="font-size:16px;">' + html + '</div>'
            file_name = "Musical-requests-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf"
            result = BytesIO()
            file = open(file_name, "wb")
            pdf = pisa.pisaDocument(BytesIO(pdf.encode("UTF-8")), file)
            file.close()
            file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "", file_name)
            
            if not os.environ.get("FTP_LOGIN"):
                session = ftplib.FTP_TLS(settings.FTP_ADDR, settings.FTP_LOGIN, settings.FTP_PWD)
            else:
                session = ftplib.FTP_TLS(settings.FTP_ADDR, os.environ.get("FTP_LOGIN"), os.environ.get("FTP_PWD"))
            fileftp = open(file_path, 'rb')
            session.cwd('requests')
            session.cwd('pdfs')
            session.storbinary('STOR ' + file_name, fileftp)
            fileftp.close()
            session.quit()
            ftp_file_path = settings.FTP_URL + file_name
            
            #return message to user that they're done, they have received email, and can see pdf on client site
            return render(request, 'events/client_requests_complete.html', {'event':event, 
                                                                             'ftp_file_path': ftp_file_path,
                                                                             'email': to, 'mode': mode,
                                                                             'client':client})
            
        
        elif "goto_confirm_final_details" in data:
            if event.dayofcontact:
                doc_name = event.dayofcontact.name
                doc_phone = event.dayofcontact.phone
                doc_email = event.dayofcontact.email
            else:
                doc_name = event.dayofcontact_name
                doc_phone = event.dayofcontact_phone
                doc_email = event.dayofcontact_email
                
            if not doc_name:
                doc_alone = True
                doc_name = event.dayofcontact_alone_name
                doc_phone = event.dayofcontact_alone_phone
            else:
                doc_alone = False
                
            etype = event.event_type_name.lower()
            do_ceremony = False
            if 'ceremony' in etype:
                do_ceremony = True

            if event.start_time:
                settime = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=15)).time()
                if event.location:
                    if "Ritz" in event.location.name:
                        settime = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=30)).time()
                else:
                    if "Ritz" in event.location_name:
                        settime = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=30)).time()
            else:
                settime = ''

            return render(request, 'events/client_final_details.html', {'event':event, 'doc_name':doc_name, 'mode': mode,
                                                                        'settime':settime, 'doc_alone':doc_alone,
                                                                        'doc_phone':doc_phone, 'doc_email':doc_email,
                                                                        'client':client, 'do_ceremony':do_ceremony})
        
        elif "goto_confirm_final_details_done" in data:
            if client.did_verify_info and event.flag_final_confirmation_rcvd:
                clientalreadyconfirmedfinal = True
            else:
                clientalreadyconfirmedfinal = False
            new_doc_name = request.POST.get('new_doc_name')
            new_doc_phone = request.POST.get('new_doc_phone')
            # new_doc_notes = request.POST.get('new_doc_notes')
            new_doc_email = request.POST.get('new_doc_email')
            new_officiant_info = request.POST.get('new_officiant_info')
            new_recessional_cue = request.POST.get('new_recessional_cue')
            new_doc_alone_name = request.POST.get('new_doc_alone_name')
            new_doc_alone_phone = request.POST.get('new_doc_alone_phone')
            
            
            # mark all pertinent flags, etc.
            client.did_verify_info = True
            client.verify_info_date = date.today()
            client.save()
            event.event_reminders_done = False
            event.flag_final_confirmation_rcvd = True
            event.confirmation_rcvddate = date.today()
            event.flag_final_confirmation_sent = True #of course, if filled out, then mark as sent
            if not event.confirmation_sentdate:
                event.confirmation_sentdate = date.today()
            
            if not clientalreadyconfirmedfinal:    
                if not event.dayofcontact and not event.dayofcontact_name and new_doc_name:
                    event.dayofcontact_name = new_doc_name
                    new_action_save(['[A] Client added planner name','dummy'], event)
                    
                if event.dayofcontact and not event.dayofcontact.phone and new_doc_phone:
                    event.dayofcontact.phone = new_doc_phone
                    new_action_save(['[A] Client added planner phone','dummy'], event)
                if not event.dayofcontact and not event.dayofcontact_phone and new_doc_phone:
                    event.dayofcontact_phone = new_doc_phone
                    new_action_save(['[A] Client added planner phone','dummy'], event)
                    
                if event.dayofcontact and not event.dayofcontact.email and new_doc_email:
                    event.dayofcontact.email = new_doc_email
                    new_action_save(['[A] Client added planner email','dummy'], event)
                if not event.dayofcontact and not event.dayofcontact_email and new_doc_email:
                    event.dayofcontact_email = new_doc_email
                    new_action_save(['[A] Client added planner email','dummy'], event)
                    
                if not event.dayofcontact_alone_name and new_doc_alone_name:
                    event.dayofcontact_alone_name = new_doc_alone_name
                    new_action_save(['[A] Client added day-of contact name','dummy'], event)
                    
                if not event.dayofcontact_alone_phone and new_doc_alone_phone:
                    event.dayofcontact_alone_phone = new_doc_alone_phone
                    new_action_save(['[A] Client added day-of contact phone','dummy'], event)
                    
                if not event.officiant_info and new_officiant_info:
                    event.officiant_info = new_officiant_info
                    new_action_save(['[A] Client added officant info','dummy'], event)
                if not event.recessional_cue and new_recessional_cue:
                    event.recessional_cue = new_recessional_cue
                    new_action_save(['[A] Client added recessional cue','dummy'], event)
                    
            temp = is_reminder_done(settings.SEND_FINAL_CONFIRMATION, event)
            process_due_dates(event)
            process_auto_reminders(event)
            process_update_flags(event)
            event.save()
            disable_reminder(settings.SEND_FINAL_CONFIRMATION, event, temp)
            check_gcal(event, False)
            if not clientalreadyconfirmedfinal:
                new_action_save(['[A] Client confirmed final details via client page','dummy'], event)
            
            # email Janie a notice
            subject = "Confirmation of final event details completed via client page for " + event.name
            greeting = "The final event details for the <a href='" + settings.WEBSITE
            greeting += str(event.id) + "/edit'>" + event.name + "</a>"
            greeting += " event (on " + event.date.strftime("%m-%d-%y") + ") "
            greeting += "have been confirmed online & automatically recorded. <br /><br />"
            from_email, to = settings.EMAIL_AUTO, settings.EMAIL_MAIN
            html_content = greeting
            text_content = strip_tags(html_content) 
            connection = mail.get_connection(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT, username=settings.EMAIL_HOST_USER_AUTO,
                                 password=settings.EMAIL_HOST_PASSWORD_AUTO, use_tls=settings.EMAIL_USE_TLS)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=[settings.EMAIL_RECORDS], connection=connection)
            msg.attach_alternative(html_content, "text/html")
            if not clientalreadyconfirmedfinal:
                msg.send()
            #save to IMAP Sent folder!
            message = str(msg.message())
            imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP)
            imap.starttls(ssl_context=ssl.create_default_context())
            imap.login(settings.EMAIL_HOST_IMAP_USER, settings.EMAIL_HOST_IMAP_PASSWORD)
            imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
            imap.logout() 
            
            return render(request, 'events/client_final_details_complete.html', {'event':event,  'mode': mode,
                                                                        'client':client})
        elif "goto_view_final_details" in data:
            if event.dayofcontact:
                doc_name = event.dayofcontact.name
                doc_phone = event.dayofcontact.phone
                doc_email = event.dayofcontact.email
            else:
                doc_name = event.dayofcontact_name
                doc_phone = event.dayofcontact_phone
                doc_email = event.dayofcontact_email

            if not doc_name:
                doc_alone = True
                doc_name = event.dayofcontact_alone_name
                doc_phone = event.dayofcontact_alone_phone
            else:
                doc_alone = False

            if event.start_time:
                settime = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=15)).time()
                if event.location:
                    if "Ritz" in event.location.name:
                        settime = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=30)).time()
                else:
                    if "Ritz" in event.location_name:
                        settime = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=30)).time()
            else:
                settime = ''
            
            return render(request, 'events/client_view_final_details.html', {'event':event, 'mode': mode, 'settime':settime,
                                                                             'doc_name':doc_name, 'doc_phone':doc_phone,
                                                                        'doc_email':doc_email, 'doc_alone':doc_alone, 'client':client})
        
        elif "goto_home_firsttime" in data:
            return render(request, 'events/client_signin.html', {'event':event, 'error':False})
        
        else:
#             pin = request.POST.get('pin')
            if (not request.POST.get('monthpin') or not request.POST.get('daypin')) and "goto_home" in data:
                pin = event.date.strftime("%m%d")
            if not "goto_home" in data:
                if (not request.POST.get('monthpin') or not request.POST.get('daypin')):
                    pin = '0000'
                else:
                    pin = request.POST.get('monthpin') + request.POST.get('daypin')
            else:
                pin = '0000'
            correctpin = event.date.strftime("%m%d")
            if pin == correctpin or ("goto_home" in data) or ("goto_gotit_extra" in data) or ("goto_gotit_deposit" in data) or ("goto_gotit_final" in data) or ("goto_gotit_full" in data):
                if "goto_gotit_full" in data:
                    #if already submitted, don't do important stuff again
                    if client.paid_total and client.paid_deposit and client.paid_final:
                        clientalreadypaidfullcheck = True
                    else:
                        clientalreadypaidfullcheck = False
                    #mark appropriate flags to show that client intends to send check, includes marking
                    #    deposit as done so that janie only has to mark FINAL as rcvd manually when she gets check
                    #
                    event.event_reminders_done = False
                    if event.deposit_fee != 0:
                        event.deposit_fee = 0
                        event.final_fee = event.fee
#maybe mark reminders as disb (instead of done).

                    event.deposit_rcvddate = date.today() #because did full, no longer need deposit
                    event.deposit_rcptdate = date.today() #because did full, no longer need dep rcpt
                    event.flag_deposit_rcvd = True #if client did it, no longer need
                    event.flag_deposit_rcpt = True #if client did it, no longer need
                    #then, mark the RECEIPT_FINAL_PAYMENT and RECEIVE_FINAL_PAYMENT
                    #reminders as being NOT auto, so that in the future Janie can checkmark it done when
                    #she receives the check, and then the button for sending it will show up again,
                    #and a popup message will also ask if she wants to do it right away
                    event.flag_deposit_sent = True #if client did it, no longer need to send deposit request
                    if not event.deposit_sentdate:
                        event.deposit_sentdate = date.today()
                    event.flag_final_payment_sent = True #if client did it, no longer need to send final request
                    if not event.final_sentdate:
                        event.final_sentdate = date.today()
                    
                    temp = is_reminder_done(settings.SEND_DEPOSIT, event)
                    temp2 = is_reminder_done(settings.RECEIVE_DEPOSIT, event)
                    temp3 = is_reminder_done(settings.RECEIPT_DEPOSIT, event)
                    temp4 = is_reminder_done(settings.SEND_FINAL_PAYMENT, event)
                    process_due_dates(event)
                    process_auto_reminders(event)
                    process_update_flags(event)
                    event.save()
                    mark_reminder_auto(event, settings.RECEIPT_FINAL_PAYMENT, False)
                    mark_reminder_auto(event, settings.RECEIVE_FINAL_PAYMENT, False)
                    disable_reminder(settings.SEND_DEPOSIT, event, temp)
                    disable_reminder(settings.RECEIVE_DEPOSIT, event, temp2)
                    disable_reminder(settings.RECEIPT_DEPOSIT, event, temp3)
                    disable_reminder(settings.SEND_FINAL_PAYMENT, event, temp4)
                    check_gcal(event, False)
                    client.paid_total = True
                    client.paid_deposit = True
                    client.paid_final = True
                    client.paid_total_date = date.today()
                    client.paid_deposit_date = date.today()
                    client.paid_final_date = date.today()
                    #this counts as getting started!
                    client.started = True
                    client.save()
                    if not clientalreadypaidfullcheck:
                        new_action_save(['[A] Client plans to mail full payment check','dummy'], event)
                    
                    #send the auto email with check info
                    if not clientalreadypaidfullcheck:
                        send_email_for_check(event.fee, 'full', email, event)
                    
                    
                    if mode != "reg":
                        client_home_path = settings.WEBSITE + 'client_home/' + str(event.id) + "/"
                        client_pin = event.date.strftime("%m%d")
                        if not clientalreadypaidfullcheck:
                            send_email_for_login(event, client)
                        return render(request, 'events/client_new.html', {'event':event, 
                                                                          'client_home_path':client_home_path,
                                                                          'client_pin':client_pin,
                                                                          'client':client, 'error':False})
                    
                    
                if "goto_gotit_deposit" in data:
                    #don't do it again if this is a re-submittal:
                    if client.paid_deposit:
                        clientalreadypaiddepositcheck = True
                    else:
                        clientalreadypaiddepositcheck = False
                    event.event_reminders_done = False
                    #mark the RECEIPT_DEPOSIT and RECEIVE_DEPOSIT
                    #reminders as being NOT auto, so that in the future Janie can checkmark it done when
                    #she receives the check, and then the button for sending it will show up again,
                    #and a popup message will also ask if she wants to do it right away
                    event.flag_deposit_sent = True #if client did it, no longer need to send deposit request
                    if not event.deposit_sentdate:
                        event.deposit_sentdate = date.today()
                        
                    temp = is_reminder_done(settings.SEND_DEPOSIT, event)
                    process_due_dates(event)
                    process_auto_reminders(event)
                    process_update_flags(event)
                    event.save()
                    #since they're sending check, receive/receipt is no longer auto
                    mark_reminder_auto(event, settings.RECEIPT_DEPOSIT, False)
                    mark_reminder_auto(event, settings.RECEIVE_DEPOSIT, False)
                    #below disables only if it originally was undone (also marks edited if changed)
                    disable_reminder(settings.SEND_DEPOSIT, event, temp)
                    check_gcal(event, False)
                    client.paid_deposit = True
                    client.paid_deposit_date = date.today()
                    #this counts as getting started!
                    client.started = True
                    client.save()
                    if not clientalreadypaiddepositcheck:
                        new_action_save(['[A] Client plans to mail deposit payment check','dummy'], event)
                    
                    #send the auto email with check info
                    if not clientalreadypaiddepositcheck:
                        send_email_for_check(event.deposit_fee, 'deposit', email, event)

                    if mode != "reg":
                        client_home_path = settings.WEBSITE + 'client_home/' + str(event.id) + "/"
                        client_pin = event.date.strftime("%m%d")
                        if not clientalreadypaiddepositcheck:
                            send_email_for_login(event, client)
                        return render(request, 'events/client_new.html', {'event':event, 
                                                                          'client_home_path':client_home_path,
                                                                          'client_pin':client_pin,
                                                                          'client':client, 'error':False})
                    
                if "goto_gotit_final" in data:
                    if client.paid_final:
                        clientalreadypaidfinalcheck = True
                    else:
                        clientalreadypaidfinalcheck = False
                    event.event_reminders_done = False
                    #mark the RECEIPT_FINAL_PAYMENT and RECEIVE_FINAL_PAYMENT
                    #reminders as being NOT auto, so that in the future Janie can checkmark it done when
                    #she receives the check, and then the button for sending it will show up again,
                    #and a popup message will also ask if she wants to do it right away
                    event.flag_final_payment_sent = True #if client did it, no longer need to send deposit request
                    if not event.final_sentdate:
                        event.final_sentdate = date.today()
                    
                    temp = is_reminder_done(settings.SEND_FINAL_PAYMENT, event)
                    process_due_dates(event)
                    process_auto_reminders(event)
                    process_update_flags(event)
                    event.save()
                    mark_reminder_auto(event, settings.RECEIPT_FINAL_PAYMENT, False)
                    mark_reminder_auto(event, settings.RECEIVE_FINAL_PAYMENT, False)
                    disable_reminder(settings.SEND_FINAL_PAYMENT, event, temp)
                    check_gcal(event, False)
                    client.paid_final = True 
                    client.paid_final_date = date.today()
                    #this counts as getting started!
                    client.started = True
                    client.save()
                    if not clientalreadypaidfinalcheck:
                        new_action_save(['[A] Client plans to mail final payment check','dummy'], event) 
                    
                    #send the auto email with check info
                    if not clientalreadypaidfinalcheck:
                        send_email_for_check(event.final_fee, 'final', email, event)

                    if mode != "reg":
                        client_home_path = settings.WEBSITE + 'client_home/' + str(event.id) + "/"
                        client_pin = event.date.strftime("%m%d")
                        if not clientalreadypaidfinalcheck:
                            send_email_for_login(event, client)
                        return render(request, 'events/client_new.html', {'event':event, 
                                                                          'client_home_path':client_home_path,
                                                                          'client_pin':client_pin,
                                                                          'client':client, 'error':False})
                    
                if "goto_gotit_extra" in data:
                    if client.paid_extra:
                        clientalreadypaidextracheck = True
                    else:
                        clientalreadypaidextracheck = False
                    event.event_reminders_done = False
                    #mark the RECEIPT_EXTRA_PAYMENT and RECEIVE_EXTRA_PAYMENT
                    #reminders as being NOT auto, so that in the future Janie can checkmark it done when
                    #she receives the check, and then the button for sending it will show up again,
                    #and a popup message will also ask if she wants to do it right away
                    event.flag_extra_sent = True #if client did it, no longer need to send request
                    if not event.extra_sentdate:
                        event.extra_sentdate = date.today()
                    
                    temp = is_reminder_done(settings.SEND_EXTRA_PAYMENT, event)
                    process_due_dates(event)
                    process_auto_reminders(event)
                    process_update_flags(event)
                    event.save()
                    mark_reminder_auto(event, settings.RECEIPT_EXTRA_PAYMENT, False)
                    mark_reminder_auto(event, settings.RECEIVE_EXTRA_PAYMENT, False)
                    disable_reminder(settings.SEND_EXTRA_PAYMENT, event, temp)
                    check_gcal(event, False)
                    client.paid_extra = True 
                    client.paid_extra_date = date.today()
                    #this counts as getting started!
                    client.started = True
                    client.save()
                    if not clientalreadypaidextracheck:
                        new_action_save(['[A] Client plans to mail extra payment check','dummy'], event) 
                    
                    #send the auto email with check info
                    if not clientalreadypaidextracheck:
                        send_email_for_check(event.extra_fee, 'extra', email, event)

                    if mode != "reg":
                        client_home_path = settings.WEBSITE + 'client_home/' + str(event.id) + "/"
                        client_pin = event.date.strftime("%m%d")
                        if not clientalreadypaidextracheck:
                            send_email_for_login(event, client)
                        return render(request, 'events/client_new.html', {'event':event, 
                                                                          'client_home_path':client_home_path,
                                                                          'client_pin':client_pin,
                                                                          'client':client, 'error':False})

                
                #provide contract, payment(deposit/final/full), music requests, final event details
                    
                contract_file_name = "Contract-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
                contract_link = settings.FTP_URL + contract_file_name
                deposit_file_name = "Deposit-payment-receipt-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
                deposit_link = settings.FTP_URL + deposit_file_name
                final_file_name = "Final-payment-receipt-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
                final_link = settings.FTP_URL + final_file_name
                full_file_name = "Full-payment-receipt-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
                full_link = settings.FTP_URL + full_file_name
                extra_file_name = "Extra-payment-receipt-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
                extra_link = settings.FTP_URL + extra_file_name
                requests_file_name = "Musical-requests-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
                requests_link = settings.FTP_URL + requests_file_name
                
                if event.start_time:
                    settime = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=15)).time()
                    if event.location:
                        if "Ritz" in event.location.name:
                            settime = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=30)).time()
                    else:
                        if "Ritz" in event.location_name:
                            settime = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=30)).time()
                else:
                    settime = ''
                
                if not specialadmin:
                    client.started = True #the usual home page is loading, so yeah, they've started :)
                client.save()
                return render(request, 'events/client_home.html', {'event':event, 'contract_link':contract_link, 'extra_link':extra_link,
                                                                   'deposit_link':deposit_link, 'final_link':final_link,
                                                                   'full_link':full_link, 'requests_link':requests_link,
                                                                   'settime':settime, 'client':client}) 
            else:
                return render(request, 'events/client_signin.html', {'event':event, 'error':True}) 
    else:
        event = get_object_or_404(Event, pk=eventnum);
        if mode == "reg" or mode == "admin":
            return render(request, 'events/client_signin.html', {'event':event, 'error':False})
        elif mode == 'contract':
            #  This is the contract-only mode, no sign-in, won't go to payment automatically either
            #  BUT, if they already went here and signed, give a thank-you-already-done-page instead
            if client.did_sign:
                paymentonly = False
                #pay_required = False
                contract_file_name = "Contract-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
                ftp_file_path = settings.FTP_URL + contract_file_name
                client_home_path = settings.WEBSITE + 'client_home/' + str(event.id) + "/"
                client_pin = event.date.strftime("%m%d")
                return render(request, 'events/client_sign_contract_complete.html', {'event':event, 'client_home_path':client_home_path, 
                                                                                     'client_pin':client_pin, 'ftp_file_path': ftp_file_path,
                                                                                     'paymentonly':paymentonly,
                                                                                     'email': email, 'mode': mode,
                                                                                     'client':client, 'pay_required':pay_required})
            else:
                etype = event.event_type_name.lower()
                do_ceremony = False
                if 'ceremony' in etype:
                    do_ceremony = True
                if client.changedlist:
                    changedlist = json.decoder.JSONDecoder().decode(client.changedlist)
                else:
                    changedlist = ['nothing']
                return render(request, 'events/client_sign_contract_prep.html', {'event':event, 'client':client, 'pay_required':pay_required,
                                                                                 'do_ceremony':do_ceremony, 'mode':mode, 'clist':changedlist}) 
               
        elif mode == 'musiclist':
            # This is the musiclist-only mode, no sign-in, won't show goto home when done
            # BUT, if they already sent music list, give the finished page again instead
            if client.did_music_list:
                file_name = "Musical-requests-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf"
                ftp_file_path = settings.FTP_URL + file_name
                if event.contact:
                    to = event.contact.email
                else:
                    to = event.contact_email
                
                return render(request, 'events/client_requests_complete.html', {'event':event, 
                                                                                 'ftp_file_path': ftp_file_path,
                                                                                 'email': to, 'mode': mode,
                                                                                 'client':client})
            else:
                num = event.ensemble_number
                if num == 1:
                    name = "solo"
                elif num == 2:
                    name = "quartet"
                elif num == 3:
                    name = "quartet"
                elif num == 4:
                    name = "quartet"
                else:
                    name = "quartet"
                #print(name)
                list_parents = get_object_or_404(MusicRequest, name=name, type="parents")
                list_groomsmens = get_object_or_404(MusicRequest, name=name, type="groomsmens")
                list_bridesmaids = get_object_or_404(MusicRequest, name=name, type="bridesmaids")
                list_brides = get_object_or_404(MusicRequest, name=name, type="brides")
                list_ceremonymusics = get_object_or_404(MusicRequest, name=name, type="ceremonymusics")
                list_recessionals = get_object_or_404(MusicRequest, name=name, type="recessionals")
                list_cocktails = get_object_or_404(MusicRequest, name=name, type="cocktails")
                list_dinners = get_object_or_404(MusicRequest, name=name, type="dinners")
                list_backgrounds = get_object_or_404(MusicRequest, name=name, type="backgrounds")
                
                parents = list_parents.list.splitlines()
                groomsmens = list_groomsmens.list.splitlines()
                bridesmaids = list_bridesmaids.list.splitlines()
                brides = list_brides.list.splitlines()
                ceremonymusics = list_ceremonymusics.list.splitlines()
                recessionals = list_recessionals.list.splitlines()
                cocktails = list_cocktails.list.splitlines()
                dinners = list_dinners.list.splitlines()
                backgrounds = list_backgrounds.list.splitlines()
                receptions = cocktails
                parents_num = event.number_parents
                bridesmaids_num = event.number_bridesmaids
                flowergirls = event.flowergirls
                
                etype = event.event_type_name.lower()
                do_ceremony = do_cocktails = do_reception = do_dinner = do_background = do_misc = False
                if 'ceremony' in etype:
                    do_ceremony = True
                if 'cocktail' in etype:
                    do_cocktails = True
                if 'reception' in etype:
                    do_reception = True
                if 'dinner' in etype:
                    do_dinner = True
                if 'background' in etype:
                    do_background = True
                if not do_ceremony and not do_cocktails and not do_reception and not do_background and not do_dinner:
                    do_misc = True
                
                
                
                return render(request, 'events/client_requests.html', {'event':event, 'mode':mode, 'groomsmens':groomsmens,
                                                                       'parents':parents, 'bridesmaids':bridesmaids,
                                                                       'brides':brides, 'ceremonymusics':ceremonymusics,
                                                                       'recessionals':recessionals,
                                                                       'cocktails':cocktails, 'dinners':dinners,
                                                                       'backgrounds':backgrounds,
                                                                       'receptions':receptions,
                                                                       'do_ceremony':do_ceremony, 
                                                                       'do_cocktails':do_cocktails,
                                                                       'do_reception':do_reception,
                                                                       'do_dinner':do_dinner,
                                                                       'do_background':do_background,
                                                                       'do_misc':do_misc, 'parents_num':parents_num,
                                                                       'bridesmaids_num':bridesmaids_num,
                                                                       'flowergirls':flowergirls,
                                                                         'error':False}) 

            
        elif mode == 'confirmation':
            # This is the confirmation-only mode, no sign-in, won't show goto home when done
            # BUT, if they already did confirmation, give the finished page again instead
            if client.did_verify_info:
                if event.dayofcontact:
                    doc_name = event.dayofcontact.name
                    doc_phone = event.dayofcontact.phone
                    doc_email = event.dayofcontact.email
                else:
                    doc_name = event.dayofcontact_name
                    doc_phone = event.dayofcontact_phone
                    doc_email = event.dayofcontact_email

                if not doc_name:
                    doc_name = event.dayofcontact_alone_name
                    doc_phone = event.dayofcontact_alone_phone
                    doc_alone = True
                else:
                    doc_alone = False

                if event.start_time:
                    settime = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=15)).time()
                    if event.location:
                        if "Ritz" in event.location.name:
                            settime = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=30)).time()
                    else:
                        if "Ritz" in event.location_name:
                            settime = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=30)).time()
                else:
                    settime = ''
                
                return render(request, 'events/client_view_final_details.html', {'event':event, 'mode': mode, 'settime':settime,
                                                                                 'doc_name':doc_name, 'doc_phone':doc_phone,
                                                                            'doc_email':doc_email, 'doc_alone':doc_alone, 'client':client})

            else:
                if event.dayofcontact:
                    doc_name = event.dayofcontact.name
                    doc_phone = event.dayofcontact.phone
                    doc_email = event.dayofcontact.email
                else:
                    doc_name = event.dayofcontact_name
                    doc_phone = event.dayofcontact_phone
                    doc_email = event.dayofcontact_email
                    
                if not doc_name:
                    doc_alone = True
                    doc_name = event.dayofcontact_alone_name
                    doc_phone = event.dayofcontact_alone_phone
                else:
                    doc_alone = False
                
                etype = event.event_type_name.lower()
                do_ceremony = False
                if 'ceremony' in etype:
                    do_ceremony = True

                if event.start_time:
                    settime = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=15)).time()
                    if event.location:
                        if "Ritz" in event.location.name:
                            settime = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=30)).time()
                    else:
                        if "Ritz" in event.location_name:
                            settime = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=30)).time()
                else:
                    settime = ''
    
                return render(request, 'events/client_final_details.html', {'event':event, 'doc_name':doc_name, 'mode': mode,
                                                                            'settime':settime, 'doc_alone':doc_alone,
                                                                            'doc_phone':doc_phone, 'doc_email':doc_email,
                                                                            'client':client, 'do_ceremony':do_ceremony})


        elif mode == 'payment':
            # This is the payment-only mode, no sign-in, won't show goto home when done
            # IF they already visited this page, doesn't matter since they may have to do another payment
            #   of some sort, or have a change to pay online instead of send a check, etc etc.
            # Can use the client_home which will have a special check for mode=payment, and only show
            #   the various payment panels, and no signout button at top, with a special message box
            #   at the top explaining that payment options are below.
            contract_file_name = "Contract-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
            contract_link = settings.FTP_URL + contract_file_name
            deposit_file_name = "Deposit-payment-receipt-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
            deposit_link = settings.FTP_URL + deposit_file_name
            final_file_name = "Final-payment-receipt-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
            final_link = settings.FTP_URL + final_file_name
            full_file_name = "Full-payment-receipt-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
            full_link = settings.FTP_URL + full_file_name
            extra_file_name = "Extra-payment-receipt-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
            extra_link = settings.FTP_URL + extra_file_name
            requests_file_name = "Musical-requests-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
            requests_link = settings.FTP_URL + requests_file_name

            if event.start_time:
                settime = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=15)).time()
                if event.location:
                    if "Ritz" in event.location.name:
                        settime = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=30)).time()
                else:
                    if "Ritz" in event.location_name:
                        settime = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=30)).time()
            else:
                settime = ''
        
            return render(request, 'events/client_home.html', {'event':event, 'contract_link':contract_link, 'extra_link':extra_link,
                                                               'deposit_link':deposit_link, 'final_link':final_link,
                                                               'full_link':full_link, 'requests_link':requests_link,
                                                               'client':client, 'mode':mode}) 








            
        
        else:
            ###########this is non-reg mode and non-anything-only mode, so it's standard first-time for new client!
            #either new client has never been here before (nothing done), or
            #they started but didn't finish (contract done, not payment)
            #or neither contract or payment is needed
            #figure out which and direct accordingly
            etype = event.event_type_name.lower()
            do_ceremony = False
            if 'ceremony' in etype:
                do_ceremony = True
            if event.waive_payment and event.waive_contract: #both waived, so if client already started, signin, else welcome
                if client.started: # just reclicked the old link by accident!
                    return render(request, 'events/client_signin.html', {'event':event, 'error':False})
                else: #clicked the link, it's the first time
                    firsttime = True
                    client_home_path = settings.WEBSITE + 'client_home/' + str(event.id) + "/"
                    client_pin = event.date.strftime("%m%d")
                    send_email_for_login(event, client)
                    #this counts as getting started!
                    client.started = True
                    client.save()
                    return render(request, 'events/client_new.html', {'event':event, 'firsttime':firsttime,
                                                                      'client_home_path':client_home_path,
                                                                      'client_pin':client_pin,
                                                                      'client':client, 'error':False})
            elif event.waive_contract and not event.waive_payment:
                #rare case, but if new client and just needs payment (no contract), take to conctract complete page, which
                #    has special circumstance built in when contract is waived to new client
                #    Check if they've made the payment (if so it's just a wrong re-click on an old link)
                if client.paid_deposit:
                    return render(request, 'events/client_signin.html', {'event':event, 'error':False})
                else:
                    paymentonly = True
                    pay_required = True
                    client_home_path = settings.WEBSITE + 'client_home/' + str(event.id) + "/"
                    client_pin = event.date.strftime("%m%d")
                    return render(request, 'events/client_sign_contract_complete.html', {'event':event, 'client_home_path':client_home_path, 
                                                                                         'client_pin':client_pin,
                                                                                         'paymentonly':paymentonly,
                                                                                         'email': email, 'mode': mode,
                                                                                         'client':client, 'pay_required':pay_required})
                
                
            elif not event.waive_contract and event.waive_payment:
                #send to sign in unless they haven't started (meaning they didn't actually finish contract)
                if client.started: #reclicked the old link by accident
                    return render(request, 'events/client_signin.html', {'event':event, 'error':False})
                else: #reclicked the old link, or clicked the first time, but didn't finish signing, so still need done
                    pay_required = False
                    etype = event.event_type_name.lower()
                    do_ceremony = False
                    if 'ceremony' in etype:
                        do_ceremony = True
                    if client.changedlist:
                        changedlist = json.decoder.JSONDecoder().decode(client.changedlist)
                    else:
                        changedlist = ['nothing']
                    return render(request, 'events/client_sign_contract_prep.html', {'event':event, 'client':client, 'pay_required':pay_required,
                                                                                     'do_ceremony':do_ceremony, 'mode':mode, 'clist':changedlist}) 
                
                
            else: #nothing waived, so see if both were done and then decide whether to sign in, or go to welcome
                if client.paid_deposit and client.did_sign: #reclicked old link by accident, they were all done
                    return render(request, 'events/client_signin.html', {'event':event, 'error':False})
                elif client.did_sign: #payment still necessary (send to last page after contract signed to continue to payment):
                    pickup = True
                    pay_required = True
                    contract_file_name = "Contract-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
                    ftp_file_path = settings.FTP_URL + contract_file_name
                    client_home_path = settings.WEBSITE + 'client_home/' + str(event.id) + "/"
                    client_pin = event.date.strftime("%m%d")
                    return render(request, 'events/client_sign_contract_complete.html', {'event':event, 'client_home_path':client_home_path, 
                                                                                         'client_pin':client_pin,
                                                                                         'pickup':pickup, 'ftp_file_path':ftp_file_path,
                                                                                         'email': email, 'mode': mode,
                                                                                         'client':client, 'pay_required':pay_required})
                
                else:  # it's not possible that client paid but didn't sign; so only choice left is to sign, then pay
                        # this is truly their first time then.
                    etype = event.event_type_name.lower()
                    do_ceremony = False
                    if 'ceremony' in etype:
                        do_ceremony = True
                    if client.changedlist:
                        changedlist = json.decoder.JSONDecoder().decode(client.changedlist)
                    else:
                        changedlist = ['nothing']
                    return render(request, 'events/client_sign_contract_prep.html', {'event':event, 'client':client, 'pay_required':pay_required,
                                                                                     'do_ceremony':do_ceremony, 'mode':mode, 'clist':changedlist}) 












def transition(request, pk):
    thisevent = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        # FIRST MAKE NEW CLIENT MODEL
        form = TransitionForm(request.POST)

        if form.is_valid():
            #what if another client model is already tied to this event?
            #delete the old one, not needed anymore
            if Client.objects.filter(event=thisevent.id).exists():
                client = get_object_or_404(Client, event=thisevent.id)
                client.delete()
            
            newclient = form.save(commit=True)
            
            #PROCESS NEW STUFF
            #process flags if newclient completed verify final event info
            if newclient.did_verify_info:
                thisevent.event_reminders_done = False
                thisevent.flag_final_confirmation_sent = True
                thisevent.flag_final_confirmation_rcvd = True
                thisevent.confirmation_sentdate = newclient.verify_info_date
                thisevent.confirmation_rcvddate = newclient.verify_info_date
                temp = is_reminder_done(settings.SEND_FINAL_CONFIRMATION, thisevent)
                temp2 = is_reminder_done(settings.RECEIVE_FINAL_CONFIRMATION, thisevent)
                process_due_dates(thisevent)
                process_auto_reminders(thisevent)
                process_update_flags(thisevent)
                thisevent.save()
                disable_reminder(settings.SEND_FINAL_CONFIRMATION, thisevent, temp)
                disable_reminder(settings.RECEIVE_FINAL_CONFIRMATION, thisevent, temp2)
                newclient.transition_verify_info = True
                #newclient.save()
                #check_gcal(thisevent, False)
                
            #process flags if newclient signed contract, AND make contract and upload!
            if newclient.did_sign:
                thisevent.event_reminders_done = False
                thisevent.flag_contract_sent = True
                thisevent.flag_contract_rcvd = True
                thisevent.flag_contract_rcpt = True
                thisevent.contract_sentdate = newclient.signature_date
                thisevent.contract_rcvddate = newclient.signature_date
                thisevent.contract_rcptdate = newclient.signature_date
                temp = is_reminder_done(settings.SEND_CONTRACT, thisevent)
                temp2 = is_reminder_done(settings.RECEIVE_CONTRACT, thisevent)
                temp3 = is_reminder_done(settings.RECEIPT_CONTRACT, thisevent)
                process_due_dates(thisevent)
                process_auto_reminders(thisevent)
                process_update_flags(thisevent)
                thisevent.save()
                disable_reminder(settings.SEND_CONTRACT, thisevent, temp)
                disable_reminder(settings.RECEIVE_CONTRACT, thisevent, temp2)
                disable_reminder(settings.RECEIPT_CONTRACT, thisevent, temp3)
                newclient.transition_contract = True
                #newclient.save()
                #check_gcal(thisevent, False)
                
                #prep contract with fields and generate pdf
                formhtml = FormHtml.objects.get(name='receipt_contract_auto')
                full_dict = make_dict(thisevent)
                t = Template(formhtml.pdf)
                c = Context(full_dict)
                pdf = t.render(c)
                pdf += '<br /><br /><br />'
                newclient.contract_pdf = pdf
                if thisevent.contact:
                    newclient.signature_email = thisevent.contact.email
                else:
                    newclient.signature_email = thisevent.contact_email
                newclient.save()
                #prep filename and save locally
                file_name = "Contract-for-" + thisevent.date.strftime("%m-%d-%y") + "-(id" + str(thisevent.id) + ")" + ".pdf"
                result = BytesIO()
                file = open(file_name, "wb")
                pdf = pisa.pisaDocument(BytesIO(pdf.encode("UTF-8")), file)
                file.close()
                file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "", file_name)
                #upload contract
                if not os.environ.get("FTP_LOGIN"):
                    session = ftplib.FTP_TLS(settings.FTP_ADDR, settings.FTP_LOGIN, settings.FTP_PWD)
                else:
                    session = ftplib.FTP_TLS(settings.FTP_ADDR, os.environ.get("FTP_LOGIN"), os.environ.get("FTP_PWD"))
                fileftp = open(file_path, 'rb')
                session.cwd('requests')
                session.cwd('pdfs')
                session.storbinary('STOR ' + file_name, fileftp)
                fileftp.close()
                session.quit()
                
            #upload music list pdf as necessary, and mark nec flags/dates in event & client models
            if newclient.did_music_list:
                thisevent.event_reminders_done = False
                thisevent.flag_music_list_rcvd = True
                thisevent.music_list_rcvddate = newclient.music_list_date
                thisevent.flag_music_list_sent = True #of course, if filled out, then mark as sent
                if not thisevent.music_list_sentdate:
                    thisevent.music_list_sentdate = newclient.music_list_date
                temp = is_reminder_done(settings.SEND_MUSIC_LIST, thisevent)
                temp2 = is_reminder_done(settings.RECEIVE_MUSIC_LIST, thisevent)
                process_due_dates(thisevent)
                process_auto_reminders(thisevent)
                process_update_flags(thisevent)
                thisevent.save()
                disable_reminder(settings.SEND_MUSIC_LIST, thisevent, temp)
                disable_reminder(settings.RECEIVE_MUSIC_LIST, thisevent, temp2)
                newclient.transition_music_list = True
                #newclient.save()
                #check_gcal(thisevent, False)
            
                #save as pdf, put onto ftp site for future reference
                pdf = '<div style="font-size:16px;">' + thisevent.music_list + '</div>'
                file_name = "Musical-requests-for-" + thisevent.date.strftime("%m-%d-%y") + "-(id" + str(thisevent.id) + ")" + ".pdf"
                result = BytesIO()
                file = open(file_name, "wb")
                pdf = pisa.pisaDocument(BytesIO(pdf.encode("UTF-8")), file)
                file.close()
                file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "", file_name)
                if not os.environ.get("FTP_LOGIN"):
                    session = ftplib.FTP_TLS(settings.FTP_ADDR, settings.FTP_LOGIN, settings.FTP_PWD)
                else:
                    session = ftplib.FTP_TLS(settings.FTP_ADDR, os.environ.get("FTP_LOGIN"), os.environ.get("FTP_PWD"))
                fileftp = open(file_path, 'rb')
                session.cwd('requests')
                session.cwd('pdfs')
                session.storbinary('STOR ' + file_name, fileftp)
                fileftp.close()
                session.quit()
                      
            #add payments/dates into client model AND event model (+related reminders cancel) with stuff marked on form.
            if newclient.paid_total:
                thisevent.event_reminders_done = False
                if thisevent.deposit_fee != 0:
                    thisevent.deposit_fee = 0
                    thisevent.final_fee = thisevent.fee
                thisevent.flag_deposit_rcvd = True #if client did it, no longer need
                thisevent.deposit_rcvddate = newclient.paid_total_date #because did full, no longer need deposit
                thisevent.flag_deposit_rcpt = True #if client did it, no longer need
                thisevent.deposit_rcptdate = newclient.paid_total_date #because did full, no longer need dep rcpt
                thisevent.flag_deposit_sent = True #if client did it, no longer need to send deposit request
                if not thisevent.deposit_sentdate:
                    thisevent.deposit_sentdate = newclient.paid_total_date
                thisevent.flag_final_payment_sent = True #if client did it, no longer need to send final request
                if not thisevent.final_sentdate:
                    thisevent.final_sentdate = newclient.paid_total_date
                thisevent.flag_final_payment_rcvd = True
                thisevent.final_rcvddate = newclient.paid_total_date
                thisevent.flag_final_payment_rcpt = True
                thisevent.final_rcptdate = newclient.paid_total_date
                
                temp = is_reminder_done(settings.SEND_DEPOSIT, thisevent)
                temp2 = is_reminder_done(settings.RECEIVE_DEPOSIT, thisevent)
                temp3 = is_reminder_done(settings.RECEIPT_DEPOSIT, thisevent)
                temp4 = is_reminder_done(settings.SEND_FINAL_PAYMENT, thisevent)
                temp5 = is_reminder_done(settings.RECEIVE_FINAL_PAYMENT, thisevent)
                temp6 = is_reminder_done(settings.RECEIPT_FINAL_PAYMENT, thisevent)
                process_due_dates(thisevent)
                process_auto_reminders(thisevent)
                process_update_flags(thisevent)
                thisevent.save()
                disable_reminder(settings.SEND_DEPOSIT, thisevent, temp)
                disable_reminder(settings.RECEIVE_DEPOSIT, thisevent, temp2)
                disable_reminder(settings.RECEIPT_DEPOSIT, thisevent, temp3)
                disable_reminder(settings.SEND_FINAL_PAYMENT, thisevent, temp4)
                disable_reminder(settings.RECEIVE_FINAL_PAYMENT, thisevent, temp5)
                disable_reminder(settings.RECEIPT_FINAL_PAYMENT, thisevent, temp6)
                #check_gcal(thisevent, False)
                #newclient.paid_total = True
                newclient.paid_deposit = True
                newclient.paid_final = True
                #newclient.paid_total_date = newclient.paid_total_date
                newclient.paid_deposit_date = newclient.paid_total_date
                newclient.paid_final_date = newclient.paid_total_date
                newclient.transition_total = True
                #newclient.save()
                #new_action_save(['[A] Client plans to mail full payment check','dummy'], event)
                
                #register new paymentreceived!
                exists = PaymentsReceived.objects.filter(event_id=thisevent.id, type='full').exists()
                if exists:
                    newpay = get_object_or_404(PaymentsReceived, event_id=thisevent.id, type='full')
                    newpay.delete()
                newpay = PaymentsReceived(type = 'full')
                newpay.date = newclient.paid_total_date
                newpay.event_id = thisevent.id
                newpay.method = "check"
                newpay.payment = thisevent.fee
                newpay.amount_due = thisevent.fee
                newpay.save()
                
            if newclient.paid_deposit and not newclient.paid_total:
                thisevent.event_reminders_done = False
                thisevent.flag_deposit_sent = True #if client did it, no longer need to send deposit request
                if not thisevent.deposit_sentdate:
                    thisevent.deposit_sentdate = newclient.paid_deposit_date
                thisevent.flag_deposit_rcvd = True
                thisevent.deposit_rcvddate = newclient.paid_deposit_date
                thisevent.flag_deposit_rcpt = True
                thisevent.deposit_rcptdate = newclient.paid_deposit_date
                    
                temp = is_reminder_done(settings.SEND_DEPOSIT, thisevent)
                temp2 = is_reminder_done(settings.RECEIVE_DEPOSIT, thisevent)
                temp3 = is_reminder_done(settings.RECEIPT_DEPOSIT, thisevent)
                process_due_dates(thisevent)
                process_auto_reminders(thisevent)
                process_update_flags(thisevent)
                thisevent.save()
                disable_reminder(settings.SEND_DEPOSIT, thisevent, temp)
                disable_reminder(settings.RECEIVE_DEPOSIT, thisevent, temp2)
                disable_reminder(settings.RECEIPT_DEPOSIT, thisevent, temp3)
                #check_gcal(thisevent, False)
                #client.paid_deposit = True
                #client.paid_deposit_date = date.today()
                newclient.transition_deposit = True
                #newclient.save()
                #new_action_save(['[A] Client plans to mail deposit payment check','dummy'], event)

                #register new paymentreceived!
                exists = PaymentsReceived.objects.filter(event_id=thisevent.id, type='deposit').exists()
                if exists:
                    newpay = get_object_or_404(PaymentsReceived, event_id=thisevent.id, type='deposit')
                    newpay.delete()
                newpay = PaymentsReceived(type = 'deposit')
                newpay.date = newclient.paid_deposit_date
                newpay.event_id = thisevent.id
                newpay.method = "check"
                newpay.payment = thisevent.deposit_fee
                newpay.amount_due = thisevent.deposit_fee
                newpay.save()
                
            if newclient.paid_final and not newclient.paid_total:
                thisevent.event_reminders_done = False
                thisevent.flag_final_payment_sent = True #if client did it, no longer need to send final request
                if not thisevent.final_sentdate:
                    thisevent.final_sentdate = newclient.paid_final_date
                thisevent.flag_final_payment_rcvd = True
                thisevent.final_rcvddate = newclient.paid_final_date
                thisevent.flag_final_payment_rcpt = True
                thisevent.final_rcptdate = newclient.paid_final_date
                    
                temp = is_reminder_done(settings.SEND_FINAL_PAYMENT, thisevent)
                temp2 = is_reminder_done(settings.RECEIVE_FINAL_PAYMENT, thisevent)
                temp3 = is_reminder_done(settings.RECEIPT_FINAL_PAYMENT, thisevent)
                process_due_dates(thisevent)
                process_auto_reminders(thisevent)
                process_update_flags(thisevent)
                thisevent.save()
                disable_reminder(settings.SEND_FINAL_PAYMENT, thisevent, temp)
                disable_reminder(settings.RECEIVE_FINAL_PAYMENT, thisevent, temp2)
                disable_reminder(settings.RECEIPT_FINAL_PAYMENT, thisevent, temp3)
                #check_gcal(thisevent, False)
                #client.paid_final = True
                #client.paid_final_date = date.today()
                newclient.transition_final = True
                #newclient.save()
                #new_action_save(['[A] Client plans to mail final payment check','dummy'], event)

                #register new paymentreceived!
                exists = PaymentsReceived.objects.filter(event_id=thisevent.id, type='final').exists()
                if exists:
                    newpay = get_object_or_404(PaymentsReceived, event_id=thisevent.id, type='final')
                    newpay.delete()
                newpay = PaymentsReceived(type = 'final')
                newpay.date = newclient.paid_final_date
                newpay.event_id = thisevent.id
                newpay.method = "check"
                newpay.payment = thisevent.final_fee
                newpay.amount_due = thisevent.final_fee
                newpay.save()

            if newclient.paid_extra:
                thisevent.event_reminders_done = False
                thisevent.flag_extra_sent = True #if client did it, no longer need to send extra request
                if not thisevent.extra_sentdate:
                    thisevent.extra_sentdate = newclient.paid_extra_date
                thisevent.flag_extra_rcvd = True
                thisevent.extra_rcvddate = newclient.paid_extra_date
                thisevent.flag_extra_rcpt = True
                thisevent.extra_rcptdate = newclient.paid_extra_date
                    
                temp = is_reminder_done(settings.SEND_EXTRA_PAYMENT, thisevent)
                temp2 = is_reminder_done(settings.RECEIVE_EXTRA_PAYMENT, thisevent)
                temp3 = is_reminder_done(settings.RECEIPT_EXTRA_PAYMENT, thisevent)
                process_due_dates(thisevent)
                process_auto_reminders(thisevent)
                process_update_flags(thisevent)
                thisevent.save()
                disable_reminder(settings.SEND_EXTRA_PAYMENT, thisevent, temp)
                disable_reminder(settings.RECEIVE_EXTRA_PAYMENT, thisevent, temp2)
                disable_reminder(settings.RECEIPT_EXTRA_PAYMENT, thisevent, temp3)
                #check_gcal(thisevent, False)
                #client.paid_extra = True
                #client.paid_extra_date = date.today()
                newclient.transition_extra = True
                #newclient.save()
                #new_action_save(['[A] Client plans to mail extra payment check','dummy'], event)
                
                #register new paymentreceived!
                exists = PaymentsReceived.objects.filter(event_id=thisevent.id, type='extra').exists()
                if exists:
                    newpay = get_object_or_404(PaymentsReceived, event_id=thisevent.id, type='extra')
                    newpay.delete()
                newpay = PaymentsReceived(type = 'extra')
                newpay.date = newclient.paid_extra_date
                newpay.event_id = thisevent.id
                newpay.method = "check"
                newpay.payment = thisevent.extra_fee
                newpay.amount_due = thisevent.extra_fee
                newpay.save()

            newclient.save()
            check_gcal(thisevent, False)

            #REDIRECT TO EVENT AGAIN WHEN DONE (no popup possible)
            return redirect('/events/' + str(thisevent.pk) + '/edit/none')
        else:
            print(form.errors)
            return HttpResponseRedirect('/error/')       

    else:
        if request.GET:
            form = TransitionForm(initial=request.GET)
        else:
            #SET DEFAULTS FOR TRANSITION CLIENT
            form = TransitionForm(initial={'event':thisevent.id,
                                           'transition':True,
                                           'started':True,
                                           'did_sign':True,
                                           'paid_deposit':True})
            
    
    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])
       
    return render(request, 'events/transition.html', {'form': form, 'event': thisevent,
                                               'soonevents': soonevents, 'soonreminder': soonreminder, 
                                               'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                                               'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                                               'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents})                



def savepaypalid(request):
    if request.is_ajax():
        tid = request.GET['id']
        ttype = request.GET['type']
        client = request.GET['client']
        thisclient = get_object_or_404(Client, pk=client)
        if ttype == 'extra':
            thisclient.paypalid_extra = tid
        if ttype == 'full':
            thisclient.paypalid_total = tid
        if ttype == 'deposit':
            thisclient.paypalid_deposit = tid
        if ttype == 'final':
            thisclient.paypalid_final = tid
        thisclient.save()
        print("########   SAVED PAYPAL ID FOR TRANSACTION   ########")
        data = {'dummy':'dummy'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


@csrf_exempt    
@require_POST    
def webhook(request):
    webhook_event = request.body.decode("utf-8")
    print(webhook_event )
    
    paypaldata = json.loads(webhook_event)
    pid = paypaldata['resource']['id']
    print(pid)
    customid = paypaldata['resource']['custom_id']
    print(customid)
    existsdeposit = Client.objects.filter(paypalid_deposit=pid).exists()
    existsfinal = Client.objects.filter(paypalid_final=pid).exists()
    existstotal = Client.objects.filter(paypalid_total=pid).exists()
    existsextra = Client.objects.filter(paypalid_extra=pid).exists()
    if existsdeposit:
        tclient = get_object_or_404(Client, paypalid_deposit=pid)
        if not tclient.paypaldone_deposit:
            updatepaypal_after(tclient, 'deposit')
        else:
            print("######## paypal deposit did NOT need doing")
    elif existsfinal:
        tclient = get_object_or_404(Client, paypalid_final=pid)
        if not tclient.paypaldone_final:
            updatepaypal_after(tclient, 'final')
        else:
            print("######## paypal final did NOT need doing")
    elif existstotal:
        tclient = get_object_or_404(Client, paypalid_total=pid)
        if not tclient.paypaldone_total:
            updatepaypal_after(tclient, 'full')
        else:
            print("######## paypal full did NOT need doing")
    elif existsextra:
        tclient = get_object_or_404(Client, paypalid_extra=pid)
        if not tclient.paypaldone_extra:
            updatepaypal_after(tclient, 'extra')
        else:
            print("######## paypal extra did NOT need doing")
    
    print("######## paypal webhook found no id matches")
    
    return HttpResponse("/")


def updatepaypal_after(thisclient, type):
    print("########################################################################")
    print("paypal needed doing!")
    print(thisclient)
    print(type)
    print("########################################################################")
    
    #thisclient = get_object_or_404(Client, pk=client)
    thisevent = get_object_or_404(Event, pk=thisclient.event_id)
    thisevent.event_reminders_done = False
    #         thisevent.save()
    if thisevent.contact:
        email = thisevent.contact.email
    else:
        email = thisevent.contact_email
    
    if type == "deposit":
        thisevent.event_reminders_done = False
        thisevent.deposit_rcvddate = date.today()
        thisevent.deposit_rcptdate = date.today()
        thisevent.flag_deposit_rcvd = True
        thisevent.flag_deposit_rcpt = True
        thisevent.flag_deposit_sent = True
        if not thisevent.deposit_sentdate:
            thisevent.deposit_sentdate = date.today()
        if (thisclient.paid_deposit) and (not thisclient.paid_final) and (not thisclient.paid_total): 
            if (not thisclient.paid_online): #planned check for deposit
                mark_reminder_auto(thisevent, settings.RECEIVE_DEPOSIT, True)
                mark_reminder_auto(thisevent, settings.RECEIPT_DEPOSIT, True)
        if (thisclient.paid_total):
            if (not thisclient.paid_final_online): #planned check for full
                mark_reminder_auto(thisevent, settings.RECEIVE_FINAL_PAYMENT, True)
                mark_reminder_auto(thisevent, settings.RECEIPT_FINAL_PAYMENT, True)
        thisclient.paid_deposit = True
        thisclient.paid_deposit_date = date.today()
        thisclient.paid_online = True
        enable_reminder(settings.RECEIVE_DEPOSIT, thisevent)
        enable_reminder(settings.RECEIPT_DEPOSIT, thisevent)
        temp = is_reminder_done(settings.SEND_DEPOSIT, thisevent)
        process_due_dates(thisevent)
        process_auto_reminders(thisevent)
        process_update_flags(thisevent)
        thisevent.save()
        disable_reminder(settings.SEND_DEPOSIT, thisevent, temp)
        check_gcal(thisevent, False)
        #this counts as getting started!
        thisclient.started = True
        thisclient.save()
        send_email_for_login(thisevent, thisclient)
        new_action_save(['[A]* Client made deposit payment via PayPal','dummy'], thisevent)
        
    if type == "final":
        thisevent.event_reminders_done = False
        thisevent.final_rcvddate = date.today()
        thisevent.final_rcptdate = date.today()
        thisevent.flag_final_payment_rcvd = True
        thisevent.flag_final_payment_rcpt = True
        thisevent.flag_final_payment_sent = True
        if not thisevent.final_sentdate:
            thisevent.final_sentdate = date.today()
        if (thisclient.paid_final) and (not thisclient.paid_total): 
            if (not thisclient.paid_final_online): #planned check for final
                mark_reminder_auto(thisevent, settings.RECEIVE_FINAL_PAYMENT, True)
                mark_reminder_auto(thisevent, settings.RECEIPT_FINAL_PAYMENT, True)
        thisclient.paid_final = True
        thisclient.paid_final_date = date.today()
        thisclient.paid_final_online = True
        mark_reminder_auto(thisevent, settings.RECEIVE_FINAL_PAYMENT, True)
        mark_reminder_auto(thisevent, settings.RECEIPT_FINAL_PAYMENT, True)
        temp = is_reminder_done(settings.SEND_FINAL_PAYMENT, thisevent)
        process_due_dates(thisevent)
        process_auto_reminders(thisevent)
        process_update_flags(thisevent)
        thisevent.save()
        disable_reminder(settings.SEND_FINAL_PAYMENT, thisevent, temp)
        check_gcal(thisevent, False)
        #this counts as getting started!
        thisclient.started = True
        thisclient.save()
        send_email_for_login(thisevent, thisclient)
        new_action_save(['[A]* Client made final payment via PayPal','dummy'], thisevent)
    
    if type == "extra":
        thisevent.event_reminders_done = False
        thisevent.extra_rcvddate = date.today()
        thisevent.extra_rcptdate = date.today()
        thisevent.flag_extra_rcvd = True
        thisevent.flag_extra_rcpt = True
        thisevent.flag_extra_sent = True
        if not thisevent.extra_sentdate:
            thisevent.extra_sentdate = date.today()
            #             if (thisclient.paid_final) and (not thisclient.paid_total): 
            #                 if (not thisclient.paid_final_online): #planned check for final
            #                     mark_reminder_auto(thisevent, settings.RECEIVE_FINAL_PAYMENT, True)
            #                     mark_reminder_auto(thisevent, settings.RECEIPT_FINAL_PAYMENT, True)
        thisclient.paid_extra = True
        thisclient.paid_extra_date = date.today()
        thisclient.paid_extra_online = True
        mark_reminder_auto(thisevent, settings.RECEIVE_EXTRA_PAYMENT, True)
        mark_reminder_auto(thisevent, settings.RECEIPT_EXTRA_PAYMENT, True)
        temp = is_reminder_done(settings.SEND_EXTRA_PAYMENT, thisevent)
        process_due_dates(thisevent)
        process_auto_reminders(thisevent)
        process_update_flags(thisevent)
        thisevent.save()
        disable_reminder(settings.SEND_EXTRA_PAYMENT, thisevent, temp)
        check_gcal(thisevent, False)
        #this counts as getting started!
        thisclient.started = True
        thisclient.save()
        send_email_for_login(thisevent, thisclient)
        new_action_save(['[A]* Client made extra payment via PayPal','dummy'], thisevent)
    
    if type == "full":
        thisevent.event_reminders_done = False
        thisevent.deposit_rcvddate = date.today()
        thisevent.final_rcvddate = date.today()
        thisevent.deposit_rcptdate = date.today()
        thisevent.final_rcptdate = date.today()
        thisevent.flag_deposit_rcvd = True
        thisevent.flag_final_payment_rcvd = True
        thisevent.flag_deposit_rcpt = True
        thisevent.flag_final_payment_rcpt = True
        thisevent.flag_deposit_sent = True
        if not thisevent.deposit_sentdate:
            thisevent.deposit_sentdate = date.today()
        thisevent.flag_final_payment_sent = True
        if not thisevent.final_sentdate:
            thisevent.final_sentdate = date.today()
        if thisevent.deposit_fee != 0:
            thisevent.deposit_fee = 0
            thisevent.final_fee = thisevent.fee
        if not thisevent.deposit_sentdate:
            thisevent.deposit_sentdate = date.today()
        if (thisclient.paid_deposit) and (not thisclient.paid_final) and (not thisclient.paid_total): 
            if (not thisclient.paid_online): #planned check for deposit
                mark_reminder_auto(thisevent, settings.RECEIVE_DEPOSIT, True)
                mark_reminder_auto(thisevent, settings.RECEIPT_DEPOSIT, True)
        if (thisclient.paid_total):
            if (not thisclient.paid_final_online): #planned check for full
                mark_reminder_auto(thisevent, settings.RECEIVE_FINAL_PAYMENT, True)
                mark_reminder_auto(thisevent, settings.RECEIPT_FINAL_PAYMENT, True)
        thisclient.paid_deposit = True
        thisclient.paid_final = True
        thisclient.paid_total = True
        thisclient.paid_deposit_date = date.today()
        thisclient.paid_final_date = date.today()
        thisclient.paid_total_date = date.today()
        thisclient.paid_online = True
        thisclient.paid_final_online = True
        temp = is_reminder_done(settings.SEND_DEPOSIT, thisevent)
        temp2 = is_reminder_done(settings.RECEIVE_DEPOSIT, thisevent)
        temp3 = is_reminder_done(settings.RECEIPT_DEPOSIT, thisevent)
        temp4 = is_reminder_done(settings.SEND_FINAL_PAYMENT, thisevent)
        process_due_dates(thisevent)
        process_auto_reminders(thisevent)
        process_update_flags(thisevent)
        thisevent.save()
        disable_reminder(settings.SEND_DEPOSIT, thisevent, temp)
        disable_reminder(settings.RECEIVE_DEPOSIT, thisevent, temp2)
        disable_reminder(settings.RECEIPT_DEPOSIT, thisevent, temp3)
        disable_reminder(settings.SEND_FINAL_PAYMENT, thisevent, temp4)
        check_gcal(thisevent, False)
        #this counts as getting started!
        thisclient.started = True
        thisclient.save()
        send_email_for_login(thisevent, thisclient)
        new_action_save(['[A]* Client made full payment via PayPal','dummy'], thisevent)
    
    
    #add new PaymentsReceived!
    exists = PaymentsReceived.objects.filter(event_id=thisevent.id, type=type).exists()
    if exists:
        newpay = get_object_or_404(PaymentsReceived, event_id=thisevent.id, type=type)
        newpay.delete()
    newpay = PaymentsReceived(type = type)
    newpay.date = date.today()
    newpay.event_id = thisevent.id
    newpay.method = "paypal"
    if type == "full":
        newpay.payment = thisevent.paypal_full_fee
        newpay.amount_due = thisevent.fee
    elif type == "deposit":
        newpay.payment = thisevent.paypal_deposit_fee
        newpay.amount_due = thisevent.deposit_fee
    elif type == "final":
        newpay.payment = thisevent.paypal_final_fee
        newpay.amount_due = thisevent.final_fee
    else:  #type == "extra"
        newpay.payment = thisevent.paypal_extra_fee
        newpay.amount_due = thisevent.extra_fee
    newpay.save()
    
        
    #generate pdf of receipt for transaction
    if type == "deposit":
        formhtml = FormHtml.objects.get(name='receipt_deposit_auto')
    if type == "final":
        formhtml = FormHtml.objects.get(name='receipt_final_auto')
    if type == "full":
        formhtml = FormHtml.objects.get(name='receipt_full_auto')
    if type == "extra":
        formhtml = FormHtml.objects.get(name='receipt_extra_auto')
    full_dict = make_dict(thisevent)
    t = Template(formhtml.pdf)
    c = Context(full_dict)
    pdf = t.render(c)
    if type == "deposit":
        file_name = "Deposit-payment-receipt-for-" + thisevent.date.strftime("%m-%d-%y") + "-(id" + str(thisevent.id) + ")" + ".pdf"
    if type == "final":
        file_name = "Final-payment-receipt-for-" + thisevent.date.strftime("%m-%d-%y") + "-(id" + str(thisevent.id) + ")" + ".pdf"
    if type == "full":
        file_name = "Full-payment-receipt-for-" + thisevent.date.strftime("%m-%d-%y") + "-(id" + str(thisevent.id) + ")" + ".pdf"
    if type == "extra":
        file_name = "Extra-payment-receipt-for-" + thisevent.date.strftime("%m-%d-%y") + "-(id" + str(thisevent.id) + ")" + ".pdf"
    result = BytesIO()
    file = open(file_name, "wb")
    pdf = pisa.pisaDocument(BytesIO(pdf.encode("UTF-8")), file)
    file.close()
    file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "", file_name)
    
    #email pdf (receipt)
    if type == "deposit":
        formhtml = FormHtml.objects.get(name='receipt_deposit_auto')
    if type == "final":
        formhtml = FormHtml.objects.get(name='receipt_final_auto')
    if type == "full":
        formhtml = FormHtml.objects.get(name='receipt_full_auto')
    if type == "extra":
        formhtml = FormHtml.objects.get(name='receipt_extra_auto')
    full_dict = make_dict(thisevent)
    t = Template(formhtml.subject)
    c = Context(full_dict)
    subject = t.render(c)
    t = Template(formhtml.body)
    c = Context(full_dict)
    bodytext = t.render(c)
    from_email, to = settings.EMAIL_MAIN, email
    html_content = bodytext
    text_content = strip_tags(html_content) 
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=[settings.EMAIL_RECORDS])
    msg.attach_alternative(html_content, "text/html")
    attachment = open(file_path, 'rb')
    msg.attach(file_name, attachment.read() , 'text/csv')
    msg.send()
    #save to IMAP Sent folder!
    message = str(msg.message())
    imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP)
    imap.starttls(ssl_context=ssl.create_default_context())
    imap.login(settings.EMAIL_HOST_IMAP_USER, settings.EMAIL_HOST_IMAP_PASSWORD)
    imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
    imap.logout() 
        
    #save pdf to ftp space for future retrieval 
    if not os.environ.get("FTP_LOGIN"):
        session = ftplib.FTP_TLS(settings.FTP_ADDR, settings.FTP_LOGIN, settings.FTP_PWD)
    else:
        session = ftplib.FTP_TLS(settings.FTP_ADDR, os.environ.get("FTP_LOGIN"), os.environ.get("FTP_PWD"))
    fileftp = open(file_path, 'rb')
    session.cwd('requests')
    session.cwd('pdfs')
    session.storbinary('STOR ' + file_name, fileftp)
    fileftp.close()
    session.quit()
    
    if type == 'deposit':
        thisclient.paypaldone_deposit = True
        thisclient.save()
    if type == 'final':
        thisclient.paypaldone_final =True
        thisclient.save()
    if type == 'full':
        thisclient.paypaldone_total = True
        thisclient.save()
    if type == 'extra':
        thisclient.paypaldone_extra = True
        thisclient.save()
        
        




def updatepaypal(request):
    data = {'newhttp':'<div class="">&nbsp;<br />All done, thank you!<br /><br /></div'}
    if request.is_ajax():
        print("######## paypal-update top ########")
        name = request.GET['name']
        amount = request.GET['amount']
        event = request.GET['event']
        type = request.GET['type']
        client = request.GET['client']
        mode = request.GET['mode']
        data = {'newhttp':'<div class="">&nbsp;<br />All done, thank you!<br /><br /></div'}
        thisclient = get_object_or_404(Client, pk=client)
        thisevent = get_object_or_404(Event, pk=event)
        thisevent.event_reminders_done = False
        print("######## paypal-update loaded client/event ########")
#         thisevent.save()
        if thisevent.contact:
            email = thisevent.contact.email
        else:
            email = thisevent.contact_email
        
        if mode == "reg":    
            newhttp = '<br /><span class="mycol-subtext mysize-large"><h5>'
            newhttp += "Thank you, " + name + ", for your payment of $"
            newhttp += amount + '.</h5></span><p><h6><span class="mycol-subtext mysize-small">'
            newhttp += 'A receipt has been sent to ' + email + '.<br /><br />Click below to return to your client home,'
            newhttp += " where you can see"
            newhttp += " if anything else needs attention at this time.</span></h6></p>"
            data = {'newhttp':newhttp}
        else:
            client_home_path = settings.WEBSITE + 'client_home/' + str(thisevent.id) + "/"
            client_pin = thisevent.date.strftime("%m%d")
            newhttp = render_to_string('events/client_new_render.html', 
                                 {'event':thisevent, 'name':name, 'client_home_path':client_home_path,
                                                                          'client_pin':client_pin,'amount':amount, 'email':email})
            data = {'newhttp':newhttp}
        #mark event flags/dates as done, and client flags/dates as done, for this type of payment
        
        #check if client previously intended to send check; if so, change reminder
        #    back to auto and that will let it be marked done
        
        print("######## paypal-update set return http ########")
        #******************
        #we have all sorts of possibilities:
        #client wrote check for deposit, final, or full
        #then instead did paypal deposit, paypal final, or paypal full
        #
        #planned check for deposit: could now be paypal deposit, paypal full
        #planned check for final: could now be paypal final
        #planned check for full: could now be paypal deposit, paypal full
        #
        #FIX below checks on that!!
        if type == "deposit":
            print("######## paypal-update starting deposit processing ########")
            thisevent.event_reminders_done = False
            thisevent.deposit_rcvddate = date.today()
            thisevent.deposit_rcptdate = date.today()
            thisevent.flag_deposit_rcvd = True
            thisevent.flag_deposit_rcpt = True
            thisevent.flag_deposit_sent = True
            if not thisevent.deposit_sentdate:
                thisevent.deposit_sentdate = date.today()
            if (thisclient.paid_deposit) and (not thisclient.paid_final) and (not thisclient.paid_total): 
                if (not thisclient.paid_online): #planned check for deposit
                    mark_reminder_auto(thisevent, settings.RECEIVE_DEPOSIT, True)
                    mark_reminder_auto(thisevent, settings.RECEIPT_DEPOSIT, True)
            if (thisclient.paid_total):
                if (not thisclient.paid_final_online): #planned check for full
                    mark_reminder_auto(thisevent, settings.RECEIVE_FINAL_PAYMENT, True)
                    mark_reminder_auto(thisevent, settings.RECEIPT_FINAL_PAYMENT, True)
            thisclient.paid_deposit = True
            thisclient.paid_deposit_date = date.today()
            thisclient.paid_online = True
            enable_reminder(settings.RECEIVE_DEPOSIT, thisevent)
            enable_reminder(settings.RECEIPT_DEPOSIT, thisevent)
            temp = is_reminder_done(settings.SEND_DEPOSIT, thisevent)
            print("######## paypal-update mid deposit processing ########")
            process_due_dates(thisevent)
            process_auto_reminders(thisevent)
            process_update_flags(thisevent)
            thisevent.save()
            disable_reminder(settings.SEND_DEPOSIT, thisevent, temp)
            check_gcal(thisevent, False)
            #this counts as getting started!
            thisclient.started = True
            thisclient.save()
            print("######## paypal-update ending deposit processing ########")
            send_email_for_login(thisevent, thisclient)
            new_action_save(['[A] Client made deposit payment via PayPal','dummy'], thisevent)
            print("######## paypal-update finished deposit processing ########")
            
        if type == "final":
            print("######## paypal-update starting final processing ########")
            thisevent.event_reminders_done = False
            thisevent.final_rcvddate = date.today()
            thisevent.final_rcptdate = date.today()
            thisevent.flag_final_payment_rcvd = True
            thisevent.flag_final_payment_rcpt = True
            thisevent.flag_final_payment_sent = True
            if not thisevent.final_sentdate:
                thisevent.final_sentdate = date.today()
            if (thisclient.paid_final) and (not thisclient.paid_total): 
                if (not thisclient.paid_final_online): #planned check for final
                    mark_reminder_auto(thisevent, settings.RECEIVE_FINAL_PAYMENT, True)
                    mark_reminder_auto(thisevent, settings.RECEIPT_FINAL_PAYMENT, True)
            thisclient.paid_final = True
            thisclient.paid_final_date = date.today()
            thisclient.paid_final_online = True
            mark_reminder_auto(thisevent, settings.RECEIVE_FINAL_PAYMENT, True)
            mark_reminder_auto(thisevent, settings.RECEIPT_FINAL_PAYMENT, True)
            temp = is_reminder_done(settings.SEND_FINAL_PAYMENT, thisevent)
            print("######## paypal-update mid final processing ########")
            process_due_dates(thisevent)
            process_auto_reminders(thisevent)
            process_update_flags(thisevent)
            thisevent.save()
            disable_reminder(settings.SEND_FINAL_PAYMENT, thisevent, temp)
            check_gcal(thisevent, False)
            #this counts as getting started!
            thisclient.started = True
            thisclient.save()
            print("######## paypal-update ending final processing ########")
            send_email_for_login(thisevent, thisclient)
            new_action_save(['[A] Client made final payment via PayPal','dummy'], thisevent)
            print("######## paypal-update finished final processing ########")
            
        if type == "extra":
            thisevent.event_reminders_done = False
            thisevent.extra_rcvddate = date.today()
            thisevent.extra_rcptdate = date.today()
            thisevent.flag_extra_rcvd = True
            thisevent.flag_extra_rcpt = True
            thisevent.flag_extra_sent = True
            if not thisevent.extra_sentdate:
                thisevent.extra_sentdate = date.today()
#             if (thisclient.paid_final) and (not thisclient.paid_total): 
#                 if (not thisclient.paid_final_online): #planned check for final
#                     mark_reminder_auto(thisevent, settings.RECEIVE_FINAL_PAYMENT, True)
#                     mark_reminder_auto(thisevent, settings.RECEIPT_FINAL_PAYMENT, True)
            thisclient.paid_extra = True
            thisclient.paid_extra_date = date.today()
            thisclient.paid_extra_online = True
            mark_reminder_auto(thisevent, settings.RECEIVE_EXTRA_PAYMENT, True)
            mark_reminder_auto(thisevent, settings.RECEIPT_EXTRA_PAYMENT, True)
            temp = is_reminder_done(settings.SEND_EXTRA_PAYMENT, thisevent)
            process_due_dates(thisevent)
            process_auto_reminders(thisevent)
            process_update_flags(thisevent)
            thisevent.save()
            disable_reminder(settings.SEND_EXTRA_PAYMENT, thisevent, temp)
            check_gcal(thisevent, False)
            #this counts as getting started!
            thisclient.started = True
            thisclient.save()
            send_email_for_login(thisevent, thisclient)
            new_action_save(['[A] Client made extra payment via PayPal','dummy'], thisevent)

        if type == "full":
            print("######## paypal-update starting full processing ########")
            thisevent.event_reminders_done = False
            thisevent.deposit_rcvddate = date.today()
            thisevent.final_rcvddate = date.today()
            thisevent.deposit_rcptdate = date.today()
            thisevent.final_rcptdate = date.today()
            thisevent.flag_deposit_rcvd = True
            thisevent.flag_final_payment_rcvd = True
            thisevent.flag_deposit_rcpt = True
            thisevent.flag_final_payment_rcpt = True
            thisevent.flag_deposit_sent = True
            if not thisevent.deposit_sentdate:
                thisevent.deposit_sentdate = date.today()
            thisevent.flag_final_payment_sent = True
            if not thisevent.final_sentdate:
                thisevent.final_sentdate = date.today()
            if thisevent.deposit_fee != 0:
                thisevent.deposit_fee = 0
                thisevent.final_fee = thisevent.fee
            if not thisevent.deposit_sentdate:
                thisevent.deposit_sentdate = date.today()
            if (thisclient.paid_deposit) and (not thisclient.paid_final) and (not thisclient.paid_total): 
                if (not thisclient.paid_online): #planned check for deposit
                    mark_reminder_auto(thisevent, settings.RECEIVE_DEPOSIT, True)
                    mark_reminder_auto(thisevent, settings.RECEIPT_DEPOSIT, True)
            if (thisclient.paid_total):
                if (not thisclient.paid_final_online): #planned check for full
                    mark_reminder_auto(thisevent, settings.RECEIVE_FINAL_PAYMENT, True)
                    mark_reminder_auto(thisevent, settings.RECEIPT_FINAL_PAYMENT, True)
            thisclient.paid_deposit = True
            thisclient.paid_final = True
            thisclient.paid_total = True
            thisclient.paid_deposit_date = date.today()
            thisclient.paid_final_date = date.today()
            thisclient.paid_total_date = date.today()
            thisclient.paid_online = True
            thisclient.paid_final_online = True
            temp = is_reminder_done(settings.SEND_DEPOSIT, thisevent)
            temp2 = is_reminder_done(settings.RECEIVE_DEPOSIT, thisevent)
            temp3 = is_reminder_done(settings.RECEIPT_DEPOSIT, thisevent)
            temp4 = is_reminder_done(settings.SEND_FINAL_PAYMENT, thisevent)
            print("######## paypal-update mid full processing ########")
            process_due_dates(thisevent)
            process_auto_reminders(thisevent)
            process_update_flags(thisevent)
            thisevent.save()
            disable_reminder(settings.SEND_DEPOSIT, thisevent, temp)
            disable_reminder(settings.RECEIVE_DEPOSIT, thisevent, temp2)
            disable_reminder(settings.RECEIPT_DEPOSIT, thisevent, temp3)
            disable_reminder(settings.SEND_FINAL_PAYMENT, thisevent, temp4)
            check_gcal(thisevent, False)
            #this counts as getting started!
            thisclient.started = True
            thisclient.save()
            print("######## paypal-update ending full processing ########")
            send_email_for_login(thisevent, thisclient)
            new_action_save(['[A] Client made full payment via PayPal','dummy'], thisevent)
            print("######## paypal-update finished full processing ########")
        
        #add new PaymentsReceived!
        exists = PaymentsReceived.objects.filter(event_id=thisevent.id, type=type).exists()
        if exists:
            newpay = get_object_or_404(PaymentsReceived, event_id=thisevent.id, type=type)
            newpay.delete()
        newpay = PaymentsReceived(type = type)
        newpay.date = date.today()
        newpay.event_id = thisevent.id
        newpay.method = "paypal"
        if type == "full":
            newpay.payment = thisevent.paypal_full_fee
            newpay.amount_due = thisevent.fee
        elif type == "deposit":
            newpay.payment = thisevent.paypal_deposit_fee
            newpay.amount_due = thisevent.deposit_fee
        elif type == "final":
            newpay.payment = thisevent.paypal_final_fee
            newpay.amount_due = thisevent.final_fee
        else:  #type == "extra"
            newpay.payment = thisevent.paypal_extra_fee
            newpay.amount_due = thisevent.extra_fee
        newpay.save()
        print("######## paypal-update did paymentsreceived processing ########")
            
        #generate pdf of receipt for transaction
        if type == "deposit":
            formhtml = FormHtml.objects.get(name='receipt_deposit_auto')
        if type == "final":
            formhtml = FormHtml.objects.get(name='receipt_final_auto')
        if type == "full":
            formhtml = FormHtml.objects.get(name='receipt_full_auto')
        if type == "extra":
            formhtml = FormHtml.objects.get(name='receipt_extra_auto')
        full_dict = make_dict(thisevent)
        t = Template(formhtml.pdf)
        c = Context(full_dict)
        pdf = t.render(c)
        if type == "deposit":
            file_name = "Deposit-payment-receipt-for-" + thisevent.date.strftime("%m-%d-%y") + "-(id" + str(thisevent.id) + ")" + ".pdf"
        if type == "final":
            file_name = "Final-payment-receipt-for-" + thisevent.date.strftime("%m-%d-%y") + "-(id" + str(thisevent.id) + ")" + ".pdf"
        if type == "full":
            file_name = "Full-payment-receipt-for-" + thisevent.date.strftime("%m-%d-%y") + "-(id" + str(thisevent.id) + ")" + ".pdf"
        if type == "extra":
            file_name = "Extra-payment-receipt-for-" + thisevent.date.strftime("%m-%d-%y") + "-(id" + str(thisevent.id) + ")" + ".pdf"
        result = BytesIO()
        file = open(file_name, "wb")
        pdf = pisa.pisaDocument(BytesIO(pdf.encode("UTF-8")), file)
        file.close()
        file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "", file_name)
        print("######## paypal-update did generate pdf processing ########")
        
        #email pdf (receipt)
        if type == "deposit":
            formhtml = FormHtml.objects.get(name='receipt_deposit_auto')
        if type == "final":
            formhtml = FormHtml.objects.get(name='receipt_final_auto')
        if type == "full":
            formhtml = FormHtml.objects.get(name='receipt_full_auto')
        if type == "extra":
            formhtml = FormHtml.objects.get(name='receipt_extra_auto')
        full_dict = make_dict(thisevent)
        t = Template(formhtml.subject)
        c = Context(full_dict)
        subject = t.render(c)
        t = Template(formhtml.body)
        c = Context(full_dict)
        bodytext = t.render(c)
        from_email, to = settings.EMAIL_MAIN, email
        html_content = bodytext
        text_content = strip_tags(html_content) 
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=[settings.EMAIL_RECORDS])
        msg.attach_alternative(html_content, "text/html")
        attachment = open(file_path, 'rb')
        msg.attach(file_name, attachment.read() , 'text/csv')
        msg.send()
        print("######## paypal-update did email receipt ########")
        #save to IMAP Sent folder!
        message = str(msg.message())
        imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP)
        imap.starttls(ssl_context=ssl.create_default_context())
        imap.login(settings.EMAIL_HOST_IMAP_USER, settings.EMAIL_HOST_IMAP_PASSWORD)
        imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
        imap.logout() 
        print("######## paypal-update did save to imap folder ########")
            
        #save pdf to ftp space for future retrieval 
        if not os.environ.get("FTP_LOGIN"):
            session = ftplib.FTP_TLS(settings.FTP_ADDR, settings.FTP_LOGIN, settings.FTP_PWD)
        else:
            session = ftplib.FTP_TLS(settings.FTP_ADDR, os.environ.get("FTP_LOGIN"), os.environ.get("FTP_PWD"))
        fileftp = open(file_path, 'rb')
        session.cwd('requests')
        session.cwd('pdfs')
        session.storbinary('STOR ' + file_name, fileftp)
        fileftp.close()
        session.quit()
        print("######## paypal-update did push to ftp ########")

        if type == 'deposit':
            thisclient.paypaldone_deposit = True
            thisclient.save()
        if type == 'final':
            thisclient.paypaldone_final =True
            thisclient.save()
        if type == 'full':
            thisclient.paypaldone_total = True
            thisclient.save()
        if type == 'extra':
            thisclient.paypaldone_extra = True
            thisclient.save()
        print("######## paypal-update did finish everything sucessfully ########")
            
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")

def send_email_for_check(amount, paytype, email, event):  
    # render stuff for the confirmation email
    formhtml = FormHtml.objects.get(name='check_sending_info')
    full_dict = make_dict(event)
    t = Template(formhtml.subject)
    c = Context(full_dict)
    subject = t.render(c)
    t = Template(formhtml.body)
    c = Context(full_dict)
    bodytext1 = t.render(c)
    bodytext2 = bodytext1.replace('(*paytype*)', paytype)
    bodytext = bodytext2.replace('(*amount*)', str(amount))
    
    from_email, to = settings.EMAIL_MAIN, email
    html_content = bodytext
    text_content = strip_tags(html_content) 
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=[settings.EMAIL_RECORDS])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    #save to IMAP Sent folder!
    message = str(msg.message())
    imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP)
    imap.starttls(ssl_context=ssl.create_default_context())
    imap.login(settings.EMAIL_HOST_IMAP_USER, settings.EMAIL_HOST_IMAP_PASSWORD)
    imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
    imap.logout() 


def send_email_for_login(event, client):
    #send email for new clients with login info for their client home
    
    name = event.friendly_name
    client_home_path = settings.WEBSITE + 'client_home/' + str(event.id) + "/"
    client_pin = event.date.strftime("%m%d")
    if event.contact:
        email = event.contact.email
    else:
        email = event.contact_email

    # render stuff for the confirmation email
    formhtml = FormHtml.objects.get(name='client_home_login')
    full_dict = make_dict(event)
    t = Template(formhtml.subject)
    c = Context(full_dict)
    subject = t.render(c)
    t = Template(formhtml.body)
    c = Context(full_dict)
    bodytext1 = t.render(c)
    clientlink = "Client Home address:  <a href='" + client_home_path + "'><b>" + client_home_path + "</b></a><br />"
    clientpin = "Login PIN:  <b>" + client_pin + "</b> (4 digits, the month and day of your event)<br /><br />"
    bodytext2 = bodytext1.replace('(*clientlink*)', clientlink)
    bodytext = bodytext2.replace('(*clientpin*)', clientpin)
    
    from_email, to = settings.EMAIL_MAIN, email
    html_content = bodytext
    text_content = strip_tags(html_content) 
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=[settings.EMAIL_RECORDS])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    #save to IMAP Sent folder!
    message = str(msg.message())
    imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP)
    imap.starttls(ssl_context=ssl.create_default_context())
    imap.login(settings.EMAIL_HOST_IMAP_USER, settings.EMAIL_HOST_IMAP_PASSWORD)
    imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
    imap.logout() 

      

def send_email_mail(request):  #unused!!!!!
    if request.is_ajax():
        email = request.GET['email']
        amount = request.GET['amount']
        #send email with info on sending check/address/amount
        bodytext = ""
        bodytext += "<br />Here is the information for sending us a check:<br /><br />"
        bodytext += "Your payment due at this time is:  <b>$" + amount + "</b>."
        bodytext += "<br /><br />"
        bodytext += "Make your check payable to '<b>Janie Spangler</b>' or '<b>Vanderbilt Strings</b>', and send to:"
        bodytext += "<br /><br />"
        bodytext += "<b>Vanderbilt Strings c/o Janie Spangler<br />93 3rd St.<br />Bonita Springs, FL  34134</b><br /><br />"
        bodytext += "<i>We must receive your payment at least 7 days before it is due,"
        bodytext += " to allow time for the check to clear.</i><br /><br /><br />"
        bodytext += "Thank you!<br />"
        
        subject = "Info for sending a check to Vanderbilt Strings"
        from_email, to = settings.EMAIL_MAIN, email
        html_content = bodytext
        text_content = strip_tags(html_content) 
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=[settings.EMAIL_RECORDS])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        #save to IMAP Sent folder!
        message = str(msg.message())
        imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP)
        imap.starttls(ssl_context=ssl.create_default_context())
        imap.login(settings.EMAIL_HOST_IMAP_USER, settings.EMAIL_HOST_IMAP_PASSWORD)
        imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
        imap.logout() 
        
        data = {'dummy':'dummy'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
    

def send_email_with_pdf(file):  #unused!!!!!
    subject, from_email, to = 'test pdf', settings.EMAIL_MAIN, settings.EMAIL_RECORDS
    html_content = 'hi there, here it is'
    text_content = strip_tags(html_content) 
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    
    attachment = open(file, 'rb')
    
    msg.attach(file, attachment.read() , 'text/csv')
    
    msg.send()
    #save to IMAP Sent folder!
    message = str(msg.message())
    imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP)
    imap.starttls(ssl_context=ssl.create_default_context())
    imap.login(settings.EMAIL_HOST_IMAP_USER, settings.EMAIL_HOST_IMAP_PASSWORD)
    imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
    imap.logout() 

class pdf(View):
    def get(self, request, *args, **kwargs):
        data = {
             'today': datetime.date.today(), 
             'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        
#         pdf = render_to_pdf('events/pdf.html', data)
#         return HttpResponse(pdf, content_type='application/pdf') 
        #combine data with template to make pdf  
        filepdf = render_to_pdf_file('events/pdf.html', data)
        filepath = filepdf[0]
        filename = filepdf[1]
        pdf = filepdf[2]
        
        #send email with pdf attached
        #send_email_with_pdf(filepath)
        
        #send pdf to ftp server
        if not os.environ.get("FTP_LOGIN"):
            session = ftplib.FTP_TLS(settings.FTP_ADDR, settings.FTP_LOGIN, settings.FTP_PWD)
        else:
            session = ftplib.FTP_TLS(settings.FTP_ADDR, os.environ.get("FTP_LOGIN"), os.environ.get("FTP_PWD"))
        file = open(filepath, 'rb')
        session.cwd('requests')
        session.cwd('pdfs')
        session.storbinary('STOR ' + filename, file)
        file.close()
        session.quit()
         
        #create sedja link for online signing and generate it
        part1 = "https://www.sejda.com/sign-pdf?files="
        part2 = '%5B%7B%22downloadUrl%22%3A%22http%3A%2F%2Fwww.vanderbiltstrings.com%2Fpdfs%2F'
        part3 = filename
        part4 = '%22%7D%5D&returnEmail=gclhome%40yahoo.com'
        link = part1 + part2 + part3 + part4
        
        #show same pdf in browser
        #return HttpResponse(pdf, content_type="application/pdf")
        
        #print link to browser
        return HttpResponse(link)    
    
class SideCalendar(HTMLCalendar):
 
    def __init__(self, pContestEvents):
        super(SideCalendar, self).__init__()
        self.contest_events = self.group_by_day(pContestEvents)
 
    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' stoday'
            if day in self.contest_events:
                cssclass += ' sfilled'
                body = ""
                etext = ""
                #figure tooltip(s)
                for contest in self.contest_events[day]:
                    if contest.start_time:
                        etext+= contest.start_time.strftime("X%I:%M%p").replace('AM','a').replace('PM','p').replace('X0','X').replace('X','').replace(':00','')
                        etext+= " - "
                    if contest.end_time:
                        etext+= contest.end_time.strftime("X%I:%M%p").replace('AM','a').replace('PM','p').replace('X0','X').replace('X','').replace(':00','')
                        etext+= " : "
                    etext+=contest.name + "<br />"
                #figure rest of body   
                body+= '<a class="tooltipped" data-position="right" data-tooltip="'
                body+= etext + '"' + 'href="/events/sidecalday/' + str(self.year) + '/'
                body+= str(self.month) + '/' + str(day) + '">'
                body+= '<div class="sdayNumber">' + str(day) + '</div>'
                body+= '<div class="scal_event">'
                count = 0
                for contest in self.contest_events[day]:
                    if count > 2:
                        body+= '<br />'
                        count = 0
                    body+= '<span>&nbsp;'
                    if contest.type == "HD":
                        body+= '&#9702;'
                    else:
                        body+= '&bull;'
                    body_= '</span>'
                    count = count + 1
                body+= '</div></a>'
                return self.day_cell(cssclass, body)
            return self.day_cell(cssclass, '<div class="sdayNumber">%d</div><div class="scal_event">&nbsp;</div>' % day)
        return self.day_cell('snoday', '&nbsp;')
         
    def formatweekheader(self):
        body = '<tr class="sweekheader">'
        body = body + '{% for day in days %}{{ day }}{% endfor %}'
        body = body + '</tr>'
        return ""
     
    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(SideCalendar, self).formatmonth(year, month)
 
    def group_by_day(self, pContestEvents):
        field = lambda contest: contest.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(pContestEvents, field)]
        )
 
    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

    def formatmonthname(self, theyear, themonth, withyear=True):
        pYear, pMonth, nYear, nMonth = prev_next(theyear, themonth)
        tYear = date.today().year
        tMonth = date.today().month
        body = '<tr style="height:50px !important;" class="ev-nav2">'
        body+= '<th style="height:50px !important;" class="ev-nav2" colspan="2"><a class="ev-nav2 scalbtn waves-effect waves-light btn-small z-depth-1" style="left:4px;font-size:20px;background-color:#eceff1 !important;color:black" '
        body+= 'href="javascript:void(0);" onclick="updateSidecal(\'' + str(pYear) + '\',\'' + str(pMonth) + '\');">'
        body+= '&#171</a></th>'
        body+= '<th colspan="3" style="height:52px;" class="month ev-nav2">'
        body+= '<a style="color:black !important;" href="javascript:void(0);" '
        body+= 'class="tooltipped ev-nav2" data-position="bottom" data-tooltip="Reset to now" '
        body+= 'onclick="updateSidecal(\'' + str(tYear) + '\',\'' + str(tMonth) + '\');">'
        body+= month_name[themonth] + ' ' + str(theyear) + '</a></th>'
        body+= '<th colspan="2" style="height:50px !important;" class="ev-nav2"><a class="ev-nav2 scalbtn waves-effect waves-light btn-small z-depth-1" style="left:-4px;font-size:20px;background-color:#eceff1 !important;color:black" '
        body+= 'href="javascript:void(0);" onclick="updateSidecal(\'' + str(nYear) + '\',\'' + str(nMonth) + '\');">'
        body+= '&#187</a></th>'
        body+= ''
        body+= '</tr>'
        body+= '<tr class="scal_weekdays_row"><td class="scal_days">Mon</td><td class="scal_days">Tue</td>'
        body+= '<td class="scal_days">Wed</td><td class="scal_days">Thu</td>'
        body+= '<td class="scal_days">Fri</td><td class="scal_days">Sat</td><td class="scal_days">Sun</td></tr>'

        return body

def sidecalmonth(request):    
    if request.is_ajax():
        year = request.GET['year']
        month = request.GET['month']
        this = Global.objects.get(pk=1)
        this.sidecal_year = year
        this.sidecal_month = month
        this.save()
        newhttp = sidecal(year, month)
        data = {'newhttp':newhttp}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")

def mycalmonth(request):
    if request.is_ajax():
        year = request.GET['year']
        month = request.GET['month']
        this = Global.objects.get(pk=1)
        this.mycal_year = year
        this.mycal_month = month
        this.save()
        newhttp = mycaljava(year, month)
        data = {'newhttp':newhttp}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
    

def sidecalpanels(request):
    if request.is_ajax():
        this = Global.objects.get(pk=1)
        pnl1 = this.pnl1
        pnl2 = this.pnl2
        pnl3 = this.pnl3
        pnl4 = this.pnl4
        pnl5 = this.pnl5
        pnl6 = this.pnl6
        data = {'pnl1':pnl1, 'pnl2':pnl2, 'pnl3':pnl3, 'pnl4':pnl4, 'pnl5':pnl5, 'pnl6':pnl6}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")

def sidecalpanelclick(request):
    if request.is_ajax():
        panel = request.GET['panel']
        this = Global.objects.get(pk=1)
        if panel == '1':
            this.pnl1 = not this.pnl1
        if panel == '2':
            this.pnl2 = not this.pnl2
        if panel == '3':
            this.pnl3 = not this.pnl3
        if panel == '4':
            this.pnl4 = not this.pnl4
        if panel == '5':
            this.pnl5 = not this.pnl5
        if panel == '5':
            this.pnl5 = not this.pnl5
        if panel == '6':
            this.pnl6 = not this.pnl6
        if panel == 'hide':
            this.hideside = not this.hideside
        this.save()
        data = {'dummy':'dummy'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")



def sidecalday(request, Year, Month, Day):
    daychosen = datetime.date(int(Year), int(Month), int(Day))
    dayevents = Event.objects.filter(date=daychosen).exclude(
        event_archived=True).order_by('start_time')
    if dayevents.count() == 1:
        #redirect to edit page
        daychosen_id = dayevents.first().id
        return redirect('/events/' + str(daychosen_id) + '/edit')
    else:
        #redirect to day browse page
        record = Global.objects.get(pk=1)
        record.browse_date = daychosen
        record.browse_mode = "DAY"
        record.save()
        return redirect('/events/browse/0')

def sidepanelupdate(request):
    if request.is_ajax():
        soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents,  pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()

        this = Global.objects.get(pk=1)
        sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])

#         pastdue = render_to_string('events/render_side_pastdue_reminders.html',
#                          {'pastduereminder':pastduereminder})
        pastdue = render_to_string('events/render_side_booking_reminders.html',
                         {'pastduereminder':pastduereminder})
        
        upcoming = render_to_string('events/render_side_upcoming_reminders.html',
                         {'pastduereminder':pastduereminder, 'soonreminder':soonreminder, 'all_soonrem_auto':all_soonrem_auto, 'sidestate':sidestate})
        activities = render_to_string('events/render_side_activities.html',
                         {'recentactivities':recentactivities})
        paymentsdue = render_to_string('events/render_side_paymentsdue.html',
                         {'pays':pays, 'pays_pd':pays_pd})

        data = {'pastdue':pastdue, 'upcoming':upcoming, 'activities':activities, 'paymentsdue':paymentsdue}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")



def addmusiciantoask(request):
    if request.is_ajax():
        name = request.GET['name']
        event = request.GET['event']
        error = False
        if Musician.objects.filter(name=name).count() == 0:
            error = True
        else:
            newmus = get_object_or_404(Musician, name=name)
            thisevent = get_object_or_404(Event, pk=event)
            if MusicianEvent.objects.filter(event=thisevent, musician=newmus).count() > 0:
                error = True
            else:
                newmusasked = MusicianEvent(musician = newmus, event = thisevent)
                newmusasked.instrument = newmus.instrument
                newmusasked.save()
        data = {'error':error}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("here")

def invitedaskedmusician(request):
    if request.is_ajax():
        musid = int(request.GET['mus'])
        event = request.GET['event']
        thismus = get_object_or_404(MusicianEvent, pk=musid)
        thismus.asked = not thismus.asked
        thismus.save()
        data = {'dummy':'dummy'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("here")
    
def gotitaskedmusician(request):
    if request.is_ajax():
        error = False
        musid = int(request.GET['mus'])
        event = request.GET['event']
        if request.GET['ensnumber']:
            ensnumber = int(request.GET['ensnumber'])
        else:
            ensnumber = 0
        thismus = get_object_or_404(MusicianEvent, pk=musid)
        thismus.gotit = not thismus.gotit
        thismus.save()
        numgotit = MusicianEvent.objects.filter(event_id=event, gotit=True).count()
        if numgotit == ensnumber:
            #all musicians responded to fact sheet!
            fact_sheets_rcvd = True
        else:
            fact_sheets_rcvd = False
        data = {'error':'false', 'fact_sheets_rcvd':fact_sheets_rcvd}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("here")
    
    
    
              
def noaskedmusician(request):
    if request.is_ajax():
        error = False
        musid = int(request.GET['mus'])
        event = request.GET['event']
        teventdate = request.GET['eventdate']
        tmusfee = request.GET['musfee']
        musfee = Decimal(tmusfee)
        eventdate = convertdatefromajax(teventdate)
        thismus = get_object_or_404(MusicianEvent, pk=musid)
        if thismus.yes and (not thismus.no): #musician was actually playing!
                                            #pull off list, add phold
            thismus.no = True
            rank = thismus.rank
            thismus.save()
            phold = get_object_or_404(Musician, name="----------")
            newevent = get_object_or_404(Event, pk=event)
            newmus = MusicianEvent(musician = phold, event = newevent)
            newmus.instrument = '----'
            newmus.rank = rank
            newmus.yes = True
            newmus.placeholder = True
            newmus.save()
            #delete PaymentsDue record!
            #if already deleted, can't do again:
            exists = PaymentsDue.objects.filter(event_id = event, musician_id = thismus.musician.id).exists()
            if exists:
                newpay = get_object_or_404(PaymentsDue, musician_id = thismus.musician.id, event_id = event)
                newpay.delete()
            
        elif thismus.yes and thismus.no: #musician was both (already playing, then cancelled)
                                            #now becomes real and playing.  Move up and del a placeh
            thismus.no = False
            #find lowest-ranked phold (make sure there is one), and delete that one entirely
            if MusicianEvent.objects.filter(event_id=event, placeholder=True).count() == 0: 
                error = True
            else:           
                temp = MusicianEvent.objects.filter(event_id=event, placeholder=True).order_by('rank')[:1].get()
                rank = temp.rank
                temp.delete()
                #put thismus in its old rank spot, and save
                thismus.rank = rank
                thismus.save()
                #add PaymentsDue record!
                #if already exists for this event and this musician, don't add again
                exists = PaymentsDue.objects.filter(event_id = event, musician_id = thismus.musician.id).exists()
                if not exists:
                    thisevent = get_object_or_404(Event, pk=event);
                    newpay = PaymentsDue(done = False)
                    newpay.payment = musfee
                    newpay.event_id = thisevent.id
                    newpay.musician_id = thismus.musician.id
                    newpay.duedate = calculate_the_next_week_day(eventdate) #first weekday following event date
                    if thismus.musician.name == "Janie Spangler" or thismus.musician.name == "Glenn Loontjens":
                        newpay.done = True
                    newpay.save()
                
                
                
                
                
        elif (not thismus.yes) and thismus.no: #musician was a no, now becoming an unknown
                                                #so do nothing
            thismus.no = False
            thismus.save()
        else:   #musician was an unknown, now becoming a no.  do nothing basically.
            thismus.no = True
            thismus.save()
        data = {'error':error}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("here")
    
def calculate_the_next_week_day(day_now):    
    if day_now.isoweekday()== 5:
        day_now += datetime.timedelta(days=3)
    elif day_now.isoweekday()== 6:
        day_now += datetime.timedelta(days=2)
    else:
        day_now += datetime.timedelta(days=1)
    return day_now

def yesaskedmusician(request):
    if request.is_ajax():
        error = False
        musid = int(request.GET['mus'])
        event = request.GET['event']
        teventdate = request.GET['eventdate']
        tmusfee = request.GET['musfee']
        musfee = Decimal(tmusfee)
        eventdate = convertdatefromajax(teventdate)
        thismus = get_object_or_404(MusicianEvent, pk=musid)
        if thismus.yes and (not thismus.no): #musician was actually playing!
                                            #now becomes none:  pull off list, add phold
            thismus.yes = False
            rank = thismus.rank
            thismus.save()
            phold = get_object_or_404(Musician, name="----------")
            newevent = get_object_or_404(Event, pk=event)
            newmus = MusicianEvent(musician = phold, event = newevent)
            newmus.instrument = '----'
            newmus.rank = rank
            newmus.yes = True
            newmus.placeholder = True
            newmus.save()
            
            #delete PaymentsDue record!
            #if already deleted, can't do again:
            exists = PaymentsDue.objects.filter(event_id = event, musician_id = thismus.musician.id).exists()
            if exists:
                newpay = get_object_or_404(PaymentsDue, musician_id = thismus.musician.id, event_id = event)
                newpay.delete()
            
        elif thismus.yes and thismus.no: #musician was both (already playing, then cancelled)
                                            #do nothing really, they're just commiting to no by unchecking yes
            thismus.yes = False
            thismus.save()
            #delete PaymentsDue record! (I guess????????????????????????????????????????????????????????????
            #if already deleted, can't do again:
            exists = PaymentsDue.objects.filter(event_id = event, musician_id = thismus.musician.id).exists()
            if exists:
                newpay = get_object_or_404(PaymentsDue, musician_id = thismus.musician.id, event_id = event)
                newpay.delete()
        elif (not thismus.yes) and thismus.no: #musician was a no, now becoming a yes
                                                #but no is still checked, so do nothing yet!
            thismus.yes = True
            thismus.save()
            #add PaymentsDue record! (I guess????????????????????????????????????????????????????????????)
            #if already exists for this event and this musician, don't add again
#             exists = PaymentsDue.objects.filter(event_id = event, musician_id = thismus.musician.id).exists()
#             if not exists:
#                 thisevent = get_object_or_404(Event, pk=event);
#                 newpay = PaymentsDue(done = False)
#                 newpay.payment = musfee
#                 newpay.event_id = thisevent.id
#                 newpay.musician_id = thismus.musician.id
#                 newpay.duedate = calculate_the_next_week_day(eventdate) #first weekday following event date
#                 newpay.save()
        else:   #musician was an unknown, now becoming a yes.  add to list
            thismus.yes = True
            #find lowest-ranked phold (make sure there is one), and delete that one entirely
            if MusicianEvent.objects.filter(event_id=event, placeholder=True).count() == 0: 
                error = True
            else:           
                temp = MusicianEvent.objects.filter(event_id=event, placeholder=True).order_by('rank')[:1].get()
                rank = temp.rank
                temp.delete()
                #put thismus in its old rank spot, and save
                thismus.rank = rank
                thismus.save()
                
                #add PaymentsDue record!
                #if already exists for this event and this musician, don't add again
                exists = PaymentsDue.objects.filter(event_id = event, musician_id = thismus.musician.id).exists()
                if not exists:
                    thisevent = get_object_or_404(Event, pk=event);
                    newpay = PaymentsDue(done = False)
                    newpay.payment = musfee
                    newpay.event_id = thisevent.id
                    newpay.musician_id = thismus.musician.id
                    newpay.duedate = calculate_the_next_week_day(eventdate) #first weekday following event date
                    if thismus.musician.name == "Janie Spangler" or thismus.musician.name == "Glenn Loontjens":
                        newpay.done = True
                    newpay.save()
                
        data = {'error':error}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("here")

def deleteaskedmusician(request):
    if request.is_ajax():
        musid = int(request.GET['mus'])
        event = request.GET['event']
        thismus = get_object_or_404(MusicianEvent, pk=musid)
        if thismus.yes and (not thismus.no): #musician was ON, actually playing!
            rank = thismus.rank
            thismus.delete()
            phold = get_object_or_404(Musician, name="----------")
            newevent = get_object_or_404(Event, pk=event)
            newmus = MusicianEvent(musician = phold, event = newevent)
            newmus.instrument = '----'
            newmus.rank = rank
            newmus.yes = True
            newmus.placeholder = True
            newmus.save()
            #delete PaymentsDue record!
            #if already deleted, can't do again:
            exists = PaymentsDue.objects.filter(event_id = event, musician_id = thismus.musician.id).exists()
            if exists:
                newpay = get_object_or_404(PaymentsDue, musician_id = thismus.musician.id, event_id = event)
                newpay.delete()
        else: #musician was NOT ON, not actually playing as far as we know at this point
            thismus.delete()
        data = {'dummy':'dummy'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("here")
        

def updatelistofaskedmusicians(request):
    if request.is_ajax():
        event = request.GET['event']
        if request.GET['ensnumber']:
            ensnumber = int(request.GET['ensnumber'])
        else:
            ensnumber = 0
        #make new render of musiciansaskedlist
        musiciansasked = MusicianEvent.objects.filter(event_id=event, placeholder=False).order_by('-pk')
        mlist = render_to_string('events/render_musiciansaskedlist.html', 
                                 {'musiciansasked':musiciansasked})
        invite_possible = False
        mark_sent_done = False
        mark_rcvd_done = False
        mark_sent_notdone = False
        mark_rcvd_notdone = False
        askable = MusicianEvent.objects.filter(event_id=event, asked=False, placeholder=False).order_by('pk')
        playing = MusicianEvent.objects.filter(event_id=event, yes=True, no=False, placeholder=False).order_by('pk')
        asked = MusicianEvent.objects.filter(event_id=event, asked=True, yes=False, placeholder=False).order_by('pk')
        #thisevent = Event.objects.filter(id=event).get()
        if askable.count() > 0:
            invite_possible = True
            if playing.count() == ensnumber:
                invite_possible = False
        if (playing.count() == ensnumber) and ensnumber > 0:
            mark_rcvd_done = True
        else:
            mark_rcvd_notdone = True
        if not ensnumber:
            temp = 0
        else:
            temp = ensnumber
        if ((asked.count() + playing.count()) >= temp) and temp > 0:
            mark_sent_done = True
        else:
            mark_sent_notdone = True
            
        #print(asked.count())
        #print(playing.count())
        #print(mark_sent_done)
        #print(mark_rcvd_done)
        #print(temp)
        
        
        data = {'mlist':mlist, 'invite_possible':invite_possible,
                'mark_musicians_sent':mark_sent_done, 'mark_musicians_rcvd':mark_rcvd_done,
                'mark_musicians_notsent':mark_sent_notdone, 'mark_musicians_notrcvd':mark_rcvd_notdone}            
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")




def updatemusicians(request):
    if request.is_ajax():
        if request.GET['number']:
            number = int(request.GET['number'])
        else:
            number = 0
        event = request.GET['event']
        #check current musicianslist and keep all musicians as possible.
        #warn if current num is greater than new number!
        #assign placeholder musicians to all spots not filled yet
        warn = False
        mlist = MusicianEvent.objects.filter(event_id=event, yes=True, no=False).order_by('rank')
        if (mlist.count() != 0) and (mlist.count() > number): #old list existed and was bigger
            extra = mlist.count() - number
            #remove some placeholders (first) or people
            phold = MusicianEvent.objects.filter(event_id=event, placeholder=True).order_by('rank')
            pholdnum = phold.count()
            if pholdnum >= extra:
                extraphold = extra
            else:
                extraphold = pholdnum
            i = 0
            while i < extraphold:
                #delete each phold
                delmus = get_object_or_404(MusicianEvent, pk=phold.last().id)
                delmus.delete()
                phold = MusicianEvent.objects.filter(event_id=event, placeholder=True).order_by('rank')
                i = i + 1
            musdel = extra - extraphold #number of musicians that need deleting!
            if musdel > 0:
                warn = True
                i = 0
                while i < musdel:
                    #delete each extra musician, by marking no true (in addition to the yes true already)
                    delmus = get_object_or_404(MusicianEvent, pk=mlist.last().id)
                    delmus.no = True
                    delmus.save()
                    mlist = MusicianEvent.objects.filter(event_id=event, yes=True, no=False).order_by('rank')
                    i = i + 1
        elif mlist.count() == 0: #old list didn't exist
            i = 1
            phold = get_object_or_404(Musician, name="----------")
            newevent = get_object_or_404(Event, pk=event)
            while i <= number:
                newmus = MusicianEvent(musician = phold, event = newevent)
                newmus.instrument = '----'
                newmus.rank = i
                newmus.yes = True
                newmus.placeholder = True
                newmus.save()
                i = i + 1
        elif (mlist.count() != 0) and (mlist.count() < number): #old list existed and was smaller
            phold = get_object_or_404(Musician, name="----------")
            newevent = get_object_or_404(Event, pk=event)
            extra = number - mlist.count()
            i = 1
            base = mlist.count()
            while i <= extra:
                newmus = MusicianEvent(musician = phold, event = newevent)
                newmus.instrument = '----'
                newmus.rank = i + base
                newmus.yes = True
                newmus.placeholder = True
                newmus.save()
                i = i + 1
        #only other way is if old list existed and was the same, so nothing done then        
        data = {'warn':warn} 
        
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
    
def updatelistofmusicians(request):
    if request.is_ajax():
        if request.GET['number']:
            number = int(request.GET['number'])
        else:
            number = 0
        event = request.GET['event']
        #get the current musicianfee, compare to the previous, and change any musicians receiving
        #the standard previous pay to the current pay
        previousfee = Decimal(request.GET['previousfee'])
        currentfee = Decimal(request.GET['currentfee'])

        #make new render of musicianslist
        musicianlistyes = MusicianEvent.objects.filter(event_id=event, yes=True, no=False).order_by('rank')
        
        for musician in musicianlistyes:
            if musician.specialfee == previousfee or not musician.specialfee:
                musician.specialfee = currentfee
                musician.save()
                # SO, if we updated musician's fee, we must update paymentdue as well, right?!
                exists = PaymentsDue.objects.filter(event_id = event, musician_id = musician.musician.id).exists()
                if exists:
                    thispd = get_object_or_404(PaymentsDue, event_id = event, musician_id = musician.musician.id);
                    thispd.payment = currentfee
                    thispd.save()
                
        thisevent = get_object_or_404(Event, pk=event)
        factsheet = thisevent.flag_fact_sheets_sent
        mlist = render_to_string('events/render_musicianslist.html', 
                                 {'musicianlistyes':musicianlistyes, 'factsheet':factsheet,
                                  'number':number})
        data = {'mlist':mlist}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")

def reordermusicians(request):
    if request.is_ajax():
        oldrank = int(request.GET['oldrank'])
        newrank = int(request.GET['newrank'])
        event = request.GET['event']
        number = int(request.GET['number'])
        if (newrank > number) or (newrank <= 0):
            data = {'error':True}
            return HttpResponse(json.dumps(data), content_type='application/json')
        #reorder now
        old = get_object_or_404(MusicianEvent, event_id=event, yes=True, no=False, rank=oldrank)
        new = get_object_or_404(MusicianEvent, event_id=event, yes=True, no=False, rank=newrank)
        old.rank = newrank
        new.rank = oldrank
        old.save()
        new.save()
        data = {'error':False}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")

def reorderdragmusicians(request):
    if request.is_ajax():
        sortednums = json.loads(request.GET['sortednums'])
#         print(sortednums)
        event = request.GET['event']
        #get set of old musicians in old rank
        #loop each item and assign new rank in i order
        mlist = MusicianEvent.objects.filter(event_id=event, yes=True, no=False).order_by('rank')
        i = 0
        newrank = 0
#         for m in mlist:
#             m.rank = sortednums[i]
#             m.save()
#             print(sortednums[i] + ',' + m.rank + ',i:' + str(i) + ',' + m.musician.name)
#             i = i + 1
        for m in mlist:
            value = m.rank
            newrank = sortednums.index(str(value))
#             print(newrank)
            m.rank = newrank + 1
            m.save()
#             print(m.rank)
#         for m in mlist:
#             print(m.rank)
            
            
            
        data = {'error':False}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


def changeinstofmusician(request):
    if request.is_ajax():
        musrank = request.GET['rank']
        event = request.GET['event']
        mus = get_object_or_404(MusicianEvent, event_id=event, yes=True, no=False,
                                rank=musrank)
        if mus.instrument == mus.musician.instrument:
            mus.instrument = mus.musician.instrument2
        else:
            mus.instrument = mus.musician.instrument
        mus.save()
        data = {'error':False}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")

    
def specialfeechangemusicians(request):
    if request.is_ajax():
        rank = int(request.GET['rank'])
        newfee = int(request.GET['newfee'])
        event = request.GET['event']
        thisme = get_object_or_404(MusicianEvent, event_id=event, yes=True, no=False, rank=rank)
        thisme.specialfee = newfee
        thisme.save()
        
        
        #since this is someone playing, we should already have a PaymentsDue record,
        #  so update it now to reflect new payment amount!
        exists = PaymentsDue.objects.filter(event_id = event, musician_id = thisme.musician.id).exists()
        if exists:
            thispay = get_object_or_404(PaymentsDue, event_id = event, musician_id = thisme.musician.id);
            thispay.payment = newfee
            thispay.save()
        
        data = {'error':False}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


def specialfeechangeaskedmusicians(request):
    if request.is_ajax():
        musid = int(request.GET['rank'])
        newfee = int(request.GET['newfee'])
        event = request.GET['event']
        thisme = get_object_or_404(MusicianEvent, pk=musid)
        thisme.specialfee = newfee
        thisme.save()
        
        #if this is someone playing, we should already have a PaymentsDue record,
        #  so update it now to reflect new payment amount!
        exists = PaymentsDue.objects.filter(event_id = event, musician_id = thisme.musician.id).exists()
        if exists:
            thispay = get_object_or_404(PaymentsDue, event_id = event, musician_id = thisme.musician.id);
            thispay.payment = newfee
            thispay.save()

        data = {'error':False}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


class ContestCalendar(HTMLCalendar):
 
    def __init__(self, pContestEvents):
        super(ContestCalendar, self).__init__()
        self.contest_events = self.group_by_day(pContestEvents)
 
    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.contest_events:
                cssclass += ' filled'
                body = []
                for contest in self.contest_events[day]:
                    body.append('<a class="cal_event" href="%s">' % contest.url_link)
                    if contest.type == "HD":
                        body.append('[HD]:<i>')
                    if contest.start_time:
                        body.append(contest.start_time.strftime("X%I:%M%p")
                                    .replace('AM','a').replace('PM','p')
                                    .replace('X0','X').replace('X','')
                                    .replace(':00',''))
                        body.append('&nbsp;')
                    body.append('<span class="cal_event_title" style="display:inline-block;word-break:break-word;">' + esc(contest.name))
                    if contest.type == "HD":
                        body.append('</span></i></a>')
                    else:
                        body.append('</span></a>')
                return self.day_cell(cssclass, '<div class="dayNumber">%d</div> %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, '<div class="dayNumber">%d</div>' % day)
        return self.day_cell('noday', '&nbsp;')
         
    def formatweekheader(self):
        body = '<tr class="weekheader">'
        body = body + '{% for day in days %}{{ day }}{% endfor %}'
        body = body + '</tr>'
        return ""
     
    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(ContestCalendar, self).formatmonth(year, month)
 
    def group_by_day(self, pContestEvents):
        field = lambda contest: contest.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(pContestEvents, field)]
        )
 
    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

    def formatmonthname(self, theyear, themonth, withyear=True):
        tYear = date.today().year
        tMonth = date.today().month
        pYear, pMonth, nYear, nMonth = prev_next(theyear, themonth)
        body = '<tr><th colspan="2">&nbsp;</th>'
        body+= '<th style="padding-left:0px;padding-right:0px;"><a class="waves-effect waves-light btn-small z-depth-3 ev-col2" style="color:white" '
        body+= 'href="javascript:void(0);" onclick="updateMycal(\'' + str(pYear) + '\',\'' + str(pMonth) + '\');">'
        body+= '<--</a></th>'
        body+= '<th colspan="1" class="month">'
        body+= '<a style="color:black !important;" href="javascript:void(0);" '
        body+= 'class="tooltipped" data-position="bottom" data-tooltip="Reset to now" '
        body+= 'onclick="updateMycal(\'' + str(tYear) + '\',\'' + str(tMonth) + '\');">'
        body+= month_name[themonth] + ' ' + str(theyear) + '</a></th>'
        body+= '<th style="padding-left:0px;padding-right:0px;"><a class="waves-effect waves-light btn-small z-depth-3 ev-col2" style="color:white" '
        body+= 'href="javascript:void(0);" onclick="updateMycal(\'' + str(nYear) + '\',\'' + str(nMonth) + '\');">'
        body+= '--></th>'
        body+= '<th></th><th><a class="wave-effect waves-light btn-small z-depth-3 ev-col2" style="color:white" '
        body+= 'href="../../../../events/gcal/' + str(theyear) + '/' + str(themonth) + '/' + '">'
        body+= 'Gcal</a></th></tr>'
        body+= '<tr class="cal_weekdays_row"><td class="cal_days">Mon</td><td class="cal_days">Tue</td>'
        body+= '<td class="cal_days">Wed</td><td class="cal_days">Thu</td>'
        body+= '<td class="cal_days">Fri</td><td class="cal_days">Sat</td><td class="cal_days">Sun</td></tr>'

        return body

def named_month(pMonthNumber):
    """
    Return the name of the month, given the month number
    """
    return date(1900, pMonthNumber, 1).strftime('%B')

# def home(request):
#     """
#     Show calendar of events this month
#     """
#     lToday = datetime.now()
#     return calendar(request, lToday.year, lToday.month)

def prev_next(lYear, lMonth):
    lPreviousYear = lYear
    lPreviousMonth = lMonth - 1
    if lPreviousMonth == 0:
        lPreviousMonth = 12
        lPreviousYear = lYear - 1
    lNextYear = lYear
    lNextMonth = lMonth + 1
    if lNextMonth == 13:
        lNextMonth = 1
        lNextYear = lYear + 1
    return lPreviousYear, lPreviousMonth, lNextYear, lNextMonth
    

def sidecal(pYear, pMonth):
    lYear = int(pYear)
    lMonth = int(pMonth)
    today = date.today()
     
    fromdate = today + relativedelta(year=lYear, month=lMonth, day=1)
    untildate = fromdate + relativedelta(day=31)
     
    lContestEvents = Event.objects.filter(date__range=[fromdate, untildate]).exclude(
        event_archived=True).order_by('date','start_time')
    lCalendar = SideCalendar(lContestEvents).formatmonth(lYear, lMonth)
     
     
    lPreviousYear = lYear
    lPreviousMonth = lMonth - 1
    if lPreviousMonth == 0:
        lPreviousMonth = 12
        lPreviousYear = lYear - 1
    lNextYear = lYear
    lNextMonth = lMonth + 1
    if lNextMonth == 13:
        lNextMonth = 1
        lNextYear = lYear + 1
    lYearAfterThis = lYear + 1
    lYearBeforeThis = lYear - 1

    return lCalendar

def mycaljava(pYear, pMonth):
    """
    Show calendar of events for specified month and year
    """
    lYear = int(pYear)
    lMonth = int(pMonth)
    today = date.today()
     
    fromdate = today + relativedelta(year=lYear, month=lMonth, day=1)
    untildate = fromdate + relativedelta(day=31)
     
    lContestEvents = Event.objects.filter(date__range=[fromdate, untildate]).exclude(
        event_archived=True).order_by('date','start_time')
    lCalendar = ContestCalendar(lContestEvents).formatmonth(lYear, lMonth)
     
     
    lPreviousYear = lYear
    lPreviousMonth = lMonth - 1
    if lPreviousMonth == 0:
        lPreviousMonth = 12
        lPreviousYear = lYear - 1
    lNextYear = lYear
    lNextMonth = lMonth + 1
    if lNextMonth == 13:
        lNextMonth = 1
        lNextYear = lYear + 1
    lYearAfterThis = lYear + 1
    lYearBeforeThis = lYear - 1
    
    return lCalendar


def mycal(request):
    """
    Show calendar of events for specified month and year
    """
    this = Global.objects.get(pk=1)
    lYear = this.mycal_year
    lMonth = this.mycal_month    
    today = date.today()
     
    fromdate = today + relativedelta(year=lYear, month=lMonth, day=1)
    untildate = fromdate + relativedelta(day=31)
     
    lContestEvents = Event.objects.filter(date__range=[fromdate, untildate]).exclude(
        event_archived=True).order_by('date','start_time')
    lCalendar = ContestCalendar(lContestEvents).formatmonth(lYear, lMonth)
     
     
    lPreviousYear = lYear
    lPreviousMonth = lMonth - 1
    if lPreviousMonth == 0:
        lPreviousMonth = 12
        lPreviousYear = lYear - 1
    lNextYear = lYear
    lNextMonth = lMonth + 1
    if lNextMonth == 13:
        lNextMonth = 1
        lNextYear = lYear + 1
    lYearAfterThis = lYear + 1
    lYearBeforeThis = lYear - 1

    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()

    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])
 
    return render(request, 'events/mycal.html', {'Calendar' : mark_safe(lCalendar),
                                                       'Month' : lMonth,
                                                       'MonthName' : named_month(lMonth),
                                                       'Year' : lYear,
                                                       'PreviousMonth' : lPreviousMonth,
                                                       'PreviousMonthName' : named_month(lPreviousMonth),
                                                       'PreviousYear' : lPreviousYear,
                                                       'NextMonth' : lNextMonth,
                                                       'NextMonthName' : named_month(lNextMonth),
                                                       'NextYear' : lNextYear,
                                                       'YearBeforeThis' : lYearBeforeThis,
                                                       'YearAfterThis' : lYearAfterThis,
                                                       'soonevents': soonevents, 'soonreminder': soonreminder, 
                                                       'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                                                       'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                                                       'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents                
                                                   })







# API_SCOPE = ['https://www.googleapis.com/auth/calendar']
# JSON_FILE = ['google-credentials.json']
# JSON_PATH = os.path.join(settings.BASE_DIR, JSON_FILE)
# if settings.DEBUG:
#     REDIRECT_URI = "http://localhost:8000/events/gcallback"
#     os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# else:
#     REDIRECT_URI = "https://vs-test1.herokuapp.com/events/gcallback"

def gauthorize(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.JSON_PATH,
        scopes=settings.API_SCOPE)
    flow.redirect_uri = settings.REDIRECT_URI
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    
    
    obj = Global.objects.get(pk=1)
    obj.code_verifier = flow.code_verifier
    obj.save()
    #request.session['cv'] = flow.code_verifier
    
#     print("#####")
#     print(flow.code_verifier)
#     print("#####")
    #print(request.session['cv'])
    
    return HttpResponseRedirect(authorization_url)
     
def save_credentials(credentials):
    #first we get the correct DB object
    obj = Global.objects.get(pk=1)
    #now we turn the passed in credentials obj into a dicts obj
    temp = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'id_token':credentials.id_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
        'expiry':datetime.datetime.strftime(credentials.expiry,'%Y-%m-%d %H:%M:%S')
    }
    #now we save it as a json_string into the DB
    obj.gtoken = json.dumps(temp)
    obj.save()
    return temp     

def load_credentials():
    #this is the function that should be called to load a credentials object     from the database.
    #it loads, refreshes, and returns a     google.oauth2.credentials.Credentials() object.
    #returns false if error
    #------
    obj = Global.objects.get(pk=1)
    #if not authorized ever, make them do it
    if (not obj.gtoken) or (obj.gtoken == ""):
        print('FALSE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        return "needs auth"
        #every routine that loads should do HttpResponseRedirect('/events/gauthorize') if false!
    #ok, if we get to here we load/create the Credentials obj()
    temp = json.loads(obj.gtoken)
    credentials = google.oauth2.credentials.Credentials(
        temp['token'],
        refresh_token=temp['refresh_token'],
        id_token=temp['id_token'],
        token_uri=temp['token_uri'],
        client_id=temp['client_id'],
        client_secret=temp['client_secret'],
        scopes=temp['scopes'],
    )
    expiry = temp['expiry']
    expiry_datetime = datetime.datetime.strptime(expiry,'%Y-%m-%d %H:%M:%S')
    credentials.expiry = expiry_datetime
    #and now we refresh the token   
    request = google.auth.transport.requests.Request()
    if credentials.expired:
        credentials.refresh(request)
    #and finally, we return this whole deal
    return credentials



def gcallback(request): 

#     print("#####")
#     print(request.session.get('cv'))
#     print("#####")
    state = request.GET['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.JSON_PATH,
        scopes=settings.API_SCOPE,
        state=state)
    flow.redirect_uri = settings.REDIRECT_URI
    
    
    obj = Global.objects.get(pk=1)
    flow.code_verifier = obj.code_verifier
    
    #flow.code_verifier = request.session.get('cv')
#     print("#####")
#     print(flow.code_verifier)
#     print("#####")
#     print(request.session.get('cv'))
#     print("#####")
    
    code = request.GET['code']
    flow.fetch_token(code=code)
    creds = flow.credentials

    temp = save_credentials(creds)
    return HttpResponseRedirect('/events') #go to home page, I guess :)


def create_gcal_event(service, vscalid, summary, thisdate, start_time, end_time, description, location, update, eventid):
    if not start_time:
        start = datetime.datetime.combine(thisdate,datetime.time(0,0,0,0))
        end = datetime.datetime.combine(thisdate,datetime.time(0,1,0,0))
    elif not end_time: #test
        start = datetime.datetime.combine(thisdate,start_time)
        end = start
    else:
        start = datetime.datetime.combine(thisdate,start_time)
        end = datetime.datetime.combine(thisdate,end_time)

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {'dateTime':start.strftime("%Y-%m-%dT%H:%M:%S"), 'timeZone': timezone.get_current_timezone_name(),},
        'end': {'dateTime':end.strftime("%Y-%m-%dT%H:%M:%S"), 'timeZone': timezone.get_current_timezone_name(),},
        }
    if update:
        return service.events().update(calendarId=vscalid, eventId=eventid, body=event, sendNotifications=False).execute()
    else:
        return service.events().insert(calendarId=vscalid, body=event, sendNotifications=False).execute()

def check_gcal(event, delete):
    #gcal event listing will not contain reminders, activity, flags, etc.
#     this = Global.objects.get(pk=1)
#     if this.gcal_date != today or this.gcal_needs:
#         this.gcal_date = today
#         this.save()
    vscalid = os.environ.get("VSCALID")
    if not vscalid:
        vscalid = settings.VSCALID
#     # If modifying these scopes, delete the file token.pickle.
#     SCOPES = ['https://www.googleapis.com/auth/calendar']
#     creds = None
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             #url = "C:/Users/Glenn/Website/Workspace/gitvs/vs/events/static/credentials.json"
#             #url = staticfiles_storage.url('credentials.json')
#             url = 'google-credentials.json'
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 url, SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)

    creds = load_credentials()
    if (not creds) or (creds==False) or (creds=="needs auth"):
        HttpResponseRedirect('/events/gauthorize')
    else:
        save_credentials(creds)
        
    service = build('calendar', 'v3', credentials=creds, cache_discovery=False)
    #  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! cache_disc was added to see if prevent
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  random oath2client error
    
    # prep new event fields here
    date = event.date
    start_time = event.start_time
    end_time = event.end_time
    if event.location:
        location = event.location.name + ", " + event.location.address
    else:
        location = event.location_name + ", " + event.location_address
    insert = "<br />[id=" + str(event.id) + "]"
    
    formhtml = FormHtml.objects.get(name='gcal')
    full_dict = make_dict(event)
    t = Template(formhtml.body)
    c = Context(full_dict)
    description1 = t.render(c) + insert
    t = Template(formhtml.subject)
    c = Context(full_dict)
    summary = t.render(c)
    
    mlist = MusicianEvent.objects.filter(event=event, yes=True, no=False).order_by('rank')
    musicianlist = ""
    for m in mlist:
        #make musician list for fact sheets
        if m.musician.name != "----------":
            musicianlist += m.musician.name
            musicianlist += ' (' + m.instrument + '), '
            musicianlist += m.musician.email + ', ' + str(m.musician.phone) + '<br />'
        else:
            musicianlist += m.instrument + ' (empty spot) ' + m.instrument + '<br />'

    description = description1.replace('(*musician_list*)', musicianlist)    

    # find event with this event's id in description
    query = "[id=" + str(event.id) + "]" + " " + summary
    results = service.events().list(calendarId=vscalid, q=query, maxResults=2, singleEvents=True, orderBy='startTime').execute()
    #if not exist, then save new one, else delete old/create new (unless delete=true, then just delete)
    result = results.get('items', [])
    if delete:
        if result:
            oldid = result[0]['id']
            service.events().delete(calendarId=vscalid, eventId=oldid, sendUpdates=None).execute()
            print("check-gcal: event " + str(event.id) + " found and deleted")
        else:
            print("check-gcal: event " + str(event.id) + " not found while trying to delete")
    else:
        if result:
            oldid = result[0]['id']
            create_gcal_event(service, vscalid, summary, date, start_time, end_time, description, location, True, oldid)
            print("check-gcal: event " + str(event.id) + " found and updated")
        else:
            create_gcal_event(service, vscalid, summary, date, start_time, end_time, description, location, False, '123')
            print("check-gcal: event " + str(event.id) + " not found before, so newly created") 
            
               
#     if not result and not delete:
#         print('none found')
#         create_gcal_event(service, vscalid, summary, date, start_time, end_time, description, location)
#     else:
#         oldid = result[0]['id']
#         service.events().delete(calendarId=vscalid, eventId=oldid, sendUpdates=None).execute()
#         if not delete:
#             create_gcal_event(service, vscalid, summary, date, start_time, end_time, description, location)
        

def syncgcal(request):

#next section just accomplishes re-authorization of gcal oauth2 token as necessary
#------------------------------------------------------------
    vscalid = os.environ.get("VSCALID")
    if not vscalid:
        vscalid = settings.VSCALID
    
    creds = load_credentials()
    if (not creds) or (creds==False) or (creds=="needs auth"):
        print('and false...')
        HttpResponseRedirect('/events/gauthorize')
    else:
        save_credentials(creds)
        
    service = build('calendar', 'v3', credentials=creds, cache_discovery=False)
    #  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! cache_disc was added to see if prevent
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  random oath2client error
    
        
#------------------------------------------------------    
    
    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])
      
    return render(request, 'events/syncgcal.html', {'soonevents': soonevents, 'soonreminder': soonreminder, 
                                                'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal),
                                                'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount,
                                                'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents})
    
        
def syncgcal_deleteold(request):
    if request.is_ajax():
        vscalid = os.environ.get("VSCALID")
        if not vscalid:
            vscalid = settings.VSCALID

        creds = load_credentials()
        if (not creds) or (creds==False) or (creds=="needs auth"):
            print('and false...')
            HttpResponseRedirect('/events/gauthorize')
        else:
            save_credentials(creds)

        service = build('calendar', 'v3', credentials=creds, cache_discovery=False)
     
        today = datetime.datetime.today()
        monthsAgo = today - relativedelta(months=3)
        future = today + relativedelta(years=3)
        tmax = future.isoformat('T') + "Z"
        tmin = monthsAgo.isoformat('T') + "Z"    
        results = service.events().list(calendarId=vscalid, maxResults=500, singleEvents=True, timeMin=tmin, timeMax=tmax, orderBy='startTime').execute()
        
        for oneevent in results['items']:
            #print(oneevent['summary'])
            oldid = oneevent['id']
            service.events().delete(calendarId=vscalid, eventId=oldid, sendUpdates=None).execute()
        
        count = len(results['items'])
        data = {'count':count,}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
    
def syncgcal_savenew(request):
    #print("------got to savenew------")
    if request.is_ajax():
        vscalid = os.environ.get("VSCALID")
        if not vscalid:
            vscalid = settings.VSCALID

        creds = load_credentials()
        if (not creds) or (creds==False) or (creds=="needs auth"):
            HttpResponseRedirect('/events/gauthorize')
        else:
            save_credentials(creds)
            service = build('calendar', 'v3', credentials=creds, cache_discovery=False)
     
        service = build('calendar', 'v3', credentials=creds, cache_discovery=False)
    
        today = datetime.date.today()
        threemonthsago = today - relativedelta(months=3)
        threeyearsfuture = today + relativedelta(years=3)
        events = Event.objects.filter(date__range=[threemonthsago, threeyearsfuture]).exclude(
            event_archived=True).order_by('date','start_time')
    
        for event in events:
            #print(event.name)
            # prep new event fields here
            date = event.date
            start_time = event.start_time
            end_time = event.end_time
            if event.location:
                location = event.location.name + ", " + event.location.address
            else:
                location = event.location_name + ", " + event.location_address
            insert = "<br />[id=" + str(event.id) + "]"
            
            formhtml = FormHtml.objects.get(name='gcal')
            full_dict = make_dict(event)
            t = Template(formhtml.body)
            c = Context(full_dict)
            description1 = t.render(c) + insert
            t = Template(formhtml.subject)
            c = Context(full_dict)
            summary = t.render(c)

            mlist = MusicianEvent.objects.filter(event=event, yes=True, no=False).order_by('rank')
            musicianlist = ""
            for m in mlist:
                #make musician list for fact sheets
                if m.musician.name != "----------":
                    musicianlist += m.musician.name
                    musicianlist += m.musician.name + ' (' + m.instrument + '), '
                    musicianlist += m.musician.email + ', ' + str(m.musician.phone) + '<br />'
                else:
                    musicianlist += m.instrument + ' (empty spot) ' + m.instrument + '<br />'
                
        
            description = description1.replace('(*musician_list*)', musicianlist)    

            create_gcal_event(service, vscalid, summary, date, start_time, end_time, description, location, False, '123')
        
        count = events.count()
        data = {'count':count,}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
            



def gcal(request, pYear, pMonth):

    vscalid = os.environ.get("VSCALID")
    if not vscalid:
        vscalid = settings.VSCALID

    creds = load_credentials()
    if (not creds) or (creds==False) or (creds=="needs auth"):
        HttpResponseRedirect('/events/gauthorize')
    else:
        save_credentials(creds)
        service = build('calendar', 'v3', credentials=creds, cache_discovery=False)
     
    service = build('calendar', 'v3', credentials=creds, cache_discovery=False)
    
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId=vscalid, timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    
#     event = {
#       'summary': 'Google I/O 2015',
#       'location': '800 Howard St., San Francisco, CA 94103',
#       'description': 'A chance to hear more about Google\'s developer products.',
#       'start': {
#         'dateTime': '2019-09-20T09:00:00-04:00',
#       },
#       'end': {
#         'dateTime': '2019-09-20T10:00:00-04:00',
#       },
#     }
#     
#     event = service.events().insert(calendarId=vscalid, body=event).execute()

    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])
    
    if int(pMonth) < 10:
        strMonth = "0" + str(pMonth)
    else:
        strMonth = str(pMonth)
    startdate = str(pYear) + strMonth + '01'
    enddate = str(pYear) + strMonth + '31'
    
    return render(request, "events/gcal.html", {"events" : events, "year":pYear, "month": pMonth,
                                                "startdate": startdate, "enddate": enddate,
                                               'soonevents': soonevents, 'soonreminder': soonreminder, 
                                               'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                                               'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                                               'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents                
                                                })










def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def fix_dates(wordsin):
    wordsout = [w.replace('/', '-') for w in wordsin]
#     wordsout = [w.replace('-2', '-02') for w in wordsout]
    
    return wordsout
                
def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    terms = fix_dates(terms)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['name', 'type', 'friendly_name',
                                               'date', 'hold_until', 'start_time',
                                               'end_time', 'ceremony_time',
                                               'event_type__name', 'event_type_name',
                                               'ensemble__name', 'ensemble_name',
                                               'location__name', 'location_name',
                                               'location_details', 'location__address',
                                               'location_address', 'location__link',
                                               'location__phone', 'location__email',
                                               'location_link', 'location_phone',
                                               'location_email', 'contact__name',
                                               'contact__agency', 'contact__phone',
                                               'contact__email', 'dayofcontact__phone',
                                               'dayofcontact__email', 'dayofcontact_alone_name',
                                               'dayofcontact_alone_phone', 'number_guests',
                                               'contact_details', 'contact_name',
                                               'contact_agency','contact_phone',
                                               'contact_email', 'dayofcontact__name',
                                               'dayofcontact_details', 'dayofcontact_name',
                                               'dayofcontact_phone', 'dayofcontact_email',
                                               'fee', 'contracting_fee', 'musician_fee',
                                               'deposit_fee', 'final_fee', 'cash_fee',
                                               'notes', 'records', 'music_list',
                                               'officiant_info', 'recessional_cue',
                                               ])
        
        reminder_query = get_query(query_string, ['name', 'date'])
        
        activity_query = get_query(query_string, ['name', 'date'])
        
        musicians_query = get_query(query_string, ['musician__name', 'musician__instrument',
                                                   'musician__instrument2', 'musician__email',
                                                   'musician__phone'])
        
        paymentsreceived_query = get_query(query_string, ['payment', 'amount_due',
                                                     'date', 'method', 'type', 'event__name',
                                                     'event__contact__name', 'event__contact_name'])
        
        paymentsdue_query = get_query(query_string, ['payment', 'duedate', 'musician__name',
                                                          'musician__email', 'musician__phone',
                                                          'event__name', 'event__contact__name',
                                                          'event__contact_name'])

        if request.GET['p'] == 'True':
            if request.GET['n'] == 'True':
                newest = True
                past = True
                found_entries = Event.objects.filter(entry_query).order_by('-date')
                found_reminders = Reminder.objects.filter(reminder_query).exclude(disb=True).order_by('-date')
                found_activities = Activity.objects.filter(activity_query).order_by('-date')
                found_musicians = MusicianEvent.objects.filter(musicians_query).order_by('-event__date')
                found_paymentsreceived = PaymentsReceived.objects.filter(paymentsreceived_query).order_by('-date')
                found_paymentsdue = PaymentsDue.objects.filter(paymentsdue_query).order_by('-duedate')
            else:
                newest = False
                past = True
                found_entries = Event.objects.filter(entry_query).order_by('date')
                found_reminders = Reminder.objects.filter(reminder_query).exclude(disb=True).order_by('date')
                found_activities = Activity.objects.filter(activity_query).order_by('date')
                found_musicians = MusicianEvent.objects.filter(musicians_query).order_by('event__date')
                found_paymentsreceived = PaymentsReceived.objects.filter(paymentsreceived_query).order_by('date')
                found_paymentsdue = PaymentsDue.objects.filter(paymentsdue_query).order_by('duedate')
        else:
            if request.GET['n'] == 'True':
                newest = True    
                past = False
                found_entries = Event.objects.filter(entry_query).exclude(
                    date__lt=datetime.date.today()
                    ).exclude(
                        event_archived=True
                        ).order_by('-date')
                found_reminders = Reminder.objects.filter(reminder_query).exclude(
                    event__date__lt=datetime.date.today()
                    ).exclude(
                        done=True
                        ).exclude(disb=True).order_by('-date')
                found_activities = Activity.objects.filter(activity_query).exclude(
                    event__date__lt=datetime.date.today()
                    ).order_by('-date')
                found_musicians = MusicianEvent.objects.filter(musicians_query).exclude(
                    event__date__lt=datetime.date.today()
                    ).exclude(
                        event__event_archived=True
                        ).order_by('-event__date')
                found_paymentsreceived = PaymentsReceived.objects.filter(paymentsreceived_query).exclude(
                    event__date__lt=datetime.date.today()
                    ).exclude(
                        event__event_archived=True
                        ).order_by('-date')
                found_paymentsdue = PaymentsDue.objects.filter(paymentsdue_query).exclude(
                    event__date__lt=datetime.date.today()
                    ).exclude(
                        event__event_archived=True
                        ).order_by('-duedate')

            else:
                newest = False    
                past = False
                found_entries = Event.objects.filter(entry_query).exclude(
                    date__lt=datetime.date.today()
                    ).exclude(
                        event_archived=True
                        ).order_by('date')
                found_reminders = Reminder.objects.filter(reminder_query).exclude(
                    event__date__lt=datetime.date.today()
                    ).exclude(
                        done=True
                        ).exclude(disb=True).order_by('date')
                found_activities = Activity.objects.filter(activity_query).exclude(
                    event__date__lt=datetime.date.today()
                    ).order_by('date')
                found_musicians = MusicianEvent.objects.filter(musicians_query).exclude(
                    event__date__lt=datetime.date.today()
                    ).exclude(
                        event__event_archived=True
                        ).order_by('event__date')
                found_paymentsreceived = PaymentsReceived.objects.filter(paymentsreceived_query).exclude(
                    event__date__lt=datetime.date.today()
                    ).exclude(
                        event__event_archived=True
                        ).order_by('date')
                found_paymentsdue = PaymentsDue.objects.filter(paymentsdue_query).exclude(
                    event__date__lt=datetime.date.today()
                    ).exclude(
                        event__event_archived=True
                        ).order_by('duedate')


    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])
    
    #recentactslist = [recentact, recentact, ...]
    #recentact = [eventdate, eventname, eventid, actslist]
    #actone = [date, name]
    #actslist = [actone, actone, ...]
    recentactslist = []
    recentact = []
    acteventid = ''
    acteventdate = ''
    acteventname = ''
    actname = ''
    actdate = ''
    actslist = []
    actone = []
    count = found_activities.count()
    for i, act in enumerate(found_activities):
        actname = act.name
        actdate = act.date
        actone = [actdate, actname]
        
        if i > 0: #there's at least one activity before
            if found_activities[i-1].event == act.event:  #if previous item's event was the same
                actslist.append(actone)
            else: #previous item's event was different
                acteventid = found_activities[i-1].event.id # get previous item's event details
                acteventdate = found_activities[i-1].event.date
                if found_activities[i-1].event.type == "HD":
                    acteventname = "[HD] " + found_activities[i-1].event.name
                else:
                    acteventname = found_activities[i-1].event.name
                if found_activities[i-1].event.date_ispast and act.event.event_archived:
                    actdatepast = "pastarch"
                elif found_activities[i-1].event.date_ispast:
                    actdatepast = "past"
                elif found_activities[i-1].event.event_archived:
                    actdatepast = "arch"
                else:
                    actdatepast = "not"
                recentact = [actdatepast, acteventdate, acteventname, acteventid, actslist] #save those details
                recentactslist.append(recentact)
                actslist = [] #start new actslist with this activity
                actslist.append(actone)
        else: #this is the first activity
            actslist.append(actone) #first activity in the actslist
        if (i+1) == count: #this is the last item, save now
            acteventid = act.event.id
            acteventdate = act.event.date
            if act.event.type == "HD":
                acteventname = "[HD] " + act.event.name
            else:
                acteventname = act.event.name
            if act.event.date_ispast and act.event.event_archived:
                actdatepast = "pastarch"
            elif act.event.date_ispast:
                actdatepast = "past"
            elif act.event.event_archived:
                actdatepast = "arch"
            else:
                actdatepast = "not"
            recentact = [actdatepast, acteventdate, acteventname, acteventid, actslist]
            recentactslist.append(recentact)


    return render(request, 'events/search_results.html',
                  { 'query_string': query_string, 'found_entries': found_entries, 
                    'found_reminders': found_reminders,
                    'past': past, 'newest':newest, 'found_musicians': found_musicians,
                    'found_paymentsreceived': found_paymentsreceived, 'found_paymentsdue':found_paymentsdue,
                    'found_activities': recentactslist,
                   'soonevents': soonevents, 'soonreminder': soonreminder, 
                   'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                   'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                   'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents                
                })
                       
def search_results(request):
    return render(request, 'events/search_results.html')    
       
def MusicianCreatePopup(request, pk = None):
    form = MusicianForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # if musician name already exists, then delete and cancel the rest
        if Musician.objects.filter(name=instance.name).count() > 1:
            instance.delete()
            return HttpResponse('<script>opener.closePopupExists(window);</script>')
            
        # check for new instrument, and add to model if necessary
        inst = instance.instrument
        inst2 = instance.instrument2
        if MusicianInstrument.objects.filter(instrument=inst).count() == 0:
            newinst = MusicianInstrument(instrument=inst)
            newinst.save()
        if MusicianInstrument.objects.filter(instrument=inst2).count() == 0:
            newinst = MusicianInstrument(instrument=inst2)
            newinst.save()
        #auto-populate asked list
        name = instance.name
        event = pk
        newmus = get_object_or_404(Musician, name=name)
        thisevent = get_object_or_404(Event, pk=event)
        newmusasked = MusicianEvent(musician = newmus, event = thisevent)
        newmusasked.instrument = newmus.instrument
        newmusasked.save()
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_musician");</script>' % (instance.pk, instance))
    return render(request, "events/musician_form.html", {"form" : form})

def MusiclistCreatePopup(request, ensnum = None, pk = None, cer = ''):
    #refresh music list!
    listobject = MusicList.objects.get(pk=1)
    variables.currentmusiclist = listobject.list.splitlines()
    
    if request.method == "POST":
        data = request.POST
#         #if already done, don't do important stuff again
#         if client.did_music_list and event.flag_music_list_rcvd:
#             clientalreadydidmusiclist = True
#         else:
#             clientalreadydidmusiclist = False
#         #collect data from form into nice format
        html = process_music_list(request, False, cer)
        
        #cut the cue line out of list
        if "<b>Cue for recessional: </b>" in html:
            tempbeg = html.split("<b>Cue for recessional: </b>", 1)
            tempend = tempbeg[1].split("<br />", 1)
            html = tempbeg[0] + tempend[1]
        #prep variables to pass to js
        if request.POST.get('recessionals_cue'):
            recess_cue = request.POST.get('recessionals_cue')
        else:
            recess_cue = ''
        if request.POST.get('parents_num'):
            num_parents = request.POST.get('parents_num')
        else:
            num_parents = 0
        if request.POST.get('bridesmaids_num'):
            num_bridesmaids = request.POST.get('bridesmaids_num')
        else:
            num_bridesmaids = 0
        if request.POST.get('flowergirls') == 'Yes':
            flowergirls = True
        else:
            flowergirls = False
        
        event = get_object_or_404(Event, pk=pk)
        if Client.objects.filter(event=event.id).exists():
            client = get_object_or_404(Client, event=event.id)
        else:
            client = Client(event=event)
            client.save()
        
        customcount = html.count("$25")
        if customcount > 0:
            register_reminder(settings.CHECK_MUSIC_LIST, date.today() + relativedelta(days=3), event)

        temp = is_reminder_done(settings.SEND_MUSIC_LIST, event)
        disable_reminder(settings.SEND_MUSIC_LIST, event, temp)
        
        client.did_music_list = True
        client.music_list_date = date.today()
        client.save()
        new_action_save(['Janie entered music list manually','dummy'], event)
    
        
        #js does:    
        #            mark event.flag_music_list_rcvd = true
        #            mark event.music_list_rcvddate = today
        #            mark event.flag_music_list_sent = true
        #            if not event.music_list_sentdate, mark it = today
        #            set recessionals_cue, parents_num, bridesmaids_num, flowergirls with passed variables
        #            process due_dates, auto_reminders, update_flags
        
                
        data = {'html':html, 'recess_cue':recess_cue, 'num_parents':num_parents, 'num_bridesmaids':num_bridesmaids, 
                'flowergirls':flowergirls,}
        return HttpResponse('<script>opener.closePopup2a(window, ' + json.dumps(data) + ');</script>')
    
    
    else:
        num = ensnum
        if num == 1:
            name = "solo"
        elif num == 2:
            name = "quartet"
        elif num == 3:
            name = "quartet"
        elif num == 4:
            name = "quartet"
        else:
            name = "quartet"
        #print(name)
        list_parents = get_object_or_404(MusicRequest, name=name, type="parents")
        list_groomsmens = get_object_or_404(MusicRequest, name=name, type="groomsmens")
        list_bridesmaids = get_object_or_404(MusicRequest, name=name, type="bridesmaids")
        list_brides = get_object_or_404(MusicRequest, name=name, type="brides")
        list_ceremonymusics = get_object_or_404(MusicRequest, name=name, type="ceremonymusics")
        list_recessionals = get_object_or_404(MusicRequest, name=name, type="recessionals")
        list_cocktails = get_object_or_404(MusicRequest, name=name, type="cocktails")
        list_dinners = get_object_or_404(MusicRequest, name=name, type="dinners")
        list_backgrounds = get_object_or_404(MusicRequest, name=name, type="backgrounds")
        
        parents = list_parents.list.splitlines()
        groomsmens = list_groomsmens.list.splitlines()
        bridesmaids = list_bridesmaids.list.splitlines()
        brides = list_brides.list.splitlines()
        ceremonymusics = list_ceremonymusics.list.splitlines()
        recessionals = list_recessionals.list.splitlines()
        cocktails = list_cocktails.list.splitlines()
        dinners = list_dinners.list.splitlines()
        backgrounds = list_backgrounds.list.splitlines()
        receptions = cocktails
        parents_num = 0
        bridesmaids_num = 0
        flowergirls = False
        
        etype = cer.lower()
        do_ceremony = do_cocktails = do_reception = do_dinner = do_background = do_misc = False
        if 'ceremony' in etype:
            do_ceremony = True
        if 'cocktail' in etype:
            do_cocktails = True
        if 'reception' in etype:
            do_reception = True
        if 'dinner' in etype:
            do_dinner = True
        if 'background' in etype:
            do_background = True
        if not do_ceremony and not do_cocktails and not do_reception and not do_background and not do_dinner:
            do_misc = True
        
        return render(request, 'events/musiclist_create.html', {'groomsmens':groomsmens,
                                                               'parents':parents, 'bridesmaids':bridesmaids,
                                                               'brides':brides, 'ceremonymusics':ceremonymusics,
                                                               'recessionals':recessionals,
                                                               'cocktails':cocktails, 'dinners':dinners,
                                                               'backgrounds':backgrounds,
                                                               'receptions':receptions,
                                                               'do_ceremony':do_ceremony, 
                                                               'do_cocktails':do_cocktails,
                                                               'do_reception':do_reception,
                                                               'do_dinner':do_dinner,
                                                               'do_background':do_background,
                                                               'do_misc':do_misc, 'parents_num':parents_num,
                                                               'bridesmaids_num':bridesmaids_num,
                                                               'flowergirls':flowergirls,
                                                                 'error':False}) 

        


    
    
    
def ReminderCreatePopup(request, pk = None):
    form = ReminderForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if pk:
            instance.event_id = pk
        instance.done = False
        instance.edited = True
        instance.save()
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_reminder");</script>' % (instance.pk, instance))
    return render(request, "events/reminder_form.html", {"form" : form})

def ActivityCreatePopup(request, pk = None):
    today = date.today()
    form = ActivityForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if pk:
            instance.event_id = pk
        instance.done = False
        instance.save()
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_activity");</script>' % (instance.pk, instance))
    form.fields['date'].initial = today
    return render(request, "events/activity_form.html", {"form" : form})


def VenueCreatePopup(request):
    form = VenueForm(request.POST or None)
    if form.is_valid():
        instance = form.save()

        ## Change the value of the "#id_author". This is the element id in the form
        
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_venue");</script>' % (instance.pk, instance))
    
    return render(request, "events/venue_form.html", {"form" : form})

def VenueEditPopup(request, pk = None):
    instance = get_object_or_404(Venue, pk = pk)
    form = VenueForm(request.POST or None, instance = instance)
    if form.is_valid():
        instance = form.save()
        
        ## Change the value of the "#id_author". This is the element id in the form
        
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_venue");</script>' % (instance.pk, instance))

    return render(request, "events/venue_form.html", {"form" : form})




@csrf_exempt
def get_venue_id(request):
    if request.is_ajax():
        venue_name = request.GET['venue_name']
        venue_id = Venue.objects.get(name = venue_name).id
        data = {'venue_id':venue_id,}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")

@csrf_exempt
def get_venue_info(request):
    if request.is_ajax():
        venue_name = request.GET['venue_name']
        if Venue.objects.filter(name=venue_name).exists():
            venue_address = Venue.objects.get(name = venue_name).address
            venue_link = Venue.objects.get(name = venue_name).link
            venue_phone = Venue.objects.get(name = venue_name).phone
            venue_email = Venue.objects.get(name = venue_name).email
            noerror = True
        else:
            noerror = False
            venue_address = ''
            venue_link = ''
            venue_phone = ''
            venue_email = ''
        data = {'venue_name':venue_name, 'noerror':noerror, 'venue_address':venue_address, 'venue_link':venue_link,
                'venue_phone':format_phone(venue_phone), 'venue_email':venue_email,}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


@csrf_exempt
def get_reminders(request):
    if request.is_ajax():
        queryset = Reminder.objects.filter(event_id = request.GET['event_id'], disb=False).order_by('done', '-donedt', 'date')
        queryset2 = Reminder.objects.filter(event_id = request.GET['event_id'], disb=True).order_by('date')
#         reminders = list(queryset.values())
#         dataraw = {'reminders':reminders}

#         test = []
#         test.instant = []
#         test.instance.id = '67'
#         test.date_ispast = False
#         print(test)
        mlist = render_to_string('events/render_reminderslist.html', 
                                 {'reminders':queryset, 'disableds':queryset2})
        num = queryset.filter(done=False).count()
        #print(num)
        num = str(num)

        today = date.today()
        sevendays = today + relativedelta(days=7)
        fourteendays = today + relativedelta(days=14)
        past182days = today + relativedelta(days=-182)
        
        booking1 = settings.INVITE_MUSICIANS
        booking2 = settings.ALL_MUSICIANS_BOOKED
    
        soonreminder = Reminder.objects.filter(date__range=[past182days, sevendays]).exclude(
            done=True).exclude(disb=True).exclude(event__date__lt=today).exclude(name=booking2, date__range=[past182days, sevendays]).exclude(
            name=booking1, date__range=[past182days, sevendays]).exclude(
            event__event_archived=True).order_by('event__pk', 'event__date', 'date')
    
        # !!!!!!!!!!!!!!!!!!!!!'pastduereminder' now actually refers to new booking-musicians reminders!'!!!!!!!!!!!!!!!!!
        pastduereminder = Reminder.objects.filter(Q(name=booking2, date__range=[past182days, fourteendays]) | Q(name=booking1, date__range=[past182days, fourteendays])).exclude(
            done=True).exclude(disb=True).exclude(event__date__lt=today).exclude(
                event__event_archived=True).order_by('-date')
        
        numtotal = soonreminder.exclude(auto=True).count() # + pastduereminder.exclude(auto=True).count()
        numbooking = pastduereminder.exclude(auto=True).count()
        
        data = {'mlist':mlist, 'num':num, 'numtotal':numtotal, 'numbooking':numbooking}

#             reminders = Reminder.objects.filter(event_id=pk, disb=False).order_by('done', 'date')
#             reminderscount = reminders.filter(done=False).count


#         data = serializers.serialize('json', queryset)
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")

@csrf_exempt
def get_5_reminders(request):  #updated so that auto=True reminders are included IF they are past due
    if request.is_ajax():
        queryset = Reminder.objects.filter(event_id = request.GET['event_id'], disb=False).filter(
            done=False).order_by('date')[:5]
            
        ommited = []
        for item in queryset:
            if item.auto and (not item.is_past_due): #in other words, exclude it if it's auto and not past due
                                                    # if it's auto and pastdue, it'll stay in list
                ommited.append(item.id)
        queryset2 = Reminder.objects.filter(event_id=request.GET['event_id']).filter(
            done=False, disb=False).exclude(id__in=[o for o in ommited]).order_by('date')[:5]
            
        data = serializers.serialize('json', queryset2)
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


def mark_reminder_done(request, reminder_id):
    #this routine is curretnly unused ! 
    thisreminder = get_object_or_404(Reminder, pk=reminder_id)
    thisreminder.done = True
    if thisreminder.done:
        if not thisreminder.donedt:
            thisreminder.donedt = datetime.datetime.now()
    else:
        thisreminder.donedt = None
    thisreminder.save()
    thisevent = get_object_or_404(Event, pk=thisreminder.event_id)
    #set flags so reminder text is recorded to flag, new action, flags right now
    thisevent.event_reminders_done = False
    set_flags(thisreminder.name, thisevent)
    process_due_dates(thisevent)
    process_auto_reminders(thisevent)
    process_update_flags(thisevent)
    thisevent.event_reminders_done = True
    thisevent.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
def get_booked_musicians(request):
    if request.is_ajax():
        queryset = MusicianEvent.objects.filter(event_id=request.GET['event_id'], yes=True, no=False).order_by('rank')
        data = ''
        for musician in queryset:
            data += musician.musician.name + ','
            data += musician.instrument + ','
        if data == '':
            data = ''
        else:
            data = data[:-1] # remove last comma
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


@csrf_exempt
def get_musiclist(request):
    if request.is_ajax():
        event = get_object_or_404(Event, pk=request.GET['event_id']);
        data = event.music_list
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
    

@csrf_exempt
def get_activities(request):
    if request.is_ajax():
        queryset = Activity.objects.filter(event_id = request.GET['event_id']).order_by('-date', '-id')
#         reminders = list(queryset.values())
#         dataraw = {'reminders':reminders}
        data = serializers.serialize('json', queryset)
        
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_activities_num(request):
    if request.is_ajax():
        queryset = Activity.objects.filter(event_id = request.GET['event_id']).order_by('-date', '-id')
        num = queryset.count()
        #print(num)
        num = str(num)

        today = date.today()
        pastsevendays = today + relativedelta(days=-7)
        recentactivities = Activity.objects.filter(date__range=[pastsevendays, today]).exclude(
            event__event_archived=True).exclude(event__date__lt=today).order_by('event__date', '-date', '-pk')
        recentactslist = []
        recentact = []
        acteventid = ''
        acteventdate = ''
        acteventname = ''
        actname = ''
        actdate = ''
        actslist = []
        actone = []
        count = recentactivities.count()
        for i, act in enumerate(recentactivities):
            actname = act.name
            actdate = act.date
            actone = [actdate, actname]
            
            if i > 0: #there's at least one activity before
                if recentactivities[i-1].event == act.event:  #if previous item's event was the same
                    actslist.append(actone)
                else: #previous item's event was different
                    acteventid = recentactivities[i-1].event.id # get previous item's event details
                    acteventdate = recentactivities[i-1].event.date
                    if recentactivities[i-1].event.type == "HD":
                        acteventname = "[HD] " + recentactivities[i-1].event.name
                    else:
                        acteventname = recentactivities[i-1].event.name
                    if recentactivities[i-1].event.date_ispast and act.event.event_archived:
                        actdatepast = "pastarch"
                    elif recentactivities[i-1].event.date_ispast:
                        actdatepast = "past"
                    elif recentactivities[i-1].event.event_archived:
                        actdatepast = "arch"
                    else:
                        actdatepast = "not"
                    recentact = [actdatepast, acteventdate, acteventname, acteventid, actslist] #save those details
                    recentactslist.append(recentact)
                    actslist = [] #start new actslist with this activity
                    actslist.append(actone)
            else: #this is the first activity
                actslist.append(actone) #first activity in the actslist
            if (i+1) == count: #this is the last item, save now
                acteventid = act.event.id
                acteventdate = act.event.date
                if act.event.type == "HD":
                    acteventname = "[HD] " + act.event.name
                else:
                    acteventname = act.event.name
                if act.event.date_ispast and act.event.event_archived:
                    actdatepast = "pastarch"
                elif act.event.date_ispast:
                    actdatepast = "past"
                elif act.event.event_archived:
                    actdatepast = "arch"
                else:
                    actdatepast = "not"
                recentact = [actdatepast, acteventdate, acteventname, acteventid, actslist]
                recentactslist.append(recentact)

        numtotal = len(recentactslist)
        
        data = {'num':num, 'numtotal': numtotal}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse(json.dumps(data), content_type='application/json')
    


def get_5_activities(request):
    if request.is_ajax():
        queryset = Activity.objects.filter(event_id = request.GET['event_id']).order_by('-date', '-id')[:5]
#         reminders = list(queryset.values())
#         dataraw = {'reminders':reminders}
        data = serializers.serialize('json', queryset)
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


@csrf_exempt
def set_remind_done(request):
    if request.is_ajax():
        remind_id = request.GET['remind_id']
        reminder = Reminder.objects.get(pk = remind_id)
        reminder.done = not reminder.done
        if reminder.done:
            if not reminder.donedt:
                reminder.donedt = datetime.datetime.now()
        else:
            reminder.donedt = None
        reminder.save()
        done = reminder.done
        text = reminder.name
        data = {'done':done,'text':text}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")

def activity_ajax_add(request):
    if request.is_ajax():
        activity_text = request.GET['activity_text']
        event_id = request.GET['event_id']
        event = get_object_or_404(Event, pk=event_id);
        newact = Activity(name = activity_text)
        newact.date = date.today()
        newact.event = event
        newact.save()
        data = {'OK':'ok'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
        

@csrf_exempt
def get_rates(request):
    if request.is_ajax():
        rate_name = request.GET['rate_name']
        hours = request.GET['hours']
        if hours == '1':
            ens1 = RateChart.objects.get(name = rate_name).solo
            ens2 = RateChart.objects.get(name = rate_name).duo
            ens3 = RateChart.objects.get(name = rate_name).trio
            ens4 = RateChart.objects.get(name = rate_name).quartet
            ensm = RateChart.objects.get(name = rate_name).musician
        if hours == '2':
            ens1 = RateChart.objects.get(name = rate_name).two_solo
            ens2 = RateChart.objects.get(name = rate_name).two_duo
            ens3 = RateChart.objects.get(name = rate_name).two_trio
            ens4 = RateChart.objects.get(name = rate_name).two_quartet
            ensm = RateChart.objects.get(name = rate_name).two_musician
        if hours == '3':
            ens1 = RateChart.objects.get(name = rate_name).three_solo
            ens2 = RateChart.objects.get(name = rate_name).three_duo
            ens3 = RateChart.objects.get(name = rate_name).three_trio
            ens4 = RateChart.objects.get(name = rate_name).three_quartet
            ensm = RateChart.objects.get(name = rate_name).three_musician
        if hours == '4':
            ens1 = RateChart.objects.get(name = rate_name).four_solo
            ens2 = RateChart.objects.get(name = rate_name).four_duo
            ens3 = RateChart.objects.get(name = rate_name).four_trio
            ens4 = RateChart.objects.get(name = rate_name).four_quartet
            ensm = RateChart.objects.get(name = rate_name).four_musician
        data = {'ens1':ens1, 'ens2':ens2, 'ens3':ens3, 'ens4':ens4, 'ensm':ensm}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


@csrf_exempt
def get_event_type_id(request):
    if request.is_ajax():
        event_type_name = request.GET['event_type_name']
        if EventType.objects.filter(name = event_type_name).exists():
            found = True
            event_type_id = EventType.objects.get(name = event_type_name).id
        else:
            found = False
            event_type_id = 0
        data = {'event_type_id':event_type_id,'found':found}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")

@csrf_exempt
def get_ensemble_id(request):
    if request.is_ajax():
        ensemble_name = request.GET['ensemble_name']
        if Ensemble.objects.filter(name = ensemble_name).exists():
            ensemble_id = Ensemble.objects.get(name = ensemble_name).id
            ensemble_number = Ensemble.objects.get(name = ensemble_name).number
            found = True
        else:
            found = False
            ensemble_number = 0
            ensemble_id = 0
        data = {'ensemble_id':ensemble_id, 'ensemble_number':ensemble_number,'found':found}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


def ContactCreatePopup(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        instance = form.save()

        ## Change the value of the "#id_author". This is the element id in the form
        
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_contact");</script>' % (instance.pk, instance))
    
    return render(request, "events/contact_form.html", {"form" : form})

def ContactEditPopup(request, pk = None):
    instance = get_object_or_404(Contact, pk = pk)
    form = ContactForm(request.POST or None, instance = instance)
    if form.is_valid():
        instance = form.save()
        
        ## Change the value of the "#id_author". This is the element id in the form
        
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_contact");</script>' % (instance.pk, instance))

    return render(request, "events/contact_form.html", {"form" : form})

@csrf_exempt
def get_contact_id(request):
    if request.is_ajax():
        contact_name = request.GET['contact_name']
        contact_id = Contact.objects.get(name = contact_name).id
        data = {'contact_id':contact_id,}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")

@csrf_exempt
def get_contact_info(request):
    if request.is_ajax():
        contact_name = request.GET['contact_name']
        if Contact.objects.filter(name=contact_name).exists(): 
            contact_agency = Contact.objects.get(name = contact_name).agency
            contact_phone = Contact.objects.get(name = contact_name).phone
            contact_email = Contact.objects.get(name = contact_name).email
            contact_friendlyname = Contact.objects.get(name = contact_name).friendlyname
            noerror = True
        else:
            noerror = False
            contact_agency = ''
            contact_phone = ''
            contact_email = ''
            contact_friendlyname = ''
        data = {'contact_name':contact_name, 'contact_agency':contact_agency, 'noerror':noerror,
                'contact_phone':format_phone(contact_phone), 'contact_email':contact_email, 'contact_friendlyname':contact_friendlyname}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


def DayofcontactCreatePopup(request):
    form = DayofcontactForm(request.POST or None)
    if form.is_valid():
        instance = form.save()

        ## Change the value of the "#id_author". This is the element id in the form
        
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_dayofcontact");</script>' % (instance.pk, instance))
    
    return render(request, "events/dayofcontact_form.html", {"form" : form})

def DayofcontactEditPopup(request, pk = None):
    instance = get_object_or_404(DayofContact, pk = pk)
    form = DayofcontactForm(request.POST or None, instance = instance)
    if form.is_valid():
        instance = form.save()
        
        ## Change the value of the "#id_author". This is the element id in the form
        
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_dayofcontact");</script>' % (instance.pk, instance))

    return render(request, "events/dayofcontact_form.html", {"form" : form})

@csrf_exempt
def get_dayofcontact_id(request):
    if request.is_ajax():
        dayofcontact_name = request.GET['dayofcontact_name']
        dayofcontact_id = DayofContact.objects.get(name = dayofcontact_name).id
        data = {'dayofcontact_id':dayofcontact_id,}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")

@csrf_exempt
def get_dayofcontact_info(request):
    if request.is_ajax():
        dayofcontact_name = request.GET['dayofcontact_name']
        if DayofContact.objects.filter(name=dayofcontact_name).exists():
            noerror = True
            dayofcontact_phone = DayofContact.objects.get(name = dayofcontact_name).phone
            dayofcontact_email = DayofContact.objects.get(name = dayofcontact_name).email
        else:
            noerror = False
            dayofcontact_phone = ''
            dayofcontact_email = ''
        data = {'dayofcontact_name':dayofcontact_name, 'noerror': noerror,
                'dayofcontact_phone':format_phone(dayofcontact_phone), 'dayofcontact_email':dayofcontact_email,}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


def test_selenium(request):
    nothing = 1
#     
#     #is this running on heroku, or on local?
#     test = os.environ.get("CHROMEDRIVER_PATH")
#     if not test:
#         driver = webdriver.Chrome()
#     else:
#         chrome_options = webdriver.ChromeOptions()
#         chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
#         chrome_options.add_argument("--headless")
#         chrome_options.add_argument("--disable-dev-shm-usage")
#         chrome_options.add_argument("--no-sandbox")
#         driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
#     
#     #start using selenium now
#     driver.get('https://www.suncoastcreditunion.com')
# #     elem = driver.find_element_by_name("q")
# #     elem.clear()
# #     elem.send_keys("pycon2")
# #     print(elem.get_attribute('value'))
# #     print('hello')
# #     elem.send_keys(Keys.RETURN)
#     
#     #login
#     member_elem = driver.find_element_by_name("memberId")
#     pass_elem = driver.find_element_by_name("password")
#     login_elem = driver.find_element_by_id("loginButton")
#     member_elem.clear()
#     pass_elem.clear()
#     test = os.environ.get("CHROMEDRIVER_PATH")
#     if not test:
#         member_elem.send_keys(settings.SUNCOAST_MEMBER)
#         pass_elem.send_keys(settings.SUNCOAST_PASS)
#     else:
#         member_elem.send_keys(os.environ.get("SUNCOAST_MEMBER"))
#         pass_elem.send_keys(os.environ.get("SUNCOAST_PASS"))
#     login_elem.click()    
#     
#     
#     
#     #driver.close()
#     
#     
#     
#     
#     soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
#     this = Global.objects.get(pk=1)
#     smallcal = sidecal(this.sidecal_year, this.sidecal_month)
#     sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])
#     return render(request, 'events/test_selenium.html', {'soonevents': soonevents, 'soonreminder': soonreminder, 
#                                                        'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
#                                                        'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
#                                                        'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents                
#                                                      })
#     
    
    


def reminder_edit_automation(request, pk = None):
    instance = get_object_or_404(Reminder, pk = pk)
    form = ReminderFormAuto(request.POST or None, instance = instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.edited = True
        if instance.done:
            if not instance.donedt:
                instance.donedt = datetime.datetime.now()
        else:
            instance.donedt = None
        instance.save()
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_reminder");</script>' % (instance.pk, instance))
    return render(request, "events/reminder_form_auto.html", {"form" : form})

def reminder_edit_regular(request, pk = None):
    instance = get_object_or_404(Reminder, pk = pk)
    form = ReminderFormAuto(request.POST or None, instance = instance)
    error = False
    if form.is_valid():
        instance = form.save(commit=False)
        instance.edited = True
        if instance.event.contact:
            tempemail = instance.event.contact.email
        else:
            tempemail = instance.event.contact_email
        if instance.auto and not tempemail: 
            #if making this auto, but no contact email, show error
            error = True
        else:
            if instance.done:
                if not instance.donedt:
                    instance.donedt = datetime.datetime.now()
            else:
                instance.donedt = None
            instance.save()
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_reminder");</script>' % (instance.pk, instance))
    auto_capable = is_reminder_automation_capable(instance.name)
    return render(request, "events/reminder_form_reg.html", {"form" : form, 'auto_capable':auto_capable, 'error':error})

def musician_edit(request, pk = None):
    instance = get_object_or_404(Musician, pk = pk)
    form = MusicianForm(request.POST or None, instance = instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_musician");</script>' % (instance.pk, instance))
    return render(request, "events/musician_form_edit.html", {"form" : form})
    

def markpayduedone(request):
    if request.is_ajax():
        pay_id = request.GET['pay_id']
        pay = PaymentsDue.objects.get(pk = pay_id)
        pay.done = True
        pay.donedate = date.today()
        pay.save()
        data = {'error':'none'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
    


def ratechartdelete(request):
    if request.is_ajax():
        chart_id = request.GET['chart_id']
        chart = RateChart.objects.get(pk = chart_id)
        chart.delete()
        data = {'error':'none'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
    

def editratecharts(request, chartname = "add"):
    error = False
    if chartname == 'add':
        thischart = RateChart(None)
    else:
        thischart = get_object_or_404(RateChart, id=int(chartname))
    
    if request.method == "POST":
        form = FormRateChart(request.POST, instance=thischart)
        if form.is_valid():
            newform = form.save(commit=False)
            #check for already existing duplicate name field and error if so
            exists = RateChart.objects.filter(name=newform.name).exists()
            if exists:
                otherid = get_object_or_404(RateChart, name=newform.name).id
            else:
                otherid = newform.id
            if exists and chartname == 'add':
                error = True
            elif chartname != 'add' and otherid != newform.id:
                error = True
            else:
                newform.save()
                return redirect('/events/rates/')
    else:
        form = FormRateChart(instance=thischart)

        #form = AddForm(request.POST, instance=thisevent)
        
    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])
    return render(request, 'events/editratecharts.html', {'form': form, 'error': error,
                                                       'soonevents': soonevents, 'soonreminder': soonreminder, 
                                                       'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                                                       'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                                                       'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents                
                                                     })
    
    

def esigdelete(request):
    if request.is_ajax():
        changedef = False
        chart_id = request.GET['chart_id']
        chart = ESig.objects.get(pk = chart_id)
        if chart.default:
            changedef = True
        chart.delete()
#         if changedef:
#             newdef = ESig.
        data = {'error':'none'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
    

def editesig(request, chartname = "add"):
    error = False
    if chartname == 'add':
        thischart = ESig(None)
    else:
        thischart = get_object_or_404(ESig, id=int(chartname))
    
    if request.method == "POST":
        form = ESigForm(request.POST, instance=thischart)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.date = date.today()
            #check for already existing duplicate name field and error if so
            exists = ESig.objects.filter(name=newform.name).exists()
            if exists:
                otherid = get_object_or_404(ESig, name=newform.name).id
            else:
                otherid = newform.id
            if exists and chartname == 'add':
                error = True
            elif chartname != 'add' and otherid != newform.id:
                error = True
            else:
                #add sigstart and sigend tags if not there yet
                if "<!-- sigstart --><div style='width:400px;overflow:hidden" not in newform.sig:
                    newform.sig = "<!-- sigstart --><div style='width:400px;overflow:hidden;'>" + newform.sig + "</div><!-- sigend -->"
    
                #if marked as default, find old default and change it
                if newform.default:
                    exists = ESig.objects.filter(default=True).exists()
                    if exists:
                        defaultsig = get_object_or_404(ESig, default=True)
                        defaultsig.default = False
                        defaultsig.save()
                #if marked as default_alt, find old default_alt and change it
                if newform.default_alt:
                    exists_alt = ESig.objects.filter(default_alt=True).exists()
                    if exists_alt:
                        defaultaltsig = get_object_or_404(ESig, default_alt=True)
                        defaultaltsig.default_alt = False
                        defaultaltsig.save()
                    
                newform.save()
                return redirect('/events/esigs/')
    else:
        form = ESigForm(instance=thischart)
        
    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])
    return render(request, 'events/editesig.html', {'form': form, 'error':error,
                                                       'soonevents': soonevents, 'soonreminder': soonreminder, 
                                                       'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                                                       'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                                                       'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents                
                                                     })
    
    

def esigs(request):
    esigs = ESig.objects.order_by('-default', '-default_alt', '-date')
    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])

    return render(request, 'events/esigs.html', {'esigs': esigs,
                                               'soonevents': soonevents, 'soonreminder': soonreminder, 
                                               'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                                               'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                                               'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents})



def editforms(request):
    forms_contract = FormHtml.objects.filter(order__gte=20, order__lte=29).order_by('order')
    forms_deposit = FormHtml.objects.filter(order__gte=30, order__lte=39).order_by('order')
    forms_final = FormHtml.objects.filter(order__gte=40, order__lte=49).order_by('order')
    forms_musiclist = FormHtml.objects.filter(order__gte=50, order__lte=59).order_by('order')
    forms_confirmation = FormHtml.objects.filter(order__gte=60, order__lte=69).order_by('order')
    forms_hold = FormHtml.objects.filter(order__gte=70, order__lte=79).order_by('order')
    forms_musicians = FormHtml.objects.filter(order__gte=80, order__lte=89).order_by('order')
    forms_other = FormHtml.objects.filter(order__gte=90, order__lte=99).order_by('order')
    forms_extra = FormHtml.objects.filter(order__gte=10, order__lte=19).order_by('order')
    
    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])
    

    return render(request, 'events/editforms.html', {'forms_contract': forms_contract, 'forms_deposit': forms_deposit,
                                                     'forms_final': forms_final, 'forms_musiclist': forms_musiclist,
                                                     'forms_confirmation': forms_confirmation, 'forms_hold': forms_hold,
                                                     'forms_musicians': forms_musicians, 'forms_other': forms_other, 'forms_extra': forms_extra,
                                                       'soonevents': soonevents, 'soonreminder': soonreminder, 
                                                       'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                                                       'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                                                       'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents                
                                                     })

def editform(request, form):
    thisform = get_object_or_404(FormHtml, pk=form)
    #template = FormHtml.objects.filter(pk=form)
    if request.method == "POST":
        form = FormHtmlForm(request.POST, instance=thisform)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.save()
            return redirect('/events/editforms/')
    else:
        form = FormHtmlForm(instance=thisform)
    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])
    return render(request, 'events/editform.html', {'form': form,
                                                       'soonevents': soonevents, 'soonreminder': soonreminder, 
                                                       'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                                                       'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                                                       'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents                
                                                     })


def delete(request, pk):
    thisform = get_object_or_404(Event, pk=pk)
    thisform.delete()
    check_gcal(thisform, True)
    return redirect('/events/archived')

def unarchive(request, pk):
    thisform = get_object_or_404(Event, pk=pk)
    thisform.event_archived = False
    thisform.save()
    check_gcal(thisform, False)
    return redirect('/events/archived')

def archive(request, pk):
    thisform = get_object_or_404(Event, pk=pk)
    thisform.event_archived = True
    thisform.save()
    check_gcal(thisform, True)
    return redirect('/events/')

def tasks(request): #no longer used!
    today = date.today()
    tendays = today + relativedelta(days=10)
    pastsevendays = today + relativedelta(days=-7)
    soon = Reminder.objects.filter(date__range=[today, tendays]).exclude(
        done=True).exclude(disb=True).exclude(event__date__lt=today).order_by('date')
    pastdue = Reminder.objects.exclude(done=True).exclude(disb=True).exclude(event__date__lt=today).filter(Q(date__lt=today)).order_by('date')
    activities = Activity.objects.filter(date__range=[pastsevendays, today]).order_by('-date')

    
 
    #process_auto_reminders(event) -- would be necessary once full automation occurs
    #    since then some things like contracts completed or musicians answered
    #    or automatic emails sent out could have happened since last looking at event
        
    return render(request, 'events/tasks.html', {'soon': soon, 'pastdue': pastdue, 'activities': activities})    



def cycle(request, mode):
    if mode == "WEEK":
        browse_mode = "MONTH"
    elif mode == "MONTH":
        browse_mode = "DAY"
    elif mode == "DAY":
        browse_mode = "WEEK"
    old_mode = Global.objects.get(pk=1)
    old_mode.browse_mode = browse_mode
    old_mode.save()
    return redirect('/events/browse/0')

def browse_forward(request, mode, event_id):
    skipped=0
    old_date = Global.objects.get(pk=1).browse_date
    if mode == "EVENT":
        old_event_date = get_object_or_404(Event, pk=event_id).date
        new_events = (Event.objects
                        .filter(date__gte=old_event_date, event_archived=False)
                        .order_by('date', 'start_time', 'id'))
        id_list = list(new_events.values_list('id', flat=True))
        try:
            next_id = id_list[id_list.index(int(event_id)) + 1]
            new_event_id = Event.objects.get(id=next_id).id 
        except IndexError:
            new_event_id = event_id   
        return redirect('/events/' + str(new_event_id) + '/edit')
    else:
        if mode == "WEEK":
            browse_date = old_date + relativedelta(weekday=calendar.MONDAY)
            if browse_date == old_date:
                browse_date = old_date + relativedelta(weekday=calendar.MONDAY, weeks=1)
        elif mode == "MONTH":
            browse_date = old_date + relativedelta(day=1, months=+1)
            if browse_date == old_date:
                browse_date = old_date + relativedelta(day=1, months=+1)
        elif mode == "DAY":
            browse_date = old_date + relativedelta(days=+1)
        old_record = Global.objects.get(pk=1)
        old_record.browse_date = browse_date
        old_record.save()
        return redirect('/events/browse/' + str(skipped))

def browse_backward(request, mode, event_id):
    skipped = 0
    old_date = Global.objects.get(pk=1).browse_date
    if mode == "EVENT":
        old_event_date = get_object_or_404(Event, pk=event_id).date
        new_events = (Event.objects
                        .filter(date__lte=old_event_date, event_archived=False)
                        .order_by('-date', '-start_time', '-id'))
        id_list = list(new_events.values_list('id', flat=True))
        try:
            next_id = id_list[id_list.index(int(event_id)) + 1]
            new_event_id = Event.objects.get(id=next_id).id 
        except IndexError:
            new_event_id = event_id   
        return redirect('/events/' + str(new_event_id) + '/edit')
    else:
        if mode == "WEEK":
            browse_date = old_date + relativedelta(weekday=calendar.MONDAY, weeks=-1)
        elif mode == "MONTH":
            browse_date = old_date + relativedelta(day=1)
            if browse_date == old_date:
                browse_date = old_date + relativedelta(day=1, months=-1)
        elif mode == "DAY":
            browse_date = old_date + relativedelta(days=-1)
        old_record = Global.objects.get(pk=1)
        old_record.browse_date = browse_date
        old_record.save()
        return redirect('/events/browse/' + str(skipped))

def edit_nextevent(request):
    today = date.today()
    new_event_id = (Event.objects
                    .filter(date__gte=today, event_archived=False)
                    .order_by('date', 'start_time', 'id')
                    .first().id)
    return redirect('/events/' + str(new_event_id) + '/edit')

def browse_today(request, mode):
    today = date.today()
    skipped = 0
    if mode == "WEEK":
        browse_date = today
    elif mode == "MONTH":
        browse_date = today
    elif mode == "DAY":
        browse_date = today
    old_record = Global.objects.get(pk=1)
    old_record.browse_date = browse_date
    old_record.save()
    return redirect('/events/browse/' + str(skipped))

               
def browse(request, skip):
    today = date.today()
    
    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
    
    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])
    if this.last_updated != today:
        this.browse_date = today
        this.save()
    browse_mode = Global.objects.get(pk=1).browse_mode
    browse_date = Global.objects.get(pk=1).browse_date
    if browse_mode == "WEEK":        
        until = browse_date + relativedelta(weekday=calendar.SUNDAY)
        browse_date = until + relativedelta(days=-6)
    if browse_mode == "MONTH":
        until = browse_date + relativedelta(day=31)
        browse_date = until + relativedelta(day=1)
    if browse_mode == "DAY":
        until = browse_date
    events = Event.objects.filter(date__range=[browse_date, until]).exclude(
        event_archived=True).order_by('date','start_time')
    
    
    this = Global.objects.get(pk=1)
    for event in events:
        
        #process due dates only when necessary
        if not event.event_reminders_done:
            process_auto_reminders(event)
            process_due_dates(event)
            process_update_flags(event)
            event.event_reminders_done = True
            event.save()
            
            
        #process_auto_reminders(event) -- would be necessary once full automation occurs
        #    since then some things like contracts completed or musicians answered
        #    or automatic emails sent out could have happened since last looking at event
        
        #only once per day:
        if this.last_updated != today:
            process_auto_reminders(event)
            process_due_dates(event)
            process_update_flags(event)
            event.save()
#             this.last_updated = today
#             this.save()
            
    this.last_updated = today
    this.save()    
    
    return render(request, 'events/browse.html', {'events': events, 'browse_mode': browse_mode,
                                                  'from': browse_date, 'until': until, 'skip': skip,
                                                  'soonevents': soonevents, 'soonreminder': soonreminder, 
                                                  'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                                                  'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                                                  'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents})    




def client_confirm_event(request, kind, eventnum):
    event = get_object_or_404(Event, pk=eventnum)
    if Client.objects.filter(event=event.id).exists():
        client = get_object_or_404(Client, event=event.id)
    else:
        client = Client(event=event)
        client.save()
    error = False
    
    if kind == 'confirmed':
         
        if client.did_verify_info and event.flag_final_confirmation_rcvd:
            clientalreadyconfirmedfinal = True
        else:
            clientalreadyconfirmedfinal = False
         
        # mark all pertinent flags, etc.
        client.did_verify_info = True
        client.verify_info_date = date.today()
        client.save()
        event.event_reminders_done = False
        event.flag_final_confirmation_rcvd = True
        event.confirmation_rcvddate = date.today()
        event.flag_final_confirmation_sent = True #of course, if filled out, then mark as sent
        if not event.confirmation_sentdate:
            event.confirmation_sentdate = date.today()
         
        temp = is_reminder_done(settings.SEND_FINAL_CONFIRMATION, event)
        process_due_dates(event)
        process_auto_reminders(event)
        process_update_flags(event)
        event.save()
        disable_reminder(settings.SEND_FINAL_CONFIRMATION, event, temp)
        check_gcal(event, False)
        if not clientalreadyconfirmedfinal:
            new_action_save(['[A] Client confirmed final details via email button','dummy'], event)
         
        # email Janie a notice
        subject = "Confirmation of final event details completed via email button for " + event.name
        greeting = "The final event details for the <a href='" + settings.WEBSITE
        greeting += str(event.id) + "/edit'>" + event.name + "</a>"
        greeting += " event (on " + event.date.strftime("%m-%d-%y") + ") "
        greeting += "have been confirmed online & automatically recorded. <br /><br />"
        from_email, to = settings.EMAIL_AUTO, settings.EMAIL_MAIN
        html_content = greeting
        text_content = strip_tags(html_content) 
        connection = mail.get_connection(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT, username=settings.EMAIL_HOST_USER_AUTO,
                                 password=settings.EMAIL_HOST_PASSWORD_AUTO, use_tls=settings.EMAIL_USE_TLS)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=[settings.EMAIL_RECORDS], connection=connection)
        msg.attach_alternative(html_content, "text/html")
        if not clientalreadyconfirmedfinal:
            msg.send()
        #save to IMAP Sent folder!
        message = str(msg.message())
        imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP)
        imap.starttls(ssl_context=ssl.create_default_context())
        imap.login(settings.EMAIL_HOST_IMAP_USER, settings.EMAIL_HOST_IMAP_PASSWORD)
        imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
        imap.logout() 
         
        return render(request, 'events/client_confirm_event.html', {'event':event,
                                                                    'client':client, 'error':error})
    
    else:
        HttpResponse("Link invalid!")
        













def inquiry(request, kind, eventnum, email, firstname):
    event = get_object_or_404(Event, pk=eventnum)
    person = get_object_or_404(Musician, email=email, name__startswith=firstname)
    musev = get_object_or_404(MusicianEvent, event=event, musician=person)
    
    error = False
    error2 = False
    bottest = False
    
    BotNames=['Googlebot', 'ads-google', 'msnbot', 'altavista', 'AhrefsBot', 'Mediapartners-Google', 'slurp', 'BingPreview', 'Slurp','Twiceler','msnbot','KaloogaBot','YodaoBot','"Baiduspider','googlebot','Speedy Spider','DotBot']
    
    useragent = request.META['HTTP_USER_AGENT']
    if not useragent:
        bottest = True
    for botname in BotNames:
        if botname.lower() in useragent.lower():
            bottest = True
    
    if bottest:
        return render(request, 'events/confirmationbot.html', {'bot':bottest}) 
        
    if kind == 'gotit':
        musev.gotit = True
        add_action(person.name + " responded 'got it' to fact sheet", event, date.today())
        
    if kind == 'yes':
        #musician was an unknown, now becoming a yes.  add to list
        #find lowest-ranked phold (make sure there is one), and delete that one entirely
        if musev.no == True:
            error = True
        elif musev.yes == True:
            error2 = True
        elif MusicianEvent.objects.filter(event_id=event, placeholder=True).count() == 0: 
            if musev.yes == True:  #enough musicians already said yes
                error2 = True
            else:
                error = True
        else:
            #get number of placeholders available
            #get ranks of placeholders available in list
            #get size of group
            #get likely instrument for this event
            
            #if Janie, always first available spot (move another violin if nec.)
            #if violin, always first available after any other violins
            #if cello, always last spot - if needed, bump up anyone in last spot currently
            #if viola, always middle spot if size=3, always third spot if size=4
            #  always second if size=2 (unless taken with cello), always middle-ish if size>4
    
            #do similar code around 3600 (def yesaskedmusician)
                       
            temp = MusicianEvent.objects.filter(event_id=event, placeholder=True).order_by('rank')[:1].get()
            rank = temp.rank
            temp.delete()
            #put thismus in its old rank spot, and save
            musev.rank = rank
            musev.yes = True
            add_action(person.name + " responded 'YES' to playing invitation", event, date.today())
            #add PaymentsDue record
            exists = PaymentsDue.objects.filter(event_id = event.id, musician_id = musev.musician.id).exists()
            if not exists:
                newpay = PaymentsDue(done = False)
                newpay.payment = event.musician_fee
                newpay.event_id = event.id
                newpay.musician_id = musev.musician.id
                newpay.duedate = calculate_the_next_week_day(event.date) #first weekday following event date
                if musev.musician.name == "Janie Spangler" or musev.musician.name == "Glenn Loontjens":
                        newpay.done = True
                newpay.save()

            #check if enough musicians said yes, if so update flags!
            ensnumber = event.ensemble_number
            if not ensnumber:
                ensnumber = 0
            playing = MusicianEvent.objects.filter(event_id=event, yes=True, no=False, placeholder=False).order_by('pk')
            if (playing.count() == ensnumber) and ensnumber > 0:
                event.flag_musicians_rcvd = True
                event.event_reminders_done = False
                process_auto_reminders(event)
                process_due_dates(event)
                process_update_flags(event)
                event.event_reminders_done = True
                event.save()
                
            #send a confirmation email to musician
            formhtml = FormHtml.objects.get(name='musician_confirmation_yes')
            full_dict = make_dict(event)
            t = Template(formhtml.subject)
            c = Context(full_dict)
            subject = t.render(c)
            t = Template(formhtml.body)
            c = Context(full_dict)
            bodytext = t.render(c)
            
            
            from_email, to = settings.EMAIL_EVENTS, email
            html_content = bodytext
            text_content = strip_tags(html_content) 
            connection = mail.get_connection(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT, username=settings.EMAIL_HOST_USER_EVENTS,
                                 password=settings.EMAIL_HOST_PASSWORD_EVENTS, use_tls=settings.EMAIL_USE_TLS)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=[settings.EMAIL_RECORDS], connection=connection)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            #save to IMAP Sent folder!
            message = str(msg.message())
            imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP_EVENTS)
            imap.starttls(ssl_context=ssl.create_default_context())
            imap.login(settings.EMAIL_HOST_IMAP_USER_EVENTS, settings.EMAIL_HOST_IMAP_PASSWORD_EVENTS)
            imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
            imap.logout() 





    if kind == 'no':
        if musev.yes == True:
            error = True
        elif musev.no == True:
            error2 = True
        else:
            musev.no = True
            add_action(person.name + " responded 'NO' to playing invitation", event, date.today())
            #delete PaymentsDue record
            exists = PaymentsDue.objects.filter(event_id = event.id, musician_id = musev.musician.id).exists()
            if exists:
                newpay = get_object_or_404(PaymentsDue, musician_id = musev.musician.id, event_id = event.id)
                newpay.delete()
                
                
            #old code - no longer sending confirmation on 'no' answers -----  send a confirmation email to musician
            formhtml = FormHtml.objects.get(name='musician_confirmation_no')
            full_dict = make_dict(event)
            t = Template(formhtml.subject)
            c = Context(full_dict)
            subject = t.render(c)
            t = Template(formhtml.body)
            c = Context(full_dict)
            bodytext = t.render(c)
            
            
            from_email, to = settings.EMAIL_EVENTS, email
            html_content = bodytext
            text_content = strip_tags(html_content) 
#             connection = mail.get_connection(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT, username=settings.EMAIL_HOST_USER_EVENTS,
#                                  password=settings.EMAIL_HOST_PASSWORD_EVENTS, use_tls=settings.EMAIL_USE_TLS)
#             msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=[settings.EMAIL_RECORDS], connection=connection)
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()
#             #save to IMAP Sent folder!
#             message = str(msg.message())
#             imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP_EVENTS)
#             imap.starttls(ssl_context=ssl.create_default_context())
#             imap.login(settings.EMAIL_HOST_IMAP_USER_EVENTS, settings.EMAIL_HOST_IMAP_PASSWORD_EVENTS)
#             imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
#             imap.logout() 

        
    musev.save()
    
    numgotit = MusicianEvent.objects.filter(event=event, gotit=True).count()
    if numgotit == event.ensemble_number:
        #all musicians responded to fact sheet!
        event.flag_fact_sheets_rcvd = True
        event.event_reminders_done = False
        process_auto_reminders(event)
        process_due_dates(event)
        process_update_flags(event)
        event.event_reminders_done = True
        event.save()
    
    if not event.start_time:
        arrival_time = None
    else:
        arrival_time = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=15)).time()
        if event.location:
            if "Ritz" in event.location.name:
                arrival_time = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=30)).time()
        else:
            if "Ritz" in event.location_name:
                arrival_time = (datetime.datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=30)).time()
    if event.location:
        location = get_object_or_404(Venue, name=event.location)
        location_name = location.name
        location_link = location.link
        location_addr = location.address
    else:
        location_name = event.location_name
        location_link = event.location_link
        location_addr = event.location_address
    if event.location_outdoors:
        outdoors = "Outdoors"
    else:
        outdoors = "Indoors"
    if event.event_type:
        eventtype = event.event_type.name
    else:
        eventtype = event.event_type_name

    title = "VS Event"
    if kind == 'gotit':
        title = "VS Event - final"
#     if not arrival_time:
#         details1 = "<b>Set time: " + "TBD" + "</b><br />" + \
#                 eventtype + " for " + event.name + "<br /><br />" + location_name + " - " + \
#                 location_addr + " - " + \
#                 event.location_details + " (" + outdoors + ")<br />" + location_link + \
#                 " <br /><br />Dress Code: " + event.dress_code
#     else:
#         details1 = "<b>Arrival time: " + arrival_time.strftime('%I:%M%p').lstrip("0") + "</b><br />" + \
#                 eventtype + " for " + event.name + "<br /><br />" + location_name + " - " + \
#                 location_addr + " - " + \
#                 event.location_details + " (" + outdoors + ")<br />" + location_link + \
#                 " <br /><br />Dress Code: " + event.dress_code
#   details1 = format_html(details1)
#     details = details1.replace('&', '%26')
    if not arrival_time:
        details1 = "[strong]Set time: " + "TBD" + "[/strong][br]" + \
                eventtype + " for " + event.name + "[br][br][strong]" + location_name + "[/strong] - " + \
                location_addr + " - " + \
                event.location_details + " (" + outdoors + ")[br]" + location_link + \
                " [br][br][strong]Dress Code: [/strong]" + event.dress_code
    else:
        details1 = "[strong]Arrival time: " + arrival_time.strftime('%I:%M%p').lstrip("0") + "[/strong][br]" + \
                eventtype + " for " + event.name + "[br][br][strong]" + location_name + "[/strong] - " + \
                location_addr + " - " + \
                event.location_details + " (" + outdoors + ")[br]" + location_link + \
                " [br][br][strong]Dress Code: [/strong]" + event.dress_code
    details = details1
    
    location = location_name
    if not event.start_time:
        startoffset = datetime.datetime.strptime('0001','%H%M').time() 
        endoffset = datetime.datetime.strptime('0005','%H%M').time()
    else:
        startoffset = event.start_time
        endoffset = event.end_time 
    start = datetime.datetime.combine(event.date,startoffset)
    end = datetime.datetime.combine(event.date,endoffset) 
    starttime = start.strftime('%Y%m%dT%H%M%S')
    endtime = end.strftime('%Y%m%dT%H%M%S')
    startdate = start.strftime('%Y-%m-%d')
    enddate = end.strftime('%Y-%m-%d')
    starttimeonly = start.strftime('%H:%M')
    endtimeonly = end.strftime('%H:%M')
    temp = end - start
    temp = temp.seconds
    #print(temp)
    hours = temp // 3600
    temp = temp - (hours * 3600)
    minutes = temp // 60
    duration = '{:02}{:02}'.format(int(hours), int(minutes))
    
    return render(request, 'events/confirmation.html', {'event':event, 'person':person, 'firstname':firstname,
                                                        'musev':musev, 'kind':kind, 'error':error, 'error2':error2,
                                                        'title':title, 'location':location,
                                                        'starttime':starttime, 'endtime':endtime,
                                                        'details':details, 'duration':duration,
                                                        'startdate':startdate, 'enddate':enddate,
                                                        'starttimeonly':starttimeonly, 'endtimeonly':endtimeonly}) 


def payments_received_older(request):
    today = date.today()
    past183days = today + relativedelta(days=-183)

    payments = PaymentsReceived.objects.filter(date__range=[past183days, today]).order_by('-date').exclude(event__event_archived=True)
    
    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])

    return render(request, 'events/payments_received_older.html', {'payments': payments,
                                               'soonevents': soonevents, 'soonreminder': soonreminder, 
                                               'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                                               'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                                               'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents})


def payments_received(request):
    today = date.today()
    past31days = today + relativedelta(days=-31)

    payments = PaymentsReceived.objects.filter(date__range=[past31days, today]).order_by('-date').exclude(event__event_archived=True)
    
    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])

    return render(request, 'events/payments_received.html', {'payments': payments,
                                               'soonevents': soonevents, 'soonreminder': soonreminder, 
                                               'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                                               'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                                               'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents})


def payments_due_older(request):
    today = date.today()
    yesterday = today + relativedelta(days=-1)
    fourteendays = today + relativedelta(days=14)
    past365days = today + relativedelta(days=-365)
    
    payments = PaymentsDue.objects.filter(donedate__range=[past365days, today]).order_by('donedate').exclude(done=False).exclude(event__event_archived=True)
    
    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])

    return render(request, 'events/payments_due_older.html', {'payments': payments,
                                               'soonevents': soonevents, 'soonreminder': soonreminder, 
                                               'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                                               'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                                               'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents})


    
def payments_due(request):
    today = date.today()
    yesterday = today + relativedelta(days=-1)
    fourteendays = today + relativedelta(days=14)
    fourweeks = today + relativedelta(days=28)
    past365days = today + relativedelta(days=-365)
    pastfourteendays = today + relativedelta(days=-14)
    
    payments = PaymentsDue.objects.filter(duedate__range=[today, fourweeks]).order_by('duedate').exclude(event__event_archived=True).exclude(done=True)
    payments_pd = PaymentsDue.objects.filter(duedate__range=[past365days, yesterday]).order_by('duedate').exclude(event__event_archived=True).exclude(done=True)
    #payments_pd = PaymentsDue.objects.filter(is_past_due=True).order_by('-duedate')
    payments_done = PaymentsDue.objects.filter(donedate__range=[pastfourteendays, today]).order_by('donedate').exclude(event__event_archived=True).exclude(done=False)
    
    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents,  pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])

    return render(request, 'events/payments_due.html', {'payments': payments, 'payments_done': payments_done,
                                                        'payments_pd': payments_pd,
                                               'soonevents': soonevents, 'soonreminder': soonreminder, 
                                               'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                                               'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                                               'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents})
    
    
    

def get_rate_chart(request):
    if request.is_ajax():
        rate_name = request.GET['rate_name']
        minhours = request.GET['minhours']
        minensnum = request.GET['minensnum']
        maxhours = request.GET['maxhours']
        maxensnum = request.GET['maxensnum']
        mode = request.GET['mode']
        html = ""
        #if ensnum = 0 then get all ensemble sizes for this hour
        #if hours = 0 then get all hours for this ensemble size
        #if both are 0, then get full chart for this rate_name
#         if ensnum == '0' and hours == '0':
#             kind = 'all'
#             number = 0
#         elif ensnum == '0':
#             kind = 'hour'
#             number = hours
#         elif hours == '0':
#             kind = 'ensemble'
#             number = ensnum
#         else:
#             kind = 'none'
#             number = 0
            
#         print(mode)
        
        theserates = get_object_or_404(RateChart, name = rate_name)
        #theserates = RateChart.objects.filter(name = rate_name)
        html = render_to_string('events/render_ratechart.html', 
                                 {'rate':theserates, 'minhours':minhours, 'maxhours':maxhours,
                                  'minensnum':minensnum, 'maxensnum':maxensnum, 'mode':mode})
        plain = render_to_string('events/render_ratechart_plain.html',
                                 {'rate':theserates, 'minhours':minhours, 'maxhours':maxhours,
                                  'minensnum':minensnum, 'maxensnum':maxensnum, 'mode':mode})
#         plain = "please paste as html, not plain text"
        
        plain = strip_tags(plain)
        
        data = {'html':html, 'plain':plain}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
    
    
    
def rates(request):
    chart = RateChart.objects.order_by('importance')
    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])

    return render(request, 'events/rates.html', {'rates': chart,
                                               'soonevents': soonevents, 'soonreminder': soonreminder, 
                                               'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                                               'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                                               'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents})
    
        

def email_pdf(request, eventnum = None, formname = None):
    #only used for contract_print, invoice, manual receipt_finalpay, receipt_deposit at this point
    event = get_object_or_404(Event, pk=eventnum);
    if request.method == "POST":
        form = FormEmailForm(request.POST)
        if form.is_valid():
            newemail = form.save(commit=False)
            newemail.sentdate = timezone.now()
            newemail.event = event
            newemail.save()
            
            #save file locally first
#TODO:  change temp file to save to some other directory, and delete it after!!!!!

            if formname == 'contract_print':
                tformname = 'Contract'
            elif formname == "receipt_deposit":
                tformname = 'Deposit-payment-receipt'
            elif formname == "receipt_finalpay":
                tformname = "Final-payment-receipt"
            elif formname == "receipt_extrapay":
                tformname = "Extra-payment-receipt"
            else:
                tformname = formname
            # if it's a receipt for actual fullpay (not just final) then give correct file name
            #    check deposit amount to determine this; no need to check client variable (since this routine is
            #    only used for rcpt if event is not automated)
            if formname == "receipt_finalpay" and (event.deposit_fee == 0 or event.deposit_fee == 0.00):
                tformname = "Full-payment-receipt"
            #print(tformname)
            file_name = tformname + "-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf"
            result = BytesIO()
            file = open(file_name, "wb")
            pdf = pisa.pisaDocument(BytesIO(newemail.pdf.encode("UTF-8")), file)
            file.close()
            file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "", file_name)

            if formname == "receipt_finalpay" or formname == "receipt_deposit" or formname == "receipt_extrapay":
                #add new PaymentsReceived!
                if tformname == "Full-payment-receipt":
                    prtype = "full"
                elif tformname == "Deposit-payment-receipt":
                    prtype = "deposit"
                elif tformname == "Final-payment-receipt":
                    prtype = "final"
                else:  #tformname == "Extra-payment-receipt"
                    prtype = "extra"
                
                exists = PaymentsReceived.objects.filter(event_id=event.id, type=prtype).exists()
                if exists:
                    newpay = get_object_or_404(PaymentsReceived, event_id=event.id, type=prtype)
                    newpay.delete()
                newpay = PaymentsReceived()
                newpay.date = date.today()
                newpay.event_id = event.id
                newpay.method = "check"
                if tformname == "Full-payment-receipt":
                    newpay.payment = event.fee
                    newpay.amount_due = event.fee
                    newpay.type = "full"
                elif tformname == "Deposit-payment-receipt":
                    newpay.payment = event.deposit_fee
                    newpay.amount_due = event.deposit_fee
                    newpay.type = "deposit"
                elif tformname == "Final-payment-receipt":
                    newpay.payment = event.final_fee
                    newpay.amount_due = event.final_fee
                    newpay.type = "final"
                else:  #tformname == "Extra-payment-receipt"
                    newpay.payment = event.extra_fee
                    newpay.amount_due = event.extra_fee
                    newpay.type = "extra"
                newpay.save()

            
            #attach, and send email   
            subject, from_email, to = newemail.subject, settings.EMAIL_MAIN, newemail.addr

            html_content = newemail.body
            text_content = strip_tags(html_content) 
            msg = EmailMultiAlternatives(subject, text_content, from_email, to.split(','), bcc=[settings.EMAIL_RECORDS])
            msg.attach_alternative(html_content, "text/html")
            ################################  NEW:  don't attach file to their email for receipts
            ############ Client will still be able to see pdf receipts from their client portal (for now)
            if formname == "receipt_finalpay" or formname == "receipt_deposit" or formname == "receipt_extrapay":
                nothing = 1
            else:
                attachment = open(file_path, 'rb')
                msg.attach(file_path, attachment.read() , 'text/csv')
            msg.send()
            #save to IMAP Sent folder!
            message = str(msg.message())
            imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP)
            imap.starttls(ssl_context=ssl.create_default_context())
            imap.login(settings.EMAIL_HOST_IMAP_USER, settings.EMAIL_HOST_IMAP_PASSWORD)
            imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
            imap.logout() 
            
            #send it via ftp to webspace
# TODO:  maybe delete it after a couple months??
            if not os.environ.get("FTP_LOGIN"):
                session = ftplib.FTP_TLS(settings.FTP_ADDR, settings.FTP_LOGIN, settings.FTP_PWD)
            else:
                session = ftplib.FTP_TLS(settings.FTP_ADDR, os.environ.get("FTP_LOGIN"), os.environ.get("FTP_PWD"))
            fileftp = open(file_path, 'rb')
            session.cwd('requests')
            session.cwd('pdfs')
            session.storbinary('STOR ' + file_name, fileftp)
            fileftp.close()
            session.quit()
            
            #delete the temporary local pdf now
            #os.remove(file_path)
            
            #close the window, done!
            form = AddForm(instance=event)
            return HttpResponse('<script>opener.closePopup3(window);</script>')
                    
    else:
        if request.GET:
            form = FormEmailForm(initial=request.GET)
        else:
            
            #NEW:  increment invoice number before loading form email (if it's an invoice)
            # when the form email gets filled, invoice will grab the new number (just below)
            if 'invoice' in formname:
                glob = Global.objects.get(pk=1)
                invoice_number_old = glob.invoice_number
                invoice_number = invoice_number_old + 1
                glob.invoice_number = invoice_number
                glob.save()
            #ENDNEW
            
            formhtml = FormHtml.objects.get(name=formname)
            full_dict = make_dict(event)
            t = Template(formhtml.subject)
            c = Context(full_dict)
            subject = t.render(c)
            if event.contact:
                contact = get_object_or_404(Contact, name=event.contact)
                email = contact.email
            else:
                email = event.contact_email
                
            #invoices always go to planner, not main contact!
            if 'invoice' in formname:
                if event.dayofcontact:
                    planner = get_object_or_404(DayofContact, name=event.dayofcontact)
                    email = planner.email
                else:
                    email = event.dayofcontact_email
                    
            t = Template(formhtml.body)
            c = Context(full_dict)
            bodytext = t.render(c)
            t = Template(formhtml.pdf)
            c = Context(full_dict)
            pdf = t.render(c)
            
            #######################################################################################################
            #NEW CODE TO AVOID ACTUALLY SENDING PDFS IN EMAIL for clients (for receipts)
            if formname == "receipt_finalpay" or formname == "receipt_deposit" or formname == "receipt_extrapay":
                no_pdf = True
            else:
                no_pdf = False
            #######################################################################################################


            
            more = 0
            esigs = ESig.objects.order_by('-default', '-default_alt', '-date')
            form = FormEmailForm(initial={'subject': subject, 'addr': email, 'body': bodytext, 'pdf': pdf})
        return render(request, 'events/email_pdf.html', {'form': form, 'esigs': esigs, 'bodytext': bodytext, 
                                                         'more': more, 'eventnum': eventnum, 'no_pdf': no_pdf,
                                                         'formname': formname})
    


def email(request, eventnum = None, formname = None):
    event = get_object_or_404(Event, pk=eventnum )
    warning = ''
    if request.method == "POST":
        form = FormEmailForm(request.POST)
        if form.is_valid():
            newemail = form.save(commit=False)
            newemail.sentdate = timezone.now()
            newemail.event = event
            newemail.save()
        
            subject, from_email, to = newemail.subject, settings.EMAIL_MAIN, newemail.addr

            #avoid problem with Dave & Lani by parsing out names from (*DO NOT EDIT *) line too,
            #and use those below for 'firstname' code too

            #if factsheet or musicians, send multi emails if multiple recipients
            if (formname == 'factsheet') or (formname == 'musicians') or (formname == 'musicians_email'):
                from_email = settings.EMAIL_EVENTS
                addresslist = newemail.addr
                addresslist = addresslist.replace('(*DO NOT EDIT*)', '')
                addresses = [x.strip() for x in addresslist.split(',')]
                
#                 if (formname == 'musicians_email'):
#                     new_action_save(['Sent general email to musicians','dummy'], event)
#                 if (formname == 'musicians_email'):
#                     new_action_save(['Sent fact sheets to musicians','dummy'], event)

                
                origbody = newemail.body
                musicianlist = ""
                for address in addresses:
                    addressonly = address.split(':')[1]
                    nameonly = address.split(':')[0]
                    #make musician list for fact sheets
                    musician = get_object_or_404(Musician, email=addressonly, name=nameonly)
                    musthisevent = get_object_or_404(MusicianEvent, event=event, musician=musician)
                    musicianlist += musician.name + ' (' + musthisevent.instrument + '), '
                    musicianlist += addressonly + ', ' + str(musician.phone) + '<br />'
                #remove last <br />
                musicianlist = musicianlist[:-6]
                for address in addresses:
                    addressonly = address.split(':')[1]
                    nameonly = address.split(':')[0]
                    #replace special button codes to identify correct person via email/urlencode
                    to = addressonly
                    newbody = origbody.replace('(*email_address*)', urllib.parse.quote(to))
                    newerbody = newbody.replace('(*musician_list*)', musicianlist)
                    #replace greetings (names)? how to get first names only?
                    musician = get_object_or_404(Musician, email=addressonly, name=nameonly)
                    musthisevent = get_object_or_404(MusicianEvent, event=event, musician=musician)
                    firstname = musician.name.split(' ')[0]
                    newestbody = newerbody.replace('(*musician_first_name*)', firstname)
                    #finalbody = newestbody.replace('(*musician_instrument*)', musthisevent.instrument)
                    if musthisevent.specialfee:
                        finalbody = newestbody.replace('(*musician_fee*)', str(musthisevent.specialfee))
                    else:
                        finalbody = newestbody.replace('(*musician_fee*)', str(event.musician_fee))
                    
                    html_content = finalbody
                    text_content = strip_tags(html_content)
                    connection = mail.get_connection(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT, username=settings.EMAIL_HOST_USER_EVENTS,
                                 password=settings.EMAIL_HOST_PASSWORD_EVENTS, use_tls=settings.EMAIL_USE_TLS)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=[settings.EMAIL_RECORDS], connection=connection)
                    msg.attach_alternative(html_content, "text/html")
                    #msg.attach_file(os.path.join(settings.STATIC_ROOT, 'images/button_gotit.png'))
                    msg.send()
                    #save to IMAP Sent folder!
                    message = str(msg.message())
                    imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP_EVENTS)
                    imap.starttls(ssl_context=ssl.create_default_context())
                    imap.login(settings.EMAIL_HOST_IMAP_USER_EVENTS, settings.EMAIL_HOST_IMAP_PASSWORD_EVENTS)
                    imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
                    imap.logout() 
                    if (formname == 'musicians'):
                        new_action_save([musician.name + ' was asked to play','dummy'], event)
                        musthisevent.asked = True
                        musthisevent.save()
            
            else:
                
                #NEW: July '23:  if sending copy of contract to planner, then get and attach the pdf.
                if (formname == 'email_planner_contract'):
                    #retrieve contract from ftp server
                    if not os.environ.get("FTP_LOGIN"):
                        session = ftplib.FTP_TLS(settings.FTP_ADDR, settings.FTP_LOGIN, settings.FTP_PWD)
                    else:
                        session = ftplib.FTP_TLS(settings.FTP_ADDR, os.environ.get("FTP_LOGIN"), os.environ.get("FTP_PWD"))
                    file_name = "Contract-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf"
                    file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "", file_name)
                    session.cwd('requests')
                    session.cwd('pdfs')
                    with open(file_name, "wb") as filelocal:
                        session.retrbinary(f"RETR {file_name}", filelocal.write)
                    filelocal.close()
                    session.quit()
                    #attach and send
                    html_content = newemail.body
                    text_content = strip_tags(html_content) 
                    msg = EmailMultiAlternatives(subject, text_content, from_email, to.split(','), bcc=[settings.EMAIL_RECORDS])
                    msg.attach_alternative(html_content, "text/html")
                    attachment = open(file_path, 'rb')
                    msg.attach(file_name, attachment.read() , 'text/csv')
                    msg.send()
                #ENDNEW
                
                else:
                    html_content = newemail.body
                    text_content = strip_tags(html_content) 
                    msg = EmailMultiAlternatives(subject, text_content, from_email, to.split(','), bcc=[settings.EMAIL_RECORDS])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                
                
                #save to IMAP Sent folder!
                message = str(msg.message())
                imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP)
                imap.starttls(ssl_context=ssl.create_default_context())
                imap.login(settings.EMAIL_HOST_IMAP_USER, settings.EMAIL_HOST_IMAP_PASSWORD)
                imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
                imap.logout() 
            
            
            #what's the below line for?
            form = AddForm(instance=event)
            return HttpResponse('<script>opener.closePopup3(window);</script>')
    else:
        if request.GET:
            form = FormEmailForm(initial=request.GET)
        else:
            formhtml = FormHtml.objects.get(name=formname)
            full_dict = make_dict(event)
            t = Template(formhtml.subject)
            c = Context(full_dict)
            subject = t.render(c)
            if event.contact:
                contact = get_object_or_404(Contact, name=event.contact)
                email = contact.email
            else:
                email = event.contact_email
            if (formname == 'email_planner') or (formname == 'email_planner_contract') or (formname == 'email_planner_musiclist'):
                if event.dayofcontact:
                    contact = get_object_or_404(DayofContact, name=event.dayofcontact)
                    email = contact.email
                else:
                    email = event.dayofcontact_email
            #if musicians or factsheet, add actual email addresses for each
                #and if factsheet, then the addresses sent to ought to be the yes list, not the (notasked) list
            if (formname == 'musicians') or (formname == 'musicians_email') or (formname == 'factsheet'):
                email = '(*DO NOT EDIT*)'
                if (formname == 'musicians'):
                    toask = MusicianEvent.objects.filter(event=eventnum, asked=False, yes=False, placeholder=False).order_by('pk')
                    emptyspots = MusicianEvent.objects.filter(event=eventnum, placeholder=True).order_by('pk')
                    if toask.count() > emptyspots.count():
                        warning = "You are inviting more musicians than there are spots available to fill!  "
                        warning += "Please make sure you want to actually send this email as is..."
                    elif toask.count() == 0:
                        warning = "You have no musicians to invite -- are you sure you want to send this to no one?"
                    else:
                        warning = ''
                elif (formname == 'musicians_email'):
                    toask = MusicianEvent.objects.filter(event=eventnum, yes=True, no=False, placeholder=False).order_by('pk')
                else:
                    toask = MusicianEvent.objects.filter(event=eventnum, yes=True, no=False, placeholder=False).order_by('pk')
                numemails = toask.count()
                i = 1
                while i <= numemails:
                    email = email + toask[i-1].musician.name + ':' + toask[i-1].musician.email
                    if i < numemails:
                        email += ', '
                    i = i + 1
#                 for toaskone in toask:
#                     if formname == 'musicians':
#                         toaskone.asked = True
#                         toaskone.save()
                         
            #handle 'more' button 
            if formname == 'more':
                more = True
            else:
                more = False
            t = Template(formhtml.body)
            c = Context(full_dict)
            bodytext = t.render(c)
            pdf = 'x'
            
            esigs = ESig.objects.order_by('-default', '-default_alt', '-date')
            form = FormEmailForm(initial={'subject': subject, 'addr': email, 'body': bodytext, 'pdf': pdf})
        return render(request, 'events/email.html', {'form': form, 'bodytext': bodytext, 'warning': warning,
                                                     'more': more, 'eventnum': eventnum, 'esigs': esigs,
                                                     'formname': formname})

def sidebar():
    today = date.today()
    fourteendays = today + relativedelta(days=14)
    sevendays = today + relativedelta(days=7)
    pastsevendays = today + relativedelta(days=-7)
    pastfourteendays = today + relativedelta(days=-14)
    yesterday = today + relativedelta(days=-1)
    past365days = today + relativedelta(days=-365)
    past182days = today + relativedelta(days=-182)
    
    pays = PaymentsDue.objects.filter(duedate__range=[today, sevendays]).order_by('duedate','event__date','event__pk').exclude(event__event_archived=True).exclude(done=True)
    pays_pd = PaymentsDue.objects.filter(duedate__range=[past365days, yesterday]).order_by('duedate').exclude(event__event_archived=True).exclude(done=True)
    #payments_pd = PaymentsDue.objects.filter(is_past_due=True).order_by('-duedate')
    #payments_done = PaymentsDue.objects.order_by('donedate').exclude(event__event_archived=True).exclude(done=False)
    
    soonevents = Event.objects.filter(date__range=[today, fourteendays]).exclude(
        event_archived=True).order_by('date','start_time')
#     soonreminder = Reminder.objects.filter(date__range=[today, sevendays]).exclude(
#         done=True).exclude(disb=True).exclude(event__date__lt=today).exclude(
#         event__event_archived=True).order_by('date')


    booking1 = settings.INVITE_MUSICIANS
    booking2 = settings.ALL_MUSICIANS_BOOKED

    #order?
    soonreminder = Reminder.objects.filter(date__range=[past182days, sevendays]).exclude(
        done=True).exclude(disb=True).exclude(event__date__lt=today).exclude(name=booking2, date__range=[past182days, sevendays]).exclude(
        name=booking1, date__range=[past182days, sevendays]).exclude(    
        event__event_archived=True).order_by('event__pk', 'event__date', 'date')

    
    
    #determine if all soonreminders are auto?
    all_soonrem_auto = True
    for soonrem in soonreminder:
        if not soonrem.auto:
            all_soonrem_auto = False
            
#     pastduereminder = Reminder.objects.exclude(done=True).exclude(disb=True).exclude(
#         event__date__lt=today).exclude(event__event_archived=True).filter(Q(date__lt=today)).order_by('date')
    
    # !!!!!!!!!!!!!!!!!!!!!'pastduereminder' now actually refers to new booking-musicians reminders!'!!!!!!!!!!!!!!!!!
    pastduereminder = Reminder.objects.filter(Q(name=booking2, date__range=[past182days, fourteendays]) | Q(name=booking1, date__range=[past182days, fourteendays])).exclude(
        done=True).exclude(disb=True).exclude(event__date__lt=today).exclude(
        event__event_archived=True).order_by('event__date')
        
    if pastduereminder:
        pastduereminder_exists = True
    else:
        pastduereminder_exists = False
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    recentactivities = Activity.objects.filter(date__range=[pastsevendays, today]).exclude(
        event__event_archived=True).exclude(event__date__lt=today).order_by('event__date', '-date', '-pk')
        
    
    nonautoremcount = soonreminder.exclude(auto=True).count()  # + pastduereminder.exclude(auto=True).count()
    
    newevents = Event.objects.filter(date_entered__range=[pastfourteendays, today]).order_by('-date_entered').exclude(
        event_archived=True).exclude(date__lt=today)
    

    #---------------------parse todo/reminder list together---------------------------------------
    recenttodoslist = []
    recenttodo = []
    todoeventid = ''
    todoeventdate = ''
    todoeventname = ''
    todoname = ''
    tododate = ''
    todoslist = []
    todoone = []
    count = soonreminder.count()
    for i, todo in enumerate(soonreminder):
        todoname = todo.name
        tododate = todo.date
        if tododate < today:
            todolate = True
        else:
            todolate = False
        if todo.auto:
            todoauto = True
        else:
            todoauto = False
        todoone = [tododate, todoname, todolate, todoauto]
        
        if i > 0: #there's at least one todo before
            if soonreminder[i-1].event == todo.event:  #if previous item's event was the same
                todoslist.append(todoone)
            else: #previous item's event was different
                todoeventid = soonreminder[i-1].event.id # get previous item's event details
                todoeventdate = soonreminder[i-1].event.date
                if soonreminder[i-1].event.type == "HD":
                    todoeventname = "[HD] " + soonreminder[i-1].event.name
                else:
                    todoeventname = soonreminder[i-1].event.name
                if soonreminder[i-1].event.date_ispast and todo.event.event_archived:
                    tododatepast = "pastarch"
                elif soonreminder[i-1].event.date_ispast:
                    tododatepast = "past"
                elif soonreminder[i-1].event.event_archived:
                    tododatepast = "arch"
                else:
                    tododatepast = "not"
                #if all todos for this event are auto:
                allauto = True
                for thisone in todoslist:
                    if not thisone[3]:
                        allauto = False
                recenttodo = [tododatepast, todoeventdate, todoeventname, todoeventid, todoslist, allauto] #save those details
                recenttodoslist.append(recenttodo)
                todoslist = [] #start new todoslist with this todoivity
                todoslist.append(todoone)
        else: #this is the first todoivity
            todoslist.append(todoone) #first todoivity in the todoslist
        if (i+1) == count: #this is the last item, save now
            todoeventid = todo.event.id
            todoeventdate = todo.event.date
            if todo.event.type == "HD":
                todoeventname = "[HD] " + todo.event.name
            else:
                todoeventname = todo.event.name
            if todo.event.date_ispast and todo.event.event_archived:
                tododatepast = "pastarch"
            elif todo.event.date_ispast:
                tododatepast = "past"
            elif todo.event.event_archived:
                tododatepast = "arch"
            else:
                tododatepast = "not"
            #if all todos for this event are auto:
            allauto = True
            for thisone in todoslist:
                if not thisone[3]:
                    allauto = False
            recenttodo = [tododatepast, todoeventdate, todoeventname, todoeventid, todoslist, allauto]
            recenttodoslist.append(recenttodo)

    #sort list based on event that has most urgent single reminder
    def sortUrgent(val):
        topdates = val[4]
        return topdates[0]
    recenttodoslistsorted = sorted(recenttodoslist, key=sortUrgent)
    
    
    #payments = PaymentsDue.objects.filter(duedate__range=[today, sevendays]).order_by('duedate').exclude(done=True)
    #payments_pd = PaymentsDue.objects.filter(duedate__range=[past365days, yesterday]).order_by('-duedate').exclude(done=True)

    #recentactslist = [recentact, recentact, ...]
    #recentact = [eventdate, eventname, eventid, actslist]
    #actone = [date, name]
    #actslist = [actone, actone, ...]
    recentactslist = []
    recentact = []
    acteventid = ''
    acteventdate = ''
    acteventname = ''
    actname = ''
    actdate = ''
    actslist = []
    actone = []
    count = recentactivities.count()
    for i, act in enumerate(recentactivities):
        actname = act.name
        actdate = act.date
        actone = [actdate, actname]
        
        if i > 0: #there's at least one activity before
            if recentactivities[i-1].event == act.event:  #if previous item's event was the same
                actslist.append(actone)
            else: #previous item's event was different
                acteventid = recentactivities[i-1].event.id # get previous item's event details
                acteventdate = recentactivities[i-1].event.date
                if recentactivities[i-1].event.type == "HD":
                    acteventname = "[HD] " + recentactivities[i-1].event.name
                else:
                    acteventname = recentactivities[i-1].event.name
                if recentactivities[i-1].event.date_ispast and act.event.event_archived:
                    actdatepast = "pastarch"
                elif recentactivities[i-1].event.date_ispast:
                    actdatepast = "past"
                elif recentactivities[i-1].event.event_archived:
                    actdatepast = "arch"
                else:
                    actdatepast = "not"
                recentact = [actdatepast, acteventdate, acteventname, acteventid, actslist] #save those details
                recentactslist.append(recentact)
                actslist = [] #start new actslist with this activity
                actslist.append(actone)
        else: #this is the first activity
            actslist.append(actone) #first activity in the actslist
        if (i+1) == count: #this is the last item, save now
            acteventid = act.event.id
            acteventdate = act.event.date
            if act.event.type == "HD":
                acteventname = "[HD] " + act.event.name
            else:
                acteventname = act.event.name
            if act.event.date_ispast and act.event.event_archived:
                actdatepast = "pastarch"
            elif act.event.date_ispast:
                actdatepast = "past"
            elif act.event.event_archived:
                actdatepast = "arch"
            else:
                actdatepast = "not"
            recentact = [actdatepast, acteventdate, acteventname, acteventid, actslist]
            recentactslist.append(recentact)
    
    #sort list based on event that has most recent single activity
    def sortUrgent2(val):
        topdates = val[4]
        return topdates[0]
    recentactslistsorted = sorted(recentactslist, key=sortUrgent2, reverse=True)
    
    
    return soonevents, recenttodoslistsorted, pastduereminder, pastduereminder_exists, recentactslistsorted, newevents, pays, pays_pd, all_soonrem_auto, nonautoremcount

def toggle_side_auto(request):
    if request.is_ajax():
        this = Global.objects.get(pk=1)
        this.auto_btn_side = not this.auto_btn_side
        this.save()
        data = {'dummy':False,}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
    
def toggle_auto(request):
    if request.is_ajax():
        this = Global.objects.get(pk=1)
        this.auto_btn = not this.auto_btn
        this.save()
        data = {'dummy':False,}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")

def toggle_home_panels(request):
    if request.is_ajax():
        this = Global.objects.get(pk=1)
        if request.GET['dummy'] == 'todo':
            this.home_todo = not this.home_todo
        if request.GET['dummy'] == 'booking':
            this.home_booking = not this.home_booking
        if request.GET['dummy'] == 'payment':
            this.home_payment = not this.home_payment
        if request.GET['dummy'] == 'history':
            this.home_history = not this.home_history
        this.save()
        data = {'dummy':False,}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


    
def toggle_show_pd(request):
    if request.is_ajax():
        this = Global.objects.get(pk=1)
        this.show_pd_btn = not this.show_pd_btn
        this.save()
        #test?
        data = {'dummy':False,}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


def home(request):
    today = date.today()
    
    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents,  pays, pays_pd, all_soonrem_auto, nonautoremcount = sidebar()


    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])
    home_todo_show = this.home_todo
    home_booking_show = this.home_booking
    home_payment_show = this.home_payment
    home_history_show = this.home_history
        
    for event in soonevents:
        
        #process due dates only when necessary
        if not event.event_reminders_done:
            process_auto_reminders(event)
            process_due_dates(event)
            process_update_flags(event)
            event.event_reminders_done = True
            event.save()
            
        #process_auto_reminders(event) -- would be necessary once full automation occurs
        #    since then some things like contracts completed or musicians answered
        #    or automatic emails sent out could have happened since last looking at event
        
        #only once per day:
        if this.last_updated != today:
            process_auto_reminders(event)
            process_due_dates(event)
            process_update_flags(event)
            event.save()
#             this.last_updated = today
#             this.save()
        
    this.last_updated = today
    this.save()    
    

#     searchform = SearchForm()
    
     
    return render(request, 'events/home-new.html', {'soonevents': soonevents, 'soonreminder': soonreminder, 
                                                    'home_todo_show': home_todo_show, 'home_payment_show': home_payment_show,
                                                    'home_history_show': home_history_show, 'home_booking_show': home_booking_show,
                                                'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal),
                                                'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount,
                                                'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents})

def archived(request):
    browse_mode = Global.objects.get(pk=1).browse_mode
    today = date.today()
    events = Event.objects.filter(event_archived=True).order_by('-date','-start_time')
 
    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])
    for event in events:
        
        #process due dates only when necessary
        if not event.event_reminders_done:
            process_auto_reminders(event)
            process_due_dates(event)
            process_update_flags(event)
            event.event_reminders_done = True
            event.save()
            
        #process_auto_reminders(event) -- would be necessary once full automation occurs
        #    since then some things like contracts completed or musicians answered
        #    or automatic emails sent out could have happened since last looking at event
        
        #only once per day:
        if this.last_updated != today:
            process_auto_reminders(event)
            process_due_dates(event)
            process_update_flags(event)
            event.save()
#             this.last_updated = today
#             this.save()
            
    this.last_updated = today
    this.save() 
       
    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
    
    return render(request, 'events/archived.html', {'events': events, 'browse_mode':browse_mode,
                                                   'soonevents': soonevents, 'soonreminder': soonreminder, 
                                                   'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                                                   'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                                                   'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents                
                                                    })


def process_cron_jobs_now(onlyevent):

#     #if automation already run today *on this event*, then don't run again until tomorrow
#     today = date.today()
#     event = get_object_or_404(Event, pk=onlyevent.id)
#     if this.last_automated == today:
#         return
#     else:
#         this.last_automated = today
#         this.save()

    #pull up each automatic reminder that's not done, not archived event,
    #    not past event, with reminder being in the range of 5dys ago to 5dys future.
    today = date.today()
    fivedayspast = today - relativedelta(days=5)
    fivedaysfuture = today + relativedelta(days=5)

    todos = Reminder.objects.filter(event_id=onlyevent.id,date__range=[fivedayspast, fivedaysfuture]).exclude(
                done=True).exclude(disb=True).exclude(
                event__date__lt=today).exclude(
                auto=False).exclude(
                event__event_archived=True).order_by('date')

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
        
        
        print("Event ID " + str(todo.event_id) + ":")
        print(todo.name)
        print(todo.date)
        print(daysleft)
        
        if (todo.name == settings.SEND_HOLD):
            #easy, send one notice on actual date and nothing else.  Done.
            if daysleft <= 0:
                send_1 = True
                atype = "hold_initial"
                done = True
                action = "Hold notice was sent"
                
                event.flag_hold_sent = True
                event.hold_sentdate = today
                event.event_reminders_done = False
                process_auto_reminders(event)
                process_due_dates(event)
                process_update_flags(event)
                event.event_reminders_done = True
                event.save()
                
            else:
                nothing = True
                
        if (todo.name == settings.HOLD_INDEFINITELY):
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
            
        if (todo.name == settings.HOLD_UNTIL):
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
            
        if (todo.name == settings.SEND_CONTRACT):  #don't need to wait for due date       
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
                
        if (todo.name == settings.RECEIVE_CONTRACT):
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
            
        if (todo.name == settings.RECEIPT_CONTRACT):
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
            
        if (todo.name == settings.SEND_DEPOSIT): #dont need to wait for duedate, but
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
            
        if (todo.name == settings.RECEIVE_DEPOSIT):
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
            
        if (todo.name == settings.RECEIPT_DEPOSIT):
            #if deposit rcvd but not rcpt yet, send_1 now and mark done
            #can be done earlier than due date, that's fine
            #if this is executed, it means event is automated but client paid by
            #    check (if automated & credit card, receipt will be done by client routines)
            #        (or if not automated, existing email routines do the receipt pdf/ftp)
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
            
        if (todo.name == settings.SEND_FINAL_PAYMENT):
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
            
        if (todo.name == settings.RECEIVE_FINAL_PAYMENT):
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
            
        if (todo.name == settings.RECEIPT_FINAL_PAYMENT):
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
            

         
        if (todo.name == settings.SEND_EXTRA_PAYMENT):
            #send_1 now only, mark done
            #if client marked on portal that they're sending a check FOR EXTRA PAY, then
            #    don't actually send extra_payment_initial -- it'll be marked done that way
            #    but Janie will still mark rcvd reminder manually when she gets check
            if Client.objects.filter(event=event.id).exists():
                client = get_object_or_404(Client, event=event.id)
                if client.paid_extra and (not client.paid_extra_online):
                    skip_send = True
            if daysleft <= 0:
                send_1 = True
                atype = "extra_payment_initial"
                done = True
                action = "Extra payment request was sent"
                #assc flag need marking for a send-extrapay reminder done
                event.flag_extra_sent = True
                event.extra_sentdate = today
                event.event_reminders_done = False
                process_auto_reminders(event)
                process_due_dates(event)
                process_update_flags(event)
                event.event_reminders_done = True
                event.save()
                check_gcal(event, False)
            else:
                nothing = True
            
        if (todo.name == settings.RECEIVE_EXTRA_PAYMENT):
            #send_1 4 days before, send_2 1 day before.
            #giveup when 1 day past.  never mark done here.
            #if client marked on portal that they're sending a check, then
            #    don't actually send 
            if Client.objects.filter(event=event.id).exists():
                client = get_object_or_404(Client, event=event.id)
                if client.paid_extra and (not client.paid_extra_online):
                    skip_send = True
            if daysleft == 4 or daysleft == 3: #send_1
                send_1 = True
                atype = "extra_payment_due_soon"
                action = "Extra-payment-due-soon reminder sent"
            elif daysleft == 1 or daysleft == 0: #send_2
                send_2 = True
                atype = "extra_payment_due_now"
                action = "Extra-payment-due-now reminder sent"
            elif daysleft <= -1: #giveup
                giveup = True
                skip_send = False
                atype = "extra_payment_giveup"
                action = "Extra-payment-past-due notice sent to Janie"
            else:
                nothing = True
            
        if (todo.name == settings.RECEIPT_EXTRA_PAYMENT):
            #if extra_payment rcvd but not rcpt yet, send_1 now and mark done
            #can be done earlier than due date, that's fine
            #if this is executed, it means event is automated but client paid by
            #    check (if automated & credit card, receipt will be done by client routines)
            #        (if not automated, existing email routines do the receipt pdf/ftp)
            #    so, in this case, we need to generate the pdf/ftp for client to
            #    review the receipt for their mailed check.  We'll do that down below
            if event.flag_extra_rcvd and not event.flag_extra_rcpt:
                send_1 = True
                atype = "extra_payment_receipt"
                action = "Extra-payment-received receipt sent"
                done = True
                #assc flag need marking for a extra receipt done
                event.flag_extra_rcpt = True
                event.extra_rcptdate = today
                event.event_reminders_done = False
                process_auto_reminders(event)
                process_due_dates(event)
                process_update_flags(event)
                event.event_reminders_done = True
                event.save()
                check_gcal(event, False)
            else:
                nothing = True
            
        
        
        if (todo.name == settings.SEND_MUSIC_LIST):
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
            
        if (todo.name == settings.RECEIVE_MUSIC_LIST):
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
            
        if (todo.name == settings.SEND_FINAL_CONFIRMATION):
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
            
        if (todo.name == settings.RECEIVE_FINAL_CONFIRMATION):
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
             
        if (todo.name == settings.ALL_FACT_SHEETS_CONFIRMED):
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
                notgotits = MusicianEvent.objects.filter(event=event, placeholder=False, yes=True, no=False, gotit=False).order_by('pk')
                for notgotit in notgotits:
                    mlist.append(notgotit.musician.email)
                    nlist.append(notgotit.musician.name)
                if daysleft == 1:  # or daysleft == 0:
                    send_1 = True
                    atype = "fact_sheets_reminder"
                    action = "Musician(s) were reminded to respond to Fact Sheet"
                elif daysleft <= 0: #giveup
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
            t = Template(formhtml.body)
            c = Context(full_dict)
            thisbody = t.render(c)
            if atype == "automation_fact_sheets_giveup":
                thisbody = thisbody + "<br /><br />No response yet from " + nlist2 + "<br /><br />"
            if 'giveup' in atype:
                subject, from_email, to = thissubject, settings.EMAIL_AUTO, settings.EMAIL_MAIN
            else:
                subject, from_email, to = thissubject, settings.EMAIL_MAIN, thisaddr
            html_content = thisbody
            text_content = strip_tags(html_content)
            if atype != "automation_fact_sheets_reminder":
                if 'giveup' in atype:
                    connection = mail.get_connection(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT, username=settings.EMAIL_HOST_USER_AUTO,
                                 password=settings.EMAIL_HOST_PASSWORD_AUTO, use_tls=settings.EMAIL_USE_TLS)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=[settings.EMAIL_RECORDS], connection=connection)
                else:
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=[settings.EMAIL_RECORDS])
            else:
                #mlist.append(settings.EMAIL_RECORDS)
                if 'giveup' in atype:
                    connection = mail.get_connection(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT, username=settings.EMAIL_HOST_USER_AUTO,
                                 password=settings.EMAIL_HOST_PASSWORD_AUTO, use_tls=settings.EMAIL_USE_TLS)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, mlist, bcc=[settings.EMAIL_RECORDS], connection=connection)
                else:
                    msg = EmailMultiAlternatives(subject, text_content, from_email, mlist, bcc=[settings.EMAIL_RECORDS])
            msg.attach_alternative(html_content, "text/html")
            if (atype != "automation_fact_sheets_received") and (not skip_send):
                msg.send()
                #save to IMAP Sent folder!
                message = str(msg.message())
                imap = imaplib.IMAP4(settings.EMAIL_HOST_IMAP)
                imap.starttls(ssl_context=ssl.create_default_context())
                imap.login(settings.EMAIL_HOST_IMAP_USER, settings.EMAIL_HOST_IMAP_PASSWORD)
                imap.append('INBOX/Sent_via_Web', '\\SEEN', imaplib.Time2Internaldate(time.time()), message.encode())  
                imap.logout() 
            #if deposit or finalpay receipt, save/upload pdf too, because if automation has to send receipt it
            #    means that event is automated but client paid via check so Janie marked rcvd manually, now receipt
            #    is being sent automatically for the first time.  
            #!!!!!this means it's the only time you use the automation_final_payment_receipt or automation_deposit_receipt
            #       (which show $ amounts based on checks), because the paypal ones (automation on or off) are done 
            #       in paypal routine(receipt_deposit_auto form etc), the full manual ones
            #       (sent from events page by janie) are done with receipt_deposit form etc.
            if todo.name == settings.RECEIPT_DEPOSIT or todo.name == settings.RECEIPT_FINAL_PAYMENT or todo.name == settings.RECEIPT_EXTRA_PAYMENT:
                t = Template(formhtml.pdf)
                c = Context(full_dict)
                pdf = t.render(c)
                if todo.name == settings.RECEIPT_DEPOSIT:
                    file_name = "Deposit-payment-receipt-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
                elif todo.name == settings.RECEIPT_EXTRA_PAYMENT:
                    file_name = "Extra-payment-receipt-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf"
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
                if not os.environ.get("FTP_LOGIN"):
                    session = ftplib.FTP_TLS(settings.FTP_ADDR, settings.FTP_LOGIN, settings.FTP_PWD)
                else:
                    session = ftplib.FTP_TLS(settings.FTP_ADDR, os.environ.get("FTP_LOGIN"), os.environ.get("FTP_PWD"))
                fileftp = open(file_path, 'rb')
                session.cwd('requests')
                session.cwd('pdfs')
                session.storbinary('STOR ' + file_name, fileftp)
                fileftp.close()
                session.quit()
                
                #add new PaymentsReceived!
                if file_name[:3] == "Ful":
                    prtype = "full"
                elif file_name[:3] == "Dep":
                    prtype = "deposit"
                elif file_name[:3] == "Ext":
                    prtype = "extra"
                else:  #file_name[:3] == "Fin"
                    prtype = "final"
                
                exists = PaymentsReceived.objects.filter(event_id=event.id, type=prtype).exists()
                if exists:
                    newpay = get_object_or_404(PaymentsReceived, event_id=event.id, type=prtype)
                    newpay.delete()
                newpay = PaymentsReceived(type = prtype)
                newpay.date = date.today()
                newpay.event_id = event.id
                newpay.method = "check"
                if file_name[:3] == "Ful":
                    newpay.payment = event.fee
                    newpay.amount_due = event.fee
                elif file_name[:3] == "Dep":
                    newpay.payment = event.deposit_fee
                    newpay.amount_due = event.deposit_fee
                elif file_name[:3] == "Ext":
                    newpay.payment = event.extra_fee
                    newpay.amount_due = event.extra_fee
                else:  #file_name[:3] == "Fin"
                    newpay.payment = event.final_fee
                    newpay.amount_due = event.final_fee
                newpay.save()
                
            
               
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

def flipheader(request):
    if request.is_ajax():
        event_id = request.GET['event_id']
        type = request.GET['type']
        #print(type)
        #reminders = Reminder.objects.filter(event_id = event_id)
        
        if type == "todos":
            if Header.objects.filter(event_id=event_id).exists():
                thisheader = get_object_or_404(Header, event_id=event_id)
                thisheader.todos = not thisheader.todos    
                thisheader.save()
            else:
                newheader = Header(event_id = event_id)
                newheader.todos = True
                newheader.save()
        if type == "notes":
            if Header.objects.filter(event_id=event_id).exists():
                thisheader = get_object_or_404(Header, event_id=event_id)
                thisheader.notes = not thisheader.notes    
                thisheader.save()
            else:
                newheader = Header(event_id = event_id)
                newheader.notes = True
                newheader.save()
        if type == "records":
            if Header.objects.filter(event_id=event_id).exists():
                thisheader = get_object_or_404(Header, event_id=event_id)
                thisheader.records = not thisheader.records    
                thisheader.save()
            else:
                newheader = Header(event_id = event_id)
                newheader.records = True
                newheader.save()
        if type == "history":
            if Header.objects.filter(event_id=event_id).exists():
                thisheader = get_object_or_404(Header, event_id=event_id)
                thisheader.history = not thisheader.history    
                thisheader.save()
            else:
                newheader = Header(event_id = event_id)
                newheader.history = True
                newheader.save()
        
        data = {'dummy':False,}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
    

def add(request):
        
    if request.method == "POST":
        form = AddForm(request.POST)
#         form['event_type_name'].value = form['event_type'].value()
        if form.is_valid():
            newevent = form.save(commit=True)
            #save new action (recent activity)
            new_action_save(['Created this event','dummy'], newevent)
            #save date entered    
            newevent.date_entered = date.today()
            #check if popup early, so new flag can be set and saved/updated
            popup = calc_popup(request.POST, newevent)
            if popup == "none":
                nothing = 1
            else:
                #set_flags(popup, newevent)
                #newevent.event_reminders_done = False
                nothing = 1
                
            # if any reminders tied to dummy event #2, then re-tie them to this new event instead :)
            if Reminder.objects.filter(event_id=2).exists():
                newreminders = Reminder.objects.filter(event_id=2)
                for reminder in newreminders:
                    thisreminder = get_object_or_404(Reminder, pk=reminder.id)
                    thisreminder.event_id = newevent.pk    
                    thisreminder.save()
            # if any activites tied to dummy event #2, then re-tie them to this new event instead :)
            if Activity.objects.filter(event_id=2).exists():
                newactivities = Activity.objects.filter(event_id=2)
                for activity in newactivities:
                    thisactivity = get_object_or_404(Activity, pk=activity.id)
                    thisactivity.event_id = newevent.pk    
                    thisactivity.save()
            # if any musicians tied to dummy event #2, then re-tie them to this new event instead :)
            if MusicianEvent.objects.filter(event_id=2).exists():
                newmusicians = MusicianEvent.objects.filter(event_id=2)
                for musician in newmusicians:
                    thismusician = get_object_or_404(MusicianEvent, pk=musician.id)
                    thismusician.event_id = newevent.pk    
                    thismusician.save()
            # if any paymentsdue tied to dummy event #2, then re-tie them to this new event instead :)
            if PaymentsDue.objects.filter(event_id=2).exists():
                newpayments = PaymentsDue.objects.filter(event_id=2)
                for payment in newpayments:
                    thispayment = get_object_or_404(PaymentsDue, pk=payment.id)
                    thispayment.event_id = newevent.pk    
                    thispayment.save()
            # if any header tied.....
            if Header.objects.filter(event_id=2).exists():
                newheaders = Header.objects.filter(event_id=2)
                for header in newheaders:
                    thisheader = get_object_or_404(Header, pk=header.id)
                    thisheader.event_id = newevent.pk
                    thisheader.save()
            # if any formautomatedemail tied.....
            if FormAutomatedEmail.objects.filter(event_id=2).exists():
                newautoemails = FormAutomatedEmail.objects.filter(event_id=2)
                for autoemail in newautoemails:
                    thisautoemail = get_object_or_404(FormAutomatedEmail, pk=autoemail.id)
                    thisautoemail.event_id = newevent.pk
                    thisautoemail.save()
            # if any formemail tied.....
            if FormEmail.objects.filter(event_id=2).exists():
                newemails = FormEmail.objects.filter(event_id=2)
                for email in newemails:
                    thisemail = get_object_or_404(FormEmail, pk=email.id)
                    thisemail.event_id = newevent.pk
                    thisemail.save()
            # if a client tied.....
            if Client.objects.filter(event_id=2).exists():
                thisclient = get_object_or_404(Client, event_id=2)
                thisclient.event_id = newevent.pk
                thisclient.save()

            
            
            #make sure routines below process fully
            newevent.event_reminders_done = False
            #fill in any behind-the-scenes database fields
            process_new_entries(form, newevent)
            #figure out auto-reminders
            process_auto_reminders(newevent)
            #calc all due/sent/rcvd dates, and save in db
            process_due_dates(newevent)
            #update flags
            process_update_flags(newevent)
            #record that reminders were done
            newevent.event_reminders_done = True
            
            #done, save!  
            newevent.save()
            check_gcal(newevent, False)

            #if friendly_name exists, and contact is a saved contact, then
            #  add this friendly_name to contact db, even if it's already there (updates it then, in case changed)
            if newevent.contact and newevent.friendly_name: #this means its a saved contact being used, and friendly_name was entered
                thiscontact = get_object_or_404(Contact, pk=newevent.contact.id)
                thiscontact.friendlyname = newevent.friendly_name
                thiscontact.save()
            
                    

 
 
            #daily automation run it once now
            #if (not '/events/archive/' in popup) and thisevent.automation:
            if (not '/events/archive/' in popup):
                process_cron_jobs_now(newevent)

                
            #redirect according to workflow (send contract? invite musicians? etc...)
#             form = AddForm(instance=newevent)
#             rates = RateChart.objects.order_by('importance')
#             reminders = Reminder.objects.filter(event_id=newevent.pk).order_by('done', 'date')
#             activities = Activity.objects.filter(event_id=newevent.pk).order_by('-date', '-id')
#             musicianlist = MusicianEvent.objects.filter(event_id=newevent.pk).exclude(
#                             placeholder=True).order_by('-pk')
#             musicianlistyes = MusicianEvent.objects.filter(event_id=newevent.pk, yes=True, no=False).order_by(
#                 'rank')
#             musicians = Musician.objects.exclude(name="----------").order_by('instrument')
#             musiciansasked = MusicianEvent.objects.filter(event_id=newevent.pk).exclude(
#                                                 placeholder=True).order_by('-pk')
            
#             if popup == 'none': #go back to home page
#                 return redirect('/events/')    
#             if '/events/archive/' in popup:
#                 return redirect(popup)  
            #go to same add(edit) page for same event and pass popup value
#             soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
#             this = Global.objects.get(pk=1)
#             smallcal = sidecal(this.sidecal_year, this.sidecal_month)
#             sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5])
            

            return redirect('/events/' + str(newevent.pk) + '/edit/' + popup)
#             
#             
#             return render(request, 'events/add.html', {'form': form, 'rates': rates, 'reminders': reminders, 
#                                                        'popup': popup, 'browse_mode': 'EVENT', 
#                                                        'activities': activities, 'musicians':musicians, 
#                                                        'musicianlist':musicianlist, 'musicianlistyes':musicianlistyes,  
#                                                        'musiciansasked':musiciansasked,
#                                                        'soonevents': soonevents, 'soonreminder': soonreminder, 
#                                                        'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
#                                                        'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
#                                                        'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents})                
        else:
            print(form.errors)
            return HttpResponseRedirect('/error/')       
    
    else:
        if request.GET:
            form = AddForm(initial=request.GET)
        else:
            form = AddForm()
    
    #clear out any junk remaining by accident!        
    if Reminder.objects.filter(event_id=2).exists():
        newreminders = Reminder.objects.filter(event_id=2)
        for reminder in newreminders:
            thisreminder = get_object_or_404(Reminder, pk=reminder.id)
            thisreminder.delete()
    # if any activites tied to dummy event #2, then re-tie them to this new event instead :)
    if Activity.objects.filter(event_id=2).exists():
        newactivities = Activity.objects.filter(event_id=2)
        for activity in newactivities:
            thisactivity = get_object_or_404(Activity, pk=activity.id)
            thisactivity.delete()
    # if any musicians tied to dummy event #2, then re-tie them to this new event instead :)
    if MusicianEvent.objects.filter(event_id=2).exists():
        newmusicians = MusicianEvent.objects.filter(event_id=2)
        for musician in newmusicians:
            thismusician = get_object_or_404(MusicianEvent, pk=musician.id)
            thismusician.delete()
    # if any paymentsdue tied to dummy event #2, then re-tie them to this new event instead :)
    if PaymentsDue.objects.filter(event_id=2).exists():
        newpayments = PaymentsDue.objects.filter(event_id=2)
        for payment in newpayments:
            thispayment = get_object_or_404(PaymentsDue, pk=payment.id)
            thispayment.delete()
    # if any paymentsrcvd tied to dummy event #2, then re-tie them to this new event instead :)
    if PaymentsReceived.objects.filter(event_id=2).exists():
        newpayments = PaymentsReceived.objects.filter(event_id=2)
        for payment in newpayments:
            thispayment = get_object_or_404(PaymentsReceived, pk=payment.id)
            thispayment.delete()
    # if any header tied.....
    if Header.objects.filter(event_id=2).exists():
        newheaders = Header.objects.filter(event_id=2)
        for header in newheaders:
            thisheader = get_object_or_404(Header, pk=header.id)
            thisheader.delete()
    # if any formautomatedemail tied.....
    if FormAutomatedEmail.objects.filter(event_id=2).exists():
        newautoemails = FormAutomatedEmail.objects.filter(event_id=2)
        for autoemail in newautoemails:
            thisautoemail = get_object_or_404(FormAutomatedEmail, pk=autoemail.id)
            thisautoemail.delete()
    # if any formautomatedemail tied.....
    if FormEmail.objects.filter(event_id=2).exists():
        newemails = FormEmail.objects.filter(event_id=2)
        for email in newemails:
            thisemail = get_object_or_404(FormEmail, pk=email.id)
            thisemail.delete()

    
    rates = RateChart.objects.order_by('importance')
    #do we need to load existing reminders or activites or musicianlist or browsemode on new blank event?  I think not...
    musicians = Musician.objects.exclude(name="----------").order_by('instrument')
    
    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])

    
    return render(request, 'events/edit-new.html', {'form': form, 'rates': rates, 'popup': 'none', 'reminderscount': '0',
                                               'musicians': musicians,
                                               'soonevents': soonevents, 'soonreminder': soonreminder, 
                                               'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                                               'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                                               'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents})

def after_email(request):
    if request.is_ajax():
        event_id = request.GET['event_id']
        type = request.GET['type']
        print(type)
        #reminders = Reminder.objects.filter(event_id = event_id)

        
        
        data = {'dummy':False,}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
    

def set_flags(popup, thisevent):
    #this routine is currently unused (i think... as of 7/1/21)
    #if these flags are already set true, then mark as already done
    # (later used by undo_setflag_etc to determine whether to undo it or not
    if '/contract/' in popup or settings.SEND_CONTRACT in popup:
        thisevent.flag_contract_sent = True
    if '/contract_print/' in popup or settings.SEND_CONTRACT in popup:
        thisevent.flag_contract_sent = True
    if '/deposit/' in popup or settings.SEND_DEPOSIT in popup:
        thisevent.flag_deposit_sent = True
    if '/depositcontract/' in popup:
        thisevent.flag_deposit_sent = True
        thisevent.flag_contract_sent = True
    if '/finalpay/' in popup or settings.SEND_FINAL_PAYMENT in popup:
        thisevent.flag_final_payment_sent = True
    if '/extrapay/' in popup or settings.SEND_EXTRA_PAYMENT in popup:
        thisevent.flag_extra_sent = True
    if '/receipt_extrapay/' in popup or settings.RECEIPT_EXTRA_PAYMENT in popup:
        thisevent.flag_extra_rcpt = True
    if '/receipt_finalpay/' in popup or settings.RECEIPT_FINAL_PAYMENT in popup:
        thisevent.flag_final_payment_rcpt = True
    if '/receipt_deposit/' in popup or settings.RECEIPT_DEPOSIT in popup:
        thisevent.flag_deposit_rcpt = True
    if '/receipt_contract/' in popup or settings.RECEIPT_CONTRACT in popup:
        thisevent.flag_contract_rcpt = True
    if settings.RECEIVE_CONTRACT in popup:
        thisevent.flag_contract_rcvd = True
    if settings.RECEIVE_DEPOSIT in popup:
        thisevent.flag_deposit_rcvd = True
    if settings.RECEIVE_FINAL_PAYMENT in popup:
        thisevent.flag_final_payment_rcvd = True
    if settings.RECEIVE_EXTRA_PAYMENT in popup:
        thisevent.flag_extra_rcvd = True
    #changed below line cause the popup alone is not enough to decide if enough
    #        musicians were asked, enough to mark this task done
    #        BUT, we still want an activity recorded showing that some were asked
    #if '/musicians/' in popup or 'Invite musicians to play' in popup:
    if '/musicians/' in popup:
        nothing = 1
        #new_action_save(['Musicians were asked to play!','dummy'], thisevent)
    if settings.INVITE_MUSICIANS in popup:
        thisevent.flag_musicians_sent = True
    if settings.ALL_MUSICIANS_BOOKED in popup:
        thisevent.flag_musicians_rcvd = True
    if '/confirmation/' in popup or settings.SEND_FINAL_CONFIRMATION in popup:
        thisevent.flag_final_confirmation_sent = True
    if settings.RECEIVE_FINAL_CONFIRMATION in popup:
        thisevent.flag_final_confirmation_rcvd = True
    if '/musiclist/' in popup or settings.SEND_MUSIC_LIST in popup:
        thisevent.flag_music_list_sent = True
    if settings.RECEIVE_MUSIC_LIST in popup:
        thisevent.flag_music_list_rcvd = True
#     if settings.CHECK_MUSIC_LIST in popup:
#         thisevent.flag_music_list_rcvd = True
    if '/factsheet/' in popup or settings.SEND_FACT_SHEETS in popup:
        thisevent.flag_fact_sheets_sent = True
    if settings.ALL_FACT_SHEETS_CONFIRMED in popup:
        thisevent.flag_fact_sheets_rcvd = True
    if '/hold/' in popup or settings.SEND_HOLD in popup:
        thisevent.flag_hold_sent = True
        
def concurrent(request, eventnum):
    id = eventnum
    return render(request, 'events/concurrent.html', {'id':id})             

def calc_popup(data, thisevent):
    if '_email_submit' in data:
        popup = '/events/email/' + str(thisevent.pk) + '/email/'
    elif '_email_planner_submit' in data:
        popup = '/events/email/' + str(thisevent.pk) + '/email_planner/'
    elif '_email_planner_contract_submit' in data:
        popup = '/events/email/' + str(thisevent.pk) + '/email_planner_contract/'
    elif '_email_planner_musiclist_submit' in data:
        popup = '/events/email/' + str(thisevent.pk) + '/email_planner_musiclist/'                
    elif '_factsheet_submit' in data:
        popup = '/events/email/' + str(thisevent.pk) + '/factsheet/'
    elif '_musicians_submit' in data:
        popup = '/events/email/' + str(thisevent.pk) + '/musicians/'
    elif '_musicians_email_submit' in data:
        popup = '/events/email/' + str(thisevent.pk) + '/musicians_email/'
    elif '_archive_submit' in data:
        popup = '/events/archive/' + str(thisevent.pk)
    elif '_deposit_submit' in data:
        popup = '/events/email/'+ str(thisevent.pk) + '/deposit/'
    elif '_confirmation_submit' in data:
        popup = '/events/email/'+ str(thisevent.pk) + '/confirmation/'
    elif '_finalpay_submit' in data:
        popup = '/events/email/'+ str(thisevent.pk) + '/finalpay/'
    elif '_extrapay_submit' in data:
        popup = '/events/email/'+ str(thisevent.pk) + '/extrapay/'
    elif '_musiclist_submit' in data:
        popup = '/events/email/'+ str(thisevent.pk) + '/musiclist/'
    elif '_contract_submit' in data:
        popup = '/events/email/'+ str(thisevent.pk) + '/contract/'
    elif '_contract_print_submit' in data:
        popup = '/events/email_pdf/'+ str(thisevent.pk) + '/contract_print/'
    elif '_invoice_submit' in data:
        popup = '/events/email_pdf/'+ str(thisevent.pk) + '/invoice/'
    elif '_invoice_deposit_submit' in data:
        popup = '/events/email_pdf/'+ str(thisevent.pk) + '/invoice_deposit/'
    elif '_invoice_final_submit' in data:
        popup = '/events/email_pdf/'+ str(thisevent.pk) + '/invoice_final/'
    elif '_invoice_extra_submit' in data:
        popup = '/events/email_pdf/'+ str(thisevent.pk) + '/invoice_extra/'
    elif '_more_submit' in data:
        popup = '/events/email/'+ str(thisevent.pk) + '/more/'
    elif '_receipt_extrapay_submit' in data:
        popup = '/events/email_pdf/'+ str(thisevent.pk) + '/receipt_extrapay/'
    elif '_receipt_finalpay_submit' in data:
        popup = '/events/email_pdf/'+ str(thisevent.pk) + '/receipt_finalpay/'
    elif '_receipt_deposit_submit' in data:
        popup = '/events/email_pdf/'+ str(thisevent.pk) + '/receipt_deposit/'
    elif '_receipt_contract_submit' in data:
        popup = '/events/email/'+ str(thisevent.pk) + '/receipt_contract/'
    elif '_depositcontract_submit' in data:
        popup = '/events/email/'+ str(thisevent.pk) + '/depositcontract/'
    elif '_hold_submit' in data:
        popup = '/events/email/'+ str(thisevent.pk) + '/hold/'
    elif '_payment_only' in data:
        popup = '/events/email/'+ str(thisevent.pk) + '/payment_only/'
    elif '_contract_only' in data:
        popup = '/events/email/'+ str(thisevent.pk) + '/contract_only/'
    elif '_musiclist_only' in data:
        popup = '/events/email/'+ str(thisevent.pk) + '/musiclist_only/'
    elif '_confirmation_only' in data:
        popup = '/events/email/'+ str(thisevent.pk) + '/confirmation_only/'
    else:
        popup= 'none'
    return popup

         

def edit(request, pk, popup2=''):
    browse_mode = 'EVENT'
    thisevent = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        #show animation
        
        nextpage = request.POST.get('next', '/events/')
        form = AddForm(request.POST, instance=thisevent)
        oldevent = form._meta.model.objects.get(pk=form.instance.pk)
        if form.is_valid():
            try:
                thisevent = form.save(commit=True)
            except ConcurrentUpdate:
                return redirect('/events/concurrent/' + str(form.instance.pk) + '/')    
                
            #check if popup early, so new corresponding flag can be set and saved/updated
            #  so that future dates in emails are correctly filled in
            popup = calc_popup(request.POST, thisevent)
            if popup == "none":
                nothing = 1
            else:
                #set_flags(popup, thisevent)
                #thisevent.event_reminders_done = False
                nothing = 1
            
            
            #thisevent.event_reminders_done = False

            #figure out auto-reminders
            process_auto_reminders(thisevent)
            #calc all sent/due/rcvd dates
            process_due_dates(thisevent)
            #fill in any behind-the-scenes database fields
            process_new_entries(form, thisevent)
            #save any new actions (recent activity)?
            process_new_actions(form, thisevent, oldevent)
            #update flags
            process_update_flags(thisevent)
            #record that reminders were done
            thisevent.event_reminders_done = True


            #if friendly_name exists, and contact is a saved contact, then
            #  add this friendly_name to contact db, even if it's already there (updates it then)!
            if thisevent.contact and thisevent.friendly_name: #this means its a saved contact being used, and friendly_name was entered
                thiscontact = get_object_or_404(Contact, pk=thisevent.contact.id)
                thiscontact.friendlyname = thisevent.friendly_name
                thiscontact.save()
 
            
            thisevent.save()            
            check_gcal(thisevent, False)
            
            #daily automation run it once now
            #if (not '/events/archive/' in popup) and thisevent.automation:
            if (not '/events/archive/' in popup):
                process_cron_jobs_now(thisevent)
            
            form = AddForm(instance=thisevent)
            rates = RateChart.objects.order_by('importance')
            reminders = Reminder.objects.filter(event_id=pk, disb=False).order_by('done', 'date')
            reminderscount = reminders.filter(done=False).count
            
            if Header.objects.filter(event_id=pk).exists():
                thisheader = Header.objects.filter(event_id=pk)
                thisheader = get_object_or_404(Header, event_id=pk)
                header = [thisheader.todos, thisheader.notes, thisheader.records, thisheader.history]    
            else:
                header = ['','','','']
            
            activities = Activity.objects.filter(event_id=pk).order_by('-date', '-id')
            musicianlist = MusicianEvent.objects.filter(event_id=pk).exclude(
                            placeholder=True).order_by('-pk')
            musicianlistyes = MusicianEvent.objects.filter(event_id=pk, yes=True, no=False).order_by(
                'rank')
            musicians = Musician.objects.exclude(name="----------").order_by('instrument')
            musiciansasked = MusicianEvent.objects.filter(event_id=pk).exclude(
                                                placeholder=True).order_by('-pk')
            #deal with possible popup
#             if popup == 'none': #go back to home page or where you came from
#                 if nextpage == ('') or ('/edit' in nextpage):
#                     return HttpResponseRedirect('/events/')
#                 else:
#                     return HttpResponseRedirect(nextpage)
            if '/events/archive/' in popup:
                return redirect(popup)
            else:   #go to same add(edit) page for same event and pass popup value
                soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
                this = Global.objects.get(pk=1)
                smallcal = sidecal(this.sidecal_year, this.sidecal_month)
                sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])
                
                if thisevent.date < date.today():
                    eventpast = True
                else:
                    eventpast = False
                            
                return render(request, 'events/edit-new.html', {'form': form, 'rates': rates, 'reminders': reminders, 'reminderscount': reminderscount,
                                                           'popup': popup, 'browse_mode': browse_mode, 'header': header,
                                                           'activities': activities, 'musicianlist':musicianlist, 
                                                           'musicians':musicians, 'musicianlistyes':musicianlistyes,  
                                                           'musiciansasked':musiciansasked, 'eventpast':eventpast,
                                                           'soonevents': soonevents, 'soonreminder': soonreminder, 
                                                           'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                                                           'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                                                           'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents})                
        
        else:
            return HttpResponseRedirect('/error/')       
    else:
        form = AddForm(instance=thisevent)
        
    if popup2 == '' or popup2 == '/' or popup2 == ' ' or popup2 == None or (not popup2):
        popup2 = 'none'
    rates = RateChart.objects.order_by('importance')
    reminders = Reminder.objects.filter(event_id=pk, disb=False).order_by('done', 'date')
    reminderscount = reminders.filter(done=False).count
    if Header.objects.filter(event_id=pk).exists():
        thisheader = Header.objects.filter(event_id=pk)
        thisheader = get_object_or_404(Header, event_id=pk)
        header = [thisheader.todos, thisheader.notes, thisheader.records, thisheader.history]    
    else:
        header = ['','','','']

    activities = Activity.objects.filter(event_id=pk).order_by('-date', '-id')
    musicianlist = MusicianEvent.objects.filter(event_id=pk).exclude(
                            placeholder=True).order_by('-pk')
    musicianlistyes = MusicianEvent.objects.filter(event_id=pk, yes=True, no=False).order_by(
        'rank')
    musicians = Musician.objects.exclude(name="----------").order_by('instrument')
    musiciansasked = MusicianEvent.objects.filter(event_id=pk).exclude(
                                                placeholder=True).order_by('-pk')
    soonevents, soonreminder, pastduereminder, pastduereminder_exists, recentactivities, newevents , pays, pays_pd, all_soonrem_auto , nonautoremcount = sidebar()
    this = Global.objects.get(pk=1)
    smallcal = sidecal(this.sidecal_year, this.sidecal_month)
    sidestate = array('b',[this.pnl1,this.pnl2,this.pnl3,this.pnl4,this.pnl5,this.auto_btn_side,this.auto_btn,this.pnl6,this.hideside,this.show_pd_btn])

    if thisevent.date < date.today():
        eventpast = True
    else:
        eventpast = False
    
    #TEMPORARY DB FIX - grab existing event and change it's primary key to '1'
    #this will make a copy, but who cares?
    exists = Event.objects.filter(pk=1).exists()
    if not exists:
        tempfix = Event.objects.get(pk=2)
        tempfix.pk = 1
        tempfix.save()
        print("the deed is done")
    
    
        
    return render(request, 'events/edit-new.html', {'form': form, 'rates': rates, 'reminders': reminders, 'reminderscount': reminderscount,
                                               'popup': popup2,  'browse_mode': browse_mode, 'header': header, 
                                               'activities': activities, 'musicianlist':musicianlist, 
                                               'musicians':musicians, 'musicianlistyes':musicianlistyes,
                                               'musiciansasked':musiciansasked, 'eventpast':eventpast,  
                                               'soonevents': soonevents, 'soonreminder': soonreminder, 
                                               'pastduereminder': pastduereminder, 'smallcal': mark_safe(smallcal), 
                                               'pastduereminder_exists': pastduereminder_exists, 'sidestate': sidestate, 'nonautoremcount': nonautoremcount, 
                                               'recentactivities': recentactivities, 'pays': pays, 'pays_pd': pays_pd, 'all_soonrem_auto': all_soonrem_auto, 'newevents': newevents})                


def c2str(instr):
    #converts empty inputs to none, ordoes str() on others
    if not instr:
        outstr = ""
    else:
        outstr = str(instr)
    return outstr

def c2strb(instr): #boolean version
    #converts empty inputs to none, ordoes str() on others
    if not instr:
        outstr = "False"
    else:
        outstr = "True"
    return outstr
    
def c2date(instr): #.strftime('%m/%d/%y')
    #converts empty input to none, or does strftime on the others
    if not instr:
        outstr = ""
    else:
        outstr = instr.strftime('%m/%d/%y').lstrip("0").replace("/0", "/")
    return outstr
    
    
def c2time(instr): # strftime('%I:%M%p')
    #converts empty input to none, or does strftime on the others
    if not instr:
        outstr = ""
    else:
        outstr = instr.strftime('%I:%M%p').lstrip("0")
    return outstr

    
def new_action(fulltext, event, typestr, oldstr, newstr):
    #forms new action given data, updates fulltext with new data.  if fulltext
    #  is longer than 200chars, saves this and starts a new fulltext
    if oldstr == newstr:
        return
    if oldstr and newstr:
        atext = "Changed " + typestr + " from '" + oldstr + "' to '" + newstr + "'"
    elif oldstr:
        atext = "Removed " + typestr + " '" + oldstr + "'"
    elif newstr:
        atext = "Added " + typestr + " '" + newstr + "'"
    else:
        atext = "Changed " + typestr
    
    if len(fulltext[0]) > 300:
        new_action_save(fulltext, event)
        fulltext[0] = atext
    elif len(fulltext[0]) > 0:
        fulltext[0] = fulltext[0] + ";  " + atext
    else:
        fulltext[0] = atext
    


    
def new_action_save(fulltext, event):
    #just saves new action for real
    newact = Activity(name = fulltext[0])
    newact.date = date.today()
    newact.event = event
    newact.save()
    

            
def process_new_actions( form, thisevent, oldevent ):
    i = thisevent
    ft = ['','dummy']
    #simple fields
    if 'name' in form.changed_data: new_action(ft, i, "Name", c2str(oldevent.name), c2str(form.cleaned_data['name']))
    if 'friendly_name' in form.changed_data: new_action(ft, i, "Friendly Name", c2str(oldevent.friendly_name), c2str(form.cleaned_data['friendly_name']))
    if 'date' in form.changed_data: new_action(ft, i, "Date", c2date(oldevent.date), c2date(form.cleaned_data['date']))
    if 'start_time' in form.changed_data: new_action(ft, i, "Start Time", c2time(oldevent.start_time), c2time(form.cleaned_data['start_time']))
    if 'end_time' in form.changed_data: new_action(ft, i, "End Time", c2time(oldevent.end_time), c2time(form.cleaned_data['end_time']))
    if 'ceremony_time' in form.changed_data: new_action(ft, i, "Ceremony Time", c2time(oldevent.ceremony_time), c2time(form.cleaned_data['ceremony_time']))
    if 'event_type_name' in form.changed_data: new_action(ft, i, "Event Type", c2str(oldevent.event_type_name), c2str(form.cleaned_data['event_type_name']))
    if 'ensemble_name' in form.changed_data: new_action(ft, i, "Ensemble Name", c2str(oldevent.ensemble_name), c2str(form.cleaned_data['ensemble_name']))
    if 'ensemble_number' in form.changed_data: new_action(ft, i, "Ensemble Number", c2str(oldevent.ensemble_number), c2str(form.cleaned_data['ensemble_number']))
    if 'fee' in form.changed_data: new_action(ft, i, "Fee", c2str(oldevent.fee), c2str(form.cleaned_data['fee']))
    if 'musician_fee' in form.changed_data:
        new_action(ft, i, "Musician Fee", c2str(oldevent.musician_fee), c2str(form.cleaned_data['musician_fee']))
        
    if 'dayofcontact_alone_name' in form.changed_data:
        new_action(ft, i, "Day of Contact Name", c2str(oldevent.dayofcontact_alone_name), c2str(form.cleaned_data['dayofcontact_alone_name']))
    if 'dayofcontact_alone_phone' in form.changed_data:
        new_action(ft, i, "Day of Contact Phone", c2str(oldevent.dayofcontact_alone_phone), c2str(form.cleaned_data['dayofcontact_alone_phone']))
    if 'number_guests' in form.changed_data:
        new_action(ft, i, "Number of Guests", c2str(oldevent.number_guests), c2str(form.cleaned_data['number_guests']))
        
        #below not necessary anymore, it's being done in ajax on the fly
        #if musician fee changed, we also need to update PaymentsDue amounts!
#         pdues = PaymentsDue.objects.filter(event_id=thisevent.id).order_by('pk')
#         for pdue in pdues:
#             pdue.payment = form.cleaned_data['musician_fee']
#             pdue.save()
    if 'deposit_fee' in form.changed_data: new_action(ft, i, "Deposit Fee", c2str(oldevent.deposit_fee), c2str(form.cleaned_data['deposit_fee']))
    if 'final_fee' in form.changed_data: new_action(ft, i, "Final Fee", c2str(oldevent.final_fee), c2str(form.cleaned_data['final_fee']))
    if 'hold_until' in form.changed_data: new_action(ft, i, "Hold Date", c2date(oldevent.hold_until), c2date(form.cleaned_data['hold_until']))
    if 'waive_contract' in form.changed_data: new_action(ft, i, "Waive Contract", c2strb(oldevent.waive_contract), c2strb(form.cleaned_data['waive_contract']))
    if 'waive_payment' in form.changed_data: new_action(ft, i, "Waive Payment", c2strb(oldevent.waive_payment), c2strb(form.cleaned_data['waive_payment']))
    if 'location_details' in form.changed_data: new_action(ft, i, "Location Notes", c2str(oldevent.location_details), c2str(form.cleaned_data['location_details']))
    if 'location_outdoors' in form.changed_data: new_action(ft, i, "Location Outdoors", c2str(oldevent.location_outdoors), c2str(form.cleaned_data['location_outdoors']))
    if 'location_address' in form.changed_data: new_action(ft, i, "Location Address", c2str(oldevent.location_address), c2str(form.cleaned_data['location_address']))
    if 'location_link' in form.changed_data: new_action(ft, i, "Location Link", c2str(oldevent.location_link), c2str(form.cleaned_data['location_link']))
    if 'location_phone' in form.changed_data: new_action(ft, i, "Location Phone", c2str(oldevent.location_phone), c2str(form.cleaned_data['location_phone']))
    if 'location_email' in form.changed_data: new_action(ft, i, "Location Email", c2str(oldevent.location_email), c2str(form.cleaned_data['location_email']))
    if 'contact_details' in form.changed_data: new_action(ft, i, "Contact Notes", c2str(oldevent.contact_details), c2str(form.cleaned_data['contact_details']))
    if 'contact_agency' in form.changed_data: new_action(ft, i, "Contact Agency", c2str(oldevent.contact_agency), c2str(form.cleaned_data['contact_agency']))
    if 'contact_phone' in form.changed_data: new_action(ft, i, "Contact Phone", c2str(oldevent.contact_phone), c2str(form.cleaned_data['contact_phone']))
    if 'contact_email' in form.changed_data: new_action(ft, i, "Contact Email", c2str(oldevent.contact_email), c2str(form.cleaned_data['contact_email']))
    if 'dayofcontact_details' in form.changed_data: new_action(ft, i, "Planner Notes", c2str(oldevent.dayofcontact_details), c2str(form.cleaned_data['dayofcontact_details']))
    if 'dayofcontact_phone' in form.changed_data: new_action(ft, i, "Planner Phone", c2str(oldevent.dayofcontact_phone), c2str(form.cleaned_data['dayofcontact_phone']))
    if 'dayofcontact_email' in form.changed_data: new_action(ft, i, "Planner Email", c2str(oldevent.dayofcontact_email), c2str(form.cleaned_data['dayofcontact_email']))
    if 'contracting_fee' in form.changed_data: new_action(ft, i, "Contracting Fee", c2str(oldevent.contracting_fee), c2str(form.cleaned_data['contracting_fee']))
    if 'cash_fee' in form.changed_data: new_action(ft, i, "Cash Fee", c2str(oldevent.cash_fee), c2str(form.cleaned_data['cash_fee']))
    if 'extra_fee' in form.changed_data: new_action(ft, i, "Extra Fee", c2str(oldevent.extra_fee), c2str(form.cleaned_data['extra_fee']))
    if 'waive_music_list' in form.changed_data: new_action(ft, i, "Waive Music List", c2strb(oldevent.waive_music_list), c2strb(form.cleaned_data['waive_music_list']))
    if 'recessional_cue' in form.changed_data: new_action(ft, i, "Recessional Cue", c2str(oldevent.recessional_cue), c2str(form.cleaned_data['recessional_cue']))
    if 'officiant_info' in form.changed_data: new_action(ft, i, "Officiant's Info", c2str(oldevent.officiant_info), c2str(form.cleaned_data['officiant_info']))
    if 'music_list' in form.changed_data: new_action(ft, i, "Music List", "", "")
    if 'notes' in form.changed_data: new_action(ft, i, "Notes", "", "")
    #other fields that require processing
    if ('location' in form.changed_data) or ('location_name' in form.changed_data) or (oldevent.location_name != "" and form.cleaned_data['location_name'] != oldevent.location_name):
        if (form.cleaned_data['location']): #if new location exists its a saved location
            
            new = get_object_or_404(Venue, id=form.cleaned_data['location'].id).name
        else:
            new = form.cleaned_data['location_name']
        if (oldevent.location): #if old location exists its  asaved location
            old = get_object_or_404(Venue, pk=oldevent.location.id).name
        else:
            old = oldevent.location_name
        if old != new:
            new_action(ft, i, "Location", c2str(old), c2str(new))
    if ('contact' in form.changed_data) or ('contact_name' in form.changed_data) or (oldevent.contact_name != "" and form.cleaned_data['contact_name'] != oldevent.contact_name):
        if (form.cleaned_data['contact']): #if new contact exists its a saved contact
            
            new = get_object_or_404(Contact, id=form.cleaned_data['contact'].id).name
        else:
            new = form.cleaned_data['contact_name']
        if (oldevent.contact): #if old contact exists its  asaved contact
            old = get_object_or_404(Contact, pk=oldevent.contact.id).name
        else:
            old = oldevent.contact_name
        if old != new:
            new_action(ft, i, "Contact", c2str(old), c2str(new))
    if ('dayofcontact' in form.changed_data) or ('dayofcontact_name' in form.changed_data) or (oldevent.dayofcontact_name != "" and form.cleaned_data['dayofcontact_name'] != oldevent.dayofcontact_name):
        if (form.cleaned_data['dayofcontact']): #if new dayofcontact exists its a saved dayofcontact
            
            new = get_object_or_404(DayofContact, id=form.cleaned_data['dayofcontact'].id).name
        else:
            new = form.cleaned_data['dayofcontact_name']
        if (oldevent.dayofcontact): #if old dayofcontact exists its  asaved dayofcontact
            old = get_object_or_404(DayofContact, pk=oldevent.dayofcontact.id).name
        else:
            old = oldevent.dayofcontact_name
        if old != new:
            new_action(ft, i, "Planner", c2str(old), c2str(new))
    if 'type' in form.changed_data:
        if form.cleaned_data['type'] == 'HD': new = "Hold"
        if form.cleaned_data['type'] == 'AB': new = "Agency"
        if form.cleaned_data['type'] == 'RG': new = "Regular"
        if oldevent.type == 'HD': old = "Hold"
        if oldevent.type == 'AB': old = "Agency"
        if oldevent.type == 'RG': old = "Regular"
        new_action(ft, i, "Type of Event", c2str(old), c2str(new))
    
    #anything else?
    
    if len(ft[0]) > 0:
        new_action_save(ft, i)
    


def process_ajax_due_dates(request):
    if request.is_ajax():

#         if request.GET['event_reminders_done'] == 'true':
#             nothing_done = True
#             data = data = {'nothing_done':nothing_done,}
#             return HttpResponse(json.dumps(data), content_type='application/json')
                            
        temp = EventTemp()
        temp.event_reminders_done = convertfromajax(request.GET['event_reminders_done'])
        
        temp.id = convertintfromajax(request.GET['id'])
        #print(temp.id)
        temp.ensemble_number = convertintfromajax(request.GET['ensemble_number'])
        temp.hold_until = convertdatefromajax(request.GET['hold_until'])
        #print(temp.hold_until)
        temp.hold_released = convertdatefromajax(request.GET['hold_released'])
        temp.date_entered = convertdatefromajax(request.GET['date_entered'])
        #print(temp.date_entered)
        if not temp.date_entered:
            temp.date_entered = date.today()
        temp.date = convertdatefromajax(request.GET['date'])
        #print(temp.date)
        if not temp.date:
            temp.date = date.today()
        temp.waive_contract = convertfromajax(request.GET['waive_contract'])
        temp.waive_payment = convertfromajax(request.GET['waive_payment'])
        temp.fee = convertintfromajax(request.GET['fee'])
        #print(temp.fee)
        temp.deposit_fee = convertintfromajax(request.GET['deposit_fee'])
        temp.final_fee = convertintfromajax(request.GET['final_fee'])
        temp.extra_fee = convertintfromajax(request.GET['extra_fee'])
        temp.automation = convertfromajax(request.GET['automation'])
        temp.accept_custom = convertfromajax(request.GET['accept_custom'])
        
        temp.contract_sentdate = convertdatefromajax(request.GET['contract_sentdate'])
        temp.deposit_sentdate = convertdatefromajax(request.GET['deposit_sentdate'])
        temp.final_sentdate = convertdatefromajax(request.GET['final_sentdate'])
        temp.music_list_sentdate = convertdatefromajax(request.GET['music_list_sentdate'])
        temp.musicians_sentdate = convertdatefromajax(request.GET['musicians_sentdate'])
        temp.confirmation_sentdate = convertdatefromajax(request.GET['confirmation_sentdate'])
        temp.fact_sheets_sentdate = convertdatefromajax(request.GET['fact_sheets_sentdate'])
        temp.hold_sentdate = convertdatefromajax(request.GET['hold_sentdate'])
        temp.extra_sentdate = convertdatefromajax(request.GET['extra_sentdate'])
        
        temp.contract_rcvddate = convertdatefromajax(request.GET['contract_rcvddate'])
        temp.deposit_rcvddate = convertdatefromajax(request.GET['deposit_rcvddate'])
        temp.final_rcvddate = convertdatefromajax(request.GET['final_rcvddate'])
        temp.music_list_rcvddate = convertdatefromajax(request.GET['music_list_rcvddate'])
        temp.musicians_rcvddate = convertdatefromajax(request.GET['musicians_rcvddate'])
        temp.confirmation_rcvddate = convertdatefromajax(request.GET['confirmation_rcvddate'])
        temp.fact_sheets_rcvddate = convertdatefromajax(request.GET['fact_sheets_rcvddate'])
        temp.extra_rcvddate = convertdatefromajax(request.GET['extra_rcvddate'])
        
        temp.contract_rcptdate = convertdatefromajax(request.GET['contract_rcptdate'])
        temp.deposit_rcptdate = convertdatefromajax(request.GET['deposit_rcptdate'])
        temp.final_rcptdate = convertdatefromajax(request.GET['final_rcptdate'])
        temp.extra_rcptdate = convertdatefromajax(request.GET['extra_rcptdate'])
        
        temp.contract_duedate = convertdatefromajax(request.GET['contract_duedate'])
        temp.deposit_duedate = convertdatefromajax(request.GET['deposit_duedate'])
        temp.final_duedate = convertdatefromajax(request.GET['final_duedate'])
        temp.music_list_duedate = convertdatefromajax(request.GET['music_list_duedate'])
        temp.musicians_duedate = convertdatefromajax(request.GET['musicians_duedate'])
        temp.confirmation_duedate = convertdatefromajax(request.GET['confirmation_duedate'])
        temp.fact_sheets_duedate = convertdatefromajax(request.GET['fact_sheets_duedate'])
        temp.extra_duedate = convertdatefromajax(request.GET['extra_duedate'])
        
        temp.contract_senddate = convertdatefromajax(request.GET['contract_senddate'])
        temp.deposit_senddate = convertdatefromajax(request.GET['deposit_senddate'])
        temp.final_senddate = convertdatefromajax(request.GET['final_senddate'])
        temp.music_list_senddate = convertdatefromajax(request.GET['music_list_senddate'])
        temp.musicians_senddate = convertdatefromajax(request.GET['musicians_senddate'])
        temp.confirmation_senddate = convertdatefromajax(request.GET['confirmation_senddate'])
        temp.fact_sheets_senddate = convertdatefromajax(request.GET['fact_sheets_senddate'])
        temp.extra_senddate = convertdatefromajax(request.GET['extra_senddate'])
        
        temp.flag_hold = convertfromajax(request.GET['flag_hold'])
        temp.flag_hold_sent = convertfromajax(request.GET['flag_hold_sent'])
        temp.waive_music_list = convertfromajax(request.GET['waive_music_list'])
        temp.automation = convertfromajax(request.GET['automation'])
        temp.reminderdisable = convertfromajax(request.GET['reminderdisable'])
        #print(temp.flag_hold)
        #print(temp.automation)
        
        temp.flag_contract_sent = convertfromajax(request.GET['flag_contract_sent'])
        temp.flag_contract_rcvd = convertfromajax(request.GET['flag_contract_rcvd'])
        temp.flag_contract_rcpt = convertfromajax(request.GET['flag_contract_rcpt'])

        temp.flag_deposit_sent = convertfromajax(request.GET['flag_deposit_sent'])
        temp.flag_deposit_rcvd = convertfromajax(request.GET['flag_deposit_rcvd'])
        temp.flag_deposit_rcpt = convertfromajax(request.GET['flag_deposit_rcpt'])

        temp.flag_music_list_sent = convertfromajax(request.GET['flag_music_list_sent'])
        temp.flag_music_list_rcvd = convertfromajax(request.GET['flag_music_list_rcvd'])

        temp.flag_musicians_sent = convertfromajax(request.GET['flag_musicians_sent'])
        temp.flag_musicians_rcvd = convertfromajax(request.GET['flag_musicians_rcvd'])

        temp.flag_final_payment_sent = convertfromajax(request.GET['flag_final_payment_sent'])
        temp.flag_final_payment_rcvd = convertfromajax(request.GET['flag_final_payment_rcvd'])
        temp.flag_final_payment_rcpt = convertfromajax(request.GET['flag_final_payment_rcpt'])

        temp.flag_extra_sent = convertfromajax(request.GET['flag_extra_sent'])
        temp.flag_extra_rcvd = convertfromajax(request.GET['flag_extra_rcvd'])
        temp.flag_extra_rcpt = convertfromajax(request.GET['flag_extra_rcpt'])

        temp.flag_final_confirmation_sent = convertfromajax(request.GET['flag_final_confirmation_sent'])
        temp.flag_final_confirmation_rcvd = convertfromajax(request.GET['flag_final_confirmation_rcvd'])

        temp.flag_fact_sheets_sent = convertfromajax(request.GET['flag_fact_sheets_sent'])
        temp.flag_fact_sheets_rcvd = convertfromajax(request.GET['flag_fact_sheets_rcvd'])

#         print("BEFORE AUTO_REMINDERS:")
#         for attr, value in temp.__dict__.items():
#             print(attr, value)
        
        #do processing now
        process_auto_reminders(temp)
        process_due_dates(temp)
        #process_update_flags(temp)
        
        #print(converttoajax(temp.flag_hold))
        #print(converttoajax(temp.automation))
        
        data = {'event_reminders_done':converttoajax(True),
                
                'contract_sentdate':convertdatetoajax(temp.contract_sentdate),
                'deposit_sentdate':convertdatetoajax(temp.deposit_sentdate),
                'final_sentdate':convertdatetoajax(temp.final_sentdate),
                'music_list_sentdate':convertdatetoajax(temp.music_list_sentdate),
                'musicians_sentdate':convertdatetoajax(temp.musicians_sentdate),
                'confirmation_sentdate':convertdatetoajax(temp.confirmation_sentdate),
                'fact_sheets_sentdate':convertdatetoajax(temp.fact_sheets_sentdate),
                'hold_sentdate':convertdatetoajax(temp.hold_sentdate),
                'extra_sentdate':convertdatetoajax(temp.extra_sentdate),
                
                'contract_rcvddate':convertdatetoajax(temp.contract_rcvddate),
                'deposit_rcvddate':convertdatetoajax(temp.deposit_rcvddate),
                'final_rcvddate':convertdatetoajax(temp.final_rcvddate),
                'music_list_rcvddate':convertdatetoajax(temp.music_list_rcvddate),
                'musicians_rcvddate':convertdatetoajax(temp.musicians_rcvddate),
                'confirmation_rcvddate':convertdatetoajax(temp.confirmation_rcvddate),
                'fact_sheets_rcvddate':convertdatetoajax(temp.fact_sheets_rcvddate),
                'extra_rcvddate':convertdatetoajax(temp.extra_rcvddate),
                
                'contract_rcptdate':convertdatetoajax(temp.contract_rcptdate),
                'deposit_rcptdate':convertdatetoajax(temp.deposit_rcptdate),
                'final_rcptdate':convertdatetoajax(temp.final_rcptdate),
                'extra_rcptdate':convertdatetoajax(temp.extra_rcptdate),
                
                'contract_duedate':convertdatetoajax(temp.contract_duedate),
                'deposit_duedate':convertdatetoajax(temp.deposit_duedate),
                'final_duedate':convertdatetoajax(temp.final_duedate),
                'music_list_duedate':convertdatetoajax(temp.music_list_duedate),
                'musicians_duedate':convertdatetoajax(temp.musicians_duedate),
                'confirmation_duedate':convertdatetoajax(temp.confirmation_duedate),
                'fact_sheets_duedate':convertdatetoajax(temp.fact_sheets_duedate),
                'extra_duedate':convertdatetoajax(temp.extra_duedate),
                
                'contract_senddate':convertdatetoajax(temp.contract_senddate),
                'deposit_senddate':convertdatetoajax(temp.deposit_senddate),
                'final_senddate':convertdatetoajax(temp.final_senddate),
                'music_list_senddate':convertdatetoajax(temp.music_list_senddate),
                'musicians_senddate':convertdatetoajax(temp.musicians_senddate),
                'confirmation_senddate':convertdatetoajax(temp.confirmation_senddate),
                'fact_sheets_senddate':convertdatetoajax(temp.fact_sheets_senddate),
                'extra_senddate':convertdatetoajax(temp.extra_senddate),
                
                'flag_hold':converttoajax(temp.flag_hold),
                'flag_hold_sent':converttoajax(temp.flag_hold_sent),
                'waive_music_list':converttoajax(temp.waive_music_list),
                'automation':converttoajax(temp.automation),
                
                'flag_contract_sent':converttoajax(temp.flag_contract_sent),
                'flag_contract_rcvd':converttoajax(temp.flag_contract_rcvd),
                'flag_contract_rcpt':converttoajax(temp.flag_contract_rcpt),

                'flag_deposit_sent':converttoajax(temp.flag_deposit_sent),
                'flag_deposit_rcvd':converttoajax(temp.flag_deposit_rcvd),
                'flag_deposit_rcpt':converttoajax(temp.flag_deposit_rcpt),

                'flag_music_list_sent':converttoajax(temp.flag_music_list_sent),
                'flag_music_list_rcvd':converttoajax(temp.flag_music_list_rcvd),

                'flag_musicians_sent':converttoajax(temp.flag_musicians_sent),
                'flag_musicians_rcvd':converttoajax(temp.flag_musicians_rcvd),

                'flag_final_payment_sent':converttoajax(temp.flag_final_payment_sent),
                'flag_final_payment_rcvd':converttoajax(temp.flag_final_payment_rcvd),
                'flag_final_payment_rcpt':converttoajax(temp.flag_final_payment_rcpt),

                'flag_extra_sent':converttoajax(temp.flag_extra_sent),
                'flag_extra_rcvd':converttoajax(temp.flag_extra_rcvd),
                'flag_extra_rcpt':converttoajax(temp.flag_extra_rcpt),

                'flag_final_confirmation_sent':converttoajax(temp.flag_final_confirmation_sent),
                'flag_final_confirmation_rcvd':converttoajax(temp.flag_final_confirmation_rcvd),

                'flag_fact_sheets_sent':converttoajax(temp.flag_fact_sheets_sent),
                'flag_fact_sheets_rcvd':converttoajax(temp.flag_fact_sheets_rcvd),
                
                'deposit_fee':convertinttoajax(temp.deposit_fee),
                'final_fee':convertinttoajax(temp.final_fee),
                'date':convertprettydatetoajax(temp.date),}
        
        
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
     
def convertfromajax(origval):
    if origval == 'false':
        return False
    else:
        return True

def converttoajax(origval):
    if origval == False:
        return 'false'
    else:
        return 'true'

def convertdatefromajax(origval):
    try:
        result = datetime.datetime.strptime(origval,"%Y-%m-%d").date()
    except ValueError:
        try: 
            result = datetime.datetime.strptime(origval, "%A, %B %d, %Y").date()
        except ValueError:
            try: 
                result = datetime.datetime.strptime(origval, "%a, %b %d, %Y").date()
            except ValueError:
                try:
                    result = datetime.datetime.strptime(origval, "%m/%d/%y").date()
                except ValueError:
                    try:
                        result = datetime.datetime.strptime(origval, "%m/%d/%Y").date()
                    except ValueError:
                        try:
                            result = datetime.datetime.strptime(origval, "%m-%d-%y").date()
                        except ValueError:
                            try:
                                result = datetime.datetime.strptime(origval, "%m-%d-%Y").date()
                            except ValueError:
                                result = None
                            return result
                        return result
                    return result
                return result
            return result
        return result
    return result
    
def convertdatetoajax(origval):
    try:
        result = origval.strftime("%Y-%m-%d")
    except AttributeError:
        result = ''
    return result

def convertprettydatetoajax(origval):
    try:
        result = origval.strftime("%A, %B %d, %Y")
    except AttributeError:
        result = ''
    return result


def convertintfromajax(origval):
#     try:
#         temp = origval.split(".", 1)[0]
#         result = int(temp)
#     except ValueError:
#         result = None
#     return result
    
    try:
        result = float(origval)
    except:
        result = None
    return result

def convertinttoajax(origval):
    try:
        result = "{:.2f}".format(origval)
        if result[-3:] == '.00':
            result = result[:-3]
    except:
        result = ''
    return result




        
def process_due_dates( thisevent ):
    # sentdates are assigned based on actions (contract sent, musicians, etc), so when
    #    when they are blank it means the action hasn't happened yet.
    
    if thisevent.event_reminders_done:
        return
    
    #if Hold Until, register hold reminder
    #if Hold, delete all un-done auto-reminders
    if thisevent.flag_hold:
        register_reminder(settings.SEND_HOLD, date.today() + relativedelta(days=3), thisevent)
        if thisevent.hold_until:
            register_reminder(settings.HOLD_UNTIL,thisevent.hold_until, thisevent)
            delete_reminder(settings.HOLD_INDEFINITELY, thisevent)
        else:
            register_reminder(settings.HOLD_INDEFINITELY, thisevent.date - relativedelta(days=5), thisevent)
            delete_reminder(settings.HOLD_UNTIL, thisevent)
        delete_undone_reminder(settings.RECEIVE_MUSIC_LIST, thisevent)
        delete_undone_reminder(settings.SEND_MUSIC_LIST, thisevent)
        delete_undone_reminder(settings.ALL_FACT_SHEETS_CONFIRMED, thisevent)
        delete_undone_reminder(settings.SEND_FACT_SHEETS, thisevent)
        delete_undone_reminder(settings.RECEIVE_FINAL_CONFIRMATION, thisevent)
        delete_undone_reminder(settings.SEND_FINAL_CONFIRMATION, thisevent)
        delete_undone_reminder(settings.ALL_MUSICIANS_BOOKED, thisevent)
        delete_undone_reminder(settings.INVITE_MUSICIANS, thisevent)
        delete_undone_reminder(settings.RECEIPT_FINAL_PAYMENT, thisevent)
        delete_undone_reminder(settings.RECEIVE_FINAL_PAYMENT, thisevent)
        delete_undone_reminder(settings.SEND_FINAL_PAYMENT, thisevent)
        delete_undone_reminder(settings.RECEIPT_DEPOSIT, thisevent)
        delete_undone_reminder(settings.RECEIVE_DEPOSIT, thisevent)
        delete_undone_reminder(settings.SEND_DEPOSIT, thisevent)
        delete_undone_reminder(settings.RECEIPT_CONTRACT, thisevent)
        delete_undone_reminder(settings.RECEIVE_CONTRACT, thisevent)
        delete_undone_reminder(settings.SEND_CONTRACT, thisevent)
        delete_undone_reminder(settings.RECEIVE_EXTRA_PAYMENT, thisevent)
        delete_undone_reminder(settings.RECEIPT_EXTRA_PAYMENT, thisevent)
        delete_undone_reminder(settings.SEND_EXTRA_PAYMENT, thisevent)
        return

    delete_undone_reminder(settings.HOLD_UNTIL, thisevent)
    delete_undone_reminder(settings.HOLD_INDEFINITELY, thisevent)
    delete_undone_reminder(settings.SEND_HOLD, thisevent)
    
    created = thisevent.date_entered
    if thisevent.hold_released:
        created = thisevent.hold_released
    event = thisevent.date
    daystoevent = abs( event - created ).days
    
    if daystoevent > settings.DAYS_SPLIT_1:
        split = 0
    elif daystoevent > settings.DAYS_SPLIT_2:
        split = 1
    elif daystoevent > settings.DAYS_SPLIT_3:
        split = 2
    elif daystoevent > settings.DAYS_SPLIT_4:
        split = 3
    else:
        split = 4
        
    contract_send = created + relativedelta(days=settings.DAYS_CONTRACT_SEND[split])
    if thisevent.contract_sentdate:
        contract_due = thisevent.contract_sentdate + relativedelta(days=settings.DAYS_CONTRACT_DUE[split])
    if thisevent.contract_rcvddate:
        contract_receipt = thisevent.contract_rcvddate + relativedelta(days=settings.DAYS_CONTRACT_RCPT[split])
            
    deposit_send = created + relativedelta(days=settings.DAYS_DEPOSIT_SEND[split])
    if thisevent.deposit_sentdate:
        deposit_due = thisevent.deposit_sentdate + relativedelta(days=settings.DAYS_DEPOSIT_DUE[split])
    if thisevent.deposit_rcvddate:
        deposit_receipt = thisevent.deposit_rcvddate + relativedelta(days=settings.DAYS_DEPOSIT_RCPT[split])
    
    if daystoevent < 29:
        final_send = created + relativedelta(days=settings.DAYS_FINAL_SEND[split]) 
    else:
        final_send = event - relativedelta(days=settings.DAYS_FINAL_SEND[split])
    if thisevent.final_sentdate:
        if daystoevent < 29:
            final_due = thisevent.final_sentdate + relativedelta(days=settings.DAYS_FINAL_DUE[split])
        else:
            final_due = event - relativedelta(days=settings.DAYS_FINAL_DUE[split])
    if daystoevent >= 29:
        final_due = event - relativedelta(days=settings.DAYS_FINAL_DUE[split])
    if thisevent.final_rcvddate:
        final_receipt = thisevent.final_rcvddate + relativedelta(days=settings.DAYS_FINAL_RCPT[split])



    if daystoevent < 29:
        extra_send = created + relativedelta(days=settings.DAYS_EXTRA_SEND[split]) 
    else:
        extra_send = event - relativedelta(days=settings.DAYS_EXTRA_SEND[split])
    if thisevent.extra_sentdate:
        extra_due = thisevent.extra_sentdate + relativedelta(days=settings.DAYS_EXTRA_DUE[split])
    if thisevent.extra_rcvddate:
        extra_receipt = thisevent.extra_rcvddate + relativedelta(days=settings.DAYS_EXTRA_RCPT[split])



    
    musicians_send = event - relativedelta(days=settings.DAYS_MUSICIANS_SEND[split])
    if thisevent.musicians_sentdate:
        musicians_due = thisevent.musicians_sentdate + relativedelta(days=settings.DAYS_MUSICIANS_DUE[split])

    confirmation_send = event - relativedelta(days=settings.DAYS_CONFIRMATION_SEND[split])
    if thisevent.confirmation_sentdate:
        if daystoevent < 15:
            confirmation_due = thisevent.confirmation_sentdate + relativedelta(days=settings.DAYS_CONFIRMATION_DUE[split])
        else:
            confirmation_due = event - relativedelta(days=settings.DAYS_CONFIRMATION_DUE[split])
    if daystoevent >= 15:
        confirmation_due = event - relativedelta(days=settings.DAYS_CONFIRMATION_DUE[split])

    fact_sheets_send = event - relativedelta(days=settings.DAYS_FACT_SHEETS_SEND[split])
    #if thisevent.fact_sheets_sentdate:
    fact_sheets_due = event - relativedelta(days=settings.DAYS_FACT_SHEETS_DUE[split])

    music_list_send = event - relativedelta(days=settings.DAYS_MUSIC_LIST_SEND[split])
#     if thisevent.music_list_sentdate:
    music_list_due = event - relativedelta(days=settings.DAYS_MUSIC_LIST_DUE[split])

#         -------------------------------------


    if thisevent.waive_music_list:
        delete_undone_reminder(settings.SEND_MUSIC_LIST, thisevent)
        delete_undone_reminder(settings.RECEIVE_MUSIC_LIST, thisevent)
    else:
        thisevent.music_list_senddate = music_list_send
        register_reminder(settings.SEND_MUSIC_LIST,music_list_send, thisevent)
        if thisevent.music_list_sentdate:
            thisevent.music_list_duedate = music_list_due
            register_reminder(settings.RECEIVE_MUSIC_LIST,music_list_due, thisevent)
         
    
    if thisevent.waive_contract:
        delete_undone_reminder(settings.SEND_CONTRACT, thisevent)
        delete_undone_reminder(settings.RECEIVE_CONTRACT, thisevent)
        delete_undone_reminder(settings.RECEIPT_CONTRACT, thisevent)
        if not thisevent.contract_sentdate:
            thisevent.contract_sentdate = None
        if not thisevent.contract_rcvddate:
            thisevent.contract_rcvddate = None
        if not thisevent.contract_rcptdate:
            thisevent.contract_rcptdate = None
        thisevent.contract_duedate = None
        thisevent.contract_senddate = contract_send
#         thisevent.flag_contract_sent = False
#         thisevent.flag_contract_rcvd = False
#         thisevent.flag_contract_rcpt = False
    else:        
        thisevent.contract_senddate = contract_send
        register_reminder(settings.SEND_CONTRACT,contract_send, thisevent)
        if thisevent.contract_sentdate:
            thisevent.contract_duedate = contract_due
            register_reminder(settings.RECEIVE_CONTRACT,contract_due, thisevent)
        if thisevent.contract_rcvddate:
            thisevent.contract_rcptdate = contract_receipt
            register_reminder(settings.RECEIPT_CONTRACT,contract_receipt, thisevent)

    if thisevent.waive_payment or (thisevent.deposit_senddate and (thisevent.deposit_senddate == thisevent.final_senddate)) or (deposit_send == final_send) or (thisevent.deposit_fee == 0) or (thisevent.deposit_fee == 0.00):
        #SKIP deposit process completely if dep and final senddates are same or if deposit==0/null
        #    (it means no time left for separate payments)
        #    set deposit to 0 if it's not already, and set final to full fee
        
        #substituted below IF statement for above IF statement, so deposits remain as entered for now.
        #if thisevent.waive_payment or (thisevent.deposit_fee == 0) or (thisevent.deposit_fee == 0.00):
        thisevent.deposit_fee = 0
        thisevent.final_fee = thisevent.fee
        delete_undone_reminder(settings.SEND_DEPOSIT, thisevent)
        delete_undone_reminder(settings.RECEIVE_DEPOSIT, thisevent)
        delete_undone_reminder(settings.RECEIPT_DEPOSIT, thisevent)
        if not thisevent.deposit_sentdate:
            thisevent.deposit_sentdate = None
        if not thisevent.deposit_rcvddate:
            thisevent.deposit_rcvddate = None
        if not thisevent.deposit_rcptdate:
            thisevent.deposit_rcptdate = None
        thisevent.deposit_duedate = None
        thisevent.deposit_senddate = deposit_send
#         thisevent.flag_deposit_sent = False
#         thisevent.flag_deposit_rcvd = False
#         thisevent.flag_deposit_rcpt = False
    else:
        thisevent.deposit_senddate = deposit_send
        register_reminder(settings.SEND_DEPOSIT,deposit_send, thisevent)
        if thisevent.deposit_sentdate:
            thisevent.deposit_duedate = deposit_due
            register_reminder(settings.RECEIVE_DEPOSIT,deposit_due, thisevent)
        if thisevent.deposit_rcvddate:
            thisevent.deposit_rcptdate = deposit_receipt
            register_reminder(settings.RECEIPT_DEPOSIT,deposit_receipt, thisevent)
    
    if thisevent.waive_payment:
        delete_undone_reminder(settings.SEND_FINAL_PAYMENT, thisevent)
        delete_undone_reminder(settings.RECEIVE_FINAL_PAYMENT, thisevent)
        delete_undone_reminder(settings.RECEIPT_FINAL_PAYMENT, thisevent)
        if not thisevent.final_sentdate:
            thisevent.final_sentdate = None
        if not thisevent.final_rcvddate:
            thisevent.final_rcvddate = None
        if not thisevent.final_rcptdate:
            thisevent.final_rcptdate = None
        thisevent.final_duedate = None
        thisevent.final_senddate = final_send
#         thisevent.flag_final_payment_sent = False
#         thisevent.flag_final_payment_rcvd = False
#         thisevent.flag_final_payment_rcpt = False
    else:
        if thisevent.deposit_senddate and ((thisevent.deposit_senddate == thisevent.final_senddate) or (deposit_send == final_send)):
            thisevent.deposit_fee = 0
            thisevent.final_fee = thisevent.fee       
        #commented out the 3 lines above, so deposits remain as entered for now.
        thisevent.final_senddate = final_send
        register_reminder(settings.SEND_FINAL_PAYMENT,final_send, thisevent)
        if thisevent.final_sentdate:
            thisevent.final_duedate = final_due
            register_reminder(settings.RECEIVE_FINAL_PAYMENT,final_due, thisevent)
        if thisevent.final_rcvddate:
            thisevent.final_rcptdate = final_receipt
            register_reminder(settings.RECEIPT_FINAL_PAYMENT,final_receipt, thisevent)

    
    
    
    
    
    
    if thisevent.waive_payment or (not thisevent.extra_fee):
        delete_undone_reminder(settings.SEND_EXTRA_PAYMENT, thisevent)
        delete_undone_reminder(settings.RECEIVE_EXTRA_PAYMENT, thisevent)
        delete_undone_reminder(settings.RECEIPT_EXTRA_PAYMENT, thisevent)
        if not thisevent.extra_sentdate:
            thisevent.extra_sentdate = None
        if not thisevent.extra_rcvddate:
            thisevent.extra_rcvddate = None
        if not thisevent.extra_rcptdate:
            thisevent.extra_rcptdate = None
        thisevent.extra_duedate = None
        thisevent.extra_senddate = extra_send
#         thisevent.flag_extra_sent = False
#         thisevent.flag_extra_rcvd = False
#         thisevent.flag_extra_rcpt = False
    else:
        thisevent.extra_senddate = extra_send
        register_reminder(settings.SEND_EXTRA_PAYMENT,extra_send, thisevent)
        if thisevent.extra_sentdate:
            thisevent.extra_duedate = extra_due
            register_reminder(settings.RECEIVE_EXTRA_PAYMENT,extra_due, thisevent)
        if thisevent.extra_rcvddate:
            thisevent.extra_rcptdate = extra_receipt
            register_reminder(settings.RECEIPT_EXTRA_PAYMENT,extra_receipt, thisevent)
            
    
    
    
    
    
    
    
    
    thisevent.musicians_senddate = musicians_send
    register_reminder(settings.INVITE_MUSICIANS,musicians_send, thisevent)
    if thisevent.musicians_sentdate:
        thisevent.musicians_duedate = musicians_due
        register_reminder(settings.ALL_MUSICIANS_BOOKED,musicians_due, thisevent)

    thisevent.confirmation_senddate = confirmation_send
    register_reminder(settings.SEND_FINAL_CONFIRMATION,confirmation_send, thisevent)
    if thisevent.confirmation_sentdate:
        thisevent.confirmation_duedate = confirmation_due
        register_reminder(settings.RECEIVE_FINAL_CONFIRMATION,confirmation_due, thisevent)

    thisevent.fact_sheets_senddate = fact_sheets_send
    register_reminder(settings.SEND_FACT_SHEETS,fact_sheets_send, thisevent)
    if thisevent.fact_sheets_sentdate:
        thisevent.fact_sheets_duedate = fact_sheets_due
        register_reminder(settings.ALL_FACT_SHEETS_CONFIRMED,fact_sheets_due, thisevent)



def is_reminder_automation_capable(message):
    if (message == settings.RECEIVE_CONTRACT or 
        message == settings.SEND_DEPOSIT or
        message == settings.RECEIVE_DEPOSIT or
        message == settings.SEND_FINAL_PAYMENT or 
        message == settings.RECEIVE_FINAL_PAYMENT or
        message == settings.SEND_EXTRA_PAYMENT or 
        message == settings.RECEIVE_EXTRA_PAYMENT or
        message == settings.SEND_FINAL_CONFIRMATION or
        message == settings.RECEIVE_FINAL_CONFIRMATION or
        message == settings.SEND_MUSIC_LIST or 
        message == settings.RECEIVE_MUSIC_LIST or
        message == settings.HOLD_UNTIL or
        message == settings.HOLD_INDEFINITELY or 
        message == settings.SEND_CONTRACT or
        message == settings.RECEIPT_EXTRA_PAYMENT or
        message == settings.RECEIPT_FINAL_PAYMENT or
        message == settings.RECEIPT_DEPOSIT or
        message == settings.RECEIPT_CONTRACT or 
        message == settings.SEND_HOLD or 
        message == settings.ALL_FACT_SHEETS_CONFIRMED):
        return True
    else:
        return False


def register_reminder(message, date, event):
    
    #if exists and done (no matter date), leave alone
    #if exists and undone MODIFY (will update dates that way if necessary) --
    #    unless 'edited' (if was edited, leave alone and don't register new one -- don't want
    #    to erase edits, which would reset dates/automation
    #if it doesn't exist at all, create it.
     
    exists = Reminder.objects.filter(event_id = event.id, name = message).exists()
    if exists:
        oldrem = get_object_or_404(Reminder, event_id = event.id, name = message)
        if (not oldrem.done) and (not oldrem.edited):
#             newrem = Reminder(name = message)
#             if date < event.date_entered:
#                 newrem.date = event.date_entered
#             else:
#                 newrem.date = date
#             newrem.done = False
#             newrem.event_id = event.id
#             newrem.in_progress = oldrem.in_progress
#             newrem.send_1 = oldrem.send_1
#             newrem.send_2 = oldrem.send_2
#             newrem.send_3 = oldrem.send_3
#             newrem.giveup = oldrem.giveup
#             if is_reminder_automation_capable(message):
#                 newrem.auto = event.automation
#             newrem.save()
#             oldrem.delete()

            changed = False
            #print(event.date_entered)
            if date < event.date_entered:
                if oldrem.date != event.date_entered:
                    oldrem.date = event.date_entered
                    changed = True
            else:
                if oldrem.date != date:
                    oldrem.date = date
                    changed = True
            if is_reminder_automation_capable(message):
                if oldrem.auto != event.automation:
                    oldrem.auto = event.automation
                    changed = True
            if changed:
                oldrem.save()
                #print(message + ": exists and updated -- " + str(oldrem.id))
            else:
                #print(message + ": exists and not updated")
                nothing = 1
    else:
        newrem = Reminder(name = message)
        if date < event.date_entered:
            newrem.date = event.date_entered
        else:
            newrem.date = date
        newrem.done = False
        newrem.donedt = None
        newrem.event_id = event.id
        if is_reminder_automation_capable(message):
            newrem.auto = event.automation
        newrem.disb = event.reminderdisable
        if Reminder.objects.filter(event_id = event.id, name = message).count() > 1:
            #print("******almost created 2 same***** " + str(event.id))
            nothing = 1
        else:
            newrem.save()
        #print(message + ": made new reminder -- " + str(newrem.id))
        
  
def complete_reminder(message, event):
    #if not exist, don't complete obviously
    #also, if disabled don't mark done!
    exists = Reminder.objects.filter(event_id = event.id).filter(name = message).exists()
    if exists:
        thisreminder = get_object_or_404(Reminder, event_id = event.id, name = message)
        if not thisreminder.disb:
            thisreminder.done = True
            if not thisreminder.donedt:
                thisreminder.donedt = datetime.datetime.now()
            thisreminder.save()


def uncomplete_reminder(message, event):
    #if not exist, don't complete obviously
    #also, if disabled don't mark done!
    exists = Reminder.objects.filter(event_id = event.id).filter(name = message).exists()
    if exists:
        thisreminder = get_object_or_404(Reminder, event_id = event.id, name = message)
        if not thisreminder.disb:
            thisreminder.done = False
            thisreminder.donedt = None
            thisreminder.save()


def is_reminder_done(message, event):
    exists = Reminder.objects.filter(event_id = event.id).filter(name = message).exists()
    if exists:
        thisreminder = get_object_or_404(Reminder, event_id = event.id, name = message)
        return thisreminder.done
    else:
        return False

def disable_reminder(message, event, donestate): # only disables if original donestate is false
    exists = Reminder.objects.filter(event_id = event.id).filter(name = message).exists()
    if exists:
        if not donestate:
            thisreminder = get_object_or_404(Reminder, event_id = event.id, name = message)
            thisreminder.disb = True
            thisreminder.done = donestate
            thisreminder.donedt = None
            thisreminder.edited = True
            thisreminder.save()
#         else:
#             thisreminder.done = donestate
#             thisreminder.save()





def enable_reminder(message, event): #only enables if it was disabled
    exists = Reminder.objects.filter(event_id = event.id).filter(name = message).exists()
    if exists:
        thisreminder = get_object_or_404(Reminder, event_id = event.id, name = message)
        if thisreminder.disb:
            thisreminder.disb = False
            thisreminder.save()


def delete_undone_reminder(message, event):
    #delete reminder if it exists AND is undone
    exists = Reminder.objects.filter(event_id = event.id).filter(name = message, done = False).exists()
    if exists:
        get_object_or_404(Reminder, event_id = event.id, name = message).delete()

def delete_reminder(message, event):
    #delete reminder if it exists
    exists = Reminder.objects.filter(event_id = event.id).filter(name = message).exists()
    if exists:
        get_object_or_404(Reminder, event_id = event.id, name = message).delete()

            
            
    
    
def add_action( action, thisevent, actiondate ):
    #Check for exact duplicate (name/date) first, if exists of course don't add action
    if action != "Custom Music requests were accepted!":
        exists = Activity.objects.filter(event_id = thisevent.id).filter(name=action).filter(date=actiondate).exists()
        if not exists:
            newact = Activity(name = action)
            newact.date = date.today()
            newact.event_id = thisevent.id
            newact.save()    
    else:
        exists = Activity.objects.filter(event_id = thisevent.id).filter(name=action).exists()
        if not exists:
            newact = Activity(name = action)
            newact.date = date.today()
            newact.event_id = thisevent.id
            newact.save()    
        
        
def process_auto_reminders ( thisevent ):
    today = date.today()

##################################################################################################################
#    NEW -- we hijack this routine to also check/update if enough musicians have been asked or accepted playing
##################################################################################################################
    if not thisevent.ensemble_number:
        ensnumber = 0
    else:
        ensnumber = thisevent.ensemble_number
    invite_possible = False
    mark_sent_done = False
    mark_rcvd_done = False
    mark_sent_notdone = False
    mark_rcvd_notdone = False
    askable = MusicianEvent.objects.filter(event_id=thisevent.id, asked=False, placeholder=False).order_by('pk')
    playing = MusicianEvent.objects.filter(event_id=thisevent.id, yes=True, no=False, placeholder=False).order_by('pk')
    asked = MusicianEvent.objects.filter(event_id=thisevent.id, asked=True, yes=False, placeholder=False).order_by('pk')
    #thisevent = Event.objects.filter(id=event).get()
    if askable.count() > 0:
        invite_possible = True
        if playing.count() == ensnumber:
            invite_possible = False
    if (playing.count() == ensnumber) and ensnumber > 0:
        mark_rcvd_done = True
    else:
        mark_rcvd_notdone = True
    if not ensnumber:
        temp = 0
    else:
        temp = ensnumber
    if ((asked.count() + playing.count()) >= temp) and temp > 0:
        mark_sent_done = True
    else:
        mark_sent_notdone = True
            
    #now make the changes as possible
    #    invite_possible is not needed (it only was there for js buttons)
    #    mark_sent_notdone and mark_rcvd_notdone are overkill, not needed
    if mark_sent_done:
        thisevent.flag_musicians_sent = True
    else:
        thisevent.flag_musicians_sent = False
        thisevent.musicians_sentdate = None
    if mark_rcvd_done:
        thisevent.flag_musicians_rcvd = True
    else:
        thisevent.flag_musicians_rcvd = False
        thisevent.musicians_rcvddate = None
    
    



    #each below sets sentdate/rcvddate, etc, AND enter new 'actions', 1st done, like evRemindCheck
#     if thisevent.hold_released:
#         complete_reminder(settings.HOLD_UNTIL, thisevent)
#         complete_reminder(settings.HOLD_INDEFINITELY, thisevent)
#         complete_reminder(settings.SEND_HOLD, thisevent)
    if thisevent.accept_custom:
        complete_reminder(settings.CHECK_MUSIC_LIST, thisevent)
        #what do we do?  add an action without knowing if it was already added?
        #add routine to check for previous action recorded?  add model to save date?
        #answer: add_action routine checks for this one and only allows it once!
        add_action("Custom Music requests were accepted!", thisevent, today)
    
    if thisevent.flag_hold_sent:
        complete_reminder(settings.SEND_HOLD, thisevent)
        if not thisevent.hold_sentdate:
            thisevent.hold_sentdate = today
            add_action("Hold notice was sent!", thisevent, today)
    
    if thisevent.flag_contract_sent:
        complete_reminder(settings.SEND_CONTRACT, thisevent)
        if not thisevent.contract_sentdate:
            thisevent.contract_sentdate = today
            add_action("Contract was sent!", thisevent, today)

    if thisevent.flag_contract_rcvd:
        complete_reminder(settings.RECEIVE_CONTRACT, thisevent)
        if not thisevent.contract_rcvddate:
            thisevent.contract_rcvddate = today
            add_action("Contract was received!", thisevent, today)
    if thisevent.flag_contract_rcpt:
        complete_reminder(settings.RECEIPT_CONTRACT, thisevent)
        if not thisevent.contract_rcptdate:
            thisevent.contract_rcptdate = today
            add_action("Contract received receipt was sent!", thisevent, today)

    if thisevent.flag_deposit_sent:
        complete_reminder(settings.SEND_DEPOSIT, thisevent)
        if not thisevent.deposit_sentdate:
            thisevent.deposit_sentdate = today
            #if not really a deposit being sent, then it was a full pay
            if thisevent.deposit_fee == 0 or thisevent.deposit_fee == 0.00:
                add_action("Payment request was sent!", thisevent, today)
                thisevent.flag_final_payment_sent = True
                thisevent.final_senddate = today
                thisevent.final_sentdate = today
            else:
                add_action("Deposit request was sent!", thisevent, today)
        if thisevent.final_fee == 0 or thisevent.final_fee == 0.00:
            thisevent.flag_final_payment_sent = True
            thisevent.final_senddate = thisevent.deposit_senddate
            thisevent.final_rcvddate = thisevent.deposit_rcvddate
            thisevent.final_rcptdate = thisevent.deposit_rcptdate
    if thisevent.flag_deposit_rcvd:
        complete_reminder(settings.RECEIVE_DEPOSIT, thisevent)
        if not thisevent.deposit_rcvddate:
            thisevent.deposit_rcvddate = today
            add_action("Deposit was received!", thisevent, today)
        if thisevent.final_fee == 0 or thisevent.final_fee == 0.00:
            thisevent.flag_final_payment_rcvd = True
            thisevent.final_senddate = thisevent.deposit_senddate
            thisevent.final_rcvddate = thisevent.deposit_rcvddate
            thisevent.final_rcptdate = thisevent.deposit_rcptdate
    if thisevent.flag_deposit_rcpt:
        complete_reminder(settings.RECEIPT_DEPOSIT, thisevent)
        if not thisevent.deposit_rcptdate:
            thisevent.deposit_rcptdate = today
            add_action("Deposit received receipt was sent!", thisevent, today)
        if thisevent.final_fee == 0 or thisevent.final_fee == 0.00:
            thisevent.flag_final_payment_rcpt = True
            thisevent.final_senddate = thisevent.deposit_senddate
            thisevent.final_rcvddate = thisevent.deposit_rcvddate
            thisevent.final_rcptdate = thisevent.deposit_rcptdate

    if thisevent.flag_final_payment_sent:
        complete_reminder(settings.SEND_FINAL_PAYMENT, thisevent)
        if not thisevent.final_sentdate:
            thisevent.final_sentdate = today
            add_action("Final payment request was sent!", thisevent, today)
    if thisevent.flag_final_payment_rcvd:
        complete_reminder(settings.RECEIVE_FINAL_PAYMENT, thisevent)
        if not thisevent.final_rcvddate:
            thisevent.final_rcvddate = today
            add_action("Final payment was received!", thisevent, today)
    if thisevent.flag_final_payment_rcpt:
        complete_reminder(settings.RECEIPT_FINAL_PAYMENT, thisevent)
        if not thisevent.final_rcptdate:
            thisevent.final_rcptdate = today
            add_action("Final payment received receipt was sent!", thisevent, today)

    if thisevent.flag_extra_sent:
        complete_reminder(settings.SEND_EXTRA_PAYMENT, thisevent)
        if not thisevent.extra_sentdate:
            thisevent.extra_sentdate = today
            add_action("Extra payment request was sent!", thisevent, today)
    if thisevent.flag_extra_rcvd:
        complete_reminder(settings.RECEIVE_EXTRA_PAYMENT, thisevent)
        if not thisevent.extra_rcvddate:
            thisevent.extra_rcvddate = today
            add_action("Extra payment was received!", thisevent, today)
    if thisevent.flag_extra_rcpt:
        complete_reminder(settings.RECEIPT_EXTRA_PAYMENT, thisevent)
        if not thisevent.extra_rcptdate:
            thisevent.extra_rcptdate = today
            add_action("Extra payment received receipt was sent!", thisevent, today)
    
    if thisevent.flag_musicians_sent:
        complete_reminder(settings.INVITE_MUSICIANS, thisevent)
        if not thisevent.musicians_sentdate:
            thisevent.musicians_sentdate = today
            add_action("Enough musicians were asked to play...", thisevent, today)
    else:
        uncomplete_reminder(settings.INVITE_MUSICIANS, thisevent)
        thisevent.musicians_sentdate = None
        #also need to make sure all_musicians_booked was not registered -- unregister if so!
        delete_reminder(settings.ALL_MUSICIANS_BOOKED, thisevent)
        
    if thisevent.flag_musicians_rcvd:
        complete_reminder(settings.ALL_MUSICIANS_BOOKED, thisevent)
        if not thisevent.musicians_rcvddate:
            thisevent.musicians_rcvddate = today
            add_action("Musicians finished responding!", thisevent, today)
    else:
        uncomplete_reminder(settings.ALL_MUSICIANS_BOOKED, thisevent)
        thisevent.musicians_rcvddate = None

    if thisevent.flag_final_confirmation_sent:
        complete_reminder(settings.SEND_FINAL_CONFIRMATION, thisevent)
        if not thisevent.confirmation_sentdate:
            thisevent.confirmation_sentdate = today
            add_action("Final details confirmation was sent!", thisevent, today)
    if thisevent.flag_final_confirmation_rcvd:
        complete_reminder(settings.RECEIVE_FINAL_CONFIRMATION, thisevent)
        if not thisevent.confirmation_rcvddate:
            thisevent.confirmation_rcvddate = today
            add_action("Final details confirmation was received!", thisevent, today)

    if thisevent.flag_fact_sheets_sent:
        complete_reminder(settings.SEND_FACT_SHEETS, thisevent)
        if not thisevent.fact_sheets_sentdate:
            thisevent.fact_sheets_sentdate = today
            add_action("Fact sheets were sent!", thisevent, today)
    if thisevent.flag_fact_sheets_rcvd:
        complete_reminder(settings.ALL_FACT_SHEETS_CONFIRMED, thisevent)
        if not thisevent.fact_sheets_rcvddate:
            thisevent.fact_sheets_rcvddate = today
            add_action("[A] Fact sheets were confirmed by all!", thisevent, today)

    if thisevent.flag_music_list_sent:
        complete_reminder(settings.SEND_MUSIC_LIST, thisevent)
        if not thisevent.music_list_sentdate:
            thisevent.music_list_sentdate = today
            add_action("Music list request was sent!", thisevent, today)
    if thisevent.flag_music_list_rcvd:
        complete_reminder(settings.RECEIVE_MUSIC_LIST, thisevent)
        if not thisevent.music_list_rcvddate:
            thisevent.music_list_rcvddate = today
            add_action("Music list was received!", thisevent, today)

def checkremindersautostatus(request):
    if request.is_ajax():
        event_id = request.GET['event_id']
        reminders = Reminder.objects.filter(event_id = event_id).order_by('pk')
        sendhold = sendcontract = senddeposit = receiptdeposit = receiptcontract = False
        sendfinalpayment = receiptfinalpayment = sendfinalconfirmation = sendmusiclist = False
        sendextrapayment = receiptextrapayment = False

        for reminder in reminders:
            if reminder.name == settings.SEND_HOLD:
                sendhold = reminder.auto
                if reminder.disb:
                    sendholddisb = True
            if reminder.name == settings.SEND_CONTRACT:
                sendcontract = reminder.auto
            if reminder.name == settings.SEND_DEPOSIT:
                senddeposit = reminder.auto
            if reminder.name == settings.RECEIPT_DEPOSIT:
                receiptdeposit = reminder.auto
            if reminder.name == settings.RECEIPT_CONTRACT:
                receiptcontract = reminder.auto
            if reminder.name == settings.SEND_FINAL_PAYMENT:
                sendfinalpayment = reminder.auto
            if reminder.name == settings.RECEIPT_FINAL_PAYMENT:
                receiptfinalpayment = reminder.auto
            if reminder.name == settings.SEND_EXTRA_PAYMENT:
                sendextrapayment = reminder.auto
            if reminder.name == settings.RECEIPT_EXTRA_PAYMENT:
                receiptextrapayment = reminder.auto
            if reminder.name == settings.SEND_FINAL_CONFIRMATION:
                sendfinalconfirmation = reminder.auto
            if reminder.name == settings.SEND_MUSIC_LIST:
                sendmusiclist = reminder.auto
        
        data = {'sendhold':sendhold, 'sendcontract':sendcontract, 'senddeposit':senddeposit,
                'receiptdeposit':receiptdeposit, 'receiptcontract':receiptcontract,
                'sendfinalpayment':sendfinalpayment, 'receiptfinalpayment':receiptfinalpayment,
                'sendextrapayment':sendextrapayment, 'receiptextrapayment':receiptextrapayment,
                'sendfinalconfirmation':sendfinalconfirmation, 'sendmusiclist':sendmusiclist}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")



def disablebuiltin(request): #all good!
    if request.is_ajax():
        event_id = request.GET['event_id']
        mode = request.GET['mode']
        if mode == "start":
            reminders = Reminder.objects.filter(event_id = event_id).order_by('pk')
            for reminder in reminders:
                if not reminder.done and not reminder.edited:
                    reminder.disb = True
                    reminder.save()
        else:
            reminders = Reminder.objects.filter(event_id = event_id).order_by('pk')
            for reminder in reminders:
                if not reminder.done and not reminder.edited:
                    reminder.disb = False
                    reminder.save()
        
        data = {'error':False}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
    
def mark_reminder_auto(event, name, auto):
    exists = Reminder.objects.filter(event_id = event.id).filter(name = name).exists()
    if exists:
        thisreminder = get_object_or_404(Reminder, event_id = event.id, name = name)
        thisreminder.auto = auto
        thisreminder.edited = True
        thisreminder.save()
        
    

def switchautomation(request):
    if request.is_ajax():
        event_id = request.GET['event_id']
        mode = request.GET['mode']
        if mode == "start":
            auto = True
        else:
            auto = False
        #get each reminder for event (that needs automation), and
        #mark them for either auto on or off
        reminders = Reminder.objects.filter(event_id = event_id).order_by('pk')
        for reminder in reminders:
            if (reminder.name == settings.RECEIVE_CONTRACT or 
                reminder.name == settings.SEND_DEPOSIT or
                reminder.name == settings.RECEIVE_DEPOSIT or
                reminder.name == settings.SEND_FINAL_PAYMENT or 
                reminder.name == settings.RECEIVE_FINAL_PAYMENT or
                reminder.name == settings.SEND_EXTRA_PAYMENT or 
                reminder.name == settings.RECEIVE_EXTRA_PAYMENT or
                reminder.name == settings.SEND_FINAL_CONFIRMATION or
                reminder.name == settings.RECEIVE_FINAL_CONFIRMATION or
                reminder.name == settings.SEND_MUSIC_LIST or 
                reminder.name == settings.RECEIVE_MUSIC_LIST or
                reminder.name == settings.HOLD_UNTIL or
                reminder.name == settings.HOLD_INDEFINITELY or 
                reminder.name == settings.SEND_CONTRACT or
                reminder.name == settings.RECEIPT_EXTRA_PAYMENT or
                reminder.name == settings.RECEIPT_FINAL_PAYMENT or
                reminder.name == settings.RECEIPT_DEPOSIT or
                reminder.name == settings.RECEIPT_CONTRACT or 
                reminder.name == settings.SEND_HOLD or 
                reminder.name == settings.ALL_FACT_SHEETS_CONFIRMED):
                
                reminder.auto = auto
                reminder.save()
        
        data = {'error':False}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
    


def process_update_flags( thisevent ):
    #update flags
#     thisevent.friendly_name = "testgcl"
    
    thisevent.color_contract = settings.FLAG_EMPTY
    thisevent.color_deposit = settings.FLAG_EMPTY
    thisevent.color_music_list = settings.FLAG_EMPTY
    thisevent.color_musicians = settings.FLAG_EMPTY
    thisevent.color_final_payment = settings.FLAG_EMPTY
    thisevent.color_final_confirmation = settings.FLAG_EMPTY
    thisevent.color_fact_sheets = settings.FLAG_EMPTY
    thisevent.color_extra_payment = settings.FLAG_EMPTY
    
    if thisevent.type == "HD":  
        thisevent.color_contract = settings.FLAG_HOLD
        if thisevent.is_hold_past_due:
            thisevent.color_contract = settings.FLAG_LATE
        

    if thisevent.waive_contract:
        thisevent.color_contract = settings.FLAG_WHITE
    else:
        if thisevent.flag_contract_sent:
            thisevent.color_contract = settings.FLAG_STARTED
        if thisevent.flag_contract_rcvd:
            thisevent.color_contract = settings.FLAG_DONE
        if thisevent.is_contract_past_due:
            thisevent.color_contract = settings.FLAG_LATE
    
    if thisevent.type == "HD":  
        thisevent.color_contract = settings.FLAG_HOLD
        if thisevent.is_hold_past_due:
            thisevent.color_contract = settings.FLAG_LATE
    
            
    if thisevent.waive_payment or (thisevent.deposit_senddate and (thisevent.deposit_senddate == thisevent.final_senddate)) or (thisevent.deposit_fee == 0) or (thisevent.deposit_fee == 0.00):
        thisevent.color_deposit = settings.FLAG_WHITE
    else:
        if thisevent.flag_deposit_sent:
            thisevent.color_deposit = settings.FLAG_STARTED
        if thisevent.flag_deposit_rcvd:
            thisevent.color_deposit = settings.FLAG_DONE
        if thisevent.is_deposit_past_due:
            thisevent.color_deposit = settings.FLAG_LATE
            
    if thisevent.waive_music_list:
        thisevent.color_music_list = settings.FLAG_WHITE
    else:
        if thisevent.flag_music_list_sent:
            thisevent.color_music_list = settings.FLAG_STARTED
        if thisevent.flag_music_list_rcvd:
            thisevent.color_music_list = settings.FLAG_DONE
        if thisevent.is_music_list_past_due:
            thisevent.color_music_list = settings.FLAG_LATE

    if thisevent.flag_musicians_sent:
        thisevent.color_musicians = settings.FLAG_STARTED
    if thisevent.flag_musicians_rcvd:
        thisevent.color_musicians = settings.FLAG_DONE
    if thisevent.is_musicians_past_due:
        thisevent.color_musicians = settings.FLAG_LATE

    if thisevent.waive_payment:
        thisevent.color_final_payment = settings.FLAG_WHITE
    else:
        if thisevent.flag_final_payment_sent:
            thisevent.color_final_payment = settings.FLAG_STARTED
        if thisevent.flag_final_payment_rcvd:
            thisevent.color_final_payment = settings.FLAG_DONE
        if thisevent.is_final_pay_past_due:
            thisevent.color_final_payment = settings.FLAG_LATE

    if thisevent.waive_payment:
        thisevent.color_extra_payment = settings.FLAG_WHITE
    else:
        if thisevent.flag_extra_sent:
            thisevent.color_extra_payment = settings.FLAG_STARTED
        if thisevent.flag_extra_rcvd:
            thisevent.color_extra_payment = settings.FLAG_DONE
        if thisevent.is_extra_pay_past_due:
            thisevent.color_extra_payment = settings.FLAG_LATE



    if thisevent.flag_final_confirmation_sent:
        thisevent.color_final_confirmation = settings.FLAG_STARTED
    if thisevent.flag_final_confirmation_rcvd:
        thisevent.color_final_confirmation = settings.FLAG_DONE
    if thisevent.is_final_confirmation_past_due:
        thisevent.color_final_confirmation = settings.FLAG_LATE

    if thisevent.flag_fact_sheets_sent:
        thisevent.color_fact_sheets = settings.FLAG_STARTED
    if thisevent.flag_fact_sheets_rcvd:
        thisevent.color_fact_sheets = settings.FLAG_DONE
    if thisevent.is_fact_sheets_past_due:
        thisevent.color_fact_sheets = settings.FLAG_LATE





def process_new_entries( form, newevent ):  
    #if contact, dayofcontact, and location are selected from existing db choices, erase any temp fields
    if form.cleaned_data['contact'] != None:
        newevent.contact_name = ''
        newevent.contact_agency = ''
        newevent.contact_email = ''
        newevent.contact_phone = ''
        newevent.contact_add = False    
    if form.cleaned_data['dayofcontact'] != None:
        newevent.dayofcontact_name = ''
        newevent.dayofcontact_email = ''
        newevent.dayofcontact_phone = ''
        newevent.dayofcontact_add = False    
    if form.cleaned_data['location'] != None:
        newevent.location_name = ''
        newevent.location_email = ''
        newevent.location_phone = ''
        newevent.location_link = ''
        newevent.location_address = ''
        newevent.location_add = False             
    #if new contact type, save if requested 
    if form.cleaned_data['contact'] == None and \
    form.cleaned_data['contact_name'] != None and form.cleaned_data['contact_add']:
#                 messages.info(request, 'Condition met')
        new_contact = Contact(name = form.cleaned_data['contact_name'])
        new_contact.agency = form.cleaned_data['contact_agency']
        new_contact.email = form.cleaned_data['contact_email']
        new_contact.phone = form.cleaned_data['contact_phone']
        new_contact.friendlyname = form.cleaned_data['friendly_name']
        new_contact.save()
        newevent.contact = new_contact
        newevent.contact_name = ''
        newevent.contact_agency = ''
        newevent.contact_email = ''
        newevent.contact_phone = ''
        newevent.contact_add = False    
    #if new dayofcontact type, save if requested    
    if form.cleaned_data['dayofcontact'] == None and \
    form.cleaned_data['dayofcontact_name'] != None and form.cleaned_data['dayofcontact_add']:
        new_dayofcontact = DayofContact(name = form.cleaned_data['dayofcontact_name'])
        new_dayofcontact.email = form.cleaned_data['dayofcontact_email']
        new_dayofcontact.phone = form.cleaned_data['dayofcontact_phone']
        new_dayofcontact.save()
        newevent.dayofcontact = new_dayofcontact
        newevent.dayofcontact_name = ''
        newevent.dayofcontact_email = ''
        newevent.dayofcontact_phone = ''
        newevent.dayofcontact_add = False    
    #if new location type, save if requested 
    if form.cleaned_data['location'] == None and \
    form.cleaned_data['location_name'] != None and form.cleaned_data['location_add']:
        new_location = Venue(name = form.cleaned_data['location_name'])
        new_location.email = form.cleaned_data['location_email']
        new_location.phone = form.cleaned_data['location_phone']
        new_location.link = form.cleaned_data['location_link']
        new_location.address = form.cleaned_data['location_address']
        new_location.save()
        newevent.location = new_location
        newevent.location_name = ''
        newevent.location_email = ''
        newevent.location_phone = ''
        newevent.location_link = ''
        newevent.location_address = ''
        newevent.location_add = False    

    