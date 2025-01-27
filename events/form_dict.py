from decimal import Decimal, ROUND_DOWN
from .models import Contact, DayofContact, Venue, MusicianEvent, Global
from django.shortcuts import get_object_or_404
from django.utils.html import format_html
from dateutil.relativedelta import relativedelta
from django.conf import settings
from datetime import date, datetime, time, timedelta
from django.template.loader import render_to_string, get_template
from .models import ESig







def conv_dt_short(value):
    if value:
        return value.strftime("%m/%d/%y")
    else:
        return value
    
def suffix(day):
    day = int(day)
    if 4 <= day <= 20 or 24 <= day <= 30:
        return "th"
    else:
        return ["st", "nd", "rd"][day % 10 - 1] 
               
def make_dict(event):
    
    #other processing first
    #TODO: music requests list, musician list
    
    
    
    
    
    
    if event.contact:
        contact = get_object_or_404(Contact, name=event.contact)
        contact_name = contact.name
        contact_agency = contact.agency
        contact_phone = contact.phone
        contact_email = contact.email
    else:
        contact_name = event.contact_name
        contact_agency = event.contact_agency
        contact_phone = event.contact_phone
        contact_email = event.contact_email
    contact_details = event.contact_details
    if not contact_phone:
        contact_phone = ""
    if contact_details:
        gcal_contact_details = "(" + contact_details + ")"
    else:
        gcal_contact_details = ''
        
    if event.dayofcontact:
        dayofcontact = get_object_or_404(DayofContact, name=event.dayofcontact)
        dayofcontact_name = dayofcontact.name
        dayofcontact_phone = dayofcontact.phone
        dayofcontact_email = dayofcontact.email
    else:
        dayofcontact_name = event.dayofcontact_name
        dayofcontact_phone = event.dayofcontact_phone
        dayofcontact_email = event.dayofcontact_email
    dayofcontact_details = event.dayofcontact_details
    if not dayofcontact_phone:
        dayofcontact_phone = ""
    if dayofcontact_details:
        gcal_dayofcontact_details = "(" + dayofcontact_details + ")"
    else:
        gcal_dayofcontact_details = ''
    
    if event.location:
        location = get_object_or_404(Venue, name=event.location)
        location_name = location.name
        location_link = location.link
        location_address = location.address
        location_phone = location.phone
        location_email = location.email
    else:
        location_name = event.location_name
        location_link = event.location_link
        location_address = event.location_address
        location_phone = event.location_phone
        location_email = event.location_email
    location_details = event.location_details
    if not location_details:
        gcal_location_details = ""
    else:
        gcal_location_details = "(" + location_details + ")"
    if event.location_outdoors:
        location_outdoors = "Outdoors"
    else:
        location_outdoors = "Indoors"
    if not location_address:
        location_address = "Address TBD"

    if event.ceremony_time:
        if_ceremony_time = '(ceremony starting at ' + event.ceremony_time.strftime("X%I:%M").replace('X0','X').replace('X','') + ')'
        fact_ceremony_time = '' + event.ceremony_time.strftime("X%I:%M").replace('X0','X').replace('X','') + ''
    else:
        if_ceremony_time = ''
        fact_ceremony_time = ''
    if event.location_details:
        if_location_details = ', ' + location_details + ''
    else:
        if_location_details = ''
    if event.location_outdoors:
        indoor_outdoor = "outdoors"
    else:
        indoor_outdoor = "indoors"
    
    if location_name:
        if location_link:
            #location_name_link = format_html('<a href="' + location_link + '">' + location_name + '</a>')
            location_name_link = location_name
        else:
            location_name_link = location_name
    else:
        location_name_link = "Location TBD"
    
     
    event_link = format_html('<a href="' + settings.WEBSITE + str(event.id) + '/edit">' + event.name + '</a>')
    
    contract_file_name = "Contract-for-" + event.date.strftime("%m-%d-%y") + "-(id" + str(event.id) + ")" + ".pdf" 
    contract_link1 = settings.FTP_URL + contract_file_name
    contract_link = '<a href="' + contract_link1 + '" target="_blank" rel="noopener">Contract for ' + event.name + ' ' + ' on ' + event.date.strftime("%m-%d-%Y") + '</a>'


