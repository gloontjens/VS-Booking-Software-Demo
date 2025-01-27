


$(document).ready(function() {
    $("#signature").jSignature({UndoButton:false,
                                width:'100%', 
                                lineWidth:1});
                                
    //init select inputs
    $('select').formSelect();
    //init date and time pickers
    $('.timepicker').timepicker();
    $('.datepicker').datepicker();
    //init tooltips
    $('.tooltipped').tooltip();
    //init collapsible
    $('.collapsible').collapsible();

//     if ( window.history.replaceState ) {
//       window.history.replaceState( null, null, window.location.href );
//     }
    $('#pin').focus();

});


$('#showmoredetails').on("click", function(e) {
    $('#see-more-details').toggleClass('client-noshow');
    if ($('#showmoredetails').val() == "See More") {
        $('#showmoredetails').val('See Less');
    } else {
        $('#showmoredetails').val('See More');
    }
    event.preventDefault(); //prevents old submit goign to event_details page!   
});

function tinyPrint() {
    //console.log(tinymce.activeEditor.mode.isReadOnly());
    tinymce.activeEditor.execCommand("mcePrint", true);
    event.preventDefault();
}


$(".nosubmit").keypress(
    function(event) {
        if (event.which == '13') {
            event.preventDefault();
        }
});


$('#payment_options').on("click", function(e) {
    $('#payment_options_panel').toggleClass('client-noshow');
    $('#payment_options').toggleClass('client-pressed');    
});
$('#payment_options2').on("click", function(e) {
    $('#payment_options_panel2').toggleClass('client-noshow');
    $('#payment_options2').toggleClass('client-pressed');    
});
$('#payment_options3').on("click", function(e) {
    $('#payment_options_panel3').toggleClass('client-noshow');
    $('#payment_options3').toggleClass('client-pressed');    
});
$('#payment_options4').on("click", function(e) {
    $('#payment_options_panel4').toggleClass('client-noshow');
    $('#payment_options4').toggleClass('client-pressed');    
});



