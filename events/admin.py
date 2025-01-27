from django.contrib import admin
from .models import Event, Musician, FormHtml, Venue, Contact, Activity
from .models import DayofContact, Reminder, RateChart, EventType, Ensemble, Global, FormEmail
from .models import MusicianEvent, MusicianInstrument, Client, ClientEmail, MusicRequest, FormAutomatedEmail 
from .models import PaymentsReceived, PaymentsDue, ESig, Dummy, Header, MusicList, BulkConvert   

class VsBulkConvert(admin.ModelAdmin):
    list_display = ('bulktext',)

class VsMusicList(admin.ModelAdmin):
    list_display = ('list',)
    
class VsDummy(admin.ModelAdmin):
    list_display = ('name',)

class VsHeader(admin.ModelAdmin):
    list_display= ('event', 'todos', 'notes', 'records', 'history')

class VsESig(admin.ModelAdmin):
    list_display = ('name', 'date', 'default')
    
class VsPaymentsReceived(admin.ModelAdmin):
    list_display = ('event', 'payment', 'amount_due', 'date', 'type', 'method')
    
class VsPaymentsDue(admin.ModelAdmin):
    list_display = ('event', 'musician', 'payment', 'duedate', 'done', 'donedate')

class VsFormAutomatedEmail(admin.ModelAdmin):
    list_display = ('event', 'sentdate', 'subject', 'addr')

class VsMusicRequest(admin.ModelAdmin):
    list_display = ('name', 'type', 'list')
    ordering = ('name', 'type',)

class VsClient(admin.ModelAdmin):
    list_display = ('event', 'signature_date', 'did_sign')
    
class VsClientEmail(admin.ModelAdmin):
    list_display = ('event', 'from_email')

class VsAdminEvent(admin.ModelAdmin):
    list_display = ('name', 'id', 'event_archived', 'version', 'date', 'start_time', 'location','ensemble','date_entered')
    ordering = ('date','start_time',)
    pass

class VsAdminMusician(admin.ModelAdmin):
    list_display = ('name','order','instrument','instrument2','email','phone',)
    ordering = ('order',)
    pass

class VsAdminMusicianEvent(admin.ModelAdmin):
    list_display = ('musician', 'event', 'asked', 'yes', 'no', 'gotit', 'instrument', 'rank')

class VsAdminReminder(admin.ModelAdmin):
    list_display = ('name', 'id', 'date', 'event', 'auto', 'done', 'edited', 'disb')
    ordering = ('id',)
    
class VsAdminFormEmail(admin.ModelAdmin):
    list_display = ('sentdate', 'addr', 'subject', 'body')
    ordering = ('sentdate', 'addr',)

class VsAdminFormHtml(admin.ModelAdmin):
    list_display = ('name', 'description', 'order', 'subject')
    ordering = ('name',)

class VsAdminActivity(admin.ModelAdmin):
    list_display = ('name', 'date', 'event', 'id')
    ordering = ('event',)
    
class VsAdminMusicianInstrument(admin.ModelAdmin):
    list_display = ('instrument',)
    
class VsAdminDayofContact(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'order')
    ordering = ('name',)


    
admin.site.register(Event, VsAdminEvent)
admin.site.register(Musician, VsAdminMusician)
admin.site.register(MusicianEvent, VsAdminMusicianEvent)
admin.site.register(Venue)
admin.site.register(Contact)
admin.site.register(DayofContact, VsAdminDayofContact)
admin.site.register(Reminder, VsAdminReminder)
admin.site.register(RateChart)
admin.site.register(EventType)
admin.site.register(Ensemble)
admin.site.register(Global)
admin.site.register(FormEmail, VsAdminFormEmail)
admin.site.register(FormHtml, VsAdminFormHtml)
admin.site.register(Activity, VsAdminActivity)
admin.site.register(MusicianInstrument, VsAdminMusicianInstrument)
admin.site.register(Client, VsClient)
admin.site.register(ClientEmail, VsClientEmail)
admin.site.register(MusicRequest, VsMusicRequest)
admin.site.register(FormAutomatedEmail, VsFormAutomatedEmail)
admin.site.register(PaymentsDue, VsPaymentsDue)
admin.site.register(PaymentsReceived, VsPaymentsReceived)
admin.site.register(ESig, VsESig)
admin.site.register(Dummy, VsDummy)
admin.site.register(Header, VsHeader)
admin.site.register(MusicList, VsMusicList)
admin.site.register(BulkConvert, VsBulkConvert)




