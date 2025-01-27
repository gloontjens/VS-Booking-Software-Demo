from django.db import models
from phone_field import PhoneField
from datetime import datetime, timedelta, date
from tinymce.models import HTMLField
import datetime
from dateutil.relativedelta import relativedelta
from _decimal import ROUND_HALF_UP
from jsignature.mixins import JSignatureFieldsMixin
from concurrency.fields import IntegerVersionField
from ool import VersionField, VersionedMixin


today = date.today()


class Sig(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    sig = models.CharField(max_length=4000)


class FormHtml(models.Model):
    body = HTMLField()
    name = models.CharField(max_length=40, blank=True)
    order = models.PositiveIntegerField(blank=True, default="100") 
    description = models.CharField(max_length=300, blank=True)
    subject = models.CharField(max_length=100, blank=True, default='')
    pdf = HTMLField()
    def __str__(self):
        return self.name
        
class Global(models.Model):
    code_verifier = models.CharField(max_length=150, blank=True)
    last_automated = models.DateField()
    last_updated = models.DateField()
    browse_mode = models.CharField(max_length=40, blank=True)
    browse_date = models.DateField()
    gcal_date = models.DateField()
    gcal_needs = models.BooleanField()
    sidecal_year = models.PositiveIntegerField()
    sidecal_month = models.PositiveIntegerField()
    pnl1 = models.BooleanField(default=False)
    pnl2 = models.BooleanField(default=False)
    pnl3 = models.BooleanField(default=False)
    pnl4 = models.BooleanField(default=False)
    pnl5 = models.BooleanField(default=False)
    pnl6 = models.BooleanField(default=False)
    home_todo = models.BooleanField(default=False)
    home_booking = models.BooleanField(default=False)
    home_payment = models.BooleanField(default=False)
    home_history = models.BooleanField(default=False)

    mycal_year = models.PositiveIntegerField()
    mycal_month = models.PositiveIntegerField()
    auto_btn_side = models.BooleanField(default=False)
    auto_btn = models.BooleanField(default=False)
    show_pd_btn = models.BooleanField(default=False )
    gtoken = models.TextField(default = '', blank=True)
    hideside = models.BooleanField(default=False)
    
    janie_sig = models.TextField(blank=True, null=True)
    invoice_number = models.PositiveIntegerField(default="201")


class Dummy(models.Model):
    name = models.CharField(max_length=100, blank=True)
    class Meta:
        verbose_name_plural = "9. (DO NOT EDIT BELOW ITEMS)"
    
    
class Venue(models.Model):
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    link = models.CharField(max_length=400, blank=True)
    phone = PhoneField(blank=True)
    email = models.EmailField(max_length=100, blank=True)
    order = models.PositiveIntegerField(blank=True, default="100")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "2. Venues [Edit Here]"
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    friendlyname = models.CharField(max_length=100, blank=True, default="")
    agency = models.CharField(max_length=100, blank=True)
    phone = PhoneField(blank=True)
    email = models.EmailField(max_length=100, blank=True)
    order = models.PositiveIntegerField(blank=True, default="100")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "3. Contacts [Edit Here]"

class DayofContact(models.Model):
    name = models.CharField(max_length=100)
    phone = PhoneField(blank=True)
    email = models.EmailField(max_length=100, blank=True)
    order = models.PositiveIntegerField(blank=True, default="100")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "4. Planners [Edit Here]"
        verbose_name = "Planner"
        
class RateChart(models.Model):
    name = models.CharField(max_length=50) #Standard, Sanibel, LaPlaya etc.
    importance = models.PositiveIntegerField(blank=True, default="100")
    solo = models.PositiveIntegerField()
    duo = models.PositiveIntegerField()
    trio = models.PositiveIntegerField()
    quartet = models.PositiveIntegerField()
    musician = models.PositiveIntegerField()
    two_solo = models.PositiveIntegerField()
    two_duo = models.PositiveIntegerField()
    two_trio = models.PositiveIntegerField()
    two_quartet = models.PositiveIntegerField()
    two_musician = models.PositiveIntegerField()
    three_solo = models.PositiveIntegerField()
    three_duo = models.PositiveIntegerField()
    three_trio = models.PositiveIntegerField()
    three_quartet = models.PositiveIntegerField()
    three_musician = models.PositiveIntegerField()
    four_solo = models.PositiveIntegerField()
    four_duo = models.PositiveIntegerField()
    four_trio = models.PositiveIntegerField()
    four_quartet = models.PositiveIntegerField()
    four_musician = models.PositiveIntegerField()
    cont_1s = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    cont_1d = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    cont_1t = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    cont_1q = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    cont_2s = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    cont_2d = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    cont_2t = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    cont_2q = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    cont_3s = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    cont_3d = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    cont_3t = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    cont_3q = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    cont_4s = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    cont_4d = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    cont_4t = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    cont_4q = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    def __str__(self):
        return self.name

class ESig(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(blank=True)
    sig = HTMLField(blank=True)
    default = models.BooleanField(default=False)
    default_alt = models.BooleanField(default=False)
    
class EventType(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(blank=True, default="100") 
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "6. Event Types [Edit Here]"

class Ensemble(models.Model):
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField(blank=True, default="4")
    order = models.PositiveIntegerField(blank=True, default="100")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "5. Ensembles [Edit Here]"

class Event(VersionedMixin, models.Model):
    TYPE_CHOICES = (
        ('RG', 'Regular'),
        ('HD', 'Hold'),
        ('AB', 'Agency'),
    )
    
    version = VersionField()
    
    
    signature = models.CharField(max_length=2000, blank=True, null=True)
    signature_date = models.DateField(blank=True, null=True)
    
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='RG')
    hold_until = models.DateField(blank=True, null=True)
    hold_released = models.DateField(blank=True, null=True)
    event_archived = models.BooleanField(default=False)
    event_reminders_done = models.BooleanField(default = False)
    
    date_entered = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=100)
    friendly_name = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    ceremony_time = models.TimeField(blank=True, null=True)
    
    #     event_type = models.CharField(max_length=3, choices=EVENT_TYPE_CHOICES, default="", blank=True)
    event_type = models.ForeignKey(EventType, on_delete=models.PROTECT, blank=True, null=True)
    event_type_name = models.CharField(max_length=100, blank=True)
    
    waive_contract = models.BooleanField(default=False)
    waive_payment = models.BooleanField(default=False)
#     ensemble = models.CharField(max_length=2, choices=ENSEMBLE_CHOICES, default="", blank=True)
    ensemble = models.ForeignKey(Ensemble, on_delete=models.PROTECT, blank=True, null=True)
    ensemble_name = models.CharField(max_length=100, blank=True)
    ensemble_number = models.PositiveIntegerField(blank=True, null=True)
    
    location = models.ForeignKey(Venue, on_delete=models.PROTECT, blank=True, null=True)
#     location = models.CharField(max_length=100, blank=True)
    location_details = models.CharField(max_length=500, blank=True)
    location_outdoors = models.BooleanField(default=True)
    location_add = models.BooleanField(default=False)
    location_name = models.CharField(max_length=100, blank=True)
    location_address = models.CharField(max_length=100, blank=True)
    location_link = models.CharField(max_length=100, blank=True)
    location_phone = PhoneField(blank=True)
    location_email = models.CharField(max_length=100, blank=True)
    
    
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT, blank=True, null=True)
    contact_details = models.CharField(max_length=500, blank=True)
    contact_add = models.BooleanField(default=False)
    contact_name = models.CharField(max_length=100, blank=True)
    contact_agency = models.CharField(max_length=100, blank=True)
    contact_phone = PhoneField(blank=True)
    contact_email = models.CharField(max_length=100, blank=True)
    
    dayofcontact = models.ForeignKey(DayofContact, on_delete=models.PROTECT, blank=True, null=True)
    dayofcontact_details = models.CharField(max_length=500, blank=True)
    dayofcontact_add = models.BooleanField(default=False)
    dayofcontact_name = models.CharField(max_length=100, blank=True)
    dayofcontact_phone = PhoneField(blank=True)
    dayofcontact_email = models.CharField(max_length=100, blank=True)
    
    fee = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2, default=0)
    contracting_fee = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2, default=0)
    musician_fee = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2, default=0)
    deposit_fee = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2, default=0)
    deposit_date = models.DateField(blank=True, null=True)
    final_fee = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2, default=0)
    final_date = models.DateField(blank=True, null=True)
    cash_fee = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2, default=0)
    extra_fee = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2, default=0)
    
    #add sent & due dates for music list, musicians, confirm, fact sheets
    contract_sentdate = models.DateField(blank=True, null=True)
    deposit_sentdate = models.DateField(blank=True, null=True)
    final_sentdate = models.DateField(blank=True, null=True)
    music_list_sentdate = models.DateField(blank=True, null=True)
    musicians_sentdate = models.DateField(blank=True, null=True)
    confirmation_sentdate = models.DateField(blank=True, null=True)
    fact_sheets_sentdate = models.DateField(blank=True, null=True)
    hold_sentdate = models.DateField(blank=True, null=True)
    extra_sentdate = models.DateField(blank=True, null=True)
    
    contract_rcvddate = models.DateField(blank=True, null=True)
    deposit_rcvddate = models.DateField(blank=True, null=True)
    final_rcvddate = models.DateField(blank=True, null=True)
    music_list_rcvddate = models.DateField(blank=True, null=True)
    musicians_rcvddate = models.DateField(blank=True, null=True)
    confirmation_rcvddate = models.DateField(blank=True, null=True)
    fact_sheets_rcvddate = models.DateField(blank=True, null=True)
    extra_rcvddate = models.DateField(blank=True, null=True)
    
    contract_rcptdate = models.DateField(blank=True, null=True)
    deposit_rcptdate = models.DateField(blank=True, null=True)
    final_rcptdate = models.DateField(blank=True, null=True)
    extra_rcptdate = models.DateField(blank=True, null=True)
    
    contract_duedate = models.DateField(blank=True, null=True)
    deposit_duedate = models.DateField(blank=True, null=True)
    final_duedate = models.DateField(blank=True, null=True)
    music_list_duedate = models.DateField(blank=True, null=True)
    musicians_duedate = models.DateField(blank=True, null=True)
    confirmation_duedate = models.DateField(blank=True, null=True)
    fact_sheets_duedate = models.DateField(blank=True, null=True)
    extra_duedate = models.DateField(blank=True, null=True)
    
    contract_senddate = models.DateField(blank=True, null=True)
    deposit_senddate = models.DateField(blank=True, null=True)
    final_senddate = models.DateField(blank=True, null=True)
    music_list_senddate = models.DateField(blank=True, null=True)
    musicians_senddate = models.DateField(blank=True, null=True)
    confirmation_senddate = models.DateField(blank=True, null=True)
    fact_sheets_senddate = models.DateField(blank=True, null=True)
    extra_senddate = models.DateField(blank=True, null=True)
    
        
    flag_hold = models.BooleanField(default=False)
    flag_hold_sent = models.BooleanField(default=False)
        
    flag_contract_sent = models.BooleanField(default=False)
    flag_contract_rcvd = models.BooleanField(default=False)
    flag_contract_rcpt = models.BooleanField(default=False)
    
    flag_deposit_sent = models.BooleanField(default=False)
    flag_deposit_rcvd = models.BooleanField(default=False)
    flag_deposit_rcpt = models.BooleanField(default=False)
    
    flag_music_list_sent = models.BooleanField(default=False)
    flag_music_list_rcvd = models.BooleanField(default=False)
    
    flag_musicians_sent = models.BooleanField(default=False)
    flag_musicians_rcvd = models.BooleanField(default=False)
    
    flag_final_payment_sent = models.BooleanField(default=False)
    flag_final_payment_rcvd = models.BooleanField(default=False)
    flag_final_payment_rcpt = models.BooleanField(default=False)
    
    flag_extra_sent = models.BooleanField(default=False)
    flag_extra_rcvd = models.BooleanField(default=False)
    flag_extra_rcpt = models.BooleanField(default=False)
    
    flag_final_confirmation_sent = models.BooleanField(default=False)
    flag_final_confirmation_rcvd = models.BooleanField(default=False)
    
    flag_fact_sheets_sent = models.BooleanField(default=False)
    flag_fact_sheets_rcvd = models.BooleanField(default=False)

    color_contract = models.CharField(max_length=10, default='#eeeeee')
    color_deposit = models.CharField(max_length=10, default='#eeeeee')
    color_music_list = models.CharField(max_length=10, default='#eeeeee')
    color_musicians = models.CharField(max_length=10, default='#eeeeee')
    color_final_payment = models.CharField(max_length=10, default='#eeeeee')
    color_final_confirmation = models.CharField(max_length=10, default='#eeeeee')
    color_fact_sheets = models.CharField(max_length=10, default='#eeeeee')
    color_extra_payment = models.CharField(max_length=10, default='#eeeeee')
    
    waive_music_list = models.BooleanField(default=False)
    number_bridesmaids = models.PositiveIntegerField(blank=True, null=True, default=0)
    number_parents = models.PositiveIntegerField(blank=True, null=True, default=0)
    recessional_cue = models.CharField(max_length=500, blank=True)
    officiant_info = models.CharField(max_length=500, blank=True)
    dress_code = models.CharField(max_length=500, default="Men: Black jacket, black shirt, black pants, long black tie. In warmer months, no jacket, roll up sleeves.  Women: Long black dress, no flip flops unless they can't be seen.")
    flowergirls = models.BooleanField(default=False)
    
    automation = models.BooleanField(default=False)
    reminderdisable = models.BooleanField(default=False)
    
    music_list = models.TextField(blank=True)
    accept_custom = models.BooleanField(default=False)
    
    notes = models.TextField(default = '', blank=True)
    #notes = HTMLField()
    records = models.TextField(default = '', blank=True)
    
    reminders_bar_hidden = models.BooleanField(default=False)
    #dummy fields
    musician = models.CharField(max_length=100, blank=True)
    instrument = models.CharField(max_length=100, blank=True)
