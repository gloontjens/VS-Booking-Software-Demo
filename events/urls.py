

from django.conf.urls import url
from . import views
from django.urls import include, path 
from django.contrib.auth.decorators import login_required
from .views import VenueCreatePopup, VenueEditPopup, get_venue_id, get_venue_info,get_event_type_id, get_ensemble_id
from .views import ContactCreatePopup, ContactEditPopup, get_contact_id, get_contact_info, get_rates
from .views import DayofcontactCreatePopup, DayofcontactEditPopup, get_dayofcontact_id, get_dayofcontact_info
from .views import set_remind_done, ReminderCreatePopup, get_reminders, editforms, search, search_results
from .views import archived, delete, unarchive, archive, browse, cycle, browse_forward, browse_backward, browse_today
from .views import tasks, edit_nextevent, gcal, mycal, pdf, email_pdf, sigtest, client_home, thankyou
from .views import ActivityCreatePopup, get_activities, activity_ajax_add, get_5_activities, get_5_reminders
from .views import mark_reminder_done, sidecalmonth, sidecalday, sidecalpanels, sidecalpanelclick, mycalmonth
from .views import sidepanelupdate, updatemusicians, updatelistofmusicians, reordermusicians
from .views import changeinstofmusician, addmusiciantoask, updatelistofaskedmusicians, deleteaskedmusician
from .views import yesaskedmusician, noaskedmusician, invitedaskedmusician, MusicianCreatePopup, inquiry
from .views import updatepaypal, send_email_mail, switchautomation, get_booked_musicians, get_musiclist
from .views import reminder_edit_automation, reminder_edit_regular, toggle_auto, toggle_side_auto
from .views import process_ajax_due_dates, syncgcal, syncgcal_deleteold, syncgcal_savenew, concurrent
from .views import disablebuiltin, musician_edit, gotitaskedmusician, gauthorize, gcallback, checkremindersautostatus
from .views import rates, get_rate_chart, payments_received, payments_due, payments_received_older, payments_due_older
from .views import editratecharts, ratechartdelete, markpayduedone, test_selenium, esigdelete, editesig, esigs, toggle_show_pd
from .views import reports, after_email, fakeajax, flipheader, get_activities_num, check_music_list, check_accept_custom
from .views import get_id_from_value, bulk_convert, toggle_home_panels, transition, webhook, savepaypalid
from .views import specialfeechangemusicians, specialfeechangeaskedmusicians, client_confirm_event
from .views import MusiclistCreatePopup, reorderdragmusicians