#     contract1 = "https://www.sejda.com/sign-pdf?files="
#     contract2 = '%5B%7B%22downloadUrl%22%3A%22http%3A%2F%2Fwww.vanderbiltstrings.com%2Fpdfs%2F'
#     contract3 = 'contract-for-' + event.date.strftime("%m-%d-%y") + '-(id' + str(event.id) + ').pdf'
#     contract4 = '%22%7D%5D&returnEmail=gclhome%40yahoo.com'
#     contract_link = contract1 + contract2 + contract3 + contract4
#     contract_pdf_link = '<a href="' + contractlink + '">this link</a>'
# 
#     invoice1 = "https://www.sejda.com/sign-pdf?files="
#     invoice2 = '%5B%7B%22downloadUrl%22%3A%22http%3A%2F%2Fwww.vanderbiltstrings.com%2Fpdfs%2F'
#     invoice3 = 'invoice-for-' + event.date.strftime("%m-%d-%y") + '-(id' + str(event.id) + ').pdf'
#     invoice4 = '%22%7D%5D&returnEmail=gclhome%40yahoo.com'
#     invoicelink = invoice1 + invoice2 + invoice3 + invoice4
#     invoice_pdf_link = '<a href="' + invoicelink + '">this link</a>'
    
    #if not waive_payment and not final fee received (actually, if no finalpay REQUEST sent, include this sentence 
#     if (not event.waive_payment) and (not event.flag_final_payment_sent):
#         if event.final_duedate:
#             final_payment_reminder_date = event.final_duedate.strftime("%m/%d/%y")
#         else:
#             final_payment_reminder_date = 'N/A'
#         final_payment_reminder = '<u>Final payment</u>:  $' + str(event.final_fee) + ' is due by ' + final_payment_reminder_date + '.  Please send a check (payable to Janie Spangler) to my address (93 3rd St., Bonita Springs, FL  34134), or use the button below to pay online via PayPal (a small fee for this service is automatically included)<br />'
#         final_payment_reminder += '<b>Pay Final Amount:&nbsp;&nbsp;</b><a href="http://paypal.me/vanderbiltstrings/' + str(event.paypal_final_fee) + '"><img style="position:relative;top:7px" src="https://www.paypalobjects.com/digitalassets/c/website/marketing/apac/C2/logos-buttons/optimize/26_Grey_PayPal_Pill_Button.png" alt="Pay now with PayPal"></img></a>'
#         final_payment_reminder += '<br /><br />'
#     else:
#         final_payment_reminder = '' 
    
    #if music choices not done yet (and not waived), include this reminder sentence
#     if (not event.flag_music_list_rcvd) and (not event.waive_music_list):
#         music_choices_reminder = '<u>Music selections due</u>:  You can either complete our form at <a href="http://requests.vanderbiltstrings.com">http://requests.vanderbiltstrings.com</a> or give us an idea of your tastes and we would be happy to choose selections for you!<br/><br />'
#     else:
#         music_choices_reminder = ''
    
    #if day-of info isn't done yet, include this reminder sentence (needs name/phone)
#     if dayofcontact_phone and dayofcontact_name:
#         dayofcontact_reminder = ''
#     else:
#         dayofcontact_reminder = '<u>On-site contact</u>:  We will need to be in touch with the venue contact or wedding planner before the event date, please send me their email and/or phone number.<br/><br />'
    
    #if there was no reminder for dayofcontact, include this sentence
#     if dayofcontact_reminder == '':
#         ifnot_dayofcontact_reminder = "In case any changes come up on the day of the event,"
#         ifnot_dayofcontact_reminder += " we'll be in touch with " + dayofcontact_name + " at " + str(dayofcontact_phone) + "."
#     else:
#         ifnot_dayofcontact_reminder = ""
    
    #if officiant info is not entered yet, include this sentences