#     search = models.CharField(max_length=100, blank=True)

    number_guests = models.PositiveIntegerField(blank=True, null=True, default=0)
    dayofcontact_alone_name = models.CharField(blank=True, null=True, max_length=100, default='')
    dayofcontact_alone_phone = PhoneField(blank=True, default='')
    
    @property
    def paypal_deposit_fee(self):
        if not self.deposit_fee:
            return 0
        else:
            num = self.deposit_fee
            num = num * 100
            num = num + 49
            num2 = float(num) / 97.01
            #final = num2 + 0.49
            return round(num2,2)

    @property
    def paypal_final_fee(self):
        if not self.final_fee:
            return 0
        else:
            num = self.final_fee
            num = num * 100
            num = num + 49
            num2 = float(num) / 97.01
            #final = num2 + 0.49
            return round(num2,2)

    @property
    def paypal_full_fee(self):
        if not self.fee:
            return 0
        else:
            num = self.fee
            num = num * 100
            num = num + 49
            num2 = float(num) / 97.01
            #final = num2 + 0.49
            return round(num2,2)

    @property
    def paypal_extra_fee(self):
        if not self.extra_fee:
            return 0
        else:
            num = self.extra_fee
            num = num * 100
            num = num + 49
            num2 = float(num) / 97.01
            #final = num2 + 0.49
            return round(num2,2)
    
    @property
    def date_ispast(self):
        if self.date < date.today():
            return True
        else:
            return False
    @property
    def date_issoon(self):
        soon = self.date - relativedelta(days=21)
        if soon < date.today():
            return True
        else:
            return False
    @property
    def date_isrealsoon(self):
        soon = self.date - relativedelta(days=7)
        if soon < date.today():
            return True
        else:
            return False
        
    @property
    def url_link(self):
        return "/events/" + str(self.id) + "/edit"
        
    @property
    def is_hold_past_due(self):
        if self.hold_until and self.type == 'HD':
            return date.today() > self.hold_until
        
        elif self.type == 'HD':
            return date.today() > (self.date - relativedelta(days=5)) 
        else:
            return False
        
    @property
    def is_deposit_due_soon(self):
        if self.flag_deposit_sent and self.deposit_duedate and not self.flag_deposit_rcvd:
            soon = self.deposit_duedate - relativedelta(days=12)
            return date.today() > soon
        else:
            return False
    @property
    def is_deposit_past_due_simple(self):
        if self.flag_deposit_sent and self.deposit_duedate and not self.flag_deposit_rcvd:
            return date.today() > self.deposit_duedate
        else:
            return False

    @property
    def is_deposit_past_due(self):
        if self.flag_deposit_sent and not self.flag_deposit_rcvd and self.deposit_duedate:
            return date.today() > self.deposit_duedate
        elif not self.flag_deposit_sent and self.deposit_senddate:
            return date.today() > self.deposit_senddate
        elif self.flag_deposit_rcvd and self.deposit_rcptdate and not self.flag_deposit_rcpt:
            return date.today() > self.deposit_rcptdate
        else:
            return False

    @property
    def is_contract_due_soon(self):
        if self.flag_contract_sent and self.contract_duedate and not self.flag_contract_rcvd:
            soon = self.contract_duedate - relativedelta(days=10)
            return date.today() > soon
        else:
            return False


    @property
    def is_contract_past_due_simple(self):
        if self.flag_contract_sent and self.contract_duedate and not self.flag_contract_rcvd:
            return date.today() > self.contract_duedate
        else:
            return False
        
    @property
    def is_contract_past_due(self):
        if self.flag_contract_sent and not self.flag_contract_rcvd and self.contract_duedate:
            return date.today() > self.contract_duedate
        elif not self.flag_contract_sent and self.contract_senddate:
            return date.today() > self.contract_senddate
        elif self.flag_contract_rcvd and self.contract_rcptdate and not self.flag_contract_rcpt:
            return date.today() > self.contract_rcptdate
        else:
            return False

    @property
    def is_music_list_past_due_simple(self):
        if self.flag_music_list_sent and self.music_list_duedate and not self.flag_music_list_rcvd:
            return date.today() > self.music_list_duedate
        else:
            return False
    @property
    def is_music_list_due_soon(self):
        if self.flag_music_list_sent and self.music_list_duedate and not self.flag_music_list_rcvd:
            soon = self.music_list_duedate - relativedelta(days=10)
            return date.today() > soon
        else:
            return False
    @property
    def is_music_list_past_due(self):
        if self.flag_music_list_sent and not self.flag_music_list_rcvd and self.music_list_duedate:
            return date.today() > self.music_list_duedate
        elif not self.flag_music_list_sent and self.music_list_senddate:
            return date.today() > self.music_list_senddate
        else:
            return False
 
    @property
    def is_musicians_past_due(self):
        if self.flag_musicians_sent and not self.flag_musicians_rcvd and self.musicians_duedate:
            return date.today() > self.musicians_duedate
        elif not self.flag_musicians_sent and self.musicians_senddate:
            return date.today() > self.musicians_senddate
        else:
            return False
 
    @property
    def is_final_pay_past_due_simple(self):
        if self.flag_final_payment_sent and self.final_duedate and not self.flag_final_payment_rcvd:
            return date.today() > self.final_duedate
        else:
            return False
    @property
    def is_final_pay_due_soon(self):
        if self.flag_final_payment_sent and self.final_duedate and not self.flag_final_payment_rcvd:
            soon = self.final_duedate - relativedelta(days=12)
            return date.today() > soon
        else:
            return False
    @property
    def is_final_pay_past_due(self):
        if self.flag_final_payment_sent and not self.flag_final_payment_rcvd and self.final_duedate:
            return date.today() > self.final_duedate
        elif not self.flag_final_payment_sent and self.final_senddate:
            return date.today() > self.final_senddate
        elif self.flag_final_payment_rcvd and self.final_rcptdate and not self.flag_final_payment_rcpt:
            return date.today() > self.final_rcptdate
        else:
            return False

    
    
    @property
    def is_extra_pay_past_due_simple(self):
        if self.flag_extra_sent and self.extra_duedate and not self.flag_extra_rcvd:
            return date.today() > self.extra_duedate
        else:
            return False
    @property
    def is_extra_pay_due_soon(self):
        if self.flag_extra_sent and self.extra_duedate and not self.flag_extra_rcvd:
            soon = self.extra_duedate - relativedelta(days=12)
            return date.today() > soon
        else:
            return False
    @property
    def is_extra_pay_past_due(self):
        if self.flag_extra_sent and not self.flag_extra_rcvd and self.extra_duedate:
            return date.today() > self.extra_duedate
        elif not self.flag_extra_sent and self.extra_senddate:
            return date.today() > self.extra_senddate
        elif self.flag_extra_rcvd and self.extra_rcptdate and not self.flag_extra_rcpt:
            return date.today() > self.extra_rcptdate
        else:
            return False



 
    @property
    def is_final_confirmation_past_due_simple(self):
        if self.flag_final_confirmation_sent and self.confirmation_duedate and not self.flag_final_confirmation_rcvd:
            return date.today() > self.confirmation_duedate
        #handle the case if we never sent final confirmation email (no conf_duedate is calculated then)
        #we say it's past due if it's past the planned senddate + 6 days, or event is less than 3 days away
        elif not self.flag_final_confirmation_sent and self.confirmation_senddate:
            normaldue = self.confirmation_senddate + relativedelta(days=6)
            eventlimitdue = self.date - relativedelta(days=3)
            return ((date.today() > normaldue) or (date.today() > eventlimitdue))
        else:
            return False
    @property
    def is_final_confirmation_due_soon(self):
        if self.flag_final_confirmation_sent and self.confirmation_duedate and not self.flag_final_confirmation_rcvd:
            soon = self.confirmation_duedate - relativedelta(days=14)
            return date.today() > soon
        #handle the case if we never sent final confirmation email (no conf_duedate is calculated then)
        #we say it's due soon if it's past the planned senddate, of course
        elif not self.flag_final_confirmation_sent and self.confirmation_senddate:
            return date.today() > self.confirmation_senddate
        else:
            return False
    @property
    def is_final_confirmation_past_due(self):
        if self.flag_final_confirmation_sent and not self.flag_final_confirmation_rcvd and self.confirmation_duedate:
            return date.today() > self.confirmation_duedate
        elif not self.flag_final_confirmation_sent and self.confirmation_senddate:
            return date.today() > self.confirmation_senddate
        else:
            return False
 
    @property
    def is_fact_sheets_past_due(self):
        if self.flag_fact_sheets_sent and not self.flag_fact_sheets_rcvd and self.fact_sheets_duedate:
            return date.today() > self.fact_sheets_duedate
        elif not self.flag_fact_sheets_sent and self.fact_sheets_senddate:
            return date.today() > self.fact_sheets_senddate
        else:
            return False
     
    class Meta:
        verbose_name_plural = "Events"
    
