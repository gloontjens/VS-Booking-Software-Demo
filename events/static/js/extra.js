

//TODO:(partially working, first time on page load only for now - pop-up calendar on focus, not just on click
//      add other calendars when working fully
$("#id_date").one('focus', function() {
//     event.stopPropagation();
    //$('#id_date').datepicker('open');
    subscribeFocus();
//    $('#id_date').off();
});
var subscribeFocus = function() {
    $('#id_date').one("focus", focusHandler());
};
function focusHandler() {
    $('#id_date').datepicker('open');
    subscribeFocus();
}
// $("#id_date").on('focus', function() {
//     subscribeFocus();
// }); 


[{"model": "events.reminder", "pk": 50, "fields": {"name": "REMIND 1", "date": "2019-01-31", "done": false, "event": 50}}]

[{"model": "events.reminder", "pk": 17, "fields": {"name": "jan 31 remind 5", "date": "2019-01-01", "done": false, "event": 50}}, {"model": "events.reminder", "pk": 21, "fields": {"name": "jan 31 remind 9", "date": "2019-01-01", "done": false, "event": 50}}, {"model": "events.reminder", "pk": 19, "fields": {"name": "jan31 remind 7", "date": "2019-01-02", "done": false, "event": 50}}, {"model": "events.reminder", "pk": 22, "fields": {"name": "jan31 remind 10", "date": "2019-01-02", "done": false, "event": 50}}, {"model": "events.reminder", "pk": 18, "fields": {"name": "jan31 remind 6", "date": "2019-01-09", "done": false, "event": 50}}, {"model": "events.reminder", "pk": 20, "fields": {"name": "jan 31 remind 8", "date": "2019-01-09", "done": false, "event": 50}}, {"model": "events.reminder", "pk": 23, "fields": {"name": "jan31 remind 11", "date": "2019-01-09", "done": false, "event": 50}}, {"model": "events.reminder", "pk": 16, "fields": {"name": "jan31 remind 4", "date": "2019-01-29", "done": false, "event": 50}}, {"model": "events.reminder", "pk": 15, "fields": {"name": "jan 31 remind 3", "date": "2019-02-14", "done": false, "event": 50}}, {"model": "events.reminder", "pk": 14, "fields": {"name": "jan31 remind 2", "date": "2019-02-28", "done": false, "event": 50}}]







