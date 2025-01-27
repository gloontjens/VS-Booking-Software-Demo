

from django import forms
from django.conf import settings
from django.forms import formset_factory 
from material import Layout, Row 
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from selectable.forms import AutoComboboxWidget, AutoCompleteSelectWidget



from .models import Event, ESig, Client, ClientEmail, Venue, Contact, Activity, DayofContact, Reminder, FormEmail, FormHtml, Sig, Musician
# from django.forms.widgets import SelectDateWidget

import selectable.forms as selectable

from .lookups import VenueLookup, EventTypeLookup, EnsembleLookup, SearchLookup, MusicListLookup
from .lookups import ContactLookup, DayofcontactLookup, MusicianLookup, InstrumentLookup
from events.models import RateChart
from tinymce import TinyMCE

    
class SigForm(forms.ModelForm):
#     date = forms.DateField(
#             input_formats=(settings.DATE_INPUT_FORMATS)
#     )
    class Meta:
        model = Sig
        fields = ('__all__')

class ESigForm(forms.ModelForm):
    class Meta:
        model = ESig()
        fields = ('__all__')
        labels = {
            'sig': ('Signature:'),
        }

class TransitionForm(forms.ModelForm):  
    paid_deposit_date = forms.DateField(input_formats=(settings.DATE_INPUT_FORMATS))
    paid_final_date = forms.DateField(input_formats=(settings.DATE_INPUT_FORMATS))
    paid_extra_date = forms.DateField(input_formats=(settings.DATE_INPUT_FORMATS))
    paid_total_date = forms.DateField(input_formats=(settings.DATE_INPUT_FORMATS))
    music_list_date = forms.DateField(input_formats=(settings.DATE_INPUT_FORMATS))
    verify_info_date = forms.DateField(input_formats=(settings.DATE_INPUT_FORMATS))
    signature_date = forms.DateField(input_formats=(settings.DATE_INPUT_FORMATS))
    class Meta:
        model = Client
        fields = ['event', 'paid_deposit', 'paid_final', 'paid_extra', 'paid_total',
                  'paid_online', 'paid_final_online', 'paid_extra_online',
                  'did_music_list', 'did_verify_info', 'did_sign',
                  'paid_deposit_date', 'paid_final_date', 'paid_extra_date', 'paid_total_date',
                  'music_list_date', 'verify_info_date', 'started', 'transition',
                  'signature_date'] 
             

class ClientForm(forms.ModelForm):
    
    signature_date = forms.DateField(
            input_formats=(settings.DATE_INPUT_FORMATS)
    )
    class Meta:
        model = Client
#         fields = ('__all__')
        fields = ['signature_date', 'signature', 'signature_email',
                  'signature_name', 'paid_deposit',
                  'paid_final', 'paid_total', 'paid_online', 'paid_final_online',
                  'signature_date', 'paid_deposit_date',
                  'paid_final_date', 'paid_total_date', 'did_music_list',
                  'contract_pdf', 'did_verify_info', 'did_sign',
                  'music_list_date', 'verify_info_date'
                  ]
        widgets = {
            'contract_pdf': TinyMCE(mce_attrs={
                        'height': 'auto',
                        'width': 'auto',
                        'cleanup_on_startup': True,
                        'custom_undo_redo_levels': 20,
                        'selector': 'textarea',
                        'theme': 'modern',
                        'plugins': '''
                                autoresize textcolor preview
                                insertdatetime image nonbreaking
                                contextmenu print 
                                autolink hr
                                ''',
                        'toolbar1': '''
                                print 
                                ''',
                        'contextmenu': 'preview | undo redo copy paste | edit format formats | fontsizeselect| hr',
                        'menubar': False,
                        'statusbar': False,
                        'toolbar': False,
                        #'inline': True,
                        'preformatted': True,
                        'autoresize_bottom_margin': 10,
#                         'max_height': 600,
#                         'min_height': 200,
#                        'min_width': 600,
                        'force_br_newlines': True,
                        'force_p_newlines': False,
                        'forced_root_block': False,
                        'entity_encoding': 'raw',
                        'readonly': True,
                        'convert_urls:': False,
                        'relative_urls': False,
                        'remove_script_host': False,
                        }),
            }

class ClientEmailForm(forms.ModelForm):
    class Meta:
        model = ClientEmail
        fields = ['event', 'from_email', 'subject', 'body']
        labels = {'from_email': ('Your Email Address'),'body': ('Your Message'),}
    
class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ('__all__')
        
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('__all__')

class DayofcontactForm(forms.ModelForm):
    class Meta:
        model = DayofContact
        fields = ('__all__')

class MusicianForm(forms.ModelForm):
    class Meta:
        model = Musician
        fields = ('__all__')
        
        