class Reminder(models.Model):
    name = models.CharField(max_length=300)
    date = models.DateField(blank=True, null=True)
    done = models.BooleanField(default=False)
    donedt = models.DateTimeField(blank=True, null=True)
    auto = models.BooleanField(default=False)
    in_progress = models.BooleanField(default=False)
    send_1 = models.BooleanField(default=False)
    send_2 = models.BooleanField(default=False)
    send_3 = models.BooleanField(default=False)
    giveup = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    disb = models.BooleanField(default=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=False, default=1)
    @property
    def is_past_due(self):
        return date.today() > self.date
    @property
    def is_this_week(self):
        isthisweek = False
        sevendays = date.today() + timedelta(days=6)
        if self.date >= date.today() and self.date <= sevendays:
            isthisweek = True        
        return isthisweek
    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField(max_length=600)
    date = models.DateField(blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=False, default=1)
    main = models.BooleanField(default=False)
    mainname = models.CharField(max_length=200, default='')
    mainclienttype = models.BooleanField(default=False)
    mainmustype = models.BooleanField(default=False)

class Header(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=False, default=1)
    todos = models.BooleanField(default=False)
    notes = models.BooleanField(default=False)
    records = models.BooleanField(default=False)
    history = models.BooleanField(default=False)

class Musician(models.Model):
    name = models.CharField(max_length=100)
    instrument = models.CharField(max_length=50)
    instrument2 = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=100)
    phone = PhoneField(blank=True)
    order = models.PositiveIntegerField(blank=True, default="100")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "1. Musicians [Edit Here]"

