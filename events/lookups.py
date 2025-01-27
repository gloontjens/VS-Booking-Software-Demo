from selectable.base import ModelLookup, LookupBase
from selectable.registry import registry
from django.db.models import Q
from django.db.models import F
from .models import Event, Venue, EventType, Ensemble, Contact, DayofContact, Musician, MusicianInstrument, MusicList
from datetime import date
from dateutil.relativedelta import relativedelta

from events import variables





class MusicListLookup(LookupBase):
    def get_query(self, request, term):
        #CurrentMusicList = ['orange','apple','pear']
#         data = ['Pachelbel Canon', 'Wedding March', 'La Rejouissance', 'Jesu, Joy of Mans Desiring']
        return [x for x in variables.currentmusiclist if term.lower() in x.lower()]


class SearchLookup(ModelLookup):
    model = Event
    search_fields = ('name__icontains','date__icontains')
    def get_item_label(self, item):
        if item.date.day < 10:
            thisday = '0' + str(item.date.day)
        else:
            thisday = str(item.date.day)
        if item.type == 'HD':
            thisname = '[HD] ' + item.name
        else:
            thisname = item.name
        return u"%s, %i-%s" % (thisname, item.date.month, thisday)
    def get_item_value(self, item):
        return u"%s {%i}" % (item.name, item.pk)
    def get_query(self, request, term):
        today = date.today()
        results = super(SearchLookup, self).get_query(request, term)
        results = results.filter(date__gt=today).filter(event_archived=False)
        results = results.order_by("date")
        return results    
    

class VenueLookup(ModelLookup):
    model = Venue
    search_fields = ('name__icontains',)
    def get_query(self, request, term):
        results = super(VenueLookup, self).get_query(request, term)
        results = results.order_by("order", "id")
        return results
    
class EventTypeLookup(ModelLookup):
    model = EventType
    search_fields = ('name__icontains',)
    def get_query(self, request, term):
        results = super(EventTypeLookup, self).get_query(request, term)
        results = results.order_by("order", "id")
        return results

class EnsembleLookup(ModelLookup):
    model = Ensemble
    search_fields = ('name__icontains',)
    def get_query(self, request, term):
        results = super(EnsembleLookup, self).get_query(request, term)
        results = results.order_by("order", "id")
        return results

class ContactLookup(ModelLookup):
    model = Contact
    search_fields = ('name__icontains',)
    def get_query(self, request, term):
        results = super(ContactLookup, self).get_query(request, term)
        results = results.order_by("order", "id")
        return results

class DayofcontactLookup(ModelLookup):
    model = DayofContact
    search_fields = ('name__icontains',)
    def get_query(self, request, term):
        results = super(DayofcontactLookup, self).get_query(request, term)
        results = results.order_by("order", "id")
        return results
    
class MusicianLookup(ModelLookup):
    model = Musician
    search_fields = ('name__icontains',)
    def get_query(self, request, term):
        results = super(MusicianLookup, self).get_query(request, term)
        instrument = request.GET.get('instrument', '')
        if instrument:
            results = results.filter(Q(instrument=instrument) | Q(instrument2=instrument))
        results = results.order_by("order", "id")
        return results
    
class InstrumentLookup(ModelLookup):
    model = MusicianInstrument
    search_fields = ('instrument__icontains',)
    def get_item_label(self, item):
        return u"%s" % item.instrument
    def get_item_value(self, item):
        return item.instrument
    def get_query(self, request, term):
        results = super(InstrumentLookup, self).get_query(request, term)
        results = results.order_by("order", "id")
        return results
    

registry.register(VenueLookup)
registry.register(EventTypeLookup)
registry.register(EnsembleLookup)
registry.register(ContactLookup)
registry.register(DayofcontactLookup)
registry.register(MusicianLookup)
registry.register(InstrumentLookup)
registry.register(SearchLookup)
registry.register(MusicListLookup)