class ReminderForm(forms.ModelForm):
    date = forms.DateField(
            input_formats=(settings.DATE_INPUT_FORMATS)
    )
    class Meta:
        model = Reminder
        fields = ['name','date', 'disb']
        labels = {
            'name': ('Reminder'),
            'date': ('Due Date'),
            'disb': ('Disable?')
        }
        
class ReminderFormAuto(forms.ModelForm):
    date = forms.DateField(
            input_formats=(settings.DATE_INPUT_FORMATS)
    )
    class Meta:
        model = Reminder
        fields = ['name','date', 'done', 'auto', 'disb']
        labels = {
            'name': ('Reminder'),
            'date': ('Due Date'),
            'done': ('Mark as Done'),
            'auto': ('Enable Automation'),
            'disb': ('Disable?')
        }


class ActivityForm(forms.ModelForm):
    date = forms.DateField(
            input_formats=(settings.DATE_INPUT_FORMATS)
    )
    class Meta:
        model = Activity
        fields = ['name','date']
        labels = {
            'name': ('Activity'),
            'date': ('Date')
        }

class FormEmailForm(forms.ModelForm):
    #body = forms.CharField(widget=TinyMCE())
    class Meta:
        model = FormEmail
        fields = ('body', 'subject', 'addr', 'pdf')
        
class FormHtmlForm(forms.ModelForm):
    #body = forms.CharField(widget=TinyMCE())
    class Meta:
        model = FormHtml
        fields = ('__all__')
        
class FormRateChart(forms.ModelForm):
    class Meta:
        model = RateChart()
        fields = ('__all__')
        
class SearchForm(forms.Form):
    search = forms.CharField(
        label='Search',
        widget=AutoComboboxWidget(SearchLookup),
        required=False,
    )

class MusicListForm(forms.Form):
    list = forms.CharField(
        label='List',
        widget=AutoCompleteSelectWidget(MusicListLookup),
        required=False,
    )
    

class AddForm(forms.ModelForm):
    
    date = forms.DateField(
            input_formats=(settings.DATE_INPUT_FORMATS)
    )
#     end_time = forms.TimeField(
#             input_formats=(settings.TIME_INPUT_FORMATS)
#     )
#     ceremony_time = forms.TimeField(
#             input_formats=(settings.TIME_INPUT_FORMATS)
#     )
    
#     layout = Layout(
#         Row('type', 'hold_until', 'waive_contract', 'waive_payment', 'name', 'friendly_name'),
#         Row('date', 'start_time', 'end_time', 'ceremony_time'),
#         Row('event_type', 'ensemble', 'ensemble_number'),
#         Row('location', 'location_details', 'location_outdoors', 'location_add',
#             'location_address', 'location_link', 'location_phone', 'location_email'),
#         Row('contact', 'contact_add', 'contact_details', 'contact_agency', 'contact_phone', 'contact_email'),
#         Row('dayofcontact', 'dayofcontact_add', 'dayofcontact_details', 'dayofcontact_phone', 'dayofcontact_email'),
#         Row('fee', 'musician_fee', 'contracting_fee', 'deposit_fee', 'final_fee', 'cash_fee')
#         )
          
    class Meta:
        model = Event
