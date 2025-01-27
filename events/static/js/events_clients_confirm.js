

$(document).ready(function() {

    var alldone = false;
    var numchecks = $(':checkbox:checked').length;
    var numreqboxes = 0;
    if (($('#new_doc_name').val() != "") && ($('#new_doc_alone_name').val() != ""))
        {numreqboxes = numreqboxes + 1;}
    if (($('#new_doc_email').val() != "") && ($('#new_doc_alone_phone').val() != ""))
        {numreqboxes = numreqboxes + 1;}
    
    if ((numchecks == 11) && (numreqboxes == 2)) {
        $('#goto_confirm_final_details_done').prop('disabled', false);
    } else {
        $('#goto_confirm_final_details_done').prop('disabled', true);
        
    }
    


    $('.necc').change(function () {
        var alldone = false;
        var numchecks = $(':checkbox:checked').length;
        var numreqboxes = 0;
        if (($('#new_doc_name').val() != "") && ($('#new_doc_alone_name').val() != ""))
            {numreqboxes = numreqboxes + 1;}
        if (($('#new_doc_email').val() != "") && ($('#new_doc_alone_phone').val() != ""))
            {numreqboxes = numreqboxes + 1;}
        
        if ((numchecks == 11) && (numreqboxes == 2)) {
            $('#goto_confirm_final_details_done').prop('disabled', false);
        } else {
            $('#goto_confirm_final_details_done').prop('disabled', true);
            
        }
    });
    $('.necc2').change(function () {
        var alldone = false;
        var numchecks = $(':checkbox:checked').length;
        var numreqboxes = 0;
        if (($('#new_doc_name').val() != "") && ($('#new_doc_alone_name').val() != ""))
            {numreqboxes = numreqboxes + 1;}
        if (($('#new_doc_email').val() != "") && ($('#new_doc_alone_phone').val() != ""))
            {numreqboxes = numreqboxes + 1;}
        
        if ((numchecks == 11) && (numreqboxes == 2)) {
            $('#goto_confirm_final_details_done').prop('disabled', false);
        } else {
            $('#goto_confirm_final_details_done').prop('disabled', true);
            
        }
    });

});


$('.limitphone').on("keypress", function(e) {
    const key = e.which || e.keyCode;
    const ZERO = 48;
    const NINE = 57;
    const SPACE = 32;
    const PARLEFT = 40;
    const PARRIGHT = 41;
    const EX = 120;
    const PLUS = 43;
    const DASH = 45;
    const isNotDigit = key < ZERO || key > NINE;
    if (isNotDigit && !(key == SPACE || key == PARLEFT || key == PARRIGHT || key == EX || key== DASH || key == PLUS)) {
        e.preventDefault();
    }    
});