#     if event.officiant_info:
#         officiant_reminder = ''
#     else:
#         officiant_reminder = "<u>Officiant's email or phone number</u>:  I will need to contact him or her to go over the ceremony details, so please email me with their info.<br /><br />"
    
    if event.hold_until:
        hold_until_sentence = '  If we do not hear from you by ' + event.hold_until.strftime("%m/%d/%y") + " we'll assume you no longer need our services and will cancel the hold.  "
        hold_until = event.hold_until.strftime("%m/%d/%y")
    else:
        hold_until_sentence = ""
        datetohold = event.date - relativedelta(days=5)
        hold_until = datetohold.strftime("%m/%d/%y")
    
    if event.type == 'HD':
        maintype = 'Hold Booking'
        if_hold = 'HOLD: '
        if event.hold_until:
            if_hold_until = '<b>until ' + event.hold_until.strftime("%m/%d/%y") + '</b><br />'
        else:
            if_hold_until = ''
    elif event.type == 'AB':
        maintype = 'Agency Booking'
        if_hold = ''
        if_hold_until = ''
    else:
        maintype = "Regular Booking"
        if_hold = ''
        if_hold_until = ''
    
    if event.waive_contract:
        waive_contract = 'contract waived'
    else:
        waive_contract = 'contract not waived'
    if event.waive_payment:
        waive_payment = 'payment waived'
    else:
        waive_payment = 'payment not waived'
    
    if not event.fee:
        fee = 0
    else:
        #fee = Decimal(str(event.fee)).quantize(Decimal('.01'), rounding=ROUND_DOWN),
        fee = event.fee
    paypal_full_fee, deposit_fee, contracting_fee, paypal_deposit_fee, final_fee, paypal_final_fee, musician_fee = 0, 0, 0, 0, 0, 0, 0
    if event.paypal_full_fee:
        paypal_full_fee = event.paypal_full_fee
    if event.deposit_fee:
        deposit_fee = event.deposit_fee
    if event.paypal_deposit_fee:
        paypal_deposit_fee = event.paypal_deposit_fee
    if event.contracting_fee:
        contracting_fee = event.contracting_fee
    if event.final_fee:
        final_fee = event.final_fee
    if event.paypal_final_fee:
        paypal_final_fee = event.paypal_final_fee
    if event.musician_fee:
        musician_fee = event.musician_fee
    if event.deposit_fee == 0 or event.deposit_fee == 0.00 or (event.deposit_senddate and (event.deposit_senddate == event.final_senddate)):
        full_or_final = 'full'
        deposit_or_final_fee = event.fee
    else:
        full_or_final = 'final'
        deposit_or_final_fee = event.deposit_fee    
    
    if event.waive_payment:
        gcal_payment = "[Payment Waived]"
    else:
        if event.flag_final_payment_rcvd:
            gcal_payment = "[final payment received]"
        elif event.flag_deposit_rcvd:
            gcal_payment = "[deposit payment received]"
        else:
            gcal_payment = "[payment not received yet]"
    if event.waive_contract:
        gcal_contract = "[Contract Waived]"
    else:
        if event.flag_contract_rcvd:
            gcal_contract = "[contract signed]"
        else:
            gcal_contract = "[contract not signed yet]"

#     {{extra_fee}}
#     {{extra_fee_paypal}}
#     {{extra_rcvddate}}
#     {{extra_duedate}}
    extra_fee, extra_fee_paypal = 0, 0
    
    if event.extra_fee:
        extra_fee = event.extra_fee
    if event.paypal_extra_fee:
        extra_fee_paypal = event.paypal_extra_fee
    
    if event.number_parents:
        num_parents = '<br />' + str(event.number_parents) + ' parents walking'
    else:
        num_parents = ''
    if event.number_bridesmaids:
        num_bridesmaids = '<br />' + str(event.number_bridesmaids) + ' bridesmaids walking'
    else:
        num_bridesmaids = ''
    if event.flowergirls:
        flowergirls = '<br />flowergirl(s) will be processing also'
    else:
        flowergirls = ''



#     yes_btn_code = '<table style="border:none;display:inline;">' + \
#                     '<tr><td><b>I will play: &nbsp;</b></td><td>' + \
#                     '<a href="' + settings.WEBSITE + 'inquiry/yes/' + \
#                     str(event.id) + '/' + '(*email_address*)' + '/(*musician_first_name*)' + \
#                     '"><img style="width:64px;" ' + \
#                     'src="' + settings.WEBSITE_EXTRAS + 'button_yes.png" ' + \
#                     'alt="Accept"></img></a></td></tr></table>'
    yes_btn_code = '<a rel="nofollow" href="' + settings.WEBSITE + 'inquiry/yes/' + \
                    str(event.id) + '/' + '(*email_address*)' + '/(*musician_first_name*)' + \
                    '"><img style="width:64px;" ' + \
                    'src="' + settings.WEBSITE_EXTRAS + 'button_yes.png" ' + \
                    'alt="Accept"></img></a>'
    yes_btn_text = settings.WEBSITE + 'inquiry/yes/' + \
                    str(event.id) + '/' + '(*email_address*)' + '/(*musician_first_name*)'
                    
#     no_btn_code = '<table style="border:none;display:inline;">' + \
#                     '<tr><td><b>I am not available: &nbsp;</b></td><td>' + \
#                     '<a href="' + settings.WEBSITE + 'inquiry/no/' + \
#                     str(event.id) + '/' + '(*email_address*)' + '/(*musician_first_name*)' + \
#                     '"><img style="margin-bottom:-14px !important;width:64px;" ' + \
#                     'src="' + settings.WEBSITE_EXTRAS + 'button_no.png" ' + \
#                     'alt="Decline"></img></a></td></tr></table>'
    no_btn_code = '<a rel="nofollow" href="' + settings.WEBSITE + 'inquiry/no/' + \
                    str(event.id) + '/' + '(*email_address*)' + '/(*musician_first_name*)' + \
                    '"><img style="width:64px;" ' + \
                    'src="' + settings.WEBSITE_EXTRAS + 'button_no.png" ' + \
                    'alt="Decline"></img></a>'
    no_btn_text = settings.WEBSITE + 'inquiry/no/' + \
                    str(event.id) + '/' + '(*email_address*)' + '/(*musician_first_name*)'

    
