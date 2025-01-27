@csrf_exempt
def get_flags(request):
    if request.is_ajax():
        event_id = request.GET['event_id']
        hold_until = request.GET['hold_until']
        event = Event.objects.get(id=event_id)
        
        deposit_pastdue = event.is_deposit_past_due
        contract_pastdue = event.is_contract_past_due
        music_list_pastdue = event.is_music_list_past_due
        musicians_pastdue = event.is_musicians_past_due
        final_pay_pastdue = event.is_final_pay_past_due
        final_confirmation_pastdue = event.is_final_confirmation_past_due
        fact_sheets_pastdue = event.is_fact_sheets_past_due
        
        hold = event.flag_hold
        hold_past_due = event.is_hold_past_due
        #if hold_until (newly entered, unsaved value) is not blank, check it instead!
        if hold_until:
            new_hold_date = datetime.strptime(hold_until,"%m/%d/%y").date()
            hold_past_due = (date.today() > new_hold_date)
        contract_sent = event.flag_contract_sent
        contract_rcvd = event.flag_contract_rcvd
        deposit_sent = event.flag_deposit_sent
        deposit_rcvd = event.flag_deposit_rcvd
        music_list_sent = event.flag_music_list_sent
        music_list_rcvd = event.flag_music_list_rcvd
        musicians_sent = event.flag_musicians_sent
        musicians_rcvd = event.flag_musicians_rcvd
        final_payment_sent = event.flag_final_payment_sent
        final_payment_rcvd = event.flag_final_payment_rcvd
        final_confirmation_sent = event.flag_final_confirmation_sent
        final_confirmation_rcvd = event.flag_final_confirmation_rcvd
        fact_sheets_sent = event.flag_fact_sheets_sent
        fact_sheets_rcvd = event.flag_fact_sheets_rcvd
        
        data = {'hold':hold, 'hold_past_due':hold_past_due, 'contract_sent':contract_sent, 'contract_rcvd':contract_rcvd,
                'deposit_sent':deposit_sent, 'deposit_rcvd':deposit_rcvd,
                'music_list_pastdue':music_list_pastdue, 'musicians_pastdue':musicians_pastdue,
                'final_pay_pastdue':final_pay_pastdue, 'final_confirmation_pastdue':final_confirmation_pastdue,
                'fact_sheets_pastdue':fact_sheets_pastdue,
                'deposit_pastdue':deposit_pastdue, 'music_list_sent':music_list_sent,
                'music_list_rcvd':music_list_rcvd, 'musicians_sent':musicians_sent,'musicians_rcvd':musicians_rcvd,
                'final_payment_sent':final_payment_sent, 'final_payment_rcvd':final_payment_rcvd,
                'final_confirmation_sent':final_confirmation_sent, 'final_confirmation_rcvd':final_confirmation_rcvd,
                'fact_sheets_sent':fact_sheets_sent, 'fact_sheets_rcvd':fact_sheets_rcvd,
                'contract_pastdue':contract_pastdue,}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")




#FORWARD:
    else:
        skipped = 0 
        if mode == "WEEK":
            browse_date = old_date + relativedelta(weekday=calendar.MONDAY)
            if browse_date == old_date:
                browse_date = old_date + relativedelta(weekday=calendar.MONDAY, weeks=1)
            until = browse_date + relativedelta(weekday=calendar.SUNDAY)
            events = Event.objects.filter(date__range=[browse_date, until]).exclude(
                event_archived=True).order_by('date','start_time')
            while not events:
                skipped = 1
                browse_date = browse_date + relativedelta(weekday=calendar.MONDAY, weeks=1)
                until = browse_date + relativedelta(weekday=calendar.SUNDAY)
                events = Event.objects.filter(date__range=[browse_date, until]).exclude(
                    event_archived=True).order_by('date','start_time')
        elif mode == "MONTH":
            browse_date = old_date + relativedelta(day=1, months=+1)
            if browse_date == old_date:
                browse_date = old_date + relativedelta(day=1, months=+1)
            until = browse_date + relativedelta(day=31)
            events = Event.objects.filter(date__range=[browse_date, until]).exclude(
                event_archived=True).order_by('date','start_time')
            while not events:
                skipped = 1
                browse_date = browse_date + relativedelta(day=1, months=+1)
                until = browse_date + relativedelta(day=31)
                events = Event.objects.filter(date__range=[browse_date, until]).exclude(
                    event_archived=True).order_by('date','start_time')
        elif mode == "DAY":
            browse_date = old_date + relativedelta(days=+1)
            until = browse_date
            events = Event.objects.filter(date__range=[browse_date, until]).exclude(
                event_archived=True).order_by('date','start_time')
            while not events:
                skipped = 1
                browse_date = browse_date + relativedelta(days=+1)
                until = browse_date
                events = Event.objects.filter(date__range=[browse_date, until]).exclude(
                    event_archived=True).order_by('date','start_time')      
        old_record = Global.objects.get(pk=1)
        old_record.browse_date = browse_date
        old_record.save()
        return redirect('/events/browse/' + str(skipped))



#BACKWARD
    else:
        skipped = 0
        if mode == "WEEK":
            browse_date = old_date + relativedelta(weekday=calendar.MONDAY, weeks=-1)
            until = browse_date + relativedelta(weekday=calendar.SUNDAY)
            events = Event.objects.filter(date__range=[browse_date, until]).exclude(
                event_archived=True).order_by('date','start_time')
            while not events:
                skipped = 1
                browse_date = browse_date + relativedelta(weekday=calendar.MONDAY, weeks=-1)
                until = browse_date + relativedelta(weekday=calendar.SUNDAY)
                events = Event.objects.filter(date__range=[browse_date, until]).exclude(
                    event_archived=True).order_by('date','start_time')
        elif mode == "MONTH":
            browse_date = old_date + relativedelta(day=1)
            if browse_date == old_date:
                browse_date = old_date + relativedelta(day=1, months=-1)
            until = browse_date + relativedelta(day=31)
            events = Event.objects.filter(date__range=[browse_date, until]).exclude(
                event_archived=True).order_by('date','start_time')
            while not events:
                skipped = 1
                browse_date = browse_date + relativedelta(day=1, months=-1)
                until = browse_date + relativedelta(day=31)
                events = Event.objects.filter(date__range=[browse_date, until]).exclude(
                    event_archived=True).order_by('date','start_time')
        elif mode == "DAY":
            browse_date = old_date + relativedelta(days=-1)
            until = browse_date
            events = Event.objects.filter(date__range=[browse_date, until]).exclude(
                event_archived=True).order_by('date','start_time')
            while not events:
                skipped = 1
                browse_date = browse_date + relativedelta(days=-1)
                until = browse_date
                events = Event.objects.filter(date__range=[browse_date, until]).exclude(
                    event_archived=True).order_by('date','start_time')      
        old_record = Global.objects.get(pk=1)
        old_record.browse_date = browse_date
        old_record.save()
        return redirect('/events/browse/' + str(skipped))


