class MusicianEvent(models.Model):
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE, blank=False, null=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=False)
    asked = models.BooleanField(default=False)
    yes = models.BooleanField(default=False)
    no = models.BooleanField(default=False)
    instrument = models.CharField(max_length=50, blank=True)
    rank = models.PositiveIntegerField(blank=True, null=True)
    placeholder = models.BooleanField(default=False)
    gotit = models.BooleanField(default=False)
    specialfee = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2, default=0)
    
class MusicianInstrument(models.Model):
    instrument = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(blank=True, default="100")
        
class Client(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=False)
    signature = models.TextField(blank=True)
    signature_date = models.DateField(blank=True, null=True)
    signature_name = models.CharField(max_length=100, blank=True, null=True)
    signature_email = models.CharField(max_length=200, blank=True, null=True)
    paid_deposit = models.BooleanField(default=False)
    paid_final = models.BooleanField(default=False)
    paid_extra = models.BooleanField(default=False)
    paid_total = models.BooleanField(default=False)
    paid_online = models.BooleanField(default=False)
    paid_final_online = models.BooleanField(default=False)
    paid_extra_online = models.BooleanField(default=False)
    did_music_list = models.BooleanField(default=False)
    contract_pdf = models.TextField(default='', blank=True)
    did_verify_info = models.BooleanField(default=False)
    did_sign = models.BooleanField(default=False)
    signature_date = models.DateField(blank=True, null=True)
    paid_deposit_date = models.DateField(blank=True, null=True)
    paid_final_date = models.DateField(blank=True, null=True)
    paid_extra_date = models.DateField(blank=True, null=True)
    paid_total_date = models.DateField(blank=True, null=True)
    music_list_date = models.DateField(blank=True, null=True)
    verify_info_date = models.DateField(blank=True, null=True)
    started = models.BooleanField(default=False)
    transition = models.BooleanField(default=False)
    transition_contract = models.BooleanField(default=False)
    transition_deposit = models.BooleanField(default=False)
    transition_final = models.BooleanField(default=False)
    transition_total = models.BooleanField(default=False)
    transition_extra = models.BooleanField(default=False)
    transition_music_list = models.BooleanField(default=False)
    transition_verify_info = models.BooleanField(default=False)
    paypalid_deposit = models.CharField(max_length=50,blank=True, null=True)
    paypalid_final = models.CharField(max_length=50,blank=True, null=True)
    paypalid_total = models.CharField(max_length=50,blank=True, null=True)
    paypalid_extra = models.CharField(max_length=50,blank=True, null=True)
    paypaldone_deposit = models.BooleanField(default=False)
    paypaldone_final = models.BooleanField(default=False)
    paypaldone_total = models.BooleanField(default=False)
    paypaldone_extra = models.BooleanField(default=False)
    changedlist = models.TextField(blank=True, null=True)
    