#     gotit_btn_code = '<table style="border:none;display:inline;">' + \
#                     '<tr><td><b>I am all set: &nbsp;</b></td><td>' + \
#                     '<a href="' + settings.WEBSITE + 'inquiry/gotit/' + \
#                     str(event.id) + '/' + '(*email_address*)'+ '/(*musician_first_name*)' + \
#                     '"><img style="margin-bottom:-14px !important;width:64px;" ' + \
#                     'src="' + settings.WEBSITE_EXTRAS + 'button_gotit.png" ' + \
#                     'alt="Got It"></img></a></td></tr></table>'
    gotit_btn_code = '<a rel="nofollow" href="' + settings.WEBSITE + 'inquiry/gotit/' + \
                    str(event.id) + '/' + '(*email_address*)'+ '/(*musician_first_name*)' + \
                    '"><img style="margin-bottom:-14px !important;width:64px;" ' + \
                    'src="' + settings.WEBSITE_EXTRAS + 'button_gotit.png" ' + \
                    'alt="Got It"></img></a>'
    gotit_btn_text = settings.WEBSITE + 'inquiry/gotit/' + \
                    str(event.id) + '/' + '(*email_address*)' + '/(*musician_first_name*)'
                    
                    
                    
    confirm_btn_code = '<a rel="nofollow" href="' + settings.WEBSITE + 'details/confirmed/' + \
                    str(event.id) + \
                    '"><img style="margin-bottom:-14px !important;width:120px;" ' + \
                    'src="' + settings.WEBSITE_EXTRAS + 'button_confirm.png" ' + \
                    'alt="Confirm"></img></a>'
    confirm_btn_text = settings.WEBSITE + 'details/confirmed/' + \
                    str(event.id)
                
    
    
    
                    
    
    if event.start_time:
        gcal_start_time = event.start_time
        arrival_time = (datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=15)).time()
        arrival_time_lead = '15'
        if event.location:
            if "Ritz" in event.location.name:
                arrival_time = (datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=30)).time()
                arrival_time_lead = '30'
        else:
            if "Ritz" in event.location_name:
                arrival_time = (datetime.combine(date(1, 1, 1), event.start_time) - timedelta(minutes=30)).time()
                arrival_time_lead = '30'
    else:
        gcal_start_time = 'Start TBD'
        arrival_time = "TBD"
        arrival_time_lead = '15'
    if event.end_time:
        gcal_end_time = event.end_time
    else:
        gcal_end_time = 'End TBD'
        
    
    if event.recessional_cue:
        gcal_recessional_cue = "Recessional Cue: " + event.recessional_cue
    else:
        gcal_recessional_cue = ''
    if event.officiant_info:
        gcal_officiant_info = "Officiant Info: " + event.officiant_info
        officiant_info_exists = "Officiant's Info:"
    else:
        gcal_officiant_info = ''
        officiant_info_exists = ""
    if event.automation:
        gcal_automation = "AUTOMATION IS ON"
    else:
        gcal_automation = "AUTOMATION IS OFF"
    
    f = []
    f.append("test")
    if event.type == "HD":
        f.append("[<a href='#'><font color='" + event.color_contract + "'>hold</font></a>]")
    else:
        f.append("[<a href='#'><font color='" + event.color_contract + "'>contract</font></a>]")
    f.append("[<a href='#'><font color='" + event.color_deposit + "'>deposit</font></a>]")
    f.append("[<a href='#'><font color='" + event.color_music_list + "'>music list</font></a>]")
    f.append("[<a href='#'><font color='" + event.color_musicians + "'>musicians</font></a>]")
    f.append("[<a href='#'><font color='" + event.color_final_payment + "'>final pay</font></a>]")
    f.append("[<a href='#'><font color='" + event.color_final_confirmation + "'>confirm</font></a>]")
    f.append("[<a href='#'><font color='" + event.color_fact_sheets + "'>fact sheets</font></a>]")
    
    #print(f)
    if event.waive_contract:
        f[1] = "[<strike><a href='#'><font color='" + event.color_contract + "'>contract</font></a></strike>]"
    if event.waive_payment or (event.deposit_fee and (event.deposit_senddate == event.final_senddate)) or event.deposit_fee == 0:
        f[2] = "[<strike><a href='#'><font color='" + event.color_deposit + "'>deposit</font></a></strike>]"
    if event.waive_music_list:
        f[3] = "[<strike><a href='#'><font color='" + event.color_music_list + "'>music list</font></a></strike>]"
    if event.waive_payment:
        f[5] = "[<strike><a href='#'><font color='" + event.color_final_payment + "'>final pay</font></a></strike>]"
    
    e = []
    for thistxt in f:
        thistxt = thistxt.replace("#eeeeee", "#a8a8a8")
        thistxt = thistxt.replace("#fff176", "#e5d86a")
        thistxt = thistxt.replace("#ffffff", "#d4d4d4")
        e.append(thistxt)
    #print(e)
    
    