$('#goto_sign_contract_complete').on("click", function(e) {

    e.preventDefault(); //this will prevent the default submit

    // your code here (But not asynchronous code such as Ajax because it does not wait for response and move to next line.)
    if ($('#signature').jSignature('getData', 'native').length == 0) {
        alert('Please Draw Your Signature...');
    } else if ($('#id_signature_name').val() == '') {
        alert('Please Type Your Name...');        
    } else {
        var sigData = $('#signature').jSignature('getData', 'default');
        $('#id_signature').val(sigData);

        $(this).unbind('click').click(); // continue the submit unbind preventDefault
    }
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

$('#send_email_mail').on("click", function(e) {
    //alert('here' + year + month);
    var data = {
        "email": $("#email").val(),
        "amount": $("#amount_to_pay").val()
    };
    $.ajax({
        type: 'GET',
        url: '/send_email_mail',
        data: data,
        success: function(data) {
            alert("Email was sent, thank you!");
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with sending check mailing instructions...");
        }
    });


});


$('.reqinputshortnum').on("change", function(e) {
    if (isNaN($(this).val())) {
        $(this).val("");
    }
});


$('#id_location_outdoors').on("change", function(e) {
    if ($('#indoorsicon').html() == 'wb_sunny') {
        $('#indoorsicon').html('store');
    } else {
        $('#indoorsicon').html('wb_sunny');
    }
});


//****************************************************************************************
$('#parents').on("change", function(e) {
    var test = $("#parents").val();
    if (test.endsWith("...")) {
        $('#parents_other').removeClass('client-noshow');
        $('#parents_customentry').removeClass('client-noshow');
        $('#parents_other').addClass('reqinline');
        $('#parents_extra').removeClass('client-noshow');
        $('#parents').addClass('reqinline');
        $('#parents').addClass('reqother');
        $('#id_parents_custom').focus();
    } else {
        $('#parents_other').addClass('client-noshow');
        $('#parents_customentry').addClass('client-noshow');
        $('#parents_notinlibrary').addClass('client-noshow');
        $('#parents_other').removeClass('reqinline');
        $('#recessionals_extra').addClass('client-noshow');
        $('#parents').removeClass('reqinline');
        $('#parents').removeClass('reqother');
        $('#id_parents_custom').removeClass('reqredbox');
        $('#id_parents_custom_notinlist').val("");
        $('#id_parents_custom').val("");
    }
    if (test.includes("No music")) {
        $('#parents_extra').addClass('client-noshow');
    } else {
        $('#parents_extra').removeClass('client-noshow');
    }
    //if something is selected, change groomsmen & bridemaids to show 'continue...'
    var test2 = $("#groomsmens").val();
    var test3 = $("#bridesmaids").val();
    if (!(test.startsWith("No music"))) {
        if (test2.startsWith("No music")) {
            $('#groomsmens').val("Continue music from parents' processional");
        }
        if (test3.startsWith("No music")) {
            $('#bridesmaids').val("Continue music from above");
        }
    } else {
        if (test2.startsWith("Continue music")) {
            $('#groomsmens').val("No music needed");
        }
        if (test3.startsWith("Continue music")) {
            $('#bridesmaids').val("No music needed");
        }
    }
});
$('#id_parents_custom').on("blur", function(e) {
   //if song is on list, fine.  if not, show warning
    var data = {
        "name": $("#id_parents_custom").val()
    };
    $.ajax({
        type: 'GET',
        url: '/check_music_list',
        data: data,
        success: function(data) {
            if ($("#id_parents_custom").val() === '') {
                $('#id_parents_custom').addClass('reqredbox');
                $('#parents_notinlibrary').addClass('client-noshow');
                $('#parents_customentry').addClass('client-noshow');
            } else {
                $('#id_parents_custom').removeClass('reqredbox');        
                if (!data['onlist']) {
                    $('#parents_notinlibrary').removeClass('client-noshow'); 
                    $('#parents_customentry').addClass('client-noshow');
                    $('#id_parents_custom_notinlist').val("<i>(TBD if available, $25)</i>");
                } else {
                    $('#parents_customentry').addClass('client-noshow');
                    $('#parents_notinlibrary').addClass('client-noshow');
                    $('#id_parents_custom').removeClass('reqredbox');
                    $('#id_parents_custom_notinlist').val("");
                }
            }
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with checking music list...");
        }
    });
});
$('#id_parents_custom').on("click", function(e) {
    $('#parents_notinlibrary').addClass('client-noshow');
    $('#parents_customentry').removeClass('client-noshow');
});





//****************************************************************************************
$('#groomsmens').on("change", function(e) {
    var test = $("#groomsmens").val();
    if (test.endsWith("...")) {
        $('#groomsmens_other').removeClass('client-noshow');
        $('#groomsmens_customentry').removeClass('client-noshow');
        $('#groomsmens_other').addClass('reqinline');
        $('#groomsmens').addClass('reqinline');
        $('#groomsmens').addClass('reqother');
        $('#id_groomsmens_custom').focus();
    } else {
        $('#groomsmens_other').addClass('client-noshow');
        $('#groomsmens_customentry').addClass('client-noshow');
        $('#groomsmens_notinlibrary').addClass('client-noshow');
        $('#groomsmens_other').removeClass('reqinline');
        $('#groomsmens').removeClass('reqinline');
        $('#groomsmens').removeClass('reqother');
        $('#id_groomsmens_custom').removeClass('reqredbox');
        $('#id_groomsmens_custom_notinlist').val("");
        $('#id_groomsmens_custom').val("");
    }
});
$('#id_groomsmens_custom').on("blur", function(e) {
   //if song is on list, fine.  if not, show warning
    var data = {
        "name": $("#id_groomsmens_custom").val()
    };
    $.ajax({
        type: 'GET',
        url: '/check_music_list',
        data: data,
        success: function(data) {
            if ($("#id_groomsmens_custom").val() === '') {
                $('#id_groomsmens_custom').addClass('reqredbox');
                $('#groomsmens_notinlibrary').addClass('client-noshow');
                $('#groomsmens_customentry').addClass('client-noshow');
            } else {
                $('#id_groomsmens_custom').removeClass('reqredbox');        
                if (!data['onlist']) {
                    $('#groomsmens_notinlibrary').removeClass('client-noshow'); 
                    $('#groomsmens_customentry').addClass('client-noshow');
                    $('#id_groomsmens_custom_notinlist').val("<i>(TBD if available, $25)</i>");
                } else {
                    $('#groomsmens_customentry').addClass('client-noshow');
                    $('#groomsmens_notinlibrary').addClass('client-noshow');
                    $('#id_groomsmens_custom').removeClass('reqredbox');
                    $('#id_groomsmens_custom_notinlist').val("");
                }
            }
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with checking music list...");
        }
    });
});
$('#id_groomsmens_custom').on("click", function(e) {
    $('#groomsmens_notinlibrary').addClass('client-noshow');
    $('#groomsmens_customentry').removeClass('client-noshow');
});








//****************************************************************************************
$('#bridesmaids').on("change", function(e) {
    var test = $("#bridesmaids").val();
    if (test.endsWith("...")) {
        $('#bridesmaids_other').removeClass('client-noshow');
        $('#bridesmaids_customentry').removeClass('client-noshow');
        $('#bridesmaids_other').addClass('reqinline');
        $('#bridesmaids_extra').removeClass('client-noshow');
        $('#bridesmaids').addClass('reqinline');
        $('#bridesmaids').addClass('reqother');
        $('#id_bridesmaids_custom').focus();
    } else {
        $('#bridesmaids_other').addClass('client-noshow');
        $('#bridesmaids_customentry').addClass('client-noshow');
        $('#bridesmaids_notinlibrary').addClass('client-noshow');
        $('#bridesmaids_other').removeClass('reqinline');
        $('#bridesmaids_extra').addClass('client-noshow');
        $('#bridesmaids').removeClass('reqinline');
        $('#bridesmaids').removeClass('reqother');
        $('#id_bridesmaids_custom').removeClass('reqredbox');
        $('#id_bridesmaids_custom_notinlist').val("");
        $('#id_bridesmaids_custom').val("");
    }
    if (test.includes("No music")) {
        $('#bridesmaids_extra').addClass('client-noshow');
    } else {
        $('#bridesmaids_extra').removeClass('client-noshow');
    }
});
$('#id_bridesmaids_custom').on("blur", function(e) {
   //if song is on list, fine.  if not, show warning
    var data = {
        "name": $("#id_bridesmaids_custom").val()
    };
    $.ajax({
        type: 'GET',
        url: '/check_music_list',
        data: data,
        success: function(data) {
            if ($("#id_bridesmaids_custom").val() === '') {
                $('#id_bridesmaids_custom').addClass('reqredbox');
                $('#bridesmaids_notinlibrary').addClass('client-noshow');
                $('#bridesmaids_customentry').addClass('client-noshow');
            } else {
                $('#id_bridesmaids_custom').removeClass('reqredbox');        
                if (!data['onlist']) {
                    $('#bridesmaids_notinlibrary').removeClass('client-noshow'); 
                    $('#bridesmaids_customentry').addClass('client-noshow');
                    $('#id_bridesmaids_custom_notinlist').val("<i>(TBD if available, $25)</i>");
                } else {
                    $('#bridesmaids_customentry').addClass('client-noshow');
                    $('#bridesmaids_notinlibrary').addClass('client-noshow');
                    $('#id_bridesmaids_custom').removeClass('reqredbox');
                    $('#id_bridesmaids_custom_notinlist').val("");
                }
            }
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with checking music list...");
        }
    });
});
$('#id_bridesmaids_custom').on("click", function(e) {
    $('#bridesmaids_notinlibrary').addClass('client-noshow');
    $('#bridesmaids_customentry').removeClass('client-noshow');
});



//****************************************************************************************
$('#brides').on("change", function(e) {
    var test = $("#brides").val();
    if (test.endsWith("...")) {
        $('#brides_other').removeClass('client-noshow');
        $('#brides_customentry').removeClass('client-noshow');
        $('#brides_other').addClass('reqinline');
        $('#brides').addClass('reqinline');
        $('#brides').addClass('reqother');
        $('#id_brides_custom').focus();
    } else {
        $('#brides_other').addClass('client-noshow');
        $('#brides_customentry').addClass('client-noshow');
        $('#brides_notinlibrary').addClass('client-noshow');
        $('#brides_other').removeClass('reqinline');
        $('#brides').removeClass('reqinline');
        $('#brides').removeClass('reqother');
        $('#id_brides_custom').removeClass('reqredbox');
        $('#id_brides_custom_notinlist').val("");
        $('#id_brides_custom').val("");
    }
});
$('#id_brides_custom').on("blur", function(e) {
   //if song is on list, fine.  if not, show warning
    var data = {
        "name": $("#id_brides_custom").val()
    };
    $.ajax({
        type: 'GET',
        url: '/check_music_list',
        data: data,
        success: function(data) {
            if ($("#id_brides_custom").val() === '') {
                $('#id_brides_custom').addClass('reqredbox');
                $('#brides_notinlibrary').addClass('client-noshow');
                $('#brides_customentry').addClass('client-noshow');
            } else {
                $('#id_brides_custom').removeClass('reqredbox');        
                if (!data['onlist']) {
                    $('#brides_notinlibrary').removeClass('client-noshow'); 
                    $('#brides_customentry').addClass('client-noshow');
                    $('#id_brides_custom_notinlist').val("<i>(TBD if available, $25)</i>");
                } else {
                    $('#brides_customentry').addClass('client-noshow');
                    $('#brides_notinlibrary').addClass('client-noshow');
                    $('#id_brides_custom').removeClass('reqredbox');
                    $('#id_brides_custom_notinlist').val("");
                }
            }
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with checking music list...");
        }
    });
});
$('#id_brides_custom').on("click", function(e) {
    $('#brides_notinlibrary').addClass('client-noshow');
    $('#brides_customentry').removeClass('client-noshow');
});




//****************************************************************************************
$('#ceremonymusics').on("change", function(e) {
    var test = $("#ceremonymusics").val();
    if (test.endsWith("...")) {
        $('#ceremonymusics_other').removeClass('client-noshow');
        $('#ceremonymusics_customentry').removeClass('client-noshow');
        $('#ceremonymusics_extra').removeClass('client-noshow');
        $('#ceremonymusics_other').addClass('reqinline');
        $('#ceremonymusics').addClass('reqinline');
        $('#ceremonymusics').addClass('reqother');
        $('#id_ceremonymusics_custom').focus();
    } else {
        $('#ceremonymusics_other').addClass('client-noshow');
        $('#ceremonymusics_customentry').addClass('client-noshow');
        $('#ceremonymusics_notinlibrary').addClass('client-noshow');
        $('#ceremonymusics_extra').addClass('client-noshow');
        $('#ceremonymusics_other').removeClass('reqinline');
        $('#ceremonymusics').removeClass('reqinline');
        $('#ceremonymusics').removeClass('reqother');
        $('#id_ceremonymusics_custom').removeClass('reqredbox');
        $('#id_ceremonymusics_custom_notinlist').val("");
        $('#id_ceremonymusics_custom').val("");
    }
    if (test.includes("No music")) {
        $('#ceremonymusics_extra').addClass('client-noshow');
    } else {
        $('#ceremonymusics_extra').removeClass('client-noshow');
    }
});
$('#id_ceremonymusics_custom').on("blur", function(e) {
   //if song is on list, fine.  if not, show warning
    var data = {
        "name": $("#id_ceremonymusics_custom").val()
    };
    $.ajax({
        type: 'GET',
        url: '/check_music_list',
        data: data,
        success: function(data) {
            if ($("#id_ceremonymusics_custom").val() === '') {
                $('#id_ceremonymusics_custom').addClass('reqredbox');
                $('#ceremonymusics_notinlibrary').addClass('client-noshow');
                $('#ceremonymusics_customentry').addClass('client-noshow');
            } else {
                $('#id_ceremonymusics_custom').removeClass('reqredbox');        
                if (!data['onlist']) {
                    $('#ceremonymusics_notinlibrary').removeClass('client-noshow'); 
                    $('#ceremonymusics_customentry').addClass('client-noshow');
                    $('#id_ceremonymusics_custom_notinlist').val("<i>(TBD if available, $25)</i>");
                } else {
                    $('#ceremonymusics_customentry').addClass('client-noshow');
                    $('#ceremonymusics_notinlibrary').addClass('client-noshow');
                    $('#id_ceremonymusics_custom').removeClass('reqredbox');
                    $('#id_ceremonymusics_custom_notinlist').val("");
                }
            }
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with checking music list...");
        }
    });
});
$('#id_ceremonymusics_custom').on("click", function(e) {
    $('#ceremonymusics_notinlibrary').addClass('client-noshow');
    $('#ceremonymusics_customentry').removeClass('client-noshow');
});





//****************************************************************************************
$('#recessionals').on("change", function(e) {
    var test = $("#recessionals").val();
    if (test.endsWith("...")) {
        $('#recessionals_other').removeClass('client-noshow');
        $('#recessionals_customentry').removeClass('client-noshow');
        $('#recessionals_extra').removeClass('client-noshow');
        $('#recessionals_other').addClass('reqinline');
        $('#recessionals').addClass('reqinline');
        $('#recessionals').addClass('reqother');
        $('#id_recessionals_custom').focus();
    } else {
        $('#recessionals_other').addClass('client-noshow');
        $('#recessionals_customentry').addClass('client-noshow');
        $('#recessionals_notinlibrary').addClass('client-noshow');
        $('#recessionals_extra').addClass('client-noshow');
        $('#recessionals_other').removeClass('reqinline');
        $('#recessionals').removeClass('reqinline');
        $('#recessionals').removeClass('reqother');
        $('#id_recessionals_custom').removeClass('reqredbox');
        $('#id_recessionals_custom_notinlist').val("");
        $('#id_recessionals_custom').val("");
    }
    if (test.includes("No music")) {
        $('#recessionals_extra').addClass('client-noshow');
    } else {
        $('#recessionals_extra').removeClass('client-noshow');
    }
});
$('#id_recessionals_custom').on("blur", function(e) {
   //if song is on list, fine.  if not, show warning
    var data = {
        "name": $("#id_recessionals_custom").val()
    };
    $.ajax({
        type: 'GET',
        url: '/check_music_list',
        data: data,
        success: function(data) {
            if ($("#id_recessionals_custom").val() === '') {
                $('#id_recessionals_custom').addClass('reqredbox');
                $('#recessionals_notinlibrary').addClass('client-noshow');
                $('#recessionals_customentry').addClass('client-noshow');
            } else {
                $('#id_recessionals_custom').removeClass('reqredbox');        
                if (!data['onlist']) {
                    $('#recessionals_notinlibrary').removeClass('client-noshow'); 
                    $('#recessionals_customentry').addClass('client-noshow');
                    $('#id_recessionals_custom_notinlist').val("<i>(TBD if available, $25)</i>");
                } else {
                    $('#recessionals_customentry').addClass('client-noshow');
                    $('#recessionals_notinlibrary').addClass('client-noshow');
                    $('#id_recessionals_custom').removeClass('reqredbox');
                    $('#id_recessionals_custom_notinlist').val("");
                }
            }
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with checking music list...");
        }
    });
});
$('#id_recessionals_custom').on("click", function(e) {
    $('#recessionals_notinlibrary').addClass('client-noshow');
    $('#recessionals_customentry').removeClass('client-noshow');
});



$('#housemixbtn').click(function(e) {
    //alert('here');
    if ($('#housemixcheck').html() == 'check_box') {
        $('#backgrounds').val('');
        $('#receptions').val('');
        $('#cocktails').val('');
        $('#housemixcheck').html('check_box_outline_blank');   
    } else {
        $('#backgrounds').val('House Mix');
        $('#receptions').val('House Mix');
        $('#cocktails').val('House Mix');
        $('#housemixcheck').html('check_box');
        $('#naplesontherockscheck').html('check_box_outline_blank');
        $('#cosmopolitancheck').html('check_box_outline_blank');
        $('#bellinicheck').html('check_box_outline_blank');
        $('#mojitocheck').html('check_box_outline_blank');
        $('#darjeelingfizzcheck').html('check_box_outline_blank');
    }  
});
$('#naplesontherocksbtn').click(function(e) {
    //alert('here');
    if ($('#naplesontherockscheck').html() == 'check_box') {
        $('#backgrounds').val('');
        $('#receptions').val('');
        $('#cocktails').val('');
        $('#naplesontherockscheck').html('check_box_outline_blank');   
    } else {
        $('#backgrounds').val('Naples On the Rocks');
        $('#receptions').val('Naples On the Rocks');
        $('#cocktails').val('Naples On the Rocks');
        $('#naplesontherockscheck').html('check_box');
        $('#housemixcheck').html('check_box_outline_blank');
        $('#cosmopolitancheck').html('check_box_outline_blank');
        $('#bellinicheck').html('check_box_outline_blank');
        $('#mojitocheck').html('check_box_outline_blank');
        $('#darjeelingfizzcheck').html('check_box_outline_blank');
    }  
});
$('#cosmopolitanbtn').click(function(e) {
    //alert('here');
    if ($('#cosmopolitancheck').html() == 'check_box') {
        $('#backgrounds').val('');
        $('#receptions').val('');
        $('#cocktails').val('');
        $('#cosmopolitancheck').html('check_box_outline_blank');   
    } else {
        $('#backgrounds').val('The Cosmopolitan');
        $('#receptions').val('The Cosmopolitan');
        $('#cocktails').val('The Cosmopolitan');
        $('#cosmopolitancheck').html('check_box');
        $('#housemixcheck').html('check_box_outline_blank');
        $('#naplesontherockscheck').html('check_box_outline_blank');
        $('#bellinicheck').html('check_box_outline_blank');
        $('#mojitocheck').html('check_box_outline_blank');
        $('#darjeelingfizzcheck').html('check_box_outline_blank');
    }  
});
$('#bellinibtn').click(function(e) {
    //alert('here');
    if ($('#bellinicheck').html() == 'check_box') {
        $('#backgrounds').val('');
        $('#receptions').val('');
        $('#cocktails').val('');
        $('#bellinicheck').html('check_box_outline_blank');   
    } else {
        $('#backgrounds').val('The Bellini');
        $('#receptions').val('The Bellini');
        $('#cocktails').val('The Bellini');
        $('#bellinicheck').html('check_box');
        $('#housemixcheck').html('check_box_outline_blank');
        $('#naplesontherockscheck').html('check_box_outline_blank');
        $('#cosmopolitancheck').html('check_box_outline_blank');
        $('#mojitocheck').html('check_box_outline_blank');
        $('#darjeelingfizzcheck').html('check_box_outline_blank');
    }  
});
$('#mojitobtn').click(function(e) {
    //alert('here');
    if ($('#mojitocheck').html() == 'check_box') {
        $('#backgrounds').val('');
        $('#receptions').val('');
        $('#cocktails').val('');
        $('#mojitocheck').html('check_box_outline_blank');   
    } else {
        $('#backgrounds').val('The Mojito');
        $('#receptions').val('The Mojito');
        $('#cocktails').val('The Mojito');
        $('#mojitocheck').html('check_box');
        $('#housemixcheck').html('check_box_outline_blank');
        $('#naplesontherockscheck').html('check_box_outline_blank');
        $('#cosmopolitancheck').html('check_box_outline_blank');
        $('#bellinicheck').html('check_box_outline_blank');
        $('#darjeelingfizzcheck').html('check_box_outline_blank');
    }  
});
$('#darjeelingfizzbtn').click(function(e) {
    //alert('here');
    if ($('#darjeelingfizzcheck').html() == 'check_box') {
        $('#backgrounds').val('');
        $('#receptions').val('');
        $('#cocktails').val('');
        $('#darjeelingfizzcheck').html('check_box_outline_blank');   
    } else {
        $('#backgrounds').val('The Darjeeling Fizz');
        $('#receptions').val('The Darjeeling Fizz');
        $('#cocktails').val('The Darjeeling Fizz');
        $('#darjeelingfizzcheck').html('check_box');
        $('#housemixcheck').html('check_box_outline_blank');
        $('#naplesontherockscheck').html('check_box_outline_blank');
        $('#cosmopolitancheck').html('check_box_outline_blank');
        $('#bellinicheck').html('check_box_outline_blank');
        $('#mojitocheck').html('check_box_outline_blank');
    }  
});








$('#dhousemixbtn').click(function(e) {
    //alert('here');
    if ($('#dhousemixcheck').html() == 'check_box') {
        $('#dinners').val('');
//         $('#receptions').val('');
//         $('#cocktails').val('');
        $('#dhousemixcheck').html('check_box_outline_blank');   
    } else {
        $('#dinners').val('House Mix');
//         $('#receptions').val('House Mix');
//         $('#cocktails').val('House Mix');
        $('#dhousemixcheck').html('check_box');
        $('#dnaplesontherockscheck').html('check_box_outline_blank');
        $('#dcosmopolitancheck').html('check_box_outline_blank');
        $('#dbellinicheck').html('check_box_outline_blank');
        $('#dmojitocheck').html('check_box_outline_blank');
        $('#ddarjeelingfizzcheck').html('check_box_outline_blank');
    }  
});
$('#dnaplesontherocksbtn').click(function(e) {
    //alert('here');
    if ($('#dnaplesontherockscheck').html() == 'check_box') {
        $('#dinners').val('');
//         $('#receptions').val('');
//         $('#cocktails').val('');
        $('#dnaplesontherockscheck').html('check_box_outline_blank');   
    } else {
        $('#dinners').val('Naples On the Rocks');
//         $('#receptions').val('Naples On the Rocks');
//         $('#cocktails').val('Naples On the Rocks');
        $('#dnaplesontherockscheck').html('check_box');
        $('#dhousemixcheck').html('check_box_outline_blank');
        $('#dcosmopolitancheck').html('check_box_outline_blank');
        $('#dbellinicheck').html('check_box_outline_blank');
        $('#dmojitocheck').html('check_box_outline_blank');
        $('#ddarjeelingfizzcheck').html('check_box_outline_blank');
    }  
});
$('#dcosmopolitanbtn').click(function(e) {
    //alert('here');
    if ($('#dcosmopolitancheck').html() == 'check_box') {
        $('#dinners').val('');
//         $('#receptions').val('');
//         $('#cocktails').val('');
        $('#dcosmopolitancheck').html('check_box_outline_blank');   
    } else {
        $('#dinners').val('The Cosmopolitan');
//         $('#dreceptions').val('The Cosmopolitan');
//         $('#dcocktails').val('The Cosmopolitan');
        $('#dcosmopolitancheck').html('check_box');
        $('#dhousemixcheck').html('check_box_outline_blank');
        $('#dnaplesontherockscheck').html('check_box_outline_blank');
        $('#dbellinicheck').html('check_box_outline_blank');
        $('#dmojitocheck').html('check_box_outline_blank');
        $('#ddarjeelingfizzcheck').html('check_box_outline_blank');
    }  
});
$('#dbellinibtn').click(function(e) {
    //alert('here');
    if ($('#dbellinicheck').html() == 'check_box') {
        $('#dinners').val('');
//         $('#receptions').val('');
//         $('#cocktails').val('');
        $('#dbellinicheck').html('check_box_outline_blank');   
    } else {
        $('#dinners').val('The Bellini');
//         $('#receptions').val('The Bellini');
//         $('#cocktails').val('The Bellini');
        $('#dbellinicheck').html('check_box');
        $('#dhousemixcheck').html('check_box_outline_blank');
        $('#dnaplesontherockscheck').html('check_box_outline_blank');
        $('#dcosmopolitancheck').html('check_box_outline_blank');
        $('#dmojitocheck').html('check_box_outline_blank');
        $('#ddarjeelingfizzcheck').html('check_box_outline_blank');
    }  
});
$('#dmojitobtn').click(function(e) {
    //alert('here');
    if ($('#dmojitocheck').html() == 'check_box') {
        $('#dinners').val('');
//         $('#receptions').val('');
//         $('#cocktails').val('');
        $('#dmojitocheck').html('check_box_outline_blank');   
    } else {
        $('#dinners').val('The Mojito');
//         $('#receptions').val('The Mojito');
//         $('#cocktails').val('The Mojito');
        $('#dmojitocheck').html('check_box');
        $('#dhousemixcheck').html('check_box_outline_blank');
        $('#dnaplesontherockscheck').html('check_box_outline_blank');
        $('#dcosmopolitancheck').html('check_box_outline_blank');
        $('#dbellinicheck').html('check_box_outline_blank');
        $('#ddarjeelingfizzcheck').html('check_box_outline_blank');
    }  
});
$('#ddarjeelingfizzbtn').click(function(e) {
    //alert('here');
    if ($('#ddarjeelingfizzcheck').html() == 'check_box') {
        $('#dinners').val('');
//         $('#receptions').val('');
//         $('#cocktails').val('');
        $('#ddarjeelingfizzcheck').html('check_box_outline_blank');   
    } else {
        $('#dinners').val('The Darjeeling Fizz');
//         $('#receptions').val('The Darjeeling Fizz');
//         $('#cocktails').val('The Darjeeling Fizz');
        $('#ddarjeelingfizzcheck').html('check_box');
        $('#dhousemixcheck').html('check_box_outline_blank');
        $('#dnaplesontherockscheck').html('check_box_outline_blank');
        $('#dcosmopolitancheck').html('check_box_outline_blank');
        $('#dbellinicheck').html('check_box_outline_blank');
        $('#dmojitocheck').html('check_box_outline_blank');
    }  
});





//********************************************************************
$("#goto_requests_done").click(function(e) {

    if ($('#id_parents_custom').hasClass('reqredbox') ||
        $('#id_groomsmens_custom').hasClass('reqredbox') ||
        $('#id_bridesmaids_custom').hasClass('reqredbox') ||
        $('#id_brides_custom').hasClass('reqredbox') ||
        $('#id_ceremonymusics_custom').hasClass('reqredbox') ||
        $('#id_recessionals_custom').hasClass('reqredbox')) {
        var msg = "You must fill in the boxes marked in red before submitting!";
        
        alert(msg);
        e.preventDefault(); //this will prevent the default submit
        return;
    }
    
    if ($('#housemixcheck').html() == 'check_box_outline_blank' &&
        $('#naplesontherockscheck').html() == 'check_box_outline_blank' &&
        $('#cosmopolitancheck').html() == 'check_box_outline_blank' &&
        $('#bellinicheck').html() == 'check_box_outline_blank' &&
        $('#mojitocheck').html() == 'check_box_outline_blank' &&
        $('#darjeelingfizzcheck').html() == 'check_box_outline_blank') {
        var msg = "You must checkmark your choice for Cocktail Hour Music first!";
        alert(msg);
        e.preventDefault();
        return;
    }
    if ($('#dhousemixcheck').html() == 'check_box_outline_blank' &&
        $('#dnaplesontherockscheck').html() == 'check_box_outline_blank' &&
        $('#dcosmopolitancheck').html() == 'check_box_outline_blank' &&
        $('#dbellinicheck').html() == 'check_box_outline_blank' &&
        $('#dmojitocheck').html() == 'check_box_outline_blank' &&
        $('#ddarjeelingfizzcheck').html() == 'check_box_outline_blank') {
        var msg = "You must checkmark your choice for Dinner Music first!";
        alert(msg);
        e.preventDefault();
        return;
    }
    
});