class ClientEmail(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=False)
    from_email = models.EmailField(max_length=100) 
    subject = models.CharField(max_length=200, blank=False)
    body = models.TextField(default = '', blank=False)
    
class MusicRequest(models.Model):
    name = models.CharField(max_length=50, blank=False) #solo, quartet, etc
    type = models.CharField(max_length=100, blank=False) #parents, brides, etc
    list = models.TextField(default='', blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "7. Music Request Recommendations [Edit Here]"

class MusicList(models.Model):
    list = models.TextField(default='', blank=True)
    def __str__(self):
        return self.list
    class Meta:
        verbose_name_plural = "8. Full Music List [Edit Here]"
    
class FormAutomatedEmail(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=False)
    body = HTMLField()
    subject = models.CharField(max_length=150, blank=True)
    addr = models.CharField(max_length=400, blank=True)
    sentdate = models.DateTimeField(blank=True, null=True)
    pdf = HTMLField(default = '')
    def __str__(self):
        return self.body 

class FormEmail(models.Model):
#     name = models.CharField(max_length=100, default="name")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=False)
    body = HTMLField()
    subject = models.CharField(max_length=150, blank=True)
    addr = models.CharField(max_length=400, blank=True)
    sentdate = models.DateTimeField(blank=True, null=True)
    pdf = HTMLField(default = '')
    def __str__(self):
        return self.body 


class PaymentsReceived(models.Model):
    payment = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    amount_due = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=False)
    date = models.DateField(blank=True, null=True)
    method = models.CharField(max_length=20, blank=True) #paypal or check
    type = models.CharField(max_length=20, blank=True) #full or final or deposit

