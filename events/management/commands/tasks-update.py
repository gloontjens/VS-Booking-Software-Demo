# from huey import crontab
from events.models import Event, Reminder, FormEmail, FormAutomatedEmail, FormHtml, Contact, Client, Global, Activity, MusicianEvent
from django.shortcuts import get_object_or_404
from datetime import datetime, date, timezone
from dateutil.relativedelta import relativedelta
from events.form_dict import make_dict
from django.template import Template, Context
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from events.views import add_action, process_due_dates, process_auto_reminders, process_update_flags, check_gcal
from io import BytesIO
from xhtml2pdf import pisa
import ftplib
import os
import struct
import socket
import select
from django.conf import settings

from django.core.management.base import BaseCommand, CommandError



class Command(BaseCommand):
    
    def handle(self, *args, **options):
        today = date.today()    
        events = Event.objects.filter(date__gte=today).exclude(
            event_archived=True).order_by('date','start_time')
         
        print("################")
        print(events) 
        print("################")  
        for event in events:
            print(event)
            event.event_reminders_done = False
            process_due_dates(event)
            process_auto_reminders(event)
            process_update_flags(event)
            event.event_reminders_done = True
            event.save()
            print(event)
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
        
        #Also, delete all DB entries for FormEmail, Activity, Reminder
        #  that are for events older than 2 months!
        sixtydaysago = today + relativedelta(days=-45)
        
        oldrems = Reminder.objects.filter(event__date__lt=sixtydaysago)
        
        oldacts = Activity.objects.filter(event__date__lt=sixtydaysago)
        
        oldemails = FormEmail.objects.filter(event__date__lt=sixtydaysago)
        
        for oldrem in oldrems:
            oldrem.delete()
        
        for oldact in oldacts:
            oldact.delete()
            
        for oldemail in oldemails:
            oldemail.delete()
            
        
        
        
        
            
