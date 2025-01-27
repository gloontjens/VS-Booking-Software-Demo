# from huey import crontab
from events.models import Event, Reminder, FormAutomatedEmail, FormHtml, Contact, Client, Global, Activity, MusicianEvent
from django.shortcuts import get_object_or_404
from datetime import datetime, date, timezone
from dateutil.relativedelta import relativedelta
from events.form_dict import make_dict
from django.template import Template, Context
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from events.views import add_action, process_due_dates, process_auto_reminders, process_update_flags, check_gcal, process_cron_jobs_now
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
        #if automation already run today, then don't run again until tomorrow
        today = date.today()
        this = Global.objects.get(pk=1)
        if this.last_automated == today:
            print("already done today")
            exit()
        else:
            this.last_automated = today
            this.save()
        
        #pull up each automatic reminder that's not done, not archived event,
        #    not past event, with reminder being in the range of 5dys ago to 5dys future.
        
        fivedayspast = today - relativedelta(days=5)
        fivedaysfuture = today + relativedelta(days=5)
        
        #what you need here is a list of events, not a list of reminders to do!  The list of reminders
        #is figured out for each event by process_cron_jobs_now() in views.py!
        
        todos = Reminder.objects.filter(date__range=[fivedayspast, fivedaysfuture]).exclude(
                    done=True).exclude(disb=True).exclude(
                    event__date__lt=today).exclude(
                    auto=False).exclude(
                    event__event_archived=True).order_by('date')
        
        usedeventnums = []
                 
        #print(todos)
        
        #loop through each, determining what type (name) and doing appropriate code
        #    to send appropriate email or whatever needs to be done
        #    Then, set appropriate flags for each type (on assoc event), and also
        #    save a record of this in FormAutomatedEmail, and finally mark this reminder as done
        for todo in todos:
            if todo.event_id not in usedeventnums:
                usedeventnums.append(todo.event_id)
                event = get_object_or_404(Event, pk=todo.event_id)
                process_cron_jobs_now(event)
            
            
            
            
            
            
            