urlpatterns = [
#     url(r'^events/tasks/$', login_required(views.tasks), name="tasks"),
    path('pdf/', pdf.as_view(), name="pdf"),
    url(r'^thankyou/$', views.thankyou, name="thankyou"),
    url(r'^events/webhook', views.webhook, name="webhook"),
    url(r'^events/savepaypalid', views.savepaypalid, name="savepaypalid"),
    url(r'^events/client_home/(?P<eventnum>\d+)/(?P<mode>[-\w]+)', views.client_home, name="clienthome"),
    url(r'^events/client_home/(?P<eventnum>\d+)/$', views.client_home, name="clienthome"),
    url(r'^events/concurrent/(?P<eventnum>\d+)/$', views.concurrent, name="concurrent"),
    url(r'^events/sigtest/$', login_required(views.sigtest), name="sigtest"),
    path('events/inquiry/<kind>/<int:eventnum>/<email>/<firstname>', views.inquiry, name="inquiry"),
    path('events/details/<kind>/<int:eventnum>', views.client_confirm_event, name="client_confirm_event"),
#     url(r'^events/inquiry/(?P<kind>[-\w]+)/(?P<eventnum>\d+)/(?P<email>[-\w]+)', views.inquiry, name="inquiry"),
    url(r'^events/email/(?P<eventnum>\d+)/(?P<formname>[-\w]+)/$', login_required(views.email), name="email"),
    url(r'^events/email_pdf/(?P<eventnum>\d+)/(?P<formname>[-\w]+)/$', login_required(views.email_pdf), name="email_pdf"),
    url(r'^events/delete/(?P<pk>\d+)/', login_required(views.delete), name="delete"),
    url(r'^events/unarchive/(?P<pk>\d+)/', login_required(views.unarchive), name="unarchive"),
    url(r'^events/archive/(?P<pk>\d+)/', login_required(views.archive), name="archive"),
    url(r'^events/cycle/(?P<mode>[-\w]+)/$', login_required(views.cycle), name="cycle"),
    url(r'^events/browse_forward/(?P<mode>[-\w]+)/(?P<event_id>\d+)/$', login_required(views.browse_forward), name="browse_forward"),
    url(r'^events/browse_backward/(?P<mode>[-\w]+)/(?P<event_id>\d+)/$', login_required(views.browse_backward), name="browse_backward"),
    url(r'^events/browse_today/(?P<mode>[-\w]+)/$', login_required(views.browse_today), name="browse_today"),
    url(r'^events/edit_nextevent/$', login_required(views.edit_nextevent), name="browse_edit_nextevent"),
    url(r'^events/browse/(?P<skip>\d+)/$', login_required(views.browse), name="browse"),
    
    url(r'^events/payments_received_older/$', login_required(views.payments_received_older), name="payments_received_older"),
    url(r'^events/payments_due_older/$', login_required(views.payments_due_older), name="payments_due_older"),
    url(r'^events/payments_received/$', login_required(views.payments_received), name="payments_received"),
    url(r'^events/payments_due/$', login_required(views.payments_due), name="payments_due"),

    url(r'^events/rates/$', login_required(views.rates), name="rates"),
    url(r'^events/esigs/$', login_required(views.esigs), name="esigs"),
    url(r'^events/tasks/$', login_required(views.tasks), name="tasks"),
    url(r'^events/search/$', login_required(views.search), name="search"),
    url(r'^events/search_results/', search_results, name="search_results"),
    url(r'^events/$', login_required(views.home), name="home"),
    url(r'^events/reports/$', login_required(views.reports), name="reports"),
    url(r'^events/gcal/(?P<pYear>\d+)/(?P<pMonth>\d+)/$', login_required(views.gcal), name="gcal"),
    url(r'^events/mycal/$', login_required(views.mycal), name="mycal"),
    url(r'^sidecalmonth', login_required(views.sidecalmonth), name="sidecalmonth"),
    url(r'^mycalmonth', login_required(views.mycalmonth), name="mycalmonth"),
    url(r'^switchautomation', login_required(views.switchautomation), name="switchautomation"),
    url(r'^disablebuiltin', login_required(views.disablebuiltin), name="disablebuiltin"),
    url(r'^checkremindersautostatus', login_required(views.checkremindersautostatus), name="checkremindersautostatus"),
    url(r'^check_accept_custom', login_required(views.check_accept_custom), name="check_accept_custom"),
    url(r'^updatepaypal', views.updatepaypal, name="updatepaypal"),
    url(r'^events/bulk_convert', login_required(views.bulk_convert), name="bulk_convert"),
    url(r'^send_email_mail', views.send_email_mail, name="send_email_mail"),
    url(r'^check_music_list', views.check_music_list, name="check_music_list"),
    url(r'^get_id_from_value', login_required(views.get_id_from_value), name="get_id_from_value"),
    url(r'^sidecalpanels', login_required(views.sidecalpanels), name="sidecalpanels"),
    url(r'^sidecalpanelclick', login_required(views.sidecalpanelclick), name="sidecalpanelclick"),
    url(r'^sidepanelupdate', login_required(views.sidepanelupdate), name="sidepanelupdate"),
    url(r'^updatemusicians', login_required(views.updatemusicians), name="updatemusicians"),
    url(r'^updatelistofmusicians', login_required(views.updatelistofmusicians), name="updatelistofmusicians"),
    url(r'^updatelistofaskedmusicians', login_required(views.updatelistofaskedmusicians), name="updatelistofaskedmusicians"),
    url(r'^addmusiciantoask', login_required(views.addmusiciantoask), name="addmusiciantoask"),
    url(r'^deleteaskedmusician', login_required(views.deleteaskedmusician), name="deleteaskedmusician"),
    url(r'^yesaskedmusician', login_required(views.yesaskedmusician), name="yesaskedmusician"),
    url(r'^noaskedmusician', login_required(views.noaskedmusician), name="noaskedmusician"),
    url(r'^gotitaskedmusician', login_required(views.gotitaskedmusician), name="gotitaskedmusician"),
    url(r'^invitedaskedmusician', login_required(views.invitedaskedmusician), name="invitedaskedmusician"),
    url(r'^reordermusicians', login_required(views.reordermusicians), name="reordermusicians"),
    url(r'^reorderdragmusicians', login_required(views.reorderdragmusicians), name="reorderdragmusicians"),
    url(r'^specialfeechangemusicians', login_required(views.specialfeechangemusicians), name="specialfeechangemusicians"),
    url(r'^specialfeechangeaskedmusicians', login_required(views.specialfeechangeaskedmusicians), name="specialfeechangeaskedmusicians"),
    url(r'^changeinstofmusician', login_required(views.changeinstofmusician), name="changeinstofmusician"),
    url(r'^events/sidecalday/(?P<Year>\d+)/(?P<Month>\d+)/(?P<Day>\d+)/$', login_required(views.sidecalday), name="sidecalday"),
    url(r'^events/archived/$', login_required(views.archived), name="archived"),
    url(r'^events/syncgcal/$', login_required(views.syncgcal), name="syncgcal"),
    url(r'^events/gauthorize/$', login_required(views.gauthorize), name="gauthorize"),
    url(r'^events/gcallback/$', login_required(views.gcallback), name="gcallback"),
    url(r'^syncgcal_deleteold/$', login_required(views.syncgcal_deleteold), name="syncgcal_deleteold"),
    url(r'^syncgcal_savenew/$', login_required(views.syncgcal_savenew), name="syncgcal_savenew"),
    url(r'^events/add/$', login_required(views.add), name="add"),
    
    path('events/<int:pk>/edit/<path:popup2>', login_required(views.edit), name="edit"),
    url(r'^events/(?P<pk>\d+)/edit', login_required(views.edit), name="edit"),
    url(r'^events/(?P<pk>\d+)/transition', login_required(views.transition), name="transition"),
    url(r'^after_email', login_required(views.after_email), name="after_email"),
    url(r'^fakeajax', login_required(views.fakeajax), name="fakeajax"),
    url(r'^flipheader', login_required(views.flipheader), name="flipheader"),
    url(r'^get_activities_num', login_required(views.get_activities_num), name="get_activities_num"),
    
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^venue/create', VenueCreatePopup, name = "VenueCreate"),
    url(r'^venue/(?P<pk>\d+)/edit', VenueEditPopup, name = "VenueEdit"),
    url(r'^venue/ajax/get_venue_id', get_venue_id, name = "get_venue_id"),
    url(r'^venue/ajax/get_venue_info', get_venue_info, name = "get_venue_info"),
    url(r'^event_type/ajax/get_event_type_id', get_event_type_id, name = "get_event_type_id"),
    url(r'^ensemble/ajax/get_ensemble_id', get_ensemble_id, name = "get_ensemble_id"),
    url(r'^contact/create', ContactCreatePopup, name = "ContactCreate"),
    url(r'^contact/(?P<pk>\d+)/edit', ContactEditPopup, name = "ContactEdit"),
    url(r'^contact/ajax/get_contact_id', get_contact_id, name = "get_contact_id"),
    url(r'^toggle_side_auto', toggle_side_auto, name = "toggle_side_auto"),
    url(r'^process_ajax_due_dates', process_ajax_due_dates, name = "process_ajax_due_dates"),
    url(r'^toggle_auto', toggle_auto, name = "toggle_auto"),
    url(r'^toggle_home_panels', toggle_home_panels, name = "toggle_home_panels"),
    url(r'^toggle_show_pd', toggle_show_pd, name = "toggle_show_pd"),
    url(r'^contact/ajax/get_contact_info', get_contact_info, name = "get_contact_info"),
    url(r'^dayofcontact/create', DayofcontactCreatePopup, name = "DayofcontactCreate"),
    url(r'^dayofcontact/(?P<pk>\d+)/edit', DayofcontactEditPopup, name = "DayofcontactEdit"),
    
    url(r'^reminder/(?P<pk>\d+)/edit_automation', reminder_edit_automation, name = "reminder_edit_automation"),
    url(r'^reminder/(?P<pk>\d+)/edit_regular', reminder_edit_regular, name = "reminder_edit_regular"),
    url(r'^musician/(?P<pk>\d+)/edit', musician_edit, name = "musician_edit"),
    
    url(r'^dayofcontact/ajax/get_dayofcontact_id', get_dayofcontact_id, name = "get_dayofcontact_id"),
    url(r'^dayofcontact/ajax/get_dayofcontact_info', get_dayofcontact_info, name = "get_dayofcontact_info"),
    url(r'^rates/ajax/get_rates', get_rates, name = "get_rates"),
    url(r'^rates/ajax/get_rate_chart', get_rate_chart, name = "get_rate_chart"),
    url(r'^remind/ajax/set_remind_done', set_remind_done, name = "set_remind_done"),
    url(r'^activity/ajax/add', activity_ajax_add, name = "activity_ajax_add"),
    
    url(r'^remind/(?P<pk>\d+)/create', ReminderCreatePopup, name = "ReminderCreate"),
    url(r'^musician/(?P<pk>\d+)/create', MusicianCreatePopup, name = "MusicianCreate"),
    path('musiclist/<int:ensnum>/<int:pk>/<str:cer>/create', MusiclistCreatePopup, name = "MusiclistCreate"),
    
    url(r'^events/mark_reminder_done/(?P<reminder_id>\d+)', mark_reminder_done, name = "mark_reminder_done"),
    url(r'^activity/(?P<pk>\d+)/create', ActivityCreatePopup, name = "ActivityCreate"),
    url(r'^remind/None/create', ReminderCreatePopup, name = "ReminderCreate"),
    url(r'^remind/ajax/get_reminders', get_reminders, name = "get_reminders"),
    url(r'^remind/ajax/get_activities', get_activities, name = "get_activities"),
    url(r'^remind/ajax/get_5_activities', get_5_activities, name = "get_5_activities"),
    url(r'^remind/ajax/get_5_reminders', get_5_reminders, name = "get_5_reminders"),
    url(r'^remind/ajax/get_booked_musicians', get_booked_musicians, name = "get_booked_musicians"),
    url(r'^ratechartdelete', ratechartdelete, name = "ratechartdelete"),
    url(r'^esigdelete', esigdelete, name = "esigdelete"),
    url(r'^events/test_selenium', test_selenium, name = "test_selenium"),
    url(r'^markpayduedone', markpayduedone, name = "markpayduedone"),
    url(r'^remind/ajax/get_musiclist', get_musiclist, name = "get_musiclist"),
    url(r'^events/editforms/', login_required(views.editforms), name="editforms"),
    url(r'^events/editratecharts/(?P<chartname>[-\w]+)', login_required(views.editratecharts), name="editratecharts"),
    url(r'^events/editesig/(?P<chartname>[-\w]+)', login_required(views.editesig), name="editesig"),
    url(r'^events/editform/(?P<form>\d+)/', login_required(views.editform), name="editform"),
    url(r'^tinymce/', include('tinymce.urls')),
    ]