#     signature = render_to_string('events/signature.html')
#     signature = signature.replace('signature_pic', settings.WEBSITE_EXTRAS + 'signature.jpg')
#     signature = signature.replace('profile_pic', settings.WEBSITE_EXTRAS + 'profilepic.jpg')
#     signature = signature.replace('facebook_pic', settings.WEBSITE_EXTRAS + 'facebook.jpg')
#     signature = signature.replace('instagram_pic', settings.WEBSITE_EXTRAS + 'instagram.jpg')
#     signature = format_html(signature)
    exists = ESig.objects.filter(default=True).exists()
    if exists:
        defaultsig = get_object_or_404(ESig, default=True)
        signature = format_html(defaultsig.sig)
    else:
        signature=""
    exists_alt = ESig.objects.filter(default_alt=True).exists()
    if exists_alt:
        defaultsig = get_object_or_404(ESig, default_alt=True)
        signature_alt = format_html(defaultsig.sig)
    else:
        signature_alt=""
    



    #FIGURE OUT FUTURE DUE DATES
    created = event.date_entered
    if event.hold_released:
        created = event.hold_released
    daystoevent = abs( event.date - created ).days
    
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
        
    if event.contract_duedate:
        calc_future_contract_duedate = event.contract_duedate
    else:
        calc_future_contract_duedate = date.today() + relativedelta(days=settings.DAYS_CONTRACT_DUE[split])

    if event.deposit_duedate:
        calc_future_deposit_duedate = event.deposit_duedate
    else:
        calc_future_deposit_duedate = date.today() + relativedelta(days=settings.DAYS_DEPOSIT_DUE[split])

    if event.final_duedate:
        calc_future_final_duedate = event.final_duedate
    else:
        if daystoevent < 29:
            calc_future_final_duedate = date.today() + relativedelta(days=settings.DAYS_FINAL_DUE[split])
        else:
            calc_future_final_duedate = event.date - relativedelta(days=settings.DAYS_FINAL_DUE[split])

    if event.extra_duedate:
        calc_future_extra_duedate = event.extra_duedate
    else:
        calc_future_extra_duedate = date.today() + relativedelta(days=settings.DAYS_EXTRA_DUE[split])


    if event.confirmation_duedate:
        calc_future_confirmation_duedate = event.confirmation_duedate
    else:
        if daystoevent < 15:
            calc_future_confirmation_duedate = date.today() + relativedelta(days=settings.DAYS_CONFIRMATION_DUE[split])
        else:
            calc_future_confirmation_duedate = event.date - relativedelta(days=settings.DAYS_CONFIRMATION_DUE[split])

    if event.music_list_duedate:
        calc_future_music_list_duedate = event.music_list_duedate
    else:
        calc_future_music_list_duedate = event.date - relativedelta(days=settings.DAYS_MUSIC_LIST_DUE[split])
    
    



    if event.ceremony_time:
        confirm_ceremony_time = '&bull;&nbsp;<b>Ceremony Time:</b> &nbsp;' + event.ceremony_time.strftime("%I:%M %p") + '<br /><br />'
    else:
        confirm_ceremony_time = ''
    if event.location:
        confirm_location = '&bull;&nbsp;<b>Location:</b> &nbsp;' + event.location.name + ', ' + event.location.address + ', ' + event.location_details + '<br />'
    else:
        confirm_location = '&bull;&nbsp;<b>Location:</b> &nbsp;' + event.location_name + ', ' + event.location_address + ', ' + event.location_details + '<br />'
    if event.dayofcontact:
        doc_name = event.dayofcontact.name
        doc_phone = event.dayofcontact.phone
        doc_email = event.dayofcontact.email
    else:
        doc_name = event.dayofcontact_name
        doc_phone = event.dayofcontact_phone
        doc_email = event.dayofcontact_email
    if doc_name:
        confirm_doc = '&bull;&nbsp;<b>Day-of Contact/Planner:</b> &nbsp;' + doc_name + ', ' + str(doc_phone) + ', ' + doc_email + '<br /><br />'
    else:
        confirm_doc = ''
 
 
 
 
        

    #     temp_music_list = event.music_list
    temp_music_list = event.music_list.partition("--Below was previously listed:--")
    music_list = temp_music_list[0]
    music_list = music_list + num_parents
    music_list = music_list + num_bridesmaids
    music_list = music_list + flowergirls




    