#         fields = ('__all__')
        #notes = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

        fields = ['type','hold_until','hold_released','event_archived','name','friendly_name','date','start_time',
                  'event_reminders_done','end_time','ceremony_time','event_type','event_type_name','waive_contract',
                  'waive_payment','ensemble','ensemble_name','ensemble_number','location',
                  'location_details','location_outdoors','location_add','location_name',
                  'location_address','location_link','location_phone','location_email',
                  'contact','contact_details','contact_add','contact_name','contact_agency',
                  'contact_phone','contact_email','dayofcontact','dayofcontact_details',
                  'dayofcontact_add','dayofcontact_name','dayofcontact_phone',
                  'dayofcontact_email','fee','contracting_fee','musician_fee',
                  'deposit_fee','deposit_date','final_fee','final_date','cash_fee',
                  'color_contract', 'color_deposit', 'color_music_list',
                  'color_musicians', 'color_final_payment', 'color_final_confirmation',
                  'color_fact_sheets', 'contract_sentdate', 'deposit_sentdate',
                  'final_sentdate', 'music_list_sentdate', 'musicians_sentdate',
                  'confirmation_sentdate', 'fact_sheets_sentdate',
                  'contract_duedate', 'deposit_duedate',
                  'final_duedate', 'music_list_duedate', 'musicians_duedate',
                  'confirmation_duedate', 'fact_sheets_duedate',
                  'contract_senddate', 'deposit_senddate',
                  'final_senddate', 'music_list_senddate', 'musicians_senddate',
                  'confirmation_senddate', 'fact_sheets_senddate',
                  'contract_rcvddate', 'deposit_rcvddate',
                  'final_rcvddate', 'music_list_rcvddate', 'musicians_rcvddate',
                  'confirmation_rcvddate', 'fact_sheets_rcvddate',
                  'contract_rcptdate', 'deposit_rcptdate',
                  'final_rcptdate', 'dress_code',                 
                  'flag_hold', 'flag_hold_sent', 'flag_contract_sent', 'flag_contract_rcvd',
                  'flag_deposit_sent', 'flag_deposit_rcvd',
                  'flag_music_list_sent', 'flag_music_list_rcvd',
                  'flag_musicians_sent', 'flag_musicians_rcvd',
                  'flag_final_payment_sent', 'flag_final_payment_rcvd',
                  'flag_final_confirmation_sent', 'flag_final_confirmation_rcvd',
                  'flag_fact_sheets_sent', 'flag_fact_sheets_rcvd',
                  'flag_contract_rcpt', 'flag_deposit_rcpt', 'flag_final_payment_rcpt',
                  'signature_date', 'signature', 'officiant_info', 'notes', 'records',
                  'recessional_cue', 'number_bridesmaids', 'number_parents', 'waive_music_list', 'music_list',
                  'musician', 'instrument', 'automation', 'version', 'date_entered',
                  'reminders_bar_hidden', 'reminderdisable', 'hold_sentdate',
                  'extra_fee', 'extra_sentdate', 'extra_rcvddate', 'extra_rcptdate',
                  'extra_duedate', 'extra_senddate', 'flag_extra_sent', 'flag_extra_rcvd',
                  'flag_extra_rcpt', 'accept_custom', 'flowergirls',
                  'dayofcontact_alone_name', 'dayofcontact_alone_phone', 'number_guests'
                  ]
