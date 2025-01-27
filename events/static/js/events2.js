
$(document).ready(function(){

    $(function() {
        $( '#id_date' ).datepicker({
            autoClose:'True',
            showDaysInNextAndPreviousMonths:'True',
            format:"ddd, mmm d, yyyy",
            firstDay: 1,
            });
    });

});

$('#submitbtn_reminder_auto_form').on("click", function(e) {

    e.preventDefault(); //this will prevent the default submit

    // your code here (But not asynchronous code such as Ajax because it does not wait for response and move to next line.)

    $('#id_name').removeAttr('disabled');
    
    $(this).unbind('click').click(); // continue the submit unbind preventDefault

});