//update all flags according to what we know
function updateFlags() {
    var event_id = $('#page_instance').val();
    var hold_until = $('#id_hold_until').val();
    var data = {"event_id":event_id, "hold_until":hold_until};
    $.ajax({
        type : 'GET',
        url :  '/flags/ajax/get_flags',
        data : data,
        success : function(data){
            if (data['hold']) {
                $('#flag_contract').removeClass();
                $('#flag_contract').attr("data-badge-caption","HOLD");
                $('#flag_contract').addClass('badge ev-badge-norm orange lighten-3');
                $('#id_color_contract').val('#ffcc80');                
                //make red if hold past-due
                if (data['hold_past_due']) {
                    $('#flag_contract').removeClass();
                    $('#flag_contract').addClass('badge ev-badge-norm red lighten-4');
                    $('#id_color_contract').val('#ffcdd2');
                }
            }
            //added red if past due for any reason
            if (data['contract_sent']) {
                $('#flag_contract').removeClass();
                $('#flag_contract').attr("data-badge-caption","contract");
                $('#flag_contract').addClass('badge ev-badge-norm yellow lighten-2');
                $('#id_color_contract').val('#fff176');
            }
            if (data['contract_rcvd']) {
                $('#flag_contract').removeClass();
                $('#flag_contract').attr("data-badge-caption","contract");
                $('#flag_contract').addClass('badge ev-badge-norm green lighten-3');
                $('#id_color_contract').val('#a5d6a7');
            }
            if (data['contract_pastdue']) {
                $('#flag_contract').removeClass();
                $('#flag_contract').attr("data-badge-caption","contract");
                $('#flag_contract').addClass('badge ev-badge-norm red lighten-4');
                $('#id_color_contract').val('#ffcdd2');
            }
            //added red if past due (!)
            if (data['deposit_sent']) {
                $('#flag_deposit').removeClass();
                $('#flag_deposit').addClass('badge ev-badge-norm yellow lighten-2');
                $('#id_color_deposit').val('#fff176');
            }
            if (data['deposit_rcvd']) {
                $('#flag_deposit').removeClass();
                $('#flag_deposit').addClass('badge ev-badge-norm green lighten-3');
                $('#id_color_deposit').val('#a5d6a7');
            }
            if (data['deposit_pastdue']) {
                $('#flag_deposit').removeClass();
                $('#flag_deposit').addClass('badge ev-badge-norm red lighten-4');
                $('#id_color_deposit').val('#ffcdd2');
            }
            //added red if past due
            if (data['music_list_sent']) {
                $('#flag_music_list').removeClass();
                $('#flag_music_list').addClass('badge ev-badge-norm yellow lighten-2');
                $('#id_color_music_list').val('#fff176');
            }
            if (data['music_list_rcvd']) {
                $('#flag_music_list').removeClass();
                $('#flag_music_list').addClass('badge ev-badge-norm green lighten-3');
                $('#id_color_music_list').val('#a5d6a7');
            }
            if (data['music_list_pastdue']) {
                $('#flag_music_list').removeClass();
                $('#flag_music_list').addClass('badge ev-badge-norm red lighten-4');
                $('#id_color_music_list').val('#ffcdd2');
            }
            //added red if past due
            if (data['musicians_sent']) {
                $('#flag_musicians').removeClass();
                $('#flag_musicians').addClass('badge ev-badge-norm yellow lighten-2');
                $('#id_color_musicians').val('#fff176');
            }
            if (data['musicians_rcvd']) {
                $('#flag_musicians').removeClass();
                $('#flag_musicians').addClass('badge ev-badge-norm green lighten-3');
                $('#id_color_musicians').val('#a5d6a7');
            }
            if (data['musicians_pastdue']) {
                $('#flag_musicians').removeClass();
                $('#flag_musicians').addClass('badge ev-badge-norm red lighten-4');
                $('#id_color_musicians').val('#ffcdd2');
            }
            //added red if past due
            if (data['final_payment_sent']) {
                $('#flag_final_pay').removeClass();
                $('#flag_final_pay').addClass('badge ev-badge-norm yellow lighten-2');
                $('#id_color_final_payment').val('#fff176');
            }
            if (data['final_payment_rcvd']) {
                $('#flag_final_pay').removeClass();
                $('#flag_final_pay').addClass('badge ev-badge-norm green lighten-3');
                $('#id_color_final_payment').val('#a5d6a7');
            }
            if (data['final_pay_pastdue']) {
                $('#flag_final_pay').removeClass();
                $('#flag_final_pay').addClass('badge ev-badge-norm red lighten-4');
                $('#id_color_final_payment').val('#ffcdd2');
            }
            //added red if past due
            if (data['final_confirmation_sent']) {
                $('#flag_confirm').removeClass();
                $('#flag_confirm').addClass('badge ev-badge-norm yellow lighten-2');
                $('#id_color_final_confirmation').val('#fff176');
            }
            if (data['final_confirmation_rcvd']) {
                $('#flag_confirm').removeClass();
                $('#flag_confirm').addClass('badge ev-badge-norm green lighten-3');
                $('#id_color_final_confirmation').val('#a5d6a7');
            }
            if (data['final_confirmation_pastdue']) {
                $('#flag_confirm').removeClass();
                $('#flag_confirm').addClass('badge ev-badge-norm red lighten-4');
                $('#id_color_final_confirmation').val('#ffcdd2');
            }
            //added red if past due
            if (data['fact_sheets_sent']) {
                $('#flag_fact_sheets').removeClass();
                $('#flag_fact_sheets').addClass('badge ev-badge-norm yellow lighten-2');
                $('#id_color_fact_sheets').val('#fff176');
            }
            if (data['fact_sheets_rcvd']) {
                $('#flag_fact_sheets').removeClass();
                $('#flag_fact_sheets').addClass('badge ev-badge-norm green lighten-3');
                $('#id_color_fact_sheets').val('#a5d6a7');
            }
            if (data['fact_sheets_pastdue']) {
                $('#flag_fact_sheets').removeClass();
                $('#flag_fact_sheets').addClass('badge ev-badge-norm red lighten-4');
                $('#id_color_fact_sheets').val('#ffcdd2');
            }
        },
        error: function(data) {
            alert('There was an error 1!');
        }
    });    
}