#         confirm_list = '&bull;&nbsp;<b>Event Date:</b> &nbsp;' + event.date.strftime("%m/%d/%y") + '<br /><br />' + \
#                     '&bull;&nbsp;<b>Contracted Time:</b> &nbsp;' + gcal_start_time.strftime("%I:%M %p") + ' - ' + gcal_end_time.strftime("%I:%M %p") + '<br /><br />' + \
#                     '&bull;&nbsp;<b>Musician Set Time:</b> &nbsp;' + arrival_time.strftime("%I:%M %p") + '<br /><br />' + \
#                     confirm_ceremony_time + \
#                     '&bull;&nbsp;<b>Ensemble:</b> &nbsp;' + event.ensemble_name + ' (' + str(event.ensemble_number) + ' musicians)<br /><br />' + \
#                     '&bull;&nbsp;<b>Event Type:</b> &nbsp;' + event.event_type_name + '<br /><br />' + \
#                     confirm_location + \
#                     confirm_doc + \
#                     '&bull;&nbsp;<b>Chairs Needed: </b><u>' + str(event.ensemble_number) + '</u> armless chairs for the musicians.  Let your planner or venue know.<br /><br />' + \
#                     '&bull;&nbsp;<b>Music List: </b>' + '<p style="margin-top:-12px;margin-left:30px;">' + music_list + '</p>'


    if event.ensemble_number and event.start_time and event.end_time:
        confirm_list = '&bull;&nbsp;<b>Event Date:</b> &nbsp;' + event.date.strftime("%m/%d/%y") + '<br /><br />' + \
                    '&bull;&nbsp;<b>Contracted Time:</b> &nbsp;' + gcal_start_time.strftime("%I:%M %p") + ' - ' + gcal_end_time.strftime("%I:%M %p") + '<br /><br />' + \
                    '&bull;&nbsp;<b>Ensemble:</b> &nbsp;' + event.ensemble_name + '<br /><br />' + \
                    '&bull;&nbsp;<b>Event Type:</b> &nbsp;' + event.event_type_name + '<br /><br />' + \
                    confirm_location + ''
    else:
        confirm_list = ''                
    
    
    
    

    client_home = '<a href="https://events.vanderbiltstrings.com/events/client_home/' + str(event.id) + '/" target="_blank" rel="noopener">Client Home</a>'
    client_portal = '<a href="https://events.vanderbiltstrings.com/events/client_home/' + str(event.id) + '/" target="_blank" rel="noopener">Client Home</a>'
    client_portal_click_here = '<a href="https://events.vanderbiltstrings.com/events/client_home/' + str(event.id) + '/" target="_blank" rel="noopener">Click here</a>'
    new_client_click_here = '<a href="https://events.vanderbiltstrings.com/events/client_home/' + str(event.id) + '/wb4yi572" target="_blank" rel="noopener">Click here</a>'
    client_portal_full_address = '<a href="https://events.vanderbiltstrings.com/events/client_home/' + str(event.id) + '/" target="_blank" rel="noopener">https://events.vanderbiltstrings.com/events/client_home/' + str(event.id) + '/</a>'
    client_portal_pin = event.date.strftime("%m%d")
    client_contract_only_click_here = '<a href="https://events.vanderbiltstrings.com/events/client_home/' + str(event.id) + '/contract" target="_blank" rel="noopener">Click here</a>'
    client_musiclist_only_click_here = '<a href="https://events.vanderbiltstrings.com/events/client_home/' + str(event.id) + '/musiclist" target="_blank" rel="noopener">Click here</a>'
    client_confirmation_only_click_here = '<a href="https://events.vanderbiltstrings.com/events/client_home/' + str(event.id) + '/confirmation" target="_blank" rel="noopener">Click here</a>'
    client_payment_only_click_here = '<a href="https://events.vanderbiltstrings.com/events/client_home/' + str(event.id) + '/payment" target="_blank" rel="noopener">Click here</a>'
    
    glob = Global.objects.get(pk=1)
    invoice_number = glob.invoice_number
    
        
    thisdict = {'client_portal': format_html(client_portal),
                'client_home': format_html(client_home),
                'new_client_click_here': format_html(new_client_click_here),
                'client_portal_click_here': format_html(client_portal_click_here),
                'client_portal_full_address': format_html(client_portal_full_address),
                'client_portal_pin': format_html(client_portal_pin),
                'client_contract_only_click_here': format_html(client_contract_only_click_here),
                'client_musiclist_only_click_here': format_html(client_musiclist_only_click_here),
                'client_confirmation_only_click_here': format_html(client_confirmation_only_click_here),
                'client_payment_only_click_here': format_html(client_payment_only_click_here),
                'num_parents': num_parents,
                'num_bridesmaids': num_bridesmaids,
                'dress_code': event.dress_code,
                'hold_until': hold_until,
                'f1': format_html(e[1]),
                'f2': format_html(e[2]),
                'f3': format_html(e[3]),
                'f4': format_html(e[4]),
                'f5': format_html(e[5]),
                'f6': format_html(e[6]),
                'f7': format_html(e[7]),
                'extra_fee': '%.2f' % extra_fee,
                'extra_fee_paypal': '%.2f' % extra_fee_paypal,
                'fee_plus_extra': '%.2f' % (fee + extra_fee),
                'extra_rcvddate': conv_dt_short(event.extra_rcvddate),
                'calc_future_extra_duedate': conv_dt_short(calc_future_extra_duedate),
                'hold_until_sentence': hold_until_sentence,
                'gcal_contract': gcal_contract,
                'gcal_payment': gcal_payment,
                'gcal_contact_details': gcal_contact_details,
                'gcal_dayofcontact_details': gcal_dayofcontact_details,
                'gcal_recessional_cue':gcal_recessional_cue,
                'gcal_officiant_info':gcal_officiant_info,
                'gcal_automation':gcal_automation,
                'gcal_location_details': gcal_location_details,
                'gcal_start_time': gcal_start_time,
                'gcal_end_time': gcal_end_time,
                'full_or_final': full_or_final,
                'deposit_or_final_fee': deposit_or_final_fee,
                'event_link': event_link,
                'music_list': format_html(music_list),
                'notes': format_html(event.notes),
                'yes_btn_invite': format_html(yes_btn_code),
                'no_btn_invite': format_html(no_btn_code),
                'gotit_btn_invite': format_html(gotit_btn_code),
                'yes_btn_text': yes_btn_text,
                'no_btn_text': no_btn_text,
                'gotit_btn_text': gotit_btn_text,
                'confirm_btn': format_html(confirm_btn_code),
                'confirm_btn_text': confirm_btn_text,
                'confirm_list': format_html(confirm_list),
                'if_hold': format_html(if_hold),
                'if_hold_until': format_html(if_hold_until),
                'type': maintype,
                'event_id': str(event.id),
                'waive_payment': waive_payment,
                'waive_contract': waive_contract,
                'contracting_fee': '%.2f' % contracting_fee,
                #'final_payment_reminder': format_html(final_payment_reminder),
                #'music_choices_reminder': format_html(music_choices_reminder),
                #'dayofcontact_reminder': format_html(dayofcontact_reminder),
                #'officiant_reminder': format_html(officiant_reminder),
                #'ifnot_dayofcontact_reminder': format_html(ifnot_dayofcontact_reminder),
                'contract_link': format_html(contract_link),
                #'invoice_pdf_link': format_html(invoice_pdf_link),
                'indoor_outdoor': indoor_outdoor,
                'location_name_link': location_name_link,
                'name': format_html(event.name),
                'friendly_name': event.friendly_name,
                'date': event.date.strftime("%B X%d").replace('X0','X').replace('X','') + str(suffix(event.date.strftime("%d"))),
                'date_weekday': event.date.strftime("%A"),
                'date_year': event.date.strftime("%Y"),
                'year': event.date.strftime("%Y"),
                'date_short': event.date.strftime("%m/%d/%y"),
                'date_today': date.today(),
                'start_time': gcal_start_time,
                'arrival_time': arrival_time,
                'arrival_time_lead': arrival_time_lead,
                'end_time': gcal_end_time,
                'ceremony_time': event.ceremony_time,
                'if_ceremony_time': if_ceremony_time,
                'fact_ceremony_time': fact_ceremony_time,
                'event_type': format_html(event.event_type_name),
                'ensemble_name': event.ensemble_name,
                'ensemble_number': event.ensemble_number,
                'fee': '%.2f' % fee,
                'fee_paypal':  '%.2f' % paypal_full_fee,
                'deposit_fee': '%.2f' % deposit_fee,
                'deposit_fee_paypal': '%.2f' % paypal_deposit_fee,
                'final_fee': '%.2f' % final_fee,
                'final_fee_paypal': '%.2f' % paypal_final_fee,
                'musician_fee': '%.2f' % musician_fee,
                'contract_rcvddate': conv_dt_short(event.contract_rcvddate),
                'deposit_rcvddate': conv_dt_short(event.deposit_rcvddate),
                'final_rcvddate': conv_dt_short(event.final_rcvddate),
                'music_list_rcvddate': conv_dt_short(event.music_list_rcvddate),
                'confirmation_rcvddate': conv_dt_short(event.confirmation_rcvddate),
                'contract_sentdate': conv_dt_short(event.contract_sentdate),
                'deposit_sentdate': conv_dt_short(event.deposit_sentdate),
                'final_sentdate': conv_dt_short(event.final_sentdate),
                'music_list_sentdate': conv_dt_short(event.music_list_sentdate),
                'confirmation_sentdate': conv_dt_short(event.confirmation_sentdate),
                
                'contract_duedate': conv_dt_short(event.contract_duedate),
                'deposit_duedate': conv_dt_short(event.deposit_duedate),
                'final_duedate': conv_dt_short(event.final_duedate),
                'music_list_duedate': conv_dt_short(event.music_list_duedate),
                'confirmation_duedate': conv_dt_short(event.confirmation_duedate),
                
                'calc_future_contract_duedate': conv_dt_short(calc_future_contract_duedate),
                'calc_future_deposit_duedate': conv_dt_short(calc_future_deposit_duedate),
                'calc_future_final_duedate': conv_dt_short(calc_future_final_duedate),
                'calc_future_music_list_duedate': conv_dt_short(calc_future_music_list_duedate),
                'calc_future_confirmation_duedate': conv_dt_short(calc_future_confirmation_duedate),
                
                
                'factsheets_sentdate': conv_dt_short(event.fact_sheets_sentdate),
#                 'signature': format_html('<hr><p>Janie Spangler, Vanderbilt Strings\
#                     <br /><a class="fr-strong" href="http://www.vanderbiltstrings.com">\
#                     www.vanderbiltstrings.com</a> &bull;\
#                     <a href="mailto:janie@vanderbiltstrings.com">janie@vanderbiltstrings.com</a> \
#                     &bull; \
#                     (239) 949-4314 &bull; 93 3rd St., Bonita Springs, FL  34134</p>'),
                'signature': signature,
                'signature_alt': signature_alt,
                'location_name': location_name,
                'location_details': location_details,
                'if_location_details': if_location_details,
                'location_address': location_address,
                'location_link': format_html(location_link),
                'location_phone': location_phone,
                'location_email': location_email,
                'location_outdoors': location_outdoors,
                'contact_name': contact_name,
                'contact_details': contact_details,
                'contact_agency': contact_agency,
                'contact_phone': contact_phone,
                'contact_email': contact_email,
                'dayofcontact_name': dayofcontact_name,
                'dayofcontact_details': dayofcontact_details,
                'dayofcontact_phone': dayofcontact_phone,
                'dayofcontact_email': dayofcontact_email,
                'officiant_info': event.officiant_info,
                'officiant_info_exists': officiant_info_exists,
                'invoice_num': invoice_number,
                #'paypal_link_deposit': format_html('<b>Pay Deposit Amount:&nbsp;&nbsp;</b><a href="http://paypal.me/vanderbiltstrings/' + str(event.paypal_deposit_fee) + '"><img style="position:relative;top:7px" src="https://www.paypalobjects.com/digitalassets/c/website/marketing/apac/C2/logos-buttons/optimize/26_Grey_PayPal_Pill_Button.png" alt="Pay now with PayPal"></img></a>'),
                #'paypal_link_full': format_html('<b>Pay Full Amount:&nbsp;&nbsp;</b><a href="http://paypal.me/vanderbiltstrings/' + str(event.paypal_full_fee) + '"><img style="position:relative;top:7px" src="https://www.paypalobjects.com/digitalassets/c/website/marketing/apac/C2/logos-buttons/optimize/26_Grey_PayPal_Pill_Button.png" alt="Pay now with PayPal"></img></a>'),
                #'paypal_link_final': format_html('<b>Pay Final Amount:&nbsp;&nbsp;</b><a href="http://paypal.me/vanderbiltstrings/' + str(event.paypal_final_fee) + '"><img style="position:relative;top:7px" src="https://www.paypalobjects.com/digitalassets/c/website/marketing/apac/C2/logos-buttons/optimize/26_Grey_PayPal_Pill_Button.png" alt="Pay now with PayPal"></img></a>'),
                #'client_portal': format_html('<a href="' + settings.WEBSITE + 'client_home/' + str(event.id) + '" target="_blank">Client Portal</a>')
                }
    
    return thisdict




# <form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
# <input type="hidden" name="cmd" value="_s-xclick">
# <input type="hidden" name="hosted_button_id" value="EQJHRF8F5X9L2">
# <table>
# <tr><td><input type="hidden" name="on0" value="Payment">Payment</td></tr><tr><td><select name="os0">
#     <option value="Deposit Only">Deposit Only $200.00 USD</option>
#     <option value="Full Payment">Full Payment $400.00 USD</option>
# </select> </td></tr>
# </table>
# <input type="hidden" name="currency_code" value="USD">
# <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_buynowCC_LG.gif" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!">
# <img alt="" border="0" src="https://www.paypalobjects.com/en_US/i/scr/pixel.gif" width="1" height="1">
# </form>
#src="https://www.paypalobjects.com/webstatic/en_US/i/buttons/pp-acceptance-small.png" alt="Buy now with PayPal" />
        