class PaymentsDue(models.Model):
    payment = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=False)
    duedate = models.DateField(blank=True, null=True)
    donedate = models.DateField(blank=True, null=True)
    done = models.BooleanField(default=False)
    auto = models.BooleanField(default=False)
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE, blank=False, null=False)
    @property
    def is_past_due(self):
        return date.today() > self.duedate
    @property
    def is_this_week(self):
        isthisweek = False
        sevendays = date.today() + timedelta(days=6)
        if self.duedate >= date.today() and self.duedate <= sevendays:
            isthisweek = True        
        return isthisweek
    

class EventTemp:
    id = models.PositiveIntegerField()
    ensemble_number = models.PositiveIntegerField()
    
    hold_until = models.DateField(blank=True, null=True)
    hold_released = models.DateField(blank=True, null=True)
    event_reminders_done = models.BooleanField(default = False)
    date_entered = models.DateField(blank=True, null=True)
    date = models.DateField()
    waive_contract = models.BooleanField(default=False)
    waive_payment = models.BooleanField(default=False)
    
    fee = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    deposit_fee = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    final_fee = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    extra_fee = models.DecimalField(blank = True, null=True, max_digits=8, decimal_places=2)
    
    contract_sentdate = models.DateField(blank=True, null=True)
    deposit_sentdate = models.DateField(blank=True, null=True)
    final_sentdate = models.DateField(blank=True, null=True)
    music_list_sentdate = models.DateField(blank=True, null=True)
    musicians_sentdate = models.DateField(blank=True, null=True)
    confirmation_sentdate = models.DateField(blank=True, null=True)
    fact_sheets_sentdate = models.DateField(blank=True, null=True)
    hold_sentdate = models.DateField(blank=True, null=True)
    extra_sentdate = models.DateField(blank=True, null=True)

    contract_rcvddate = models.DateField(blank=True, null=True)
    deposit_rcvddate = models.DateField(blank=True, null=True)
    final_rcvddate = models.DateField(blank=True, null=True)
    music_list_rcvddate = models.DateField(blank=True, null=True)
    musicians_rcvddate = models.DateField(blank=True, null=True)
    confirmation_rcvddate = models.DateField(blank=True, null=True)
    fact_sheets_rcvddate = models.DateField(blank=True, null=True)
    extra_rcvddate = models.DateField(blank=True, null=True)

    contract_rcptdate = models.DateField(blank=True, null=True)
    deposit_rcptdate = models.DateField(blank=True, null=True)
    final_rcptdate = models.DateField(blank=True, null=True)
    extra_rcptdate = models.DateField(blank=True, null=True)
    
    contract_duedate = models.DateField(blank=True, null=True)
    deposit_duedate = models.DateField(blank=True, null=True)
    final_duedate = models.DateField(blank=True, null=True)
    music_list_duedate = models.DateField(blank=True, null=True)
    musicians_duedate = models.DateField(blank=True, null=True)
    confirmation_duedate = models.DateField(blank=True, null=True)
    fact_sheets_duedate = models.DateField(blank=True, null=True)
    extra_duedate = models.DateField(blank=True, null=True)

    contract_senddate = models.DateField(blank=True, null=True)
    deposit_senddate = models.DateField(blank=True, null=True)
    final_senddate = models.DateField(blank=True, null=True)
    music_list_senddate = models.DateField(blank=True, null=True)
    musicians_senddate = models.DateField(blank=True, null=True)
    confirmation_senddate = models.DateField(blank=True, null=True)
    fact_sheets_senddate = models.DateField(blank=True, null=True)
    extra_senddate = models.DateField(blank=True, null=True)
    
        
    flag_hold = models.BooleanField(default=False)    
    flag_hold_sent = models.BooleanField(default=False)

    flag_contract_sent = models.BooleanField(default=False)
    flag_contract_rcvd = models.BooleanField(default=False)
    flag_contract_rcpt = models.BooleanField(default=False)
    
    flag_deposit_sent = models.BooleanField(default=False)
    flag_deposit_rcvd = models.BooleanField(default=False)
    flag_deposit_rcpt = models.BooleanField(default=False)
    
    flag_music_list_sent = models.BooleanField(default=False)
    flag_music_list_rcvd = models.BooleanField(default=False)
    
    flag_musicians_sent = models.BooleanField(default=False)
    flag_musicians_rcvd = models.BooleanField(default=False)
    
    flag_final_payment_sent = models.BooleanField(default=False)
    flag_final_payment_rcvd = models.BooleanField(default=False)
    flag_final_payment_rcpt = models.BooleanField(default=False)
    
    flag_extra_sent = models.BooleanField(default=False)
    flag_extra_rcvd = models.BooleanField(default=False)
    flag_extra_rcpt = models.BooleanField(default=False)

    flag_final_confirmation_sent = models.BooleanField(default=False)
    flag_final_confirmation_rcvd = models.BooleanField(default=False)
    
    flag_fact_sheets_sent = models.BooleanField(default=False)
    flag_fact_sheets_rcvd = models.BooleanField(default=False)

    waive_music_list = models.BooleanField(default=False)
    accept_custom = models.BooleanField(default=False)

    automation = models.BooleanField(default=False)
    reminderdisable = models.BooleanField(default=False)
    
class BulkConvert(models.Model):
    bulktext = models.TextField(blank=True)
    