#         help_texts = {
#             'name': ('Bride and/or Groom, or general event name'),
#             'friendly_name': ('Email greeting'),
#             'location': ('Select or type'),
#             'contact': ('Select or type'),
#             'dayofcontact': ('Select or type'),
#             'event_type': ('Select or type'),
#             'ensemble': ('Select or type'),
#             'ensemble_number': (''),
#             'date': (''),
#         }
        widgets = {
            'location': selectable.AutoComboboxSelectWidget(lookup_class=VenueLookup),
            'event_type': selectable.AutoComboboxSelectWidget(lookup_class=EventTypeLookup),
            'ensemble': selectable.AutoComboboxSelectWidget(lookup_class=EnsembleLookup),
            'contact': selectable.AutoComboboxSelectWidget(lookup_class=ContactLookup),
            'dayofcontact': selectable.AutoComboboxSelectWidget(lookup_class=DayofcontactLookup),
            'musician': selectable.AutoComboboxWidget(lookup_class=MusicianLookup),
            'instrument': selectable.AutoComboboxWidget(lookup_class=InstrumentLookup),
#             'search': selectable.AutoComboboxWidget(lookup_class=SearchLookup),
            'notes': TinyMCE(mce_attrs={
                        'height': 106,
                        'width': 'auto',
                        'toolbar_items_size': 'small',
                        'cleanup_on_startup': True,
                        'custom_undo_redo_levels': 20,
                        'selector': 'textarea',
                        'theme': 'modern',
                        'plugins': '''
                                autoresize paste textcolor preview
                                insertdatetime image nonbreaking
                                contextmenu 
                                autolink hr
                                ''',
                        'toolbar1': '''
                                bold italic underline | 
                                fontsizeselect forecolor |
                                ''',
                        'contextmenu': 'preview | undo redo copy paste pastetext | bold italic underline | edit format formats | fontsizeselect| hr',
                        'menubar': False,
                        'paste_as_text': True,
                        'statusbar': False,
                        'toolbar': False,
#                         'inline': True,
#                         'inline': True,
                        'preformatted': True,
                        'autoresize_bottom_margin': 7,
                        'autoresize_max_height': 900,
                        'autoresize_min_height': 106,
                        'force_br_newlines': True,
                        'force_p_newlines': False,
                        'forced_root_block': False,
                        'entity_encoding': 'raw',
                        'convert_urls:': False,
                        'relative_urls': False,
                        'remove_script_host': False,
                        'content_style': 'body { font-size: 13px; }',
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        #'setup': 'function(ed) { ed.onClick.add(function(ed, e) { alert("Editor was clicked"); }); }',
                        }),
            'records': TinyMCE(mce_attrs={
                        'height': 325,
                        'width': 'auto',
                        'toolbar_items_size': 'small',
                        'cleanup_on_startup': True,
                        'custom_undo_redo_levels': 20,
                        'selector': 'textarea',
                        'theme': 'modern',
                        'plugins': '''
                                autoresize paste textcolor preview
                                insertdatetime  nonbreaking
                                contextmenu image table
                                autolink hr insertdatetime
                                ''',
                        'toolbar1': '''
                                bold italic underline | 
                                fontsizeselect forecolor backcolor | insertdatetime |
                                ''',
                        'contextmenu': 'preview | undo redo copy paste pasttext | bold italic underline | edit format formats | fontsizeselect| hr',
                        'menubar': False,
                        'paste_as_text': True,
                        'statusbar': False,
                        'toolbar': True,
#                         'inline': True,
                        'preformatted': True,
                        'autoresize_bottom_margin': 7,
                        'autoresize_max_height': 900,
                        'autoresize_min_height': 325,
                        'force_br_newlines': True,
                        'force_p_newlines': False,
                        'forced_root_block': False,
                        'entity_encoding': 'raw',
                        'convert_urls:': False,
                        'relative_urls': False,
                        'remove_script_host': False,
                        'content_style': 'body { font-size: 13px; }',
                        'insertdatetime_timeformat': '%A, %B %d, %Y (at %I:%M%p)',
                        'insertdatetime_dateformat': '%A, %B %d, %Y (at %I:%M%p)',
                        'insertdatetime_formats': ["<b><font color='#0000ff'>%A, %B %d, %Y (at %I:%M%p)<font color='#0000ff'></b>:", "<b>%A, %B %d, %Y (at %I:%M%p)</b>:", "%A, %B %d, %Y"],
                        #'setup': 'function(ed) { ed.onClick.add(function(ed, e) { alert("Editor was clicked"); }); }',
                        }),
            
            'music_list': TinyMCE(mce_attrs={
                        'height': 59,
                        'width': 'auto',
                        'toolbar_items_size': 'small',
                        'cleanup_on_startup': True,
                        'custom_undo_redo_levels': 20,
                        'selector': 'textarea',
                        'theme': 'modern',
                        'plugins': '''
                                autoresize paste textcolor preview
                                insertdatetime image nonbreaking
                                contextmenu 
                                autolink hr
                                ''',
                        'toolbar1': '''
                                bold italic underline | 
                                fontsizeselect forecolor |
                                ''',
                        'contextmenu': 'preview | undo redo copy paste pastetext | bold italic underline | edit format formats | fontsizeselect| hr',
                        'menubar': False,
                        'paste_as_text': True,
                        'statusbar': False,
                        'toolbar': False,
                        #'inline': True,
                        'preformatted': True,
                        'autoresize_bottom_margin': 4,
                        'autoresize_max_height': 350,
                        'autoresize_min_height': 59,
                        'force_br_newlines': True,
                        'force_p_newlines': False,
                        'forced_root_block': False,
                        'entity_encoding': 'raw',
                        'convert_urls:': False,
                        'relative_urls': False,
                        'remove_script_host': False,
                        'content_style': 'body { font-size: 13.5px; background-color: #78909c; color: white; }',
#                         'content_css': staticfiles_storage.url('css/tinymce.css'),
                        }),
            
        }
        labels = {
            'ceremony_time': ('Ceremony'),
            'ensemble_number': ('Number'),
            'location_add': ('Save?'),
            'location_outdoors': ('Outdoors'),
            'contact_add': ('Save?'),
            'dayofcontact_add': ('Save?'),
            'dayofcontact_details': ('Note...'),
            'contact_details': ('Note...'),
            'location_details': ('Note...'),
            'fee': ('Total'),
            'musician_fee':('Musician'),
            'deposit_fee':('Deposit'),
            'final_fee':('Final'),
            'contracting_fee':('Contracting'),
            'extra_fee':('Extra'),
            'cash_fee':('Cash'),
            'deposit_date':('Date Rcvd'),
            'final_date':('Date Rcvd'),
            'contact_agency':('Agency'),
            'contact_phone':('Phone'),
            'contact_email':('Email'),
            'dayofcontact_phone':('Phone'),
            'dayofcontact_email':('Email'),
            'location_address':('Address'),
            'location_phone':('Phone'),
            'location_email':('Email'),
            'location_link':('Link'),
            'start_time':('Start'),
            'end_time':('End'),
            'waive_music_list':('Waive Music List'),
            'waive_contract':('Waive Contract'),
            'waive_payment':('Waive Payment'),
            'officiant_info':('Officiant\'s Info'),
            'recessional_cue':('Recessional Cue'),
            'instrument':('Inst.'),
            'musician':('Add Musician'),
            'friendly_name':("Friendly Name"),
            'date':('Event Date'),
            'name':("Name of Event or Person(s)"),
            'type':("Booking"),
            'dayofcontact':("Day-Of Contact"),
            'number_bridesmaids':("bridesmaids"),
            'number_parents':("parents"),
            'dayofcontact_alone_name':("Day-of-only Name"),
            'dayofcontact_alone_phone':("Day-of-only Phone"),
            'number_guests':("Guests"),
        }



