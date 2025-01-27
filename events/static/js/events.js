/*jshint multistr: true */
/*jshint esversion: 6 */






//var to identify popup type
var popuptype = "none";
 
//Toggles  for 'details' buttons
var toggle = "";
var toggle2 = "";
var toggle3 = "";
var toggle4 = "";

//color constants
var flag_empty = "#f8f8f8";
var flag_started = "#fff176";
var flag_done = "#a5d6a7";
var flag_late = "#ffcdd2";
var flag_hold = "#ffcc80";
var flag_white = "#bbbbbb";

//state constants
var flag_contract_sent = $('#id_flag_contract_sent').prop('checked');
var flag_deposit_sent = $('#id_flag_deposit_sent').prop('checked');
var flag_final_sent = $('#id_flag_final_payment_sent').prop('checked');
var flag_musicians_sent = $('#id_flag_musicians_sent').prop('checked');
var flag_extra_sent = $('#id_flag_extra_sent').prop('checked');

//helper to see if actually empty or null
function isEmptyOrSpaces(str) {
    return str === null || str.match(/^ *$/) !== null;
}
//helper to see if &nbsp or empty
function isEmptyOrNbsp(str) {
    if (str === null || str=='' || str=='&nbsp;') {
        return true;
    } else {
        return false;
    }
}
function isEmptyOrZero(tocheck) {
    if (tocheck == '0' || tocheck === 0 || tocheck =='' || tocheck == '&nbsp;') {
        return true;
    } else {
        return false;
    }
}

$.fn.nval = function() {
    return Number(this.val());
};

//save old extra fee for calculation
var oldextrafee = $("#id_extra_fee").nval();


$(document).ready(function() {
    $('.collapsible').collapsible({
        accordion: false,
    });
 
    //unknown?
    $('select').formSelect();
    //set Type hidden fields when choice changes (regular/hold/agency)
    var today = new Date();
    today.setHours(0, 0, 0, 0);
    $('#id_indooroutdoor').change(function() {
        var el = document.getElementById("id_indooroutdoor");
        var selected = el.options[el.selectedIndex].text;
        if (selected == "Indoors") {
            $('#id_location_outdoors').prop("checked", false);
        } else {
            $('#id_location_outdoors').prop("checked", true); 
        }    
    });
    $('#id_type').change(function() {
        var el = document.getElementById("id_type");
        var selected = el.options[el.selectedIndex].text;
        if (selected == "Hold") {
            $('#id_waive_payment').prop("checked", false);
            $('#id_waive_contract').prop("checked", false);
            $('#toggle_hold').show();
            $('#toggle_agency_booking').hide();
            $('#id_hold_released').val('');
            $('#id_flag_hold').prop("checked", true);
            $('#id_event_reminders_done').prop("checked", false);
            //add default hold time of 3 weeks
            var htoday = new Date();
            htoday.setHours(0, 0, 0, 0);
            var hresult = new Date(htoday);
            hresult.setDate(hresult.getDate() + 21);
            var hrday = hresult.getDate();
            var hrmonth = hresult.getMonth() + 1;
            var hryear = hresult.getFullYear() - 2000;
            var htextresult = hrmonth + '/' + hrday + '/' + hryear;
            $('#id_hold_until').val(htextresult);
            //updateFlags();
            
        } else if (selected == "Agency") {
            $('#id_waive_payment').prop("checked", true);
            $('#id_waive_contract').prop("checked", true);
            $('#toggle_hold').hide();
            $('#toggle_agency_booking').show();
            if ($('#id_flag_hold').prop('checked')) {
                //previously held, so record hold_released date
                $('#id_hold_released').val(formatDate(today, true));
            }
            //$('#id_hold_until').val("");
            $('#id_flag_hold').prop("checked", false);
            $('#id_event_reminders_done').prop("checked", false);
        } else {
            $('#id_waive_payment').prop("checked", false);
            $('#id_waive_contract').prop("checked", false);
            $('#toggle_agency_booking').hide();
            $('#toggle_hold').hide();
            if ($('#id_flag_hold').prop('checked')) {
                //previously held, so record hold_released date
                $('#id_hold_released').val(formatDate(today, true));
            }
            //$('#id_hold_until').val("");
            $('#id_flag_hold').prop("checked", false);
            $('#id_event_reminders_done').prop("checked", false);
        }
        updateFlags();
        M.updateTextFields();
    });
    //when hold date is changed, updateFlags
    $('#id_hold_until').change(function() {
        //alert($('#id_hold_until').val());
        $('#id_event_reminders_done').prop("checked", false);
        updateFlags();
        M.updateTextFields();
    });
    //when waive contract is changed, clear event_reminders_done flag!
    $('#id_waive_contract').change(function() {
        $('#id_event_reminders_done').prop("checked", false);
        updateFlags();
        M.updateTextFields();
    });
    //when waive payment is changed, clear event_reminders_done flag!
    $('#id_waive_payment').change(function() {
        $('#id_event_reminders_done').prop("checked", false);
        updateFlags();
        M.updateTextFields();
    });
    //when waive musiclist is changed, clear event_reminders_done flag!
    $('#id_waive_music_list').change(function() {
        $('#id_event_reminders_done').prop("checked", false);
        updateFlags();
        M.updateTextFields();
    });

    //update nav bar according to page_flag value    
    var flag = $('#page_flag').val();
    if (flag == 'new') {
        $('#nav_new, #navs_new').addClass("active");
        $('#nav_home, #navs_home').removeClass("active");
        $('#nav_arrows').addClass("ev-nav-hide");
        $('#nav_editforms, #navs_editforms').removeClass("active");
        $('#nav_dropdown').removeClass("active");
        $('#nav_archived, #navs_archived').removeClass("active");
        $('#nav_browse, #navs_browse').removeClass("active");
        $('#nav_tasks, #navs_tasks').removeClass("active");
        $('#btn_calendar').addClass("lighten-5");
        $('#btn_calendar').removeClass("lighten-4");
        $('#nav_rates, #navs_rates').removeClass("active");
        $('#nav_payments_due, #navs_payments_due').removeClass("active");
        $('#nav_payments_received, #navs_payments_received').removeClass("active");
        $('#nav_syncgcal, #navs_syncgcal').removeClass("active");
        $('#nav_esigs, #navs_esigs').removeClass("active");
        $('#nav_calendar, #navs_calendar').removeClass("active");
        $('#nav_reports, #navs_reports').removeClass("active");
        //add more menu items as necessary?
        $('id_name').focus();
    }

    //update toggles for contact/location/dayofcontact when in edit mode and they're not blank
    if (flag == 'edit') {
        if (!isEmptyOrSpaces($('#id_contact_0').val())) {
            toggle = "show";
            $('#contact_email_show').removeClass('noshow');
            $('#contact_email_add').addClass('noshow');
        }
        if (!isEmptyOrSpaces($('#id_location_0').val())) {
            toggle3 = "show";
        }
        if (!isEmptyOrSpaces($('#id_dayofcontact_0').val())) {
            toggle2 = "show";
        }
    }
    //show popup if necessary
    var popup = $('#page_popup').val();
    if (popup != 'none') {
        popuptype = popup;
        showEditPopupLarge(popup);
        //dummy =  setTimeout(function() { showEditPopupLarge(popup); }, 2000);
//         $('#page_popup'.val("none"));
    }
    //show-hide contact, dayofcontact, location and fee details 
    $('#contact_button').click(function() {
        if (toggle == "add") {
            $('#toggle_contact_add').toggleClass("ev-closed");
        } else if (toggle == "show") {
            $('#toggle_contact_show').toggleClass("ev-closed");
        } else {
            //do nothing in reponse to button click if neither should be open
            $('#contact_button').prop("checked", false);
        }
        $('#form').trigger('rescan.areYouSure');
    });
    $('#dayofcontact_button').click(function() {
        if (toggle2 == "add") {
            $('#toggle_dayofcontact_add').toggleClass("ev-closed");
            if ($('#toggle_dayofcontact_add').hasClass('ev-closed')) {
                $('#toggle_dayofcontact_alone').addClass("ev-closed");
            } else {
                $('#toggle_dayofcontact_alone').removeClass("ev-closed");   
            }
        } else if (toggle2 == "show") {
            $('#toggle_dayofcontact_show').toggleClass("ev-closed");
            if ($('#toggle_dayofcontact_show').hasClass('ev-closed')) {
                $('#toggle_dayofcontact_alone').addClass("ev-closed");
            } else {
                $('#toggle_dayofcontact_alone').removeClass("ev-closed");   
            }
        } else {
            //do nothing except show _alone section, in reponse to button click if neither should be open
            $('#toggle_dayofcontact_alone').toggleClass("ev-closed");
            //$('#dayofcontact_button').prop("checked", false);
        }
        $('#form').trigger('rescan.areYouSure');
    });
    $('#location_button').click(function() {
        if (toggle3 == "add") {
            $('#toggle_location_add').toggleClass("ev-closed");
        } else if (toggle3 == "show") {
            $('#toggle_location_show').toggleClass("ev-closed");
        } else {
            //do nothing in reponse to button click if neither should be open
            $('#location_button').prop("checked", false);
        }
        $('#form').trigger('rescan.areYouSure');
    });
    $('#musicians_button').click(function() {
        $('#id_musician').val('');
        $('#id_instrument').val('');
        $('#toggle_musicians').toggleClass("ev-closed3");
        $('#musicians_hr').toggleClass("noshow");
        $('#form').trigger('rescan.areYouSure');    
    });
    $('#fee_button').click(function() {
        $('#toggle_fee').toggleClass("ev-closed2");
        $('#form').trigger('rescan.areYouSure');
    });
    $('#musiclist_button').click(function() {
        $('#toggle_musiclist').toggleClass("ev-closed2");
        $('#form').trigger('rescan.areYouSure');
    });
    
    
    
        $(".dropdown-trigger").dropdown({
        alignment: 'right',
        constrainWidth: false,
        coverTrigger: false,
        inDuration: 0,
        outDuration: 0,
        hover: false,
        closeOnClick: false
    });

    
    $('.modal').modal({
        inDuration: 0,
        outDuration: 0,
        opacity: 0.5
    });

    $('#reminders_bar_header').click(function() {
        $('#reminders_bar_header').removeClass("evx-focusin2");
        var data = {
            "type": "todos",
            "event_id": $("#page_instance").val()
        };
        $.ajaxq("MyQueue", {
            type: 'GET',
            url: '/flipheader',
            data: data,
            success: function(data) {
                
            },
            error: function(data) {
                alert("Something Went Wrong, likely with header bar click...");
            }
        });
    });
    $('#notes_bar_header').click(function() {
        $('#notes_bar_header').removeClass("evx-focusin2");
        var data = {
            "type": "notes",
            "event_id": $("#page_instance").val()
        };
        $.ajaxq("MyQueue", {
            type: 'GET',
            url: '/flipheader',
            data: data,
            success: function(data) {
                
            },
            error: function(data) {
                alert("Something Went Wrong, likely with header bar click...");
            }
        });
    });
    $('#records_bar_header').click(function() {
        $('#records_bar_header').removeClass("evx-focusin2");
        var data = {
            "type": "records",
            "event_id": $("#page_instance").val()
        };
        $.ajaxq("MyQueue", {
            type: 'GET',
            url: '/flipheader',
            data: data,
            success: function(data) {
                
            },
            error: function(data) {
                alert("Something Went Wrong, likely with header bar click...");
            }
        });
    });
    $('#history_bar_header').click(function() {
        $('#history_bar_header').removeClass("evx-focusin2");
        var data = {
            "type": "history",
            "event_id": $("#page_instance").val()
        };
        $.ajaxq("MyQueue", {
            type: 'GET',
            url: '/flipheader',
            data: data,
            success: function(data) {
                
            },
            error: function(data) {
                alert("Something Went Wrong, likely with header bar click...");
            }
        });
    });
    
    //initialize all date and time pickers
    $(function() {
        $('#id_hold_until').datepicker({
            autoClose: 'True',
            showDaysInNextAndPreviousMonths: 'True',
            format: 'm/d/yy',
            firstDay: 1,
        });
    });
    $(function() {
        $('#id_deposit_date').datepicker({
            autoClose: 'True',
            showDaysInNextAndPreviousMonths: 'True',
            format: 'm/d/yy',
            firstDay: 1,
        });
    });
    $(function() {
        $('#id_final_date').datepicker({
            autoClose: 'True',
            showDaysInNextAndPreviousMonths: 'True',
            format: 'm/d/yy',
            firstDay: 1,
        });
    });
    $(function() {
        $('#id_start_time').timepicker({
            autoClose: 'True',
        });
    });
    $(function() {
        $('#id_end_time').timepicker({
            autoClose: 'True',
        });
    });
    $(function() {
        $('#id_ceremony_time').timepicker({
            autoClose: 'True',
        });
    });


    //Determine if hidden fields have anything while main fields are blank.  If so, copy value
    //      to main related fields, and set the toggles appropriately    
    $(function() {
        var hidden = $('#id_contact_name').val();
        var main = $('#id_contact_0').val();
        if ((!isEmptyOrSpaces(hidden)) && (isEmptyOrSpaces(main))) {
            $('#id_contact_0').val(hidden);
            
            toggle = "add";
            $('#contact_email_show').addClass('noshow');
            $('#contact_email_add').removeClass('noshow');
        }
        if ((isEmptyOrSpaces(hidden)) && (isEmptyOrSpaces(main))) {
            $('#contact_email_show').addClass('noshow');
            $('#contact_email_add').removeClass('noshow');            
        }
    });
    $(function() {
        var hidden = $('#id_dayofcontact_name').val();
        var main = $('#id_dayofcontact_0').val();
        if ((!isEmptyOrSpaces(hidden)) && (isEmptyOrSpaces(main))) {
            $('#id_dayofcontact_0').val(hidden);
            toggle2 = "add";
        }
    });
    $(function() {
        var hidden = $('#id_location_name').val();
        var main = $('#id_location_0').val();
        if ((!isEmptyOrSpaces(hidden)) && (isEmptyOrSpaces(main))) {
            $('#id_location_0').val(hidden);
            toggle3 = "add";
        }
    });
    $(function() {
        var hidden = $('#id_event_type_name').val();
        var main = $('#id_event_type_0').val();
        if ((!isEmptyOrSpaces(hidden)) && (isEmptyOrSpaces(main))) {
            $('#id_event_type_0').val(hidden);
        }
    });
    $(function() {
        var hidden = $('#id_ensemble_name').val();
        var main = $('#id_ensemble_0').val();
        if ((!isEmptyOrSpaces(hidden)) && (isEmptyOrSpaces(main))) {
            $('#id_ensemble_0').val(hidden);
        }
    });

    //update values in 'show' hidden sections in case its an existing location
    updateValues();
    
    
    //prevent user from leaving changed form
    $('form').areYouSure({
        'message':'These event details are not saved!'
    });
//     $('form.form').areYouSure({
//         change: function() {
//               // Enable save button only if the form is dirty. i.e. something to save.
//               if ($(this).hasClass('dirty')) {
//                 $(this).find('#submitbtn').removeAttr('disabled');
//               } else {
//                 $(this).find('#submitbtn').attr('disabled', 'disabled');
//               }
//             }
//     });
    //init floating action bar
    $('#id_action_button').floatingActionButton({
        hoverEnabled: false,
        direction: 'top'
    });
    //init floating more bar
    $('#id_more_button').floatingActionButton({
        hoverEnabled: false,
        direction: 'top'
    });
    
    
    $("#musname-sortable").sortable();
    
    
//     $('#id_contact_fab').floatingActionButton({
//         hoverEnabled: false,
//         direction: 'top'
//     });
//     $("#id_contact_fab").dropdown({
//         alignment: 'right',
//         constrainWidth: false,
//         coverTrigger: false,
//         inDuration: 0,
//         outDuration: 0,
//         hover: false,
//         closeOnClick: true
//     });
//     $("#id_contact_fab_invoice").dropdown({
//         alignment: 'right',
//         constrainWidth: false,
//         coverTrigger: false,
//         inDuration: 0,
//         outDuration: 0,
//         hover: false,
//         closeOnClick: true
//     });
//     $("#id_contact_fab_nologin").dropdown({
//         alignment: 'right',
//         constrainWidth: false,
//         coverTrigger: false,
//         inDuration: 0,
//         outDuration: 0,
//         hover: false,
//         closeOnClick: true
//     });
    
    
    
    
    
    //init sidebar mobile menu
    $('.sidenav.sidenav-right').sidenav({
        edge: 'right'
    });
    //init sidebars
    $('.sidenav.sidenav-left').sidenav({
        edge: 'left'
    });
    //init tooltips
    $('.tooltipped').tooltip();
    //init dropdown
    $(".dropdown-trigger").dropdown({
        alignment: 'right',
        constrainWidth: false,
        coverTrigger: false,
        inDuration: 0,
        outDuration: 0,
        hover: false,
        closeOnClick: false
    });
    //init sidebar collapsibles
    $('.collapsible').collapsible({
        accordion: false,
    });
    //init add musician/instrument dropdowns
    function newParameters(query) {
        query.instrument = $('#id_instrument').val();
    }
    $('#id_musician').djselectable('option', 'prepareQuery', newParameters);
    //update musicians asked/toask panel
    updateMusiciansAskedList();
    //updateMusiciansList();
    
    //dummy = setTimeout(updateFlags, 1000);
    //updateFlags();

//     $('#id_date').change(function() {
//         //alert('date changed');
//         updateFlags();
//     });

//     $('div.mce-toolbar').hide();
// 
//     tinymce.init({
//         setup: function (ed) {
//             ed.on('focus', function () {
//                 $(this.contentAreaContainer.parentElement).find("div.mce-toolbar-grp").show();
//             });
//             ed.on('blur', function () {
//                 $(this.contentAreaContainer.parentElement).find("div.mce-toolbar-grp").hide();
//             });
//             ed.on("init", function() {
//                 $(this.contentAreaContainer.parentElement).find("div.mce-toolbar-grp").hide();
//             });
//         }
//     });    

//     $('#id_notes').tinymce({
//         setup: function(ed) {
//             ed.onClick.add(function(ed, e) {
//                 alert('Editor was clicked: ' + e.target.nodeName);
//             });
//         }
//     });

    M.textareaAutoResize($("#id_location_details"));
    M.textareaAutoResize($("#id_contact_details"));
    M.textareaAutoResize($("#id_dayofcontact_details"));



//     tinymce.init({
//       selector: '#id_body',
//       plugins: 'code wordcount',
//       toolbar: 'undo redo | currentdate',
//       content_css: [
//         '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
//         '//www.tiny.cloud/css/codepen.min.css'],
//       
//       setup: function(editor) {
//         
//         function toTimeHtml(date) {
//           return '<time datetime="' + date.toString() + '">' + date.toDateString() + '</time>';
//         }
//         
//         function insertDate() {
//           var html = toTimeHtml(new Date());
//           editor.insertContent(html);
//         }
//     
//         editor.addButton('currentdate', {
//           icon: 'insertdatetime',
//           //image: 'http://p.yusukekamiyamane.com/icons/search/fugue/icons/calendar-blue.png',
//           tooltip: "Insert Current Date",
//           onclick: insertDate
//         });
//       }
//     });


    if ( window.history.replaceState ) {
      window.history.replaceState( null, null, window.location.href );
    }

    $('form').on('dirty.areYouSure', function() {
      //alert('dirty');
      // Enable save button only as the form is dirty.
      $(this).find('#submitbtn').addClass('submitpulse');
      //$('#form').trigger('rescan.areYouSure');
    }); 
    $('form').on('clean.areYouSure', function() {
      //alert('clean');
      // Enable save button only as the form is dirty.
      $(this).find('#submitbtn').removeClass('submitpulse');
      //$('#form').trigger('rescan.areYouSure');
    }); 
    
    rescan_now();
    
    //catch blur on tinymce fields!
    $( window ).load(function(){
        tinymce.get('id_notes').on('blur', function(e) {
            //var content = tinymce.get('id');
            //console.log(content);
            //alert("here");
            $('#form').trigger('checkform.areYouSure');
            
        });
    });    
    $( window ).load(function(){
        tinymce.get('id_music_list').on('blur', function(e) {
            //var content = tinymce.get('id');
            //console.log(content);
            //alert("here");
            $('#form').trigger('checkform.areYouSure');
            
        });
    });    
    $( window ).load(function(){
        tinymce.get('id_records').on('blur', function(e) {
            //var content = tinymce.get('id');
            //console.log(content);
            //alert("here");
            $('#form').trigger('checkform.areYouSure');
            
        });
    });    
    
    
    $(window).resize(function() {
        $('#hide1').trigger('input');        
        $('#hide2').trigger('input');
    });
    
    
    $(function(){
      $('#hide1').text($('#id_name').val());
      if (placeholderActive('#id_name')) {
        $('#hide1').text($('#id_name').attr('placeholder'));   
      }
      var wide = Number($('#hide1').width());
      wide = wide + 4;
      $('#id_name').width(wide);
      //$('#id_name').width($('#hide1').width());
    }).on('input', function () {
      $('#hide1').text($('#id_name').val());
      if (placeholderActive('#id_name')) {
        $('#hide1').text($('#id_name').attr('placeholder'));   
      }
      var wide = Number($('#hide1').width());
      wide = wide + 4;
      $('#id_name').width(wide);
//       $('#id_name').width($('#hide1').width());
    });
    
    
    $(function(){
      $('#hide2').text($('#id_event_type_0').val());
      if (placeholderActive('#id_event_type_0')) {
        $('#hide2').text($('#id_event_type_0').attr('placeholder'));   
      }
      var wide = Number($('#hide2').width());
      wide = wide + 4;
      $('#id_event_type_0').width(wide);
//       $('#id_event_type_0').width($('#hide2').width());
//       var wide = Number($('#hide2').width());
//       if (wide > 300) {wide = 300;}
//       wide = wide + 10;
//       $('.evx-btntry .ui-combo-button').css("left", wide);
    }).on('input', function () {
      $('#hide2').text($('#id_event_type_0').val());
      if (placeholderActive('#id_event_type_0')) {
        $('#hide2').text($('#id_event_type_0').attr('placeholder'));   
      }
      var wide = Number($('#hide2').width());
      wide = wide + 4;
      $('#id_event_type_0').width(wide);
//       $('#id_event_type_0').width($('#hide2').width());
//       var wide = Number($('#hide2').width());
//       if (wide > 300) {wide = 300;}
//       wide = wide + 10;
//       $('.evx-btntry .ui-combo-button').css("left", wide);
    });

    $(function(){
      $('#hide3').text($('#id_ensemble_0').val());
      if (placeholderActive('#id_ensemble_0')) {
        $('#hide3').text($('#id_ensemble_0').attr('placeholder'));   
      }
      var wide = Number($('#hide3').width());
      wide = wide + 4;
      $('#id_ensemble_0').width(wide);
//       $('#id_ensemble_0').width($('#hide3').width());
//       var wide = Number($('#hide3').width());
//       if (wide > 220) {wide = 220;}
//       wide = wide + 10;
//       $('.evx-btntry2 .ui-combo-button').css("left", wide);
    }).on('input', function () {
      $('#hide3').text($('#id_ensemble_0').val());
      if (placeholderActive('#id_ensemble_0')) {
        $('#hide3').text($('#id_ensemble_0').attr('placeholder'));   
      }
      var wide = Number($('#hide3').width());
      wide = wide + 4;
      $('#id_ensemble_0').width(wide);
//       $('#id_ensemble_0').width($('#hide3').width());
//       var wide = Number($('#hide3').width());
//       if (wide > 220) {wide = 220;}
//       wide = wide + 10;
//       $('.evx-btntry2 .ui-combo-button').css("left", wide);
    });

    $(function(){
      $('#hide4').text($('#id_location_0').val());
      if (placeholderActive('#id_location_0')) {
        $('#hide4').text($('#id_location_0').attr('placeholder'));   
      }
      var wide = Number($('#hide4').width());
      wide = wide + 4;
      $('#id_location_0').width(wide);
//       $('#id_location_0').width($('#hide4').width());
//       var wide = Number($('#hide4').width());
//       if (wide > 280) {wide = 280;}
//       wide = wide + 7;
//       $('.evx-btntry3 .ui-combo-button').css("left", wide);
    }).on('input', function () {
      $('#hide4').text($('#id_location_0').val());
      if (placeholderActive('#id_location_0')) {
        $('#hide4').text($('#id_location_0').attr('placeholder'));   
      }
      var wide = Number($('#hide4').width());
      wide = wide + 4;
      $('#id_location_0').width(wide);
//       $('#id_location_0').width($('#hide4').width());
//       var wide = Number($('#hide4').width());
//       if (wide > 280) {wide = 280;}
//       wide = wide + 7;
//       $('.evx-btntry3 .ui-combo-button').css("left", wide);
    });

    $(function(){
      $('#hide5').text($('#id_location_details').val());
      if (placeholderActive('#id_location_details')) {
        $('#hide5').text($('#id_location_details').attr('placeholder'));   
      }
      var wide = Number($('#hide5').width());
      wide = wide + 4;
      $('#id_location_details').width(wide);
//       $('#id_location_details').width($('#hide5').width());
    }).on('input', function () {
      $('#hide5').text($('#id_location_details').val());
      if (placeholderActive('#id_location_details')) {
        $('#hide5').text($('#id_location_details').attr('placeholder'));   
      }
      var wide = Number($('#hide5').width());
      wide = wide + 4;
      $('#id_location_details').width(wide);
//       $('#id_location_details').width($('#hide5').width());
    });

    $(function(){
      $('#hide6').text($('#id_contact_0').val());
      if (placeholderActive('#id_contact_0')) {
        $('#hide6').text($('#id_contact_0').attr('placeholder'));   
      }
      var wide = Number($('#hide6').width());
      wide = wide + 4;
      $('#id_contact_0').width(wide);
//       $('#id_contact_0').width($('#hide6').width());
//       var wide = Number($('#hide6').width());
//       if (wide > 260) {wide = 260;}
//       wide = wide + 7;
//       $('.evx-btntry4 .ui-combo-button').css("left", wide);
    }).on('input', function () {
      $('#hide6').text($('#id_contact_0').val());
      if (placeholderActive('#id_contact_0')) {
        $('#hide6').text($('#id_contact_0').attr('placeholder'));   
      }
      var wide = Number($('#hide6').width());
      wide = wide + 4;
      $('#id_contact_0').width(wide);
//       $('#id_contact_0').width($('#hide6').width());
//       var wide = Number($('#hide6').width());
//       if (wide > 260) {wide = 260;}
//       wide = wide + 7;
//       $('.evx-btntry4 .ui-combo-button').css("left", wide);
    });

    $(function(){
      $('#hide7').text($('#id_contact_details').val());
      if (placeholderActive('#id_contact_details')) {
        $('#hide7').text($('#id_contact_details').attr('placeholder'));   
      }
      var wide = Number($('#hide7').width());
      wide = wide + 4;
      $('#id_contact_details').width(wide);
//       $('#id_contact_details').width($('#hide7').width());
    }).on('input', function () {
      $('#hide7').text($('#id_contact_details').val());
      if (placeholderActive('#id_contact_details')) {
        $('#hide7').text($('#id_contact_details').attr('placeholder'));   
      }
      var wide = Number($('#hide7').width());
      wide = wide + 4;
      $('#id_contact_details').width(wide);
//       $('#id_contact_details').width($('#hide7').width());
    });

    $(function(){
      $('#hide8').text($('#id_friendly_name').val());
      if (placeholderActive('#id_friendly_name')) {
        $('#hide8').text($('#id_friendly_name').attr('placeholder'));   
      }
      var wide = Number($('#hide8').width());
      wide = wide + 4;
      $('#id_friendly_name').width(wide);
//       $('#id_friendly_name').width($('#hide8').width());
    }).on('input', function () {
      $('#hide8').text($('#id_friendly_name').val());
      if (placeholderActive('#id_friendly_name')) {
        $('#hide8').text($('#id_friendly_name').attr('placeholder'));   
      }
      var wide = Number($('#hide8').width());
      wide = wide + 4;
      $('#id_friendly_name').width(wide);
//       $('#id_friendly_name').width($('#hide8').width());
    });

    $(function(){
      $('#hide9').text($('#id_contact_email').val());
      if (placeholderActive('#id_contact_email')) {
        $('#hide9').text($('#id_contact_email').attr('placeholder'));   
      }
      var wide = Number($('#hide9').width());
      wide = wide + 4;
      $('#id_contact_email').width(wide);
//       $('#id_contact_email').width($('#hide9').width());
    }).on('input', function () {
      $('#hide9').text($('#id_contact_email').val());
      if (placeholderActive('#id_contact_email')) {
        $('#hide9').text($('#id_contact_email').attr('placeholder'));   
      }
      var wide = Number($('#hide9').width());
      wide = wide + 4;
      $('#id_contact_email').width(wide);
//       $('#id_contact_email').width($('#hide9').width());
    });

    $(function(){
      $('#hide10').text($('#id_dayofcontact_0').val());
      if (placeholderActive('#id_dayofcontact_0')) {
        $('#hide10').text($('#id_dayofcontact_0').attr('placeholder'));   
      }
      var wide = Number($('#hide10').width());
      wide = wide + 4;
      $('#id_dayofcontact_0').width(wide);
//       $('#id_dayofcontact_0').width($('#hide10').width());
//       var wide = Number($('#hide10').width());
//       if (wide > 275) {wide = 275;}
//       wide = wide + 7;
//       $('.evx-btntry5 .ui-combo-button').css("left", wide);
    }).on('input', function () {
      $('#hide10').text($('#id_dayofcontact_0').val());
      if (placeholderActive('#id_dayofcontact_0')) {
        $('#hide10').text($('#id_dayofcontact_0').attr('placeholder'));   
      }
      var wide = Number($('#hide10').width());
      wide = wide + 4;
      $('#id_dayofcontact_0').width(wide);
//       $('#id_dayofcontact_0').width($('#hide10').width());
//       var wide = Number($('#hide10').width());
//       if (wide > 275) {wide = 275;}
//       wide = wide + 7;
//       $('.evx-btntry5 .ui-combo-button').css("left", wide);
    });

    $(function(){
      $('#hide11').text($('#id_dayofcontact_details').val());
      if (placeholderActive('#id_dayofcontact_details')) {
        $('#hide11').text($('#id_dayofcontact_details').attr('placeholder'));   
      }
      var wide = Number($('#hide11').width());
      wide = wide + 4;
      $('#id_dayofcontact_details').width(wide);
//       $('#id_dayofcontact_details').width($('#hide11').width());
    }).on('input', function () {
      $('#hide11').text($('#id_dayofcontact_details').val());
      if (placeholderActive('#id_dayofcontact_details')) {
        $('#hide11').text($('#id_dayofcontact_details').attr('placeholder'));   
      }
      var wide = Number($('#hide11').width());
      wide = wide + 4;
      $('#id_dayofcontact_details').width(wide);
//       $('#id_dayofcontact_details').width($('#hide11').width());
    });









    if ($('#id_event_type_0').val().includes('eremony') || $('#id_event_type_name').val().includes('eremony')) {
        $('#cerdiv').attr('style','margin-top:5px;');
    } else {
        $('#cerdiv').attr('style', 'display:none !important;margin-top:5px;');
    }

    $('#id_event_type_0').on('change', function () {
        if ($('#id_event_type_0').val().includes('eremony')) {
            $('#cerdiv').attr('style','margin-top:5px;');
        } else {
            $('#cerdiv').attr('style', 'display:none !important;margin-top:5px;');
        }
    });

    //set focus to name input
    if (flag == 'new') {
        $('#id_name').focus();
    }

    //show/hide accept custom checkmark
    show_accept_custom();
    
    

    //var parts = $('#eventdate_norm').val().split('-');
    //var mydate = new Date(parts[2],parts[0]-1,parts[1]);
    $(function() {
        $('#id_date').datepicker({
            autoClose: 'True',
            showDaysInNextAndPreviousMonths: 'True',
            format: 'dddd, mmmm d, yyyy',
            firstDay: 1,
            //setDefaultDate: 'True',
            //defaultDate: mydate,
        });
    });
    //when date is changed, clear event_reminders_done flag!
    $('#id_date').on('change', function() {
        $('#id_event_reminders_done').prop("checked", false);
        //alert('doing13');
        updateFlags();
        M.updateTextFields();
    });
   
     //update badges/flags
    updateFlags();
    //updateActivities();
   
});



$("#musname-sortable").on("sortstop", afterDrag); 

$(".cursor-drag").on("mousedown", function () {
    $(this).addClass("mouseDown");  
}).on("mouseup", function () {
    $(this).removeClass("mouseDown");
});



function afterDrag() {
    var sortedIDs = $("#musname-sortable").sortable("toArray");
//     alert(sortedIDs);
//     alert(sortedIDs[0]);
//     alert(sortedIDs[1]);
//     alert(sortedIDs[2]);
//     alert(sortedIDs.length);
    var sortednums = [];
    $.each(sortedIDs, function(index, value) {
        sortednums[index] = sortedIDs[index].substr(7);
    });
//     alert(sortednums);
    var data = {
        "sortednums": JSON.stringify(sortednums),
        "event": $("#page_instance").val(),
    };    
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/reorderdragmusicians',
        data: data,
        success: function(data) {
            //alert(data['error']);
            if (data['error'] == true) {
                alert('The rank you entered is not allowed!');
            } else {
                updateMusiciansList();
//                 $("#musname-sortable").sortable();
            }
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with reordering musicianslist...");
        }
    });    
}




function show_accept_custom() {
    var data = {
//         "event_id": $('#page_instance').val()
        "music_list": $('#id_music_list').val()
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/check_accept_custom',
        data: data,
        success: function(data) {
            var dollars = Number(data['dollars']);
            //alert(dollars);
            if (dollars == 0) {
                //alert('add noshow');
                $("#id_accept_custom_hide").addClass("noshow");
            } else {
                $("#id_accept_custom_hide").removeClass("noshow");
            }
        },
        error: function(data) {
            alert("Something went wrong, with show_accept_custom");
        }   
    });
}




function rescan_now() {
    //$('#id_event_reminders_done').prop("checked", true);
    //
    //use fake ajax so it cues behind all others
    var data = {
        "dummy": "dummy",
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/fakeajax',
        data: data,
        success: function(data) {
            $('#form').trigger('reinitialize.areYouSure');
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with rescan_now...");
        }
    });
}
function recheck_now() {
    //$('#id_event_reminders_done').prop("checked", true);
    //
    //use fake ajax so it cues behind all others
    var data = {
        "dummy": "dummy",
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/fakeajax',
        data: data,
        success: function(data) {
            $('#form').trigger('checkform.areYouSure');
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with rescan_now...");
        }
    });
}







function cursor_wait()
{
    // switch to cursor wait for the current element over
    var elements = $(':hover');
    if (elements.length)
    {
        // get the last element which is the one on top
        elements.last().addClass('cursor-wait');
    }
    // use .off() and a unique event name to avoid duplicates
    $('html').
    off('mouseover.cursorwait').
    on('mouseover.cursorwait', function(e)
    {
        // switch to cursor wait for all elements you'll be over
        $(e.target).addClass('cursor-wait');
    });
}

function remove_cursor_wait()
{
    $('html').off('mouseover.cursorwait'); // remove event handler
    $('.cursor-wait').removeClass('cursor-wait'); // get back to default
}

$(document).ajaxStart(function () {
    cursor_wait();
});
$(document).ajaxComplete(function () {
    remove_cursor_wait();
});




$("#pnl1").on("click", function(e) {
    var data = {
        "panel": "1",
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/sidecalpanelclick',
        data: data,
        success: function(data) {
            var nothing = 1;
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with the side panel being clicked...");
        }
    });
});
$("#pnl2").on("click", function(e) {
    var data = {
        "panel": "2",
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/sidecalpanelclick',
        data: data,
        success: function(data) {
            var nothing = 1;
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with the side panel being clicked...");
        }
    });
});
$("#pnl3").on("click", function(e) {
    var data = {
        "panel": "3",
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/sidecalpanelclick',
        data: data,
        success: function(data) {
            var nothing = 1;
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with the side panel being clicked...");
        }
    });
});
$("#pnl4").on("click", function(e) {
    var data = {
        "panel": "4",
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/sidecalpanelclick',
        data: data,
        success: function(data) {
            var nothing = 1;
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with the side panel being clicked...");
        }
    });
});
$("#pnl5").on("click", function(e) {
    var data = {
        "panel": "5",
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/sidecalpanelclick',
        data: data,
        success: function(data) {
            var nothing = 1;
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with the side panel being clicked...");
        }
    });
});
$("#pnl6").on("click", function(e) {
    var data = {
        "panel": "6",
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/sidecalpanelclick',
        data: data,
        success: function(data) {
            var nothing = 1;
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with the side panel being clicked...");
        }
    });
});



//helper function to convert yyyy-mm-dd to javascript date object
function convertdate(date) {
    var parts = date.split("-");
    return new Date(parts[0], parts[1] - 1, parts[2]);
}
//helper function to convert mm/dd/yy to javascript date object
function convertdate2(date) {
    var parts = date.split("/");
    return new Date(20 + parts[2], parts[0] - 1, parts[1]);
}


//**************************newest*****************************************
//*******************************************************************



//if any location field is focused, determine if panel is already
//   open, and if not, auto-open it?




//set fees fields to nothing on focus if they are currently 0
$('#id_fee').on('focus', function(event, ui) {
    if (!$('#id_fee').nval()) {
        $('#id_fee').val('');
    }   
});
$('#id_fee').on('blur', function(event, ui) {
    if (!$('#id_fee').nval()) {
        $('#id_fee').val('0');
        M.updateTextFields();
    }   
});
$('#id_deposit_fee').on('focus', function(event, ui) {
    if (!$('#id_deposit_fee').nval()) {
        $('#id_deposit_fee').val('');
    }   
});
$('#id_deposit_fee').on('blur', function(event, ui) {
    if (!$('#id_deposit_fee').nval()) {
        $('#id_deposit_fee').val('0');
        M.updateTextFields();
    }   
});
$('#id_extra_fee').on('focus', function(event, ui) {
    if (!$('#id_extra_fee').nval()) {
        $('#id_extra_fee').val('');
    }   
});
$('#id_extra_fee').on('blur', function(event, ui) {
    if (!$('#id_extra_fee').nval()) {
        $('#id_extra_fee').val('0');
        M.updateTextFields();
    }   
});
$('#id_final_fee').on('focus', function(event, ui) {
    if (!$('#id_final_fee').nval()) {
        $('#id_final_fee').val('');
    }   
});
$('#id_final_fee').on('blur', function(event, ui) {
    if (!$('#id_final_fee').nval()) {
        $('#id_final_fee').val('0');
        M.updateTextFields();
    }   
});
$('#id_cash_fee').on('focus', function(event, ui) {
    if (!$('#id_cash_fee').nval()) {
        $('#id_cash_fee').val('');
    }   
});
$('#id_cash_fee').on('blur', function(event, ui) {
    if (!$('#id_cash_fee').nval()) {
        $('#id_cash_fee').val('0');
        M.updateTextFields();
    }   
});
$('#id_musician_fee').on('focus', function(event, ui) {
    if (!$('#id_musician_fee').nval()) {
        $('#id_musician_fee').val('');
    }   
});
$('#id_musician_fee').on('blur', function(event, ui) {
    if (!$('#id_musician_fee').nval()) {
        $('#id_musician_fee').val('0');
        M.updateTextFields();
    }   
});
$('#id_contracting_fee').on('focus', function(event, ui) {
    if (!$('#id_contracting_fee').nval()) {
        $('#id_contracting_fee').val('');
    }   
});
$('#id_contracting_fee').on('blur', function(event, ui) {
    if (!$('#id_contracting_fee').nval()) {
        $('#id_contracting_fee').val('0');
        M.updateTextFields();
    }   
});
$('#id_number_guests').on('focus', function(event, ui) {
    if (!$('#id_number_guests').nval()) {
        $('#id_number_guests').val('');
    }   
});
$('#id_number_guests').on('blur', function(event, ui) {
    if (!$('#id_number_guests').nval()) {
        $('#id_number_guests').val('0');
        M.updateTextFields();
    }   
});







$("#id_search").on('click', function(event, ui) {
    $("#id_search").next().click();
});

$("#id_search").on('djselectableselect', function(event, ui) {
    //alert($("#id_search").val()); 
    var chosen = $("#id_search").val();
    var chosenid = chosen.substring(
        chosen.lastIndexOf("{") + 1,
        chosen.lastIndexOf("}")
        );   
    var newurl = "/events/" + chosenid + "/edit";
    setTimeout(function(){document.location.href = newurl;},50);
});

$("#search_results_show_extras").on('click', function(event, ui) {
    //alert('clicked');
    $("#search_results_extras").toggleClass('noshow'); 
    if ($("#search_results_show_extras").html() == 'Show Full Results...') {
        $("#search_results_show_extras").html('Hide Full Results...');    
    } else {
        $("#search_results_show_extras").html('Show Full Results...');    
    }  
});




$( window ).resize(function() {
    //alert("change");
    M.textareaAutoResize($("#id_location_details"));
    M.textareaAutoResize($("#id_contact_details"));
    M.textareaAutoResize($("#id_dayofcontact_details"));
    //M.textareaAutoResize($("#id_contact_email"));
    
});


$("#id_search").keypress(function(e) {
    if (e.which == '13') {
        if (!$('#id_search').val()) {
            e.preventDefault();
        }
    }
});



$("#id_type").on('keydown', function(e) {
    if (e.which == '9' && !e.shiftKey) {
        $('#id_start_time').focus();
        e.preventDefault();
    }
});
$("#id_start_time").on('keydown', function(e) {
    if (e.which == '9' && e.shiftKey) {
        $('#id_type').focus();
        e.preventDefault();
    }
});

// $(".choosefirst").keydown(function(e) {
//     if (e.which == '40' && !$(this).val()) {
//         var elementid = $(this).attr('id');
//         $(this).next().click();
//     }
// });

$(".choosefirst").keypress(function(e) {
    if (e.which == '13') {
        var elementid = $(this).attr('id');
        var thisid = '';
        var hiddenid = '';
        if (elementid == 'id_event_type_0') {
            thisid = 'ui-id-2';
            hiddenid = 'id_event_type_1';
        }
        if (elementid == 'id_ensemble_0') {
            thisid = 'ui-id-3';
            hiddenid = 'id_ensemble_1';
        }
        if (elementid == 'id_location_0') {
            thisid = 'ui-id-4';
            hiddenid = 'id_location_1';
        }
        if (elementid == 'id_contact_0') {
            thisid = 'ui-id-5';
            hiddenid = 'id_contact_1';
        }
        if (elementid == 'id_dayofcontact_0') {
            thisid = 'ui-id-6';
            hiddenid = 'id_dayofcontact_1';
        }
        if (elementid == 'id_instrument') {
            thisid = 'ui-id-7';
            hiddenid = 'id_instrument_1';
        }
        if (elementid == 'id_musician') {
            thisid = 'ui-id-8';
            hiddenid = 'id_musician_1';
        }
        
        var firstitem = $('#' + thisid + '.ui-autocomplete.ui-front.ui-menu.ui-widget.ui-widget-content li:nth-child(1)').text();
        $(this).val(firstitem);
        
        
        var data = {
            "item": firstitem,
            'element': elementid
        };
        $.ajaxq("MyQueue", {
            type: 'GET',
            url: '/get_id_from_value',
            data: data,
            success: function(data) {
                var newidforitem = Number(data['newid']);
                $('#' + hiddenid).val(newidforitem);
            },
            error: function(data) {
                //don't register an error, otherwise pressing return on
                //blank line generates the error :)
                //alert("Something went wrong, with get_id_from_value");
            }   
        });
        
        $(this).trigger("blur");
//         $(this).trigger("djselectablechange");
        $(this).trigger("djselectableselect");
        $(this).trigger("focus");
    }        
    
});


$(".nosubmit").keypress(
    function(event) {
        if (event.which == '13') {
            event.preventDefault();
            //if was from id_musician then
            //click addmusician_btn
            if ($(this).hasClass("specialsubmit")) {
//                 $(this).trigger("djselectableclose");
                $("#addmusician_btn").click();
                $("#id_instrument").focus();
                $("#id_musician").focus();
            }
        }
});


$("#id_type").on('focusin', function() {
    $('#id_type').addClass("evx-focusin");
});
$("#id_type").on('focusout', function() {
    $('#id_type').removeClass("evx-focusin");
});
$("#reminders_bar_header").on('focusin', function() {
    $('#reminders_bar_header').addClass("evx-focusin2");
});
$("#reminders_bar_header").on('focusout', function() {
    $('#reminders_bar_header').removeClass("evx-focusin2");
});
$("#notes_bar_header").on('focusin', function() {
    $('#notes_bar_header').addClass("evx-focusin2");
});
$("#notes_bar_header").on('focusout', function() {
    $('#notes_bar_header').removeClass("evx-focusin2");
});
$("#records_bar_header").on('focusin', function() {
    $('#records_bar_header').addClass("evx-focusin2");
});
$("#records_bar_header").on('focusout', function() {
    $('#records_bar_header').removeClass("evx-focusin2");
});
$("#history_bar_header").on('focusin', function() {
    $('#history_bar_header').addClass("evx-focusin2");
});
$("#history_bar_header").on('focusout', function() {
    $('#history_bar_header').removeClass("evx-focusin2");
});
$("#id_indooroutdoor").on('focusin', function() {
    $('#id_indooroutdoor').addClass("evx-focusin4");
});
$("#id_indooroutdoor").on('focusout', function() {
    $('#id_indooroutdoor').removeClass("evx-focusin4");
});
// $("#id_reminderdisable").on('focusin', function() {
//     $('#reminderdisable_lbl').addClass("evx-focusin3");
// });
// $("#id_reminderdisable").on('focusout', function() {
//     $('#reminderdisable_lbl').removeClass("evx-focusin3");
// });
// $("#id_automation").on('focusin', function() {
//     $('#automation_lbl').addClass("evx-focusin3");
// });
// $("#id_automation").on('focusout', function() {
//     $('#automation_lbl').removeClass("evx-focusin3");
// });



$("#search_form").on('focusin', function() {
    $('#search_lbl').removeClass("ev_search_lbl");
});
$("#search_form").on('focusout', function() {
    $('#search_lbl').addClass("ev_search_lbl");
});

//  $("#id_notes").on("focusout", function(e) {
//      alert("here");
//      $('#form').trigger('checkform.areYouSure');
//  });


    function placeholderActive(selector) {
      var el = document.querySelector(selector);
      if (el.getAttribute('placeholder') && el.value === '') {
        return true;
      }
      return false;
    }

    $("#id_ceremony_time").on('change', function() {
        if (placeholderActive('#id_ceremony_time')) {
            $("#ceremon_time_adj").addClass("evx-time3a");
            $("#ceremon_time_adj").removeClass("evx-time3");
        } else {
            $("#ceremon_time_adj").addClass("evx-time3");
            $("#ceremon_time_adj").removeClass("evx-time3a");
        }
    });

//     $("#location_box").on('click', function() {
//         alert("clicked!");    
//         
//         
//     });
    








//***********************end newest******************************



function roundtime(time) {
    if (time == '') {
        return time;
    }
    //if no am/pm, add it and assume PM
    if (!isNaN(time.slice(-1))) {
        time = time + " PM";
    }
    //if only a or p, change it to AM/PM
    if (time.slice(-1) == 'm' || time.slice(-1) == 'M') {
        if (time.slice(-2) == 'am' || time.slice(-2) == 'AM') {
            time = time.slice(0, -2) + 'AM';         
        } else if (time.slice(-2) == 'pm' || time.slice(-2) == 'PM') {
            time = time.slice(0, -2) + 'PM';
        } else {
            time = 'error';
            return time;
        }
    } else {
        if (time.slice(-1) == 'a' || time.slice(-1) == 'A') {
            time = time.slice(0,-1) + 'AM';
        } else if (time.slice(-1) == 'p' || time.slice(-1) == 'P') {
            time = time.slice(0,-1) + 'PM';
        } else {
            time = 'error';
            return time;
        }
        
    }
    //if no space before am/pm, add it
    if (time.substr(-3,1) != ' ') {
        time = time.slice(0, -2) + ' ' + time.slice(-2);
    }
    //if no minutes, add :00 AND if 3 or 4 digits exist, assume colon
//     if (time.substr(-6, 1) != ':') {
//         time = time.slice(0, -3) + ':00' + time.slice(-3);    
//     }
    
    //if no colon:  either add :00 or parse into proper minutes
    var colon = time.indexOf(':');
    if (colon == -1) {
        var firstpart = time.substr(0, time.indexOf(' '));
        //alert(firstpart);
        //alert(firstpart.length);
        if (firstpart.length < 3) {
            
            //firstpart is 1 or 2 digits, so add :00
            time = time.slice(0, -3) + ':00' + time.slice(-3);        
        } else {
            //alert(time);
            //firstpart is 3 or more, so assume we entered minutes but with no colon
            time = time.slice(0, -5) + ':' + time.slice(-5);
        }
        
    }
        
    //round minutes to nearest 5
    var temptime = time.split(":");
    var hourstr = temptime[0];
    var minstr = temptime[1].split(" ");
    var ampmstr = minstr[1];
    var min = parseInt(minstr[0], 10);
    var hour = parseInt(hourstr, 10);
    roundedmin = Math.round(min /5 ) * 5;
    if (roundedmin == 60) {
        roundedmin = 0;
    }
    var newhouri = hour.toString();
    var newhour = newhouri.padStart(2, '0');
    var newmini = roundedmin.toString();
    var newmin = newmini.padStart(2, '0');
    var newtime = newhour + ":" + newmin + " " + ampmstr;
    
    newtime = newtime.replace(/^0+/,'');
    return newtime;
}


$("#id_start_time").on('change', function() {
    var time = $("#id_start_time").val();
    var newtime = roundtime(time);
    $("#id_start_time").val(newtime);
});
$("#id_end_time").on('change', function() {
    var time = $("#id_end_time").val();
    var newtime = roundtime(time);
    $("#id_end_time").val(newtime);
});
$("#id_ceremony_time").on('change', function() {
    var time = $("#id_ceremony_time").val();
    var newtime = roundtime(time);
    $("#id_ceremony_time").val(newtime);
});













//changed below to not used pulled database flags, but use current page id flags
//then, added version of models' _is_past_due methods here in java to determine if red
//  I put py version of this updateFlags routine in views, called
//                  before loading home page or browse pages
//       finally, add something similar if user changes hold->regular in js,
//                  add something similar if user changes event date
//                  add something similar if user changes contract/deposit rcvd dates directly
function updateFlags2() {
    //first get the latest duedates and reminders in place
    //updateDueDates();


    //alert('flags');
    var el = document.getElementById("id_type");
    var selected = el.options[el.selectedIndex].text;
    var hold_pastdue = false;
    var contract_pastdue = false;
    var deposit_pastdue = false;
    var final_pastdue = false;
    var music_list_pastdue = false;
    var musicians_pastdue = false;
    var confirmation_pastdue = false;
    var fact_sheets_pastdue = false;
    var extra_pastdue = false;
    var today = new Date();
    today.setHours(0, 0, 0, 0);


    if (selected == 'Hold' && !isEmptyOrSpaces($('#id_hold_until').val())) {
        if (today > convertdate2($('#id_hold_until').val())) {
            hold_pastdue = true;
        }
    }

    if ($('#id_flag_contract_sent').prop('checked') && !$('#id_flag_contract_rcvd').prop('checked')) {
        if (today > convertdate($('#id_contract_duedate').val())) {
            contract_pastdue = true;
        }
    } else if (!$('#id_flag_contract_sent').prop('checked')) {
        if (today > convertdate($('#id_contract_senddate').val())) {
            contract_pastdue = true;
        }
    } else if ($('#id_flag_contract_rcvd').prop('checked') && !$('#id_flag_contract_rcpt').prop('checked')) {
        if (today > convertdate($('#id_contract_rcptdate').val())) {
            contract_pastdue = true;
        }
    }

    if ($('#id_flag_deposit_sent').prop('checked') && !$('#id_flag_deposit_rcvd').prop('checked')) {
        if (today > convertdate($('#id_deposit_duedate').val())) {
            deposit_pastdue = true;
        }
    } else if (!$('#id_flag_deposit_sent').prop('checked')) {
        if (today > convertdate($('#id_deposit_senddate').val())) {
            deposit_pastdue = true;
        }
    } else if ($('#id_flag_deposit_rcvd').prop('checked') && !$('#id_flag_deposit_rcpt').prop('checked')) {
        if (today > convertdate($('#id_deposit_rcptdate').val())) {
            deposit_pastdue = true;
        }
    }

    if ($('#id_flag_music_list_sent').prop('checked') && !$('#id_flag_music_list_rcvd').prop('checked')) {
        if (today > convertdate($('#id_music_list_duedate').val())) {
            music_list_pastdue = true;
        }
    } else if (!$('#id_flag_music_list_sent').prop('checked')) {
        if (today > convertdate($('#id_music_list_senddate').val())) {
            music_list_pastdue = true;
        }
    }

    if ($('#id_flag_musicians_sent').prop('checked') && !$('#id_flag_musicians_rcvd').prop('checked')) {
        if (today > convertdate($('#id_musicians_duedate').val())) {
            musicians_pastdue = true;
        }
    } else if (!$('#id_flag_musicians_sent').prop('checked')) {
        if (today > convertdate($('#id_musicians_senddate').val())) {
            musicians_pastdue = true;
        }
    }

    if ($('#id_flag_final_payment_sent').prop('checked') && !$('#id_flag_final_payment_rcvd').prop('checked')) {
        if (today > convertdate($('#id_final_duedate').val())) {
            final_pastdue = true;
        }
    } else if (!$('#id_flag_final_payment_sent').prop('checked')) {
        if (today > convertdate($('#id_final_senddate').val())) {
            final_pastdue = true;
        }
    } else if ($('#id_flag_final_payment_rcvd').prop('checked') && !$('#id_flag_final_payment_rcpt').prop('checked')) {
        if (today > convertdate($('#id_final_rcptdate').val())) {
            final_pastdue = true;
        }
    }


    if ($('#id_flag_extra_sent').prop('checked') && !$('#id_flag_extra_rcvd').prop('checked')) {
        if (today > convertdate($('#id_extra_duedate').val())) {
            extra_pastdue = true;
        }
    } else if (!$('#id_flag_extra_sent').prop('checked')) {
        if (today > convertdate($('#id_extra_senddate').val())) {
            extra_pastdue = true;
        }
    } else if ($('#id_flag_extra_rcvd').prop('checked') && !$('#id_flag_extra_rcpt').prop('checked')) {
        if (today > convertdate($('#id_extra_rcptdate').val())) {
            extra_pastdue = true;
        }
    }






    if ($('#id_flag_final_confirmation_sent').prop('checked') && !$('#id_flag_final_confirmation_rcvd').prop('checked')) {
        if (today > convertdate($('#id_confirmation_duedate').val())) {
            confirmation_pastdue = true;
        }
    } else if (!$('#id_flag_final_confirmation_sent').prop('checked')) {
        if (today > convertdate($('#id_confirmation_senddate').val())) {
            confirmation_pastdue = true;
        }
    }

    if ($('#id_flag_fact_sheets_sent').prop('checked') && !$('#id_flag_fact_sheets_rcvd').prop('checked')) {
        if (today > convertdate($('#id_fact_sheets_duedate').val())) {
            fact_sheets_pastdue = true;
        }
    } else if (!$('#id_flag_fact_sheets_sent').prop('checked')) {
        if (today > convertdate($('#id_fact_sheets_senddate').val())) {
            fact_sheets_pastdue = true;
        }
    }


    $('#flag_contract').removeClass();
//     $('#flag_contract').attr("data-badge-caption", "contract");
    $('#flag_contract').html('<i class="material-icons prefix evx-progress">event_note</i>');
    $('#flag_contract').addClass('flag-empty evx-circle');
    $('#id_color_contract').val(flag_empty);

    $('#btn_factsheet').removeClass();
    $('#btn_musicians').removeClass();
    $('#btn_confirmation').removeClass();
    $('#btn_receipt_finalpay').removeClass();
    $('#btn_receipt_finalpay').addClass('noshow');
    $('#btn_finalpay').removeClass();
    
    $('#btn_extrapay').removeClass();
    $('#btn_extrapay').addClass('noshow');
    $('#btn_receipt_extrapay').removeClass();
    $('#btn_receipt_extrapay').addClass('noshow');
        
    $('#btn_musiclist').removeClass();
    $('#btn_receipt_deposit').removeClass();
    $('#btn_receipt_deposit').addClass('noshow');
    $('#btn_receipt_contract').removeClass();
    $('#btn_receipt_contract').addClass('noshow');
    $('#btn_deposit').removeClass();
    $('#btn_contract').removeClass();
    $('#btn_depositcontract').removeClass();
    $('#btn_hold').removeClass();
    $('#btn_hold').addClass('noshow');
    
    //all fab_ and fab_check_ id's default to bold
    //      and no checks, EXCEPT hold and receipts which
    //      default to lite (and no checks)
//temporarily disable the following, till Janie decides she want
//send buttons to show the stuff that needs doing, doesn't need doing,
//or doesn't make sense (bold, reg, lite, checks).
//this block of code below sets the defaults only - after that, all
//the other code that decides and toggles the items still needs to be
//added, lower in this function...
//     $('#fab_depositcontract').removeClass();
//     $('#fab_depositcontract').addClass('fab-bold');
//     $('#fab_check_depositcontract').removeClass('fab-check');
//     $('#fab_check_depositcontract').addClass('fab-nocheck');
//     
//     $('#fab_hold').removeClass();
//     $('#fab_hold').addClass('fab-lite');
//     $('#fab_check_hold').removeClass('fab-check');
//     $('#fab_check_hold').addClass('fab-nocheck');
//     
//     $('#fab_contract').removeClass();
//     $('#fab_contract').addClass('fab-bold');
//     $('#fab_check_contract').removeClass('fab-check');
//     $('#fab_check_contract').addClass('fab-nocheck');
//     
//     $('#fab_deposit').removeClass();
//     $('#fab_deposit').addClass('fab-bold');
//     $('#fab_check_deposit').removeClass('fab-check');
//     $('#fab_check_deposit').addClass('fab-nocheck');
//     
//     $('#fab_receipt_contract').removeClass();
//     $('#fab_receipt_contract').addClass('fab-lite');
//     $('#fab_check_receipt_contract').removeClass('fab-check');
//     $('#fab_check_receipt_contract').addClass('fab-nocheck');
//     
//     $('#fab_receipt_deposit').removeClass();
//     $('#fab_receipt_deposit').addClass('fab-lite');
//     $('#fab_check_receipt_deposit').removeClass('fab-check');
//     $('#fab_check_receipt_deposit').addClass('fab-nocheck');
//     
//     $('#fab_finalpay').removeClass();
//     $('#fab_finalpay').addClass('fab-bold');
//     $('#fab_check_finalpay').removeClass('fab-check');
//     $('#fab_check_finalpay').addClass('fab-nocheck');
// 
//     $('#fab_receipt_finalpay').removeClass();
//     $('#fab_receipt_finalpay').addClass('fab-lite');
//     $('#fab_check_receipt_finalpay').removeClass('fab-check');
//     $('#fab_check_receipt_finalpay').addClass('fab-nocheck');
// 
//     $('#fab_extrapay').removeClass();
//     $('#fab_extrapay').addClass('fab-bold');
//     $('#fab_check_extrapay').removeClass('fab-check');
//     $('#fab_check_extrapay').addClass('fab-nocheck');
//     
//     $('#fab_receipt_extrapay').removeClass();
//     $('#fab_receipt_extrapay').addClass('fab-lite');
//     $('#fab_check_receipt_extrapay').removeClass('fab-check');
//     $('#fab_check_receipt_extrapay').addClass('fab-nocheck');
//     
//     $('#fab_confirmation').removeClass();
//     $('#fab_confirmation').addClass('fab-bold');
//     $('#fab_check_confirmation').removeClass('fab-check');
//     $('#fab_check_confirmation').addClass('fab-nocheck');




    if ($('#id_waive_contract').prop('checked')) {
        $('#flag_contract').removeClass();
        $('#flag_contract').html('<i class="material-icons prefix evx-progress">event_note</i>');
        $('#flag_contract').addClass('flag-white evx-circle');
        $('#id_color_contract').val(flag_white);
//         $('#flag_contract').attr("style", "text-decoration:line-through");
        $('#flag_contract_cross').removeClass("noshow");
        //hide all contract buttons
        $('#btn_contract').addClass('noshow');
        $('#btn_depositcontract').addClass('noshow');
    } else {
        $('#flag_contract_cross').addClass("noshow");
        if ($('#id_flag_contract_sent').prop('checked')) {
            $('#flag_contract').removeClass();
            $('#flag_contract').html('<i class="material-icons prefix evx-progress">event_note</i>');
            $('#flag_contract').addClass('flag-started evx-circle');
            $('#id_color_contract').val(flag_started);
            //hide contract btns
            $('#btn_contract').addClass('noshow');
            $('#btn_depositcontract').addClass('noshow');
        }
        if ($('#id_flag_contract_rcvd').prop('checked')) {
            $('#flag_contract').removeClass();
            $('#flag_contract').html('<i class="material-icons prefix evx-progress">event_note</i>');
            $('#flag_contract').addClass('flag-done evx-circle');
            $('#id_color_contract').val(flag_done);
            //hide contract btns, show receipt btn
            $('#btn_contract').addClass('noshow');
            $('#btn_depositcontract').addClass('noshow');
            $('#btn_receipt_contract').removeClass();
            //hide receipt btn if already sent
            if ($('#id_flag_contract_rcpt').prop('checked')) {
                $('#btn_receipt_contract').addClass('noshow');
            }
        }
        if (contract_pastdue) {
            $('#flag_contract').removeClass();
            $('#flag_contract').html('<i class="material-icons prefix evx-progress">event_note</i>');
            $('#flag_contract').addClass('flag-late evx-circle');
            $('#id_color_contract').val(flag_late);
        }
    }
    
    if (selected == 'Hold') {
        $('#flag_contract').removeClass();
//         $('#flag_contract').attr("data-badge-caption", "HOLD");
        $('#flag_contract').html('<i class="material-icons prefix evx-progress">pan_tool</i>');
        $('#flag_contract').addClass('flag-hold evx-circle');
        $('#id_color_contract').val(flag_hold);
        //hide almost all showing buttons, cause we're in a hold               
        $('#btn_factsheet').addClass('noshow');
        $('#btn_musicians').addClass('noshow');
        $('#btn_confirmation').addClass('noshow');
        $('#btn_finalpay').addClass('noshow');
        $('#btn_musiclist').addClass('noshow');
        $('#btn_deposit').addClass('noshow');
        $('#btn_contract').addClass('noshow');
        $('#btn_depositcontract').addClass('noshow');
        $('#btn_extrapay').addClass('noshow');
        
        $('#btn_hold').removeClass();
        //make red if hold past-due
        if (hold_pastdue) {
            $('#flag_contract').removeClass();
            $('#flag_contract').addClass('flag-late evx-circle');
            $('#id_color_contract').val(flag_late);
        }
    }


    if ($('#id_waive_payment').prop('checked') || ($("#id_deposit_senddate").val() && ($("#id_deposit_senddate").val() == $("#id_final_senddate").val())) || ($("#id_deposit_fee").val() == '0') || ($("#id_deposit_fee").val() == '0.00')) {
        $('#flag_deposit').removeClass();
        $('#flag_deposit').addClass('flag-white evx-circle');
        $('#id_color_deposit').val(flag_white);
        $('#flag_deposit_cross').removeClass("noshow");
        //hide all deposit buttons
        $('#btn_deposit').addClass('noshow');
        $('#btn_depositcontract').addClass('noshow');
        //if NOT waive_payment, then we're here because deposit is void and only finalpay is due.
        //  in that case, we check if contract button is being shown and if so, also show depositcontract button
        if (!($('#id_waive_payment').prop('checked'))) {
            if (!($('#btn_contract').hasClass('noshow'))) {
                $('#btn_depositcontract').removeClass('noshow');
            }            
        }
    } else {
        $('#flag_deposit_cross').addClass("noshow");
        $('#flag_deposit').removeClass();
        $('#flag_deposit').addClass('flag-empty evx-circle');
        if ($('#id_flag_deposit_sent').prop('checked')) {
            $('#flag_deposit').removeClass();
            $('#flag_deposit').addClass('flag-started evx-circle');
            $('#id_color_deposit').val(flag_started);
            //hide deposit btns
            $('#btn_deposit').addClass('noshow');
            $('#btn_depositcontract').addClass('noshow');
        }
        if ($('#id_flag_deposit_rcvd').prop('checked')) {
            $('#flag_deposit').removeClass();
            $('#flag_deposit').addClass('flag-done evx-circle');
            $('#id_color_deposit').val(flag_done);
            //hide deposit btns, show receipt btn
            $('#btn_deposit').addClass('noshow');
            $('#btn_depositcontract').addClass('noshow');
            $('#btn_receipt_deposit').removeClass();
            //hide receipt btn if already sent
            if ($('#id_flag_deposit_rcpt').prop('checked')) {
                $('#btn_receipt_deposit').addClass('noshow');
            }
        }
        if (deposit_pastdue) {
            $('#flag_deposit').removeClass();
            $('#flag_deposit').addClass('flag-late evx-circle');
            $('#id_color_deposit').val(flag_late);
        }
    }


    if ($('#id_waive_music_list').prop('checked')) {
        $('#flag_music_list').removeClass();
        $('#flag_music_list').addClass('flag-white evx-circle');
        $('#id_color_music_list').val(flag_white);
        $('#flag_music_list_cross').removeClass("noshow");
        //hide musiclist button
        $('#btn_musiclist').addClass('noshow');
    } else {
        $('#flag_music_list_cross').addClass("noshow");
        $('#flag_music_list').removeClass();
        $('#flag_music_list').addClass('flag-empty evx-circle');
        if ($('#id_flag_music_list_sent').prop('checked')) {
            $('#flag_music_list').removeClass();
            $('#flag_music_list').addClass('flag-started evx-circle');
            $('#id_color_music_list').val(flag_started);
            //hide musiclist button
            $('#btn_musiclist').addClass('noshow');
        }
        if ($('#id_flag_music_list_rcvd').prop('checked')) {
            $('#flag_music_list').removeClass();
            $('#flag_music_list').addClass('flag-done evx-circle');
            $('#id_color_music_list').val(flag_done);
            //hide musiclist button
            $('#btn_musiclist').addClass('noshow');
        }
        if (music_list_pastdue) {
            $('#flag_music_list').removeClass();
            $('#flag_music_list').addClass('flag-late evx-circle');
            $('#id_color_music_list').val(flag_late);
        }
    }

    if ($('#id_flag_musicians_sent').prop('checked')) {
        $('#flag_musicians').removeClass();
        $('#flag_musicians').addClass('flag-started evx-circle');
        $('#id_color_musicians').val(flag_started);
        //don't yet hide musicians button
        //$('#btn_musicians').addClass('noshow');
        //also include xbtn_musicians
        //var dummy;
        //dummy =  setTimeout(updateMusiciansAskedList, 1000);
    }
    if ($('#id_flag_musicians_rcvd').prop('checked')) {
        $('#flag_musicians').removeClass();
        $('#flag_musicians').addClass('flag-done evx-circle');
        $('#id_color_musicians').val(flag_done);
        //now hide musicians button, cause all hired
        $('#btn_musicians').addClass('noshow');
    }
    if (musicians_pastdue) {
        $('#flag_musicians').removeClass();
        $('#flag_musicians').addClass('flag-late evx-circle');
        $('#id_color_musicians').val(flag_late);
    }

    if ($('#id_waive_payment').prop('checked')) {
        $('#flag_final_pay').removeClass();
        $('#flag_final_pay').addClass('flag-white evx-circle');
        $('#id_color_final_payment').val(flag_white);
        $('#flag_final_pay_cross').removeClass("noshow");
        //hide finalpay button
        $('#btn_finalpay').addClass('noshow');
    } else {
        $('#flag_final_pay_cross').addClass("noshow");
        $('#flag_final_pay').removeClass();
        $('#flag_final_pay').addClass('flag-empty evx-circle');
        if ($('#id_flag_final_payment_sent').prop('checked')) {
            $('#flag_final_pay').removeClass();
            $('#flag_final_pay').addClass('flag-started evx-circle');
            $('#id_color_final_payment').val(flag_started);
            //hide finalpay button
            $('#btn_finalpay').addClass('noshow');
        }
        if ($('#id_flag_final_payment_rcvd').prop('checked')) {
            $('#flag_final_pay').removeClass();
            $('#flag_final_pay').addClass('flag-done evx-circle');
            $('#id_color_final_payment').val(flag_done);
            //hide finalpay btn, show receipt btn
            $('#btn_finalpay').addClass('noshow');
            $('#btn_receipt_finalpay').removeClass();
            //hide receipt btn if already sent
            if ($('#id_flag_final_payment_rcpt').prop('checked')) {
                $('#btn_receipt_finalpay').addClass('noshow');
            }
        }
        if (final_pastdue) {
            $('#flag_final_pay').removeClass();
            $('#flag_final_pay').addClass('flag-late evx-circle');
            $('#id_color_final_payment').val(flag_late);
        }
    }



    if ($('#id_waive_payment').prop('checked') || ($('#id_extra_fee').val() == 0 || !$('#id_extra_fee').val())) {
        $('#flag_extra_pay_cross').addClass('flag-white evx-circle-sm');
        $('#id_color_extra_payment').val(flag_white);
        $('#flag_extra_pay_cross').addClass("noshow");
        //hide extrapay button
        $('#btn_extrapay').addClass('noshow');
    } else {
        $('#btn_extrapay').removeClass('noshow');
        $('#flag_extra_pay_cross').removeClass("noshow");
        $('#flag_extra_pay_cross').addClass('flag-empty evx-circle-sm');
        if ($('#id_flag_extra_sent').prop('checked')) {
            $('#flag_extra_pay_cross').addClass('flag-started evx-circle-sm');
            $('#id_color_extra_payment').val('flag_started');
            //hide extrapay button
            $('#btn_extrapay').addClass('noshow');
        }
        if ($('#id_flag_extra_rcvd').prop('checked')) {
            $('#flag_extra_pay_cross').addClass('flag-done evx-circle-sm');
            $('#id_color_extra_payment').val('flag_done');
            //hide extrapay btn, show receipt btn
            $('#btn_extrapay').addClass('noshow');
            $('#btn_receipt_extrapay').removeClass();
            //hide receipt btn if already sent
            if ($('#id_flag_extra_rcpt').prop('checked')) {
                $('#btn_receipt_extrapay').addClass('noshow');
            }
        }
        if (extra_pastdue) {
            $('#flag_extra_pay_cross').addClass('flag-late evx-circle-sm');
            $('#id_color_extra_payment').val('flag_late');
        }
    }






    if ($('#id_flag_final_confirmation_sent').prop('checked')) {
        $('#flag_confirm').removeClass();
        $('#flag_confirm').addClass('flag-started evx-circle');
        $('#id_color_final_confirmation').val(flag_started);
        //hide confirmation button
        $('#btn_confirmation').addClass('noshow');
    }
    if ($('#id_flag_final_confirmation_rcvd').prop('checked')) {
        $('#flag_confirm').removeClass();
        $('#flag_confirm').addClass('flag-done evx-circle');
        $('#id_color_final_confirmation').val(flag_done);
        //hide confirmation button
        $('#btn_confirmation').addClass('noshow');
    }
    if (confirmation_pastdue) {
        $('#flag_confirm').removeClass();
        $('#flag_confirm').addClass('flag-late evx-circle');
        $('#id_color_final_confirmation').val(flag_late);
    }

    if ($('#id_flag_fact_sheets_sent').prop('checked')) {
        $('#flag_fact_sheets').removeClass();
        $('#flag_fact_sheets').addClass('flag-started evx-circle');
        $('#id_color_fact_sheets').val(flag_started);
        //hide factsheet button
        $('#btn_factsheet').addClass('noshow');
    }
    if ($('#id_flag_fact_sheets_rcvd').prop('checked')) {
        $('#flag_fact_sheets').removeClass();
        $('#flag_fact_sheets').addClass('flag-done evx-circle');
        $('#id_color_fact_sheets').val(flag_done);
        //hide factsheet button
        $('#btn_factsheet').addClass('noshow');
    }
    if (fact_sheets_pastdue) {
        $('#flag_fact_sheets').removeClass();
        $('#flag_fact_sheets').addClass('flag-late evx-circle');
        $('#id_color_fact_sheets').val(flag_late);
    }

    //new section for automation:
    //certain buttons hidden
    if ($('#id_automation').prop("checked") == true) {
        //not all auto reminders
        //are necessarily individually enabled to be 'auto'
        //anymore.  So need to check each one before hiding
        //associated buttons. 
        // SEND_HOLD, SEND_CONTRACT, SEND_DEPOSIT
        // (and if either of those two true hide depositcontract btn too)
        // RECEIPT_DEPOSIT, RECEIPT_CONTRACT,SEND_FINAL_PAYMENT, 
        //RECEIPT_FINAL_PAYMENT, SEND_FINAL_CONFIRMATION, SEND_MUSIC_LIST
        
        event.stopPropagation();
        var data = {
            "event_id": $('#page_instance').val()
        };
        $.ajaxq("MyQueue", {
            type: 'GET',
            url: '/checkremindersautostatus',
            data: data,
            success: function(data) {
                //got it
                if (data['sendhold'] == true) {
                    $('#btn_hold').addClass('noshow');
                }
                if (data['sendcontract'] == true) {
                    $('#btn_contract').addClass('noshow');
                    $('#btn_depositcontract').addClass('noshow');
                }
                if (data['senddeposit'] == true) {
                    $('#btn_deposit').addClass('noshow');
                    $('#btn_depositcontract').addClass('noshow');
                }
                if (data['receiptdeposit'] == true) {
                    $('#btn_receipt_deposit').addClass('noshow');
                }
                if (data['receiptcontract'] == true) {
                    $('#btn_receipt_contract').addClass('noshow');
                }
                if (data['sendfinalpayment'] == true) {
                    $('#btn_finalpay').addClass('noshow');
                }
                if (data['receiptfinalpayment'] == true) {
                    $('#btn_receipt_finalpay').addClass('noshow');
                }
                if (data['sendextrapayment'] == true) {
                    $('#btn_extrapay').addClass('noshow');
                }
                if (data['receiptextrapayment'] == true) {
                    $('#btn_receipt_extrapay').addClass('noshow');
                }
                if (data['sendfinalconfirmation'] == true) {
                    $('#btn_confirmation').addClass('noshow');
                }
                if (data['sendmusiclist'] == true) {
                    $('#btn_musiclist').addClass('noshow');
                }
                
            },
            error: function(data) {
                alert("Error in retrieving reminders auto status");
            }    
        });
    }
    disable_sendbtn();
        
}

function disable_sendbtn() {
    //ADD check here to see if all buttons are hidden?
    //    if so, disable the "Send" main button too!


    //use fake ajax so it cues behind all others
    var data = {
        "dummy": "dummy",
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/fakeajax',
        data: data,
        success: function(data) {

            var noemails = true;
            if (!($('#btn_factsheet').hasClass('noshow'))) {
                noemails = false;    
            }
            if (!($('#btn_musicians').hasClass('noshow'))) {
                noemails = false;    
            }
            if (!($('#btn_confirmation').hasClass('noshow'))) {
                noemails = false;    
            }
            if (!($('#btn_receipt_finalpay').hasClass('noshow'))) {
                noemails = false;    
            }
            if (!($('#btn_finalpay').hasClass('noshow'))) {
                noemails = false;    
            }
            if (!($('#btn_receipt_extrapay').hasClass('noshow'))) {
                noemails = false;    
            }
            if (!($('#btn_extrapay').hasClass('noshow'))) {
                noemails = false;    
            }
            if (!($('#btn_musiclist').hasClass('noshow'))) {
                noemails = false;    
            }
            if (!($('#btn_receipt_deposit').hasClass('noshow'))) {
                noemails = false;    
            }
            if (!($('#btn_receipt_contract').hasClass('noshow'))) {
                noemails = false;    
            }
            if (!($('#btn_deposit').hasClass('noshow'))) {
                noemails = false;    
            }
            if (!($('#btn_contract').hasClass('noshow'))) {
                noemails = false;    
            }
            if (!($('#btn_depositcontract').hasClass('noshow'))) {
                noemails = false;    
            }
            if (!($('#btn_hold').hasClass('noshow'))) {
                noemails = false;   
            }
            if (noemails) {
                $('#id_action_button').addClass('sendbtn_disable');
                //alert('disabled');
            } else {
                $('#id_action_button').removeClass('sendbtn_disable');    
                //alert("not disabled");
            }

        },
        error: function(data) {
            alert("Something Went Wrong, likely something with rescan_now...");
        }
    });
}



$(document).on('click', '#id_reminderdisable', function() {
    //change existing reminders to auto-mode if enabled,
    //or change existing reminders to non-auto-mode if disabled
    event.stopPropagation();
    if ($('#id_reminderdisable').prop("checked") == true) {
        var data = {
            "mode": "start",
            "event_id": $('#page_instance').val()
        };
        $.ajaxq("MyQueue", {
            type: 'GET',
            url: '/disablebuiltin',
            data: data,
            success: function(data) {
                $('#id_automation').prop('disabled', true);
                $('#id_event_reminders_done').prop("checked", false);
                updateFlags();
            },
            error: function(data) {
                alert('There was an error checking disable built-in');
            }
        });            
                
    } else {
        var data = {
            "mode": "end",
            "event_id": $('#page_instance').val()
        };
        $.ajaxq("MyQueue", {
            type: 'GET',
            url: '/disablebuiltin',
            data: data,
            success: function(data) {
                $('#id_automation').prop('disabled', false);
                $('#id_event_reminders_done').prop("checked", false);
                updateFlags();
            },
            error: function(data) {
                alert('There was an error unchecking disable built-in');
            }
        });            
         
    } 
  
    //updateReminders();   
});








$(document).on('click', '#id_automation', function() {
    //change existing reminders to auto-mode if enabled,
    //or change existing reminders to non-auto-mode if disabled
    if ($('#id_automation').prop("checked") == true) {
        var data = {
            "mode": "start",
            "event_id": $('#page_instance').val()
        };
        $.ajaxq("MyQueue", {
            type: 'GET',
            url: '/switchautomation',
            data: data,
            success: function(data) {
                //nothing;
                alert("\n\nBe aware that any automatic reminders due today (or any info emails for reminders due soon) will be run/sent immediately when you click the Save button!\n\nTo avoid this, disable automation until you're ready or edit the reminder(s)' dates manually.\n\n");
                $('#id_reminderdisable').prop('disabled', true);
                $('#id_event_reminders_done').prop("checked", false);
                updateFlags();
            },
            error: function(data) {
                alert('There was an error enabling automation');
            }
        });            
                
    } else {
        var data = {
            "mode": "end",
            "event_id": $('#page_instance').val()
        };
        $.ajaxq("MyQueue", {
            type: 'GET',
            url: '/switchautomation',
            data: data,
            success: function(data) {
                //nothing
                $('#id_reminderdisable').prop('disabled', false);
                $('#id_event_reminders_done').prop("checked", false);
                updateFlags();
            },
            error: function(data) {
                alert('There was an error disabling automation');
            }
        });            
         
    } 
  
    //updateReminders();   
});


$(".edit_automation").click(evEditAutomated);
function evEditAutomated() {
    var remind_id = this.id.substr(16);
    var url = "/reminder/" + remind_id + "/edit_automation";
    showEditPopup(url);
    //updateReminders();
}

$(".edit_regular").click(evEditRegular);
function evEditRegular() {
    var remind_id = this.id.substr(13);
    var url = "/reminder/" + remind_id + "/edit_regular";
    showEditPopup(url);
    //updateReminders();
}

$(".edit_musician").click(evEditMusician);
function evEditMusician() {
    var musician_id = this.id.substr(14);
    var url = "/musician/" + musician_id + "/edit";
    showEditPopup(url);
    //updateMusiciansAskedList();
    //dummy = setTimeout(updateMusiciansList, 6000);
}





//when a reminder checkbox is clicked, find the db field and change 'done', refresh list on screen
$(".ev-remind-check").on('click', evRemindCheck);


//added procedure if user checks payment received manually, as in check received,
//  to ask if user wants rcpt sent now?
function evRemindCheck() {
    //just does the real work of above, needs to be called from other places, so its separate :) 
    //IF: reminder being checked is an auto reminder, mark associated _sentdate, _rcvddate,
    //          _rcptdate, flag_ fields in database, so that everything stays in sync
    //          (e.g. janie marks task done because she didn't need to finish it, flags will follow)
    var remind_id = this.id.substr(10);
    var data = {
        "remind_id": remind_id
    };

    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/remind/ajax/set_remind_done',
        data: data,
        success: function(data) {
            var today = new Date();
            today.setHours(0, 0, 0, 0);
            text = data['text'];

            if (text == HOLD_UNTIL) {
                //do nothing (activity only needs recording if user
                //also changed 'type' from Hold to Regular/Agency...
                //no pertinent flags to change either until that is done...
                //which, btw, will be done in views.py
            }
            if (text == HOLD_INDEFINITELY) {
                //do nothing
            }
            if (text == SEND_HOLD) {
                //do nothing
            }
            if (text == RECEIVE_CONTRACT) {
                $('#id_flag_contract_rcvd').prop("checked", data['done']);
                $('#id_contract_rcvddate').val(formatDate(today, data['done']));
                if ($('#id_flag_contract_rcvd').prop("checked") == true) {
                    addActivity(remind_id, "Contract was marked received!");
                    if ($('#id_automation').prop("checked") == false) {
                        if (confirm('Would you also like to send a receipt for the contract now?')) {
                            $('#special1').remove();
                            var input = $("<input id='special1'>")
                                            .attr("type", "hidden")
                                            .attr("name", "_receipt_contract_submit").val("bla");
                            $('#form').append(input);
                            $('#submitbtn').trigger('click');
                        }
                    }
                } else {
                    addActivity(remind_id, "Contract was marked NOT received!");
                }
            }
            if (text == SEND_CONTRACT) {
                $('#id_flag_contract_sent').prop("checked", data['done']);
                $('#id_contract_sentdate').val(formatDate(today, data['done']));
                if ($('#id_flag_contract_sent').prop("checked") == true) {
                    addActivity(remind_id, "Contract was marked sent!");
                } else {
                    addActivity(remind_id, "Contract was marked NOT sent!");
                }
            }
            if (text == RECEIPT_CONTRACT) {
                $('#id_flag_contract_rcpt').prop("checked", data['done']);
                $('#id_contract_rcptdate').val(formatDate(today, data['done']));
                if ($('#id_flag_contract_rcpt').prop("checked") == true) {
                    addActivity(remind_id, "Contract received receipt was marked sent!");
                } else {
                    addActivity(remind_id, "Contract received receipt was marked NOT sent!");
                }
            }

            if (text == SEND_DEPOSIT) {
                $('#id_flag_deposit_sent').prop("checked", data['done']);
                $('#id_deposit_sentdate').val(formatDate(today, data['done']));
                if ($('#id_flag_deposit_sent').prop("checked") == true) {
                    addActivity(remind_id, "Deposit request was marked sent!");
                } else {
                    addActivity(remind_id, "Deposit request was marked NOT sent!");
                }
            }
            if (text == RECEIVE_DEPOSIT) {
                $('#id_flag_deposit_rcvd').prop("checked", data['done']);
                $('#id_deposit_rcvddate').val(formatDate(today, data['done']));
                if ($('#id_flag_deposit_rcvd').prop("checked") == true) {
                    $('#deposit_visual').removeClass('noshow');
                    addActivity(remind_id, "Deposit was marked received!");
                    if ($('#id_automation').prop("checked") == false) {
                        if (confirm('Would you also like to send a receipt for the deposit now?')) {
                            $('#special1').remove();
                            var input = $("<input id='special1'>")
                                            .attr("type", "hidden")
                                            .attr("name", "_receipt_deposit_submit").val("bla");
                            $('#form').append(input);
                            $('#submitbtn').trigger('click');
                        }
                    }
                } else {
                    addActivity(remind_id, "Deposit was marked NOT received!");
                    $('#deposit_visual').addClass('noshow');
                }
            }
            if (text == RECEIPT_DEPOSIT) {
                $('#id_flag_deposit_rcpt').prop("checked", data['done']);
                $('#id_deposit_rcptdate').val(formatDate(today, data['done']));
                if ($('#id_flag_deposit_rcpt').prop("checked") == true) {
                    addActivity(remind_id, "Deposit received receipt was marked sent!");
                } else {
                    addActivity(remind_id, "Deposit received receipt was market NOT sent!");
                }
            }

            if (text == SEND_FINAL_PAYMENT) {
                $('#id_flag_final_payment_sent').prop("checked", data['done']);
                $('#id_final_sentdate').val(formatDate(today, data['done']));
                if ($('#id_flag_final_payment_sent').prop("checked") == true) {
                    addActivity(remind_id, "Final payment request was marked sent!");
                } else {
                    addActivity(remind_id, "Final payment request was marked NOT sent!");
                }
            }
            if (text == RECEIVE_FINAL_PAYMENT) {
                $('#id_flag_final_payment_rcvd').prop("checked", data['done']);
                $('#id_final_rcvddate').val(formatDate(today, data['done']));
                if ($('#id_flag_final_payment_rcvd').prop("checked") == true) {
                    addActivity(remind_id, "Final payment was marked received!");
                    $('#final_visual').removeClass('noshow');
                    if ($('#id_automation').prop("checked") == false) {
                        if (confirm('Would you also like to send a receipt for the final payment now?')) {
                            $('#special1').remove();
                            var input = $("<input id='special1'>")
                                            .attr("type", "hidden")
                                            .attr("name", "_receipt_finalpay_submit").val("bla");
                            $('#form').append(input);
                            $('#submitbtn').trigger('click');
                        }
                    }
                } else {
                    addActivity(remind_id, "Final payment was marked NOT received!");
                    $('#final_visual').addClass('noshow');
                }
            }
            if (text == RECEIPT_FINAL_PAYMENT) {
                $('#id_flag_final_payment_rcpt').prop("checked", data['done']);
                $('#id_final_rcptdate').val(formatDate(today, data['done']));
                if ($('#id_flag_final_payment_rcpt').prop("checked") == true) {
                    addActivity(remind_id, "Final payment receipt was marked sent!");
                } else {
                    addActivity(remind_id, "Final payment receipt was marked NOT sent!");
                }
            }



            if (text == SEND_EXTRA_PAYMENT) {
                $('#id_flag_extra_sent').prop("checked", data['done']);
                $('#id_extra_sentdate').val(formatDate(today, data['done']));
                if ($('#id_flag_extra_sent').prop("checked") == true) {
                    addActivity(remind_id, "Extra payment request was marked sent!");
                } else {
                    addActivity(remind_id, "Extra payment request was marked NOT sent!");
                }
            }
            if (text == RECEIVE_EXTRA_PAYMENT) {
                $('#id_flag_extra_rcvd').prop("checked", data['done']);
                $('#id_extra_rcvddate').val(formatDate(today, data['done']));
                if ($('#id_flag_extra_rcvd').prop("checked") == true) {
                    addActivity(remind_id, "Extra payment was marked received!");
                    $('#extra_visual').removeClass('noshow');
                    if ($('#id_automation').prop("checked") == false) {
                        if (confirm('Would you also like to send a receipt for the extra payment now?')) {
                            $('#special1').remove();
                            var input = $("<input id='special1'>")
                                            .attr("type", "hidden")
                                            .attr("name", "_receipt_extrapay_submit").val("bla");
                            $('#form').append(input);
                            $('#submitbtn').trigger('click');
                        }
                    }
                } else {
                    addActivity(remind_id, "Extra payment was marked NOT received!");
                    $('#extra_visual').addClass('noshow');
                }
            }
            if (text == RECEIPT_EXTRA_PAYMENT) {
                $('#id_flag_extra_rcpt').prop("checked", data['done']);
                $('#id_extra_rcptdate').val(formatDate(today, data['done']));
                if ($('#id_flag_extra_rcpt').prop("checked") == true) {
                    addActivity(remind_id, "Extra payment receipt was marked sent!");
                } else {
                    addActivity(remind_id, "Extra payment receipt was marked NOT sent!");
                }
            }





            if (text == INVITE_MUSICIANS) {
                $('#id_flag_musicians_sent').prop("checked", data['done']);
                $('#id_musicians_sentdate').val(formatDate(today, data['done']));
                if ($('#id_flag_musicians_sent').prop("checked") == true) {
                    addActivity(remind_id, "Musicians were marked as asked to play!");
                } else {
                    addActivity(remind_id, "Musicians were marked as NOT asked to play!");
                }
            }
            if (text == ALL_MUSICIANS_BOOKED) {
                $('#id_flag_musicians_rcvd').prop("checked", data['done']);
                $('#id_musicians_rcvddate').val(formatDate(today, data['done']));
                if ($('#id_flag_musicians_rcvd').prop("checked") == true) {
                    addActivity(remind_id, "Musicians marked as finished responding!");
                } else {
                    addActivity(remind_id, "Musicians marked as NOT finished responding!");
                }
            }

            if (text == SEND_FINAL_CONFIRMATION) {
                $('#id_flag_final_confirmation_sent').prop("checked", data['done']);
                $('#id_confirmation_sentdate').val(formatDate(today, data['done']));
                if ($('#id_flag_final_confirmation_sent').prop("checked") == true) {
                    addActivity(remind_id, "Final details confirmation was marked sent!");
                } else {
                    addActivity(remind_id, "Final details confirmation was marked NOT sent!");
                }
            }
            if (text == RECEIVE_FINAL_CONFIRMATION) {
                $('#id_flag_final_confirmation_rcvd').prop("checked", data['done']);
                $('#id_confirmation_rcvddate').val(formatDate(today, data['done']));
                if ($('#id_flag_final_confirmation_rcvd').prop("checked") == true) {
                    addActivity(remind_id, "Final details confirmation was marked received!");
                } else {
                    addActivity(remind_id, "Final details confirmation was marked NOT received!");
                }
            }

            if (text == SEND_MUSIC_LIST) {
                $('#id_flag_music_list_sent').prop("checked", data['done']);
                $('#id_music_list_sentdate').val(formatDate(today, data['done']));
                if ($('#id_flag_music_list_sent').prop("checked") == true) {
                    addActivity(remind_id, "Music list request was marked sent!");
                } else {
                    addActivity(remind_id, "Music list request was marked NOT sent!");
                }
            }
            if (text == RECEIVE_MUSIC_LIST) {
                $('#id_flag_music_list_rcvd').prop("checked", data['done']);
                $('#id_music_list_rcvddate').val(formatDate(today, data['done']));
                if ($('#id_flag_music_list_rcvd').prop("checked") == true) {
                    addActivity(remind_id, "Music list was marked received!");
                } else {
                    addActivity(remind_id, "Music list was marked NOT received!");
                }
            }

            if (text == SEND_FACT_SHEETS) {
                //set rcvddate & rcvd flag
                $('#id_flag_fact_sheets_sent').prop("checked", data['done']);
                $('#id_fact_sheets_sentdate').val(formatDate(today, data['done']));
                if ($('#id_flag_fact_sheets_sent').prop("checked") == true) {
                    addActivity(remind_id, "Fact sheets were marked sent!");
                } else {
                    addActivity(remind_id, "Fact sheets were marked NOT sent!");
                }
            }
            if (text == ALL_FACT_SHEETS_CONFIRMED) {
                //set rcvddate & rcvd flag
                $('#id_flag_fact_sheets_rcvd').prop("checked", data['done']);
                $('#id_fact_sheets_rcvddate').val(formatDate(today, data['done']));
                if ($('#id_flag_fact_sheets_rcvd').prop("checked") == true) {
                    addActivity(remind_id, "Fact sheets were marked as confirmed!");
                } else {
                    addActivity(remind_id, "Fact sheets were marked NOT confirmed!");
                }
            }


            if (text == CHECK_MUSIC_LIST) {
                addActivity(remind_id, "Check Custom Song(s) to-do was clicked (on or off)!");
            }


            $('#id_event_reminders_done').prop("checked", false);
            updateFlags();
            updateActivities();
            recheck_now();
        },
        error: function(data) {
            alert('There was an error 2!');
        }
    });
}

//helper function to output standard date format
function formatDate(date, checked) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    if (checked == true) {
        return [year, month, day].join('-');
    } else {
        return '';
    }
}
//helper function to output short (m/d) date format
function formatDate2(date, checked) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (checked == true) {
        return [month, day].join('/');
    } else {
        return '';
    }
}
//helper function to output (m/d/y) date format
function formatDate3(date, checked) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear().toString().substr(-2);

    if (checked == true) {
        return [month, day, year].join('/');
    } else {
        return '';
    }
}

//TODO:  need function for adding activity from JS
function addActivity(remind_id, activity_text) {
    var data = {
        "event_id": $('#page_instance').val(),
        "activity_text": activity_text
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/activity/ajax/add',
        data: data,
        success: function(data) {
            //do nothing, all good
            //anything else?
            updateActivities();
        },
        error: function(data) {
            alert('There was an error 5!');
        }
    });
}


// refresh the activity list
function updateActivities() {
    var data = {
        "event_id": $('#page_instance').val()
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/remind/ajax/get_activities',
        data: data,
        success: function(data) {
            //if checked, gray it out
            //if unchecked, restore color
            var fullhtml = "<br />";
            var myhtml = "";
            var rdate;
            var friendlydate = "";
            var week = new Date();
            var today = new Date();
            today.setHours(0, 0, 0, 0);
            week.setHours(0, 0, 0, 0);
            week.setDate(week.getDate() + 6);
            var year, month, day;
            $.each(JSON.parse(data), function(index, object) {
                //alert(object.fields.name);
                year = object.fields.date.substr(0, 4);
                month = object.fields.date.substr(5, 2);
                day = object.fields.date.substr(8, 2);
                year = Number(year);
                month = Number(month) - 1;
                day = Number(day);

                rdate = new Date(year, month, day);

                myhtml = '<span class="ev-activity-list"><b>&nbsp;{{ activity.date|date:"n/j" }}:</b> &nbsp;{{ activity.name }}<br /><span style="font-size:1px;">&nbsp;<br /></span></span>';

                month = month + 1;
                friendlydate = month + "\/" + day;
                myhtml = myhtml.replace('{{ activity.date|date:"n/j" }}', friendlydate);
                myhtml = myhtml.replace('{{ activity.name }}', object.fields.name);

                fullhtml = fullhtml + myhtml;

            });
            $('#id_activities_list').html(fullhtml);
            
            updateSidePanels();
        },

        error: function(data) {
            alert('There was an error 4!');
        }
    });
    var data = {
        "event_id": $('#page_instance').val()
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/get_activities_num',
        data: data,
        success: function(data) {
            //do nothing, all good
            //anything else?
            //updateActivities();
            $('#history_bar_num').html(data['num']);
            $('#history_bar_num_side').html(data['numtotal']);
        },
        error: function(data) {
            alert('There was an error 73!');
        }
    });

}




// refresh the reminders list
function updateReminders() {
    var data = {
        "event_id": $('#page_instance').val()
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/remind/ajax/get_reminders',
        data: data,
        success: function(data) {
            //if checked, gray it out
            //if unchecked, restore color
            //alert(data['mlist']);
            $('#id_reminders_list').html(data['mlist']);
//             $('#reminders_bar').html("To-do's");
            $('#todos_bar_num').html(data['num']);
            $('#todos_bar_num_side').html(data['numtotal']);
            $('#booking_bar_num_side').html(data['numbooking']);
            
            //also important, rebind event handlers to new list of reminders!
            $(".ev-remind-check").on('click', evRemindCheck);
            $(".edit_automation").click(evEditAutomated);
            $(".edit_regular").click(evEditRegular);
            $("#show_disabled_reminders").click(function() {
                $('#show_disabled').toggleClass("noshow");
                $('#show_disabled_buffer').toggleClass("noshow");
            });
            //updateSidePanels();
            
        },

        error: function(data) {
            alert('There was an error 3!');
        }
    });

}






function popupclosed() { 
    //popup closed with SEND button, email was actually
    //  sent.  So, mark associated flags (like views'
    //  set_flags routine). Add action only if date already
    //  was recorded -- that means it's a second sending,
    //  so we want a record that is was done again manually. 
    //  And then run all updates here.
    //  this routine will need to SAVE event because of this...
    
    var popupsplit = popuptype.split("/");
    var lastsplit = popupsplit[popupsplit.length - 2];
    //alert(lastsplit); 
    popuptype = "none"; 
    var remind_id = "1";
    
    if ((lastsplit == 'contract') || (lastsplit == 'contract_print')) {
        $("#id_flag_contract_sent").prop("checked", true);
        if ($("#id_contract_sentdate").val()) {
            addActivity(remind_id, "Contract request was sent manually");    
        }
    }
    if (lastsplit == 'contract_only') {
        $("#id_flag_contract_sent").prop("checked", true);
        if ($("#id_contract_sentdate").val()) {
            addActivity(remind_id, "Contract request (no-login) was sent manually");    
        }
    }
    if (lastsplit == 'deposit') {
        $("#id_flag_deposit_sent").prop("checked", true);
        if ($("#id_deposit_sentdate").val()) {
            addActivity(remind_id, "Deposit request was sent manually");    
        }
    }
    if (lastsplit == 'depositcontract') {
        //alert('depositcontract sent!');
        $("#id_flag_deposit_sent").prop("checked", true);
        $("#id_flag_contract_sent").prop("checked", true);
        if ($("#id_contract_sentdate").val()) {
            addActivity(remind_id, "Contract request was sent manually");    
        }
        if ($("#id_deposit_sentdate").val()) {
            addActivity(remind_id, "Deposit request was sent manually");    
        }
    }
    if (lastsplit == 'finalpay') {
        $("#id_flag_final_payment_sent").prop("checked", true);
        if ($("#id_final_sentdate").val()) {
            addActivity(remind_id, "Final payment request was sent manually");    
        }
    }
    if (lastsplit == 'receipt_finalpay') {
        $("#id_flag_final_payment_rcpt").prop("checked", true);
        if ($("#id_final_rcptdate").val()) {
            addActivity(remind_id, "Final payment received receipt was sent manually");    
        }
    }
    if (lastsplit == 'extrapay') {
        $("#id_flag_extra_sent").prop("checked", true);
        if ($("#id_extra_sentdate").val()) {
            addActivity(remind_id, "Extra payment request was sent manually");    
        }
    }
    if (lastsplit == 'receipt_extrapay') {
        $("#id_flag_extra_rcpt").prop("checked", true);
        if ($("#id_extra_rcptdate").val()) {
            addActivity(remind_id, "Extra payment received receipt was sent manually");    
        }
    }
    if (lastsplit == 'receipt_deposit') {
        $("#id_flag_deposit_rcpt").prop("checked", true);
        if ($("#id_deposit_rcptdate").val()) {
            addActivity(remind_id, "Deposit received receipt was sent manually");    
        }
    }
    if (lastsplit == 'receipt_contract') {
        $("#id_flag_contract_rcpt").prop("checked", true);
        if ($("#id_contract_rcptdate").val()) {
            addActivity(remind_id, "Contract received receipt was sent manually");    
        }
    }
    if (lastsplit == 'confirmation') {
        $("#id_flag_final_confirmation_sent").prop("checked", true);
        if ($("#id_confirmation_sentdate").val()) {
            addActivity(remind_id, "Final details confirmation was sent manually");    
        }
    }
    if (lastsplit == 'confirmation_only') {
        $("#id_flag_final_confirmation_sent").prop("checked", true);
        if ($("#id_confirmation_sentdate").val()) {
            addActivity(remind_id, "Final details confirmation (no-login)was sent manually");    
        }
    }
    if (lastsplit == 'musiclist') {
        $("#id_flag_music_list_sent").prop("checked", true);
        if ($("#id_music_list_sentdate").val()) {
            addActivity(remind_id, "Music list request was sent manually");    
        }
    }
    if (lastsplit == 'musiclist_only') {
        $("#id_flag_music_list_sent").prop("checked", true);
        if ($("#id_music_list_sentdate").val()) {
            addActivity(remind_id, "Music list (no-login) request was sent manually");    
        }
    }
    if (lastsplit == 'factsheet') {
        $("#id_flag_fact_sheets_sent").prop("checked", true);
        if ($("#id_fact_sheets_sentdate").val()) {
            addActivity(remind_id, "Fact sheets were sent manually");    
        }
    }
    if (lastsplit == 'hold') {
        $("#id_flag_hold_sent").prop("checked", true);
        if ($("#id_hold_sentdate").val()) {
            addActivity(remind_id, "Hold notice was sent manually");    
        }
    }
    if (lastsplit == 'email') {
        addActivity(remind_id, "General email to contact was sent manually");    
    }
    if (lastsplit == 'musicians_email') {
        addActivity(remind_id, "General email to musicians was sent manually");    
    }
    if (lastsplit == 'email_planner') {
        addActivity(remind_id, "General email to planner was sent manually");    
    }
    if (lastsplit == 'email_planner_contract') {
        addActivity(remind_id, "Contract pdf was sent to planner manually");    
    }
    if (lastsplit == 'email_planner_musiclist') {
        addActivity(remind_id, "Music list was sent to planner manually");    
    }
    if (lastsplit == 'invoice') {
        addActivity(remind_id, "Invoice (full) was sent manually");    
    }
    if (lastsplit == 'invoice_deposit') {
        addActivity(remind_id, "Invoice (deposit) was sent manually");    
    }
    if (lastsplit == 'invoice_final') {
        addActivity(remind_id, "Invoice (final) was sent manually");    
    }
    if (lastsplit == 'invoice_extra') {
        addActivity(remind_id, "Invoice (extra) was sent manually");    
    }
    if (lastsplit == 'musicians') {
        //addActivity(remind_id, "Musician(s) invite was sent manually");    
    }
    if (lastsplit == 'payment_only') {
        addActivity(remind_id, "A payment request (no-login) was sent manually");    
    }

    $('#id_event_reminders_done').prop("checked", false);
            
   
//     xhr = null;
//     dummy =  setTimeout(updateFlags, 2500); //which updates Reminders
//     dummy =  setTimeout(updateActivities, 5500);
//     dummy =  setTimeout(updateValues, 6000);
//     dummy =  setTimeout(updateMusiciansAskedList, 6500);            
//     //dummy = setTimeout(updateMusiciansList, 7000);
//     $('#id_event_reminders_done').prop("checked", false);
//     $('#form').trigger('rescan.areYouSure');
    
//     });
    
}


// function popupclosed2(win) {
//     //alert("popup not closed"); 
//     win.onbeforeunload = null;
//     popuptype = "none";   
// }
// 
// function popuptimed(win) {
//     win.onbeforeunload = popupclosed();
// }

//Show or hide all edit and add popus
function showEditPopup(url) {
    var win = window.open(url, "Edit",
        'height=620,width=420,resizable=yes,scrollbars=yes');
    return false;
}
function showEditPopup2(url) {
    url = url + $('#id_event_type_0').val() + '/create'
    var win = window.open(url, "Edit",
        'height=800,width=1000,resizable=yes,scrollbars=yes');
    return false;
}


function showEditPopupLarge(url) {
    var win = window.open(url, "Edit",
        'height=800,width=1200,resizable=yes,scrollbars=yes');
    //dummy =  setTimeout(function() { popuptimed(win); }, 3500);
    return false;
}

function showAddPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^add_/, '');
    href = triggeringLink.href;
    var win = window.open(href, name, 'height=640,width=420,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}


function closePopup(win, newID, newRepr, id) {
    $(id).append('<option value=' + newID + ' selected >' + newRepr + '</option>');
    //     updateValues();
//     dummy = setTimeout(updateFlags, 200);
//     dummy =  setTimeout(updateActivities, 3000);
//     dummy =  setTimeout(updateValues, 3500);
//     dummy =  setTimeout(updateMusiciansAskedList, 4000);
//     dummy = setTimeout(updateMusiciansList, 5000);
    updateFlags();
    updateActivities();
    updateValues();
    updateMusiciansAskedList();
    updateMusiciansList();
    win.close();
}

function closePopup2(win) {
    //    $(id).append('<option value=' + newID + ' selected >' + newRepr + '</option>');
    //     updateValues();
    updateFlags();
    updateActivities();
    updateValues();
    updateMusiciansAskedList();
    updateMusiciansList();
    win.close();
}

function closePopupExists(win) {
    //    $(id).append('<option value=' + newID + ' selected >' + newRepr + '</option>');
    //     updateValues();
    alert("An entry with this name already exists!");
    updateFlags();
    updateActivities();
    updateValues();
    updateMusiciansAskedList();
    updateMusiciansList();
    win.close();
}

function closePopup2a(win, data) {
    //    $(id).append('<option value=' + newID + ' selected >' + newRepr + '</option>');
    //     updateValues();
    
    //if list already exists, append to the top of it
    var curlist = $(tinymce.get('id_music_list').getBody()).html();
    if ((curlist == '') || (curlist == '<br data-mce-bogus="1">')) {
        $(tinymce.get('id_music_list').getBody()).html(data['html']);
    } else {
        var newlist = data['html'] + '<br /><br /><b>--Below was previously listed:--</b><br />' + curlist;
        $(tinymce.get('id_music_list').getBody()).html(newlist);
    }
    win.close();
    $('#musiclist_button').focus();
    var e =jQuery.Event("keydown");
    e.which = 9;
    e.keyCode = 9;
    $('#id_music_list').trigger(e);
    $('#musiclist_button').trigger(e);
    $('#musiclist_button').focus();
    $('#id_music_list').click();
    $(tinymce.get('id_music_list').getBody()).click();
    tinyMCE.triggerSave();
    $('#form').trigger('checkform.areYouSure');
    
    //do all the other new stuff to follow up
    var today = new Date();
    today.setHours(0, 0, 0, 0);

    $('#id_flag_music_list_rcvd').prop("checked", true);
    $('#id_music_list_rcvddate').val(formatDate(today, true));
    $('#id_flag_music_list_sent').prop("checked", true);
    if (!($('#id_music_list_sentdate').val())) {
        $('#id_music_list_sentdate').val(formatDate(today, true));
    }
    $('#id_recessional_cue').val(data['recess_cue']);
    $('#id_number_parents').val(data['num_parents']);
    $('#id_number_bridesmaids').val(data['num_bridesmaids']);
    if (data['flowergirls'] == true) {
        $('#id_flowergirls').prop("checked", true);    
    } else {
        $('#id_flowergirls').prop("checked", false);        
    }
    M.updateTextFields();
    
    updateFlags();
    updateActivities();
    updateValues();
    updateMusiciansAskedList();
    updateMusiciansList();

}

function closePopup3(win) {
    //same as above, except called after *email* popup
    //so process new info, like musicians invited
    //win.onbeforeunload = popupclosed2(win);
//     dummy = setTimeout(updateFlags, 2500);
//     dummy =  setTimeout(updateActivities, 4500);
//     dummy =  setTimeout(updateValues, 5250);
//     dummy =  setTimeout(updateMusiciansAskedList, 6000);
    win.close();
    var dummy = setTimeout(resaveevent, 600);
}
function resaveevent() {
    //$('#id_event_reminders_done').prop("checked", false);
//     $('#special1').remove();
//     var input = $("<input id='special1'>")
//                     .attr("type", "hidden")
//                     .attr("name", "_submit").val("bla");
//     $('#form').append(input);
    $('#submitbtn').trigger('click');    
}


//function to update values after a contact, dayofcontact or location is edited
function updateValues() {
    venue_name = $("#id_location_0").val();
    var data = {
        "venue_name": venue_name
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/venue/ajax/get_venue_info',
        data: data,
        success: function(data) {
            //             put code here to show this associated data on the screen (with an edit button too)
            if (data['noerror'] == true) {
                $('#location_show_address').html(data['venue_address']);
                $('#location_show_link').html(data['venue_link']);
                $('#location_show_phone').html(data['venue_phone']);
                $('#location_show_email').html(data['venue_email']);
            }
        },
    });
    contact_name = $("#id_contact_0").val();
    data = {
        "contact_name": contact_name
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/contact/ajax/get_contact_info',
        data: data,
        success: function(data) {
            //             put code here to show this associated data on the screen (with an edit button too)
            ///put data in contact_show fields
            if (data['noerror'] == true) {
                $('#contact_show_agency').html(data['contact_agency']);
                $('#contact_show_phone').html(data['contact_phone']);
                $('#contact_show_email').html(data['contact_email']);
            }
        },
    });
    dayofcontact_name = $("#id_dayofcontact_0").val();
    data = {
        "dayofcontact_name": dayofcontact_name
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/dayofcontact/ajax/get_dayofcontact_info',
        data: data,
        success: function(data) {
            //             put code here to show this associated data on the screen (with an edit button too)
            //             alert(data['dayofcontact_name'] + data['dayofcontact_address'] + data['dayofcontact_link']+ data['dayofcontact_phone'] + data['dayofcontact_email']);
            ///put data in dayofcontact_show fields
            if (data['noerror'] == true) {
                $('#dayofcontact_show_phone').html(data['dayofcontact_phone']);
                $('#dayofcontact_show_email').html(data['dayofcontact_email']);
            }
        },
    });
}

//function to limit numbers to 2 decimal places, plus drop '.00'
function roundNum(num) {
    var newnum = num.toFixed(2);
    if (newnum.slice(-2) == "00") {
        newnum = newnum.slice(0,-3)
    }
    return newnum
}


//automatically enter fee info into correct fields when a rate chart number is clicked
function enterRates(chosen, hours, ensnum) {
    var data = {
        "rate_name": chosen,
        "hours": hours,
        "ensnum": ensnum
    };
    var contracting;
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/rates/ajax/get_rates',
        data: data,
        success: function(data) {
            //             alert(data['ens1hm']);
            var num = $("#id_ensemble_number").val();
            //             if (num != "1" && num != "2" && num != "3" && num != "4") {
            //                 alert("The ensemble number is not valid for auto rate to be filled-in!");
            //             }
            if (flag_contract_sent || flag_deposit_sent || flag_final_sent) {
                if (confirm("Contract, deposit request and/or final payment request have already "
                            + "been sent with previous fees!\nClick OK to change them anyways, or Cancel\n")) {
                } else {
                    return;
                }
            }
            if (num != ensnum) {
                if (confirm("This selection does not match the form's Ensemble Number.\n")) {
                    //ensnum = num;
                } else {
                    return;
                }
            }
            if (ensnum == "1") {
                $("#id_fee").val(roundNum(data['ens1']));
                $("#id_musician_fee").val(roundNum(data['ensm']));
                contracting = data['ens1'] - (data['ensm'] * num);
                $("#id_contracting_fee").val(roundNum(contracting));
                if ($("#id_extra_fee").nval()) {
                    var newcontr = $("#id_contracting_fee").nval() + $("#id_extra_fee").nval();
                    $("#id_contracting_fee").val(newcontr);
                }
                $("#id_deposit_fee").val(roundNum($("#id_fee").nval() / 2));
                $("#id_final_fee").val(roundNum($("#id_fee").nval() / 2));
                M.updateTextFields();
            }
            if (ensnum == "2") {
                $("#id_fee").val(roundNum(data['ens2']));
                $("#id_musician_fee").val(roundNum(data['ensm']));
                contracting = data['ens2'] - (data['ensm'] * num);
                $("#id_contracting_fee").val(roundNum(contracting));
                if ($("#id_extra_fee").nval()) {
                    var newcontr = $("#id_contracting_fee").nval() + $("#id_extra_fee").nval();
                    $("#id_contracting_fee").val(newcontr);
                }
                $("#id_deposit_fee").val(roundNum($("#id_fee").nval() / 2));
                $("#id_final_fee").val(roundNum($("#id_fee").nval() / 2));
                M.updateTextFields();
            }
            if (ensnum == "3") {
                $("#id_fee").val(roundNum(data['ens3']));
                $("#id_musician_fee").val(roundNum(data['ensm']));
                contracting = data['ens3'] - (data['ensm'] * num);
                $("#id_contracting_fee").val(roundNum(contracting));
                if ($("#id_extra_fee").nval()) {
                    var newcontr = $("#id_contracting_fee").nval() + $("#id_extra_fee").nval();
                    $("#id_contracting_fee").val(newcontr);
                }
                $("#id_deposit_fee").val(roundNum($("#id_fee").nval() / 2));
                $("#id_final_fee").val(roundNum($("#id_fee").nval() / 2));
                M.updateTextFields();
            }
            if (ensnum == "4") {
                $("#id_fee").val(roundNum(data['ens4']));
                $("#id_musician_fee").val(roundNum(data['ensm']));
                contracting = data['ens4'] - (data['ensm'] * num);
                $("#id_contracting_fee").val(roundNum(contracting));
                if ($("#id_extra_fee").nval()) {
                    var newcontr = $("#id_contracting_fee").nval() + $("#id_extra_fee").nval();
                    $("#id_contracting_fee").val(newcontr);
                }
                $("#id_deposit_fee").val(roundNum($("#id_fee").nval() / 2));
                $("#id_final_fee").val(roundNum($("#id_fee").nval() / 2));
                M.updateTextFields();
            }
            $('#id_used_ratechart').prop("checked", true);
            $('#id_event_reminders_done').prop("checked", false);
            updateFlags();
            updateMusiciansList();
            updateMusiciansAskedList();
            var newmusfee = $('#id_musician_fee').val();
            $('#previous_musician_fee').val(newmusfee);
            $('#id_fee').focus();
        },
        error: function(data) {
            alert("Something Went Wrong, likely that rate chart doesn't exist");
        }
    });
}













//clicked the add musician to list button
$('#addmusician_btn').click(function() {
    thisname = $('#id_musician').val();
    if (isEmptyOrSpaces(thisname)) {
        return;
    }
    var data = {'name': thisname,
                "event": $("#page_instance").val(),
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/addmusiciantoask',
        data: data,
        success: function(data) {
            if (data['error'] == true) {
                alert('Musician has already been asked, or name given is invalid.\nTo add a new musician, click the "New" button.');
            } else {
                updateMusiciansAskedList();
                $('#id_musician').val('');
                $('#id_instrument').val('');
            }
        },
        error: function(data) {
            alert("Something Went Wrong, likely with adding musician to asked list...");
        }
    });        
});

//clicked a musician's invited button
$(document).on('click', '.addmusician_asked', function() {
    var mus = this.id.substr(10);
    if (window.confirm("Are you sure you want to manually change this musician's invited status?")) {
        var data = {
            "mus": mus,
            "event": $("#page_instance").val(),
        };    
        $.ajaxq("MyQueue", {
            type: 'GET',
            url: '/invitedaskedmusician',
            data: data,
            success: function(data) {
                updateMusiciansAskedList();
                //dummy = setTimeout(updateMusiciansList, 500); 
            },
            error: function(data) {
                alert("Something Went Wrong, likely with marking musician as having been 'invited'...");
            }
        });    
    } else {
        var nothing = 1;
    }
});
//ot the no-verify version for Janie's case:
$(document).on('click', '.addmusician_asked_noverify', function() {
var mus = this.id.substr(10);
    var data = {
        "mus": mus,
        "event": $("#page_instance").val(),
    };    
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/invitedaskedmusician',
        data: data,
        success: function(data) {
            updateMusiciansAskedList();
            //dummy = setTimeout(updateMusiciansList, 500); 
        },
        error: function(data) {
            alert("Something Went Wrong, likely with marking musician as having been 'invited'...");
        }
    });    
});




//clicked a musician's yes button
$(document).on('click', '.addmusician_yes', function() {
    var mus = this.id.substr(10);
    //this musician's fee is maybe special
    var musfee = $('#id_addmsf_' + mus).val();
    
    var data = {
        "mus": mus,
        "event": $("#page_instance").val(),
        'eventdate': $("#id_date").val(),
        'musfee': musfee
    };    
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/yesaskedmusician',
        data: data,
        success: function(data) {
            if (data['error'] == true) {
                alert("You can't add any more musicians to this event");
            } else {
                updateMusiciansAskedList();
                updateMusiciansList();
                //MUST also update main fee #s now, since this musician
                //     was maybe added (or subtracted) to playing list
                //use fake ajax so it cues behind all others
                var data = {
                    "dummy": "dummy",
                };
                $.ajaxq("MyQueue", {
                    type: 'GET',
                    url: '/fakeajax',
                    data: data,
                    success: function(data) {
                        $(".updateFeesMus").trigger('change');
                    },
                    error: function(data) {
                        alert("Something Went Wrong, likely triggering updateFeesMus...");
                    }
                });
                //$(".updateFeesMus").trigger('change');
            }
        },
        error: function(data) {
            alert("Something Went Wrong, likely with marking asked musician as 'yes'...");
        }
    });    
});

//clicked a musician's no button
$(document).on('click', '.addmusician_no', function() {
    var mus = this.id.substr(10);
    //this musician's fee is maybe special
    var musfee = $('#id_addmsf_' + mus).val();

    var data = {
        "mus": mus,
        "event": $("#page_instance").val(),
        'eventdate': $("#id_date").val(),
        'musfee': musfee
    };    
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/noaskedmusician',
        data: data,
        success: function(data) {
            if (data['error'] == true) {
                alert("You can't add any more musicians to this event");
            } else {
                updateMusiciansAskedList();
                updateMusiciansList();
                //MUST also update main fee #s now, since this musician
                //     was maybe added (or subtracted) to playing list
                //use fake ajax so it cues behind all others
                var data = {
                    "dummy": "dummy",
                };
                $.ajaxq("MyQueue", {
                    type: 'GET',
                    url: '/fakeajax',
                    data: data,
                    success: function(data) {
                        $(".updateFeesMus").trigger('change');
                    },
                    error: function(data) {
                        alert("Something Went Wrong, likely triggering updateFeesMus...");
                    }
                });
                //$(".updateFeesMus").trigger('change');
            }
        },
        error: function(data) {
            alert("Something Went Wrong, likely with marking asked musician as 'no'...");
        }
    });    
});



//clicked a musician's delete button
$(document).on('click', '.addmusician_delete', function() {
    var mus = this.id.substr(10);
    if (window.confirm("Are you sure you want to delete this musician?")) {
        var data = {
            "mus": mus,
            "event": $("#page_instance").val(),
        };    
        $.ajaxq("MyQueue", {
            type: 'GET',
            url: '/deleteaskedmusician',
            data: data,
            success: function(data) {
                updateMusiciansAskedList();
                updateMusiciansList();
            },
            error: function(data) {
                alert("Something Went Wrong, likely with deleting asked musician...");
            }
        });    
    } else {
        var nothing = 1;
    }
    
});


//clicked a musician's gotit button
$(document).on('click', '.addmusician_gotit', function() {
    var mus = this.id.substr(10);
    var data = {
        "mus": mus,
        "event": $("#page_instance").val(),
        "ensnumber": $("#id_ensemble_number").val(),
    };    
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/gotitaskedmusician',
        data: data,
        success: function(data) {
            if (data['error'] == true) {
                alert("Error with marking gotit");
            } else {
                var dummy;
                if (data['fact_sheets_rcvd'] == true) {
                    $('#id_flag_fact_sheets_rcvd').prop("checked", true);
                    $('#id_event_reminders_done').prop("checked", false);
                    updateFlags();
                }
                updateMusiciansAskedList();
                updateMusiciansList();
            }
        },
        error: function(data) {
            alert("Something Went Wrong, likely with marking asked musician as 'gotit'...");
        }
    });    
});




//general function to update the musicians asked panel
function updateMusiciansAskedList() {
    var data = {
        "event": $("#page_instance").val(),
        "ensnumber": $("#id_ensemble_number").val(),
    };
    var today = new Date();
    today.setHours(0, 0, 0, 0);
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/updatelistofaskedmusicians',
        data: data,
        success: function(data) {
            $("#musiciansaskedlist").html(data['mlist']);
            if (data['invite_possible'] == true) {
                $('#btn_musicians').removeClass('noshow');
                $('#xbtn_musicians').prop('disabled', false);    
            } else {
                $('#btn_musicians').addClass('noshow');
                $('#xbtn_musicians').prop('disabled', true);                    
            }
            //alert(data['mark_musicians_sent']);
            if (data['mark_musicians_sent'] == true) {
                if ($('#id_flag_musicians_sent').prop("checked")) {
                    //do nothing
                } else {
                    $('#id_flag_musicians_sent').prop("checked", true);
                    //if no date yet entered, the process_auto_reminders routine
                    //will do it, plus it will enter action "mus finished..."
                    $('#id_event_reminders_done').prop("checked", false);    
                    updateFlags();
                    $('#secret_change').val("X");
                    recheck_now();
                }
            } else {
                if (!$('#id_flag_musicians_sent').prop("checked")) {
                    //do nothing
                } else {
                    $('#id_flag_musicians_sent').prop("checked", false);
    //                dont enter the date yet, erase it if already entered
                    $('#id_musicians_sentdate').val('');
                    $('#id_event_reminders_done').prop("checked", false);    
                    updateFlags();
                    $('#secret_change').val("X");
                    recheck_now();
                }
            }
            if (data['mark_musicians_rcvd'] == true) {
                if ($('#id_flag_musicians_rcvd').prop("checked")) {
                    //do nothing
                } else {
                    $('#id_flag_musicians_rcvd').prop("checked", true);
                    //if no date yet entered, the process_auto_reminders routine
                    //will do it, plus it will enter action "mus finished..."
                    $('#id_event_reminders_done').prop("checked", false);    
                    updateFlags();
                    $('#secret_change').val("X");
                    recheck_now();
                }
            } else {
                if (!$('#id_flag_musicians_rcvd').prop("checked")) {
                    //do nothing
                } else {
                    $('#id_flag_musicians_rcvd').prop("checked", false);
    //                dont enter the date yet, erase it if already entered
                    $('#id_musicians_rcvddate').val('');
                    $('#id_event_reminders_done').prop("checked", false);    
                    updateFlags();
                    $('#secret_change').val("X");
                    recheck_now();
                }
            }
            //rebind event handlers
            $(".edit_musician").click(evEditMusician);
            //dummy = setTimeout(updateFlags, 500);
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with updating asked musicianslist...");
        }
    });    
}





//on-change when assigned musician's inst dropdown is changed
$(document).on('change', '.musinputinstcol', function() {
    var rank = this.id.substr(10);
    var data = {
        "rank": rank,
        "event": $("#page_instance").val(),
    };    
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/changeinstofmusician',
        data: data,
        success: function(data) {
            var nothing = 1;
        },
        error: function(data) {
            alert("Something Went Wrong, likely with changing assigned musician's instrument...");
        }
    });    
});


//update and reorder musicians list when number is changed
$(document).on('change', '.musinput', function() {
    var this_id = this.id.substr(10);
    var data = {
        "oldrank": this_id,
        "newrank": this.value,
        "event": $("#page_instance").val(),
        "number": $("#id_ensemble_number").val(),
    };    
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/reordermusicians',
        data: data,
        success: function(data) {
            //alert(data['error']);
            if (data['error'] == true) {
                alert('The rank you entered is not allowed!');
            } else {
                updateMusiciansList();
            }
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with reordering musicianslist...");
        }
    });    
});


//update musicians list with blanks when ensemble number changed
//consider problem when current musicianslist has more musicians?
$("#id_ensemble_number").on('change', function(event, ui) {
    var data = {
        "number": $("#id_ensemble_number").val(),
        "event": $("#page_instance").val(),
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/updatemusicians',
        data: data,
        success: function(data) {
            if (data['warn'] == true) {
                alert("Extra musicians were removed!");
            }
            updateMusiciansList();
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with udpating musicians...");
        }
    });
    
    //dummy =  setTimeout(updateMusiciansAskedList, 500);    
});

function updateMusiciansList() {
    var data = {
        "number": $("#id_ensemble_number").val(),
        "event": $("#page_instance").val(),
        "currentfee": $("#id_musician_fee").val(),
        "previousfee": $("#previous_musician_fee").val(),
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/updatelistofmusicians',
        data: data,
        success: function(data) {
            $("#musicianslist").html(data['mlist']);
            //dummy = setTimeout(updateFlags, 500);
            //rebind draggable-sortable and rebind to sortstop event
            $("#musname-sortable").sortable();
            $("#musname-sortable").on("sortstop", afterDrag); 
            //rebind cursor-changing code
            $(".cursor-drag").on("mousedown", function () {
                $(this).addClass("mouseDown");  
            }).on("mouseup", function () {
                $(this).removeClass("mouseDown");
            });            
            
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with udpating musicianslist...");
        }
    });    
}

//update stuff when musicians individual fee number is changed in
//      the main musicians' panel ('yes' musicians playing)
$(document).on('change', '.musinputfee', function() {
    var this_id = this.id.substr(10);
    var data = {
        "rank": this_id,
        "newfee": this.value,
        "event": $("#page_instance").val(),
    };    
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/specialfeechangemusicians',
        data: data,
        success: function(data) {
            //alert(data['error']);
            if (data['error'] == true) {
                alert('The fee you entered is not allowed!');
            } else {
                updateMusiciansList();
                updateMusiciansAskedList();
                //MUST also update main fee #s now, since this musician
                //     is definitely playing already!
                //use fake ajax so it cues behind all others
                var data = {
                    "dummy": "dummy",
                };
                $.ajaxq("MyQueue", {
                    type: 'GET',
                    url: '/fakeajax',
                    data: data,
                    success: function(data) {
                        $(".updateFeesMus").trigger('change');
                    },
                    error: function(data) {
                        alert("Something Went Wrong, likely triggering updateFeesMus...");
                    }
                });
                //$(".updateFeesMus").trigger('change');
            }
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with specialfeechange musicians...");
        }
    });    
});
//update stuff when musicians individual fee number is changed in
//      the asked musicians' panel (not yet playing, maybe)
$(document).on('change', '.addmusician_specialfee', function() {
    var this_id = this.id.substr(10);
    var data = {
        "rank": this_id,
        "newfee": this.value,
        "event": $("#page_instance").val(),
    };    
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/specialfeechangeaskedmusicians',
        data: data,
        success: function(data) {
            //alert(data['error']);
            if (data['error'] == true) {
                alert('The fee you entered is not allowed!');
            } else {
                updateMusiciansList();
                updateMusiciansAskedList();
                //MUST also update main fee #s now, since this musician
                //     *might* be playing already!
                //use fake ajax so it cues behind all others
                var data = {
                    "dummy": "dummy",
                };
                $.ajaxq("MyQueue", {
                    type: 'GET',
                    url: '/fakeajax',
                    data: data,
                    success: function(data) {
                        $(".updateFeesMus").trigger('change');
                    },
                    error: function(data) {
                        alert("Something Went Wrong, likely triggering updateFeesMus...");
                    }
                });
            }
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with specialfeechange askedmusicians...");
        }
    });    
});


function calctotalspecialfees() {
    var total = 0;
    var thisfee = 0;
    var thisid = '';
    var normaltotal = ($("#id_musician_fee").nval() * $("#id_ensemble_number").nval());
    for (let step = 1; step <= $('#id_ensemble_number').nval(); step++) {
        thisid = 'id_rerann_' + String(step);
//         alert(thisid);
//         alert($('#' + thisid).val());
        if ($('#' + thisid).val() == '---' || $('#' + thisid).nval() == 0 || !$('#' + thisid).val() ) {
            total = total + $('#id_musician_fee').nval(); 
//             alert('hi');
            //alert(total);   
        } else {
            if ($('#' + thisid).nval() == $('#previous_musician_fee').nval()) { //not special
                total = total + $('#id_musician_fee').nval();   
            } else {
                total = total + $('#' + thisid).nval();
            }
            //alert($('#' + thisid).nval());
            //alert(total);
        }
    }
//     alert(Number(total));
    return Number(total);    
}
function calctotalspecialfeesonly() {
    var total = 0;
    var thisfee = 0;
    var thisid = '';
    var normaltotal = ($("#id_musician_fee").nval() * $("#id_ensemble_number").nval());
    for (let step = 1; step <= $('#id_ensemble_number').nval(); step++) {
        thisid = 'id_rerann_' + String(step);
        if ($('#' + thisid).val() == '---' || $('#' + thisid).nval() == 0 || !$('#' + thisid).val() ) {
            total = total + 0;    
        } else {
            if ($('#' + thisid).nval() != $('#previous_musician_fee').nval()) { //special
                total = total + $('#' + thisid).nval();
            } else {
                total = total + 0;
            }
        }
    }
    return Number(total);    
}
function calcensnumregularfee() {
    var total = 0;
    var thisfee = 0;
    var thisid = '';
    var normaltotal = ($("#id_musician_fee").nval() * $("#id_ensemble_number").nval());
    for (let step = 1; step <= $('#id_ensemble_number').nval(); step++) {
        thisid = 'id_rerann_' + String(step);
        if ($('#' + thisid).val() == '---' || $('#' + thisid).nval() == 0 || !$('#' + thisid).val() ) {
            total = total + 1;    
        } else {
            if ($('#' + thisid).nval() == $('#previous_musician_fee').nval()) {
                total = total + 1;
            } else {
                total = total + 0;
            }
        }
    }
    return Number(total);    
}
//update the fees when fee is changed
//fees now default to 0, so some checks are no longer needed
$(".updateFeesMain").on('change', function(event, ui) {
    if (flag_contract_sent || flag_deposit_sent || flag_final_sent) {
        if (confirm("Contract, deposit request and/or final payment request have already "
                    + "been sent with previous fees!\nClick OK to change them anyways, or Cancel\n")) {
        } else {
            return;
        }
    }
    if ($("#id_fee").nval() && $("#id_musician_fee").nval() && $("#id_ensemble_number").nval()) {
        var totalmusfees = calctotalspecialfees();
        var contracting = $("#id_fee").nval() + $("#id_extra_fee").nval() - totalmusfees;
        $("#id_contracting_fee").val(roundNum(contracting));
//         if ($("#id_extra_fee").nval()) {
//             var newcontr = $("#id_contracting_fee").nval() + $("#id_extra_fee").nval();
//             $("#id_contracting_fee").val(newcontr);
//         }
        $("#id_deposit_fee").val(roundNum($("#id_fee").nval() / 2));
        $("#id_final_fee").val(roundNum($("#id_fee").nval() / 2));
        M.updateTextFields();
        $('#id_event_reminders_done').prop("checked", false);
        updateFlags();
    } else if ($("#id_fee").nval()) {
        $("#id_deposit_fee").val(roundNum($("#id_fee").nval() / 2));
        $("#id_final_fee").val(roundNum($("#id_fee").nval() / 2));
        M.updateTextFields();
        $('#id_event_reminders_done').prop("checked", false);
        updateFlags();
    } 
});

//update the fees when ensemble_number is changed
$(".updateFees").on('change', function(event, ui) {
    if ($("#id_fee").nval() && $("#id_musician_fee").nval() && $("#id_ensemble_number").nval()) {
//         if ($("#id_extra_fee").nval()) {
//             var contracting = $("#id_fee").nval() + $("#id_extra_fee").nval() - ($("#id_musician_fee").nval() * $("#id_ensemble_number").nval());
//         } else {
//             var contracting = $("#id_fee").nval() - ($("#id_musician_fee").nval() * $("#id_ensemble_number").nval());
//         }
        var totalmusfees = calctotalspecialfees();
        var contracting = $("#id_fee").nval() + $("#id_extra_fee").nval() - totalmusfees;
        $("#id_contracting_fee").val(roundNum(contracting));
        M.updateTextFields();
        $('#id_event_reminders_done').prop("checked", false);
        updateFlags();
    }
});
//update flags when extra_fee is changed, so dates, reminders etc get updated
$(".updateFeesExtra").on('change', function(event, ui) {
    if (flag_extra_sent) {
        if (confirm("Extra fee request has already "
                    + "been sent with previous fee!\nClick OK to change them anyways, or Cancel\n")) {
        } else {
            return;
        }
    }
    if ($("#id_extra_fee").nval() || $("#id_extra_fee").nval() == 0) {
        var contracting = $("#id_contracting_fee").nval() - Number(oldextrafee) + $("#id_extra_fee").nval();
        $('#id_contracting_fee').val(roundNum(contracting));
    }
    M.updateTextFields();
    $('#id_event_reminders_done').prop("checked", false);
    oldextrafee = $("#id_extra_fee").nval();
    updateFlags();
});
//update the fees when  musician_fee is changed
$(".updateFeesMus").on('change', function(event, ui) {
    if (flag_musicians_sent) {
//         if (confirm("Musicians have already "
//                     + "been asked to play with previous fees!\nClick OK to change them anyways, or Cancel\n")) {
//         } else {
//             return;
//         }
    }
//     var tempfee = Number($("#id_ensemble_number").nval());
//     $("#id_ensemble_number").val(tempfee);
    if ($("#id_fee").nval() && $("#id_musician_fee").nval() && $("#id_ensemble_number").nval()) {
//         if ($("#id_extra_fee").nval()) {
//             var contracting = $("#id_fee").nval() + $("#id_extra_fee").nval() - ($("#id_musician_fee").nval() * $("#id_ensemble_number").nval());
//         } else {
//             var contracting = $("#id_fee").nval() - ($("#id_musician_fee").nval() * $("#id_ensemble_number").nval());
//         }
        var totalmusfees = calctotalspecialfees();
        var contracting = $("#id_fee").nval() + $("#id_extra_fee").nval() - totalmusfees;
        $("#id_contracting_fee").val(roundNum(contracting));
        M.updateTextFields();
        $('#id_event_reminders_done').prop("checked", false);
        updateFlags();
        updateMusiciansList();
        updateMusiciansAskedList();
        var newmusfee = $('#id_musician_fee').val();
        $('#previous_musician_fee').val(newmusfee);
    }
});











//update musician_fee if contracting fee is changed manually
$(".updateFeesContracting").on('change', function(event, ui) {
    if (flag_musicians_sent) {
        if (confirm("Musicians have already "
                    + "been asked to play with previous fees!\nClick OK to change them anyways, or Cancel\n")) {
        } else {
            return;
        }
    }
    if ($("#id_fee").nval() && $("#id_musician_fee").nval() && $("#id_ensemble_number").nval()) {
//         if ($("#id_extra_fee").nval()) {
//             var musicians = ($("#id_fee").nval() + $("#id_extra_fee").nval() - $("#id_contracting_fee").nval()) / $("#id_ensemble_number").nval();
//         } else {
//             var musicians = ($("#id_fee").nval() - $("#id_contracting_fee").nval()) / $("#id_ensemble_number").nval();
//         }
        var ensnumregularfee = calcensnumregularfee();
        var totalspecialfeesonly = calctotalspecialfeesonly();
        var leftoverfees = $("#id_fee").nval() + $("#id_extra_fee").nval() - $("#id_contracting_fee").nval() - totalspecialfeesonly
        var musicians = leftoverfees / ensnumregularfee;
        $("#id_musician_fee").val(roundNum(musicians));
        M.updateTextFields();
        updateFlags();
        updateMusiciansList();
        updateMusiciansAskedList();
        var newmusfee = $('#id_musician_fee').val();
        $('#previous_musician_fee').val(newmusfee);
    }
});
//update deposit/final fees upon manual change
$(".updateFeesDeposit").on('change', function(event, ui) {
    if (flag_deposit_sent || flag_final_sent) {
        if (confirm("Deposit request and/or final payment request have already "
                    + "been sent with previous fees!\nClick OK to change them anyways, or Cancel\n")) {
        } else {
            return;
        }
    }
    if ($("#id_deposit_fee").nval() && $("#id_fee").nval()) {
        var final = ($("#id_fee").nval() - $("#id_deposit_fee").nval());
        $("#id_final_fee").val(roundNum(final));
        M.updateTextFields();
        $('#id_event_reminders_done').prop("checked", false);
        updateFlags();
    }
});
$(".updateFeesFinal").on('change', function(event, ui) {
    if (flag_deposit_sent || flag_final_sent) {
        if (confirm("Deposit request and/or final payment request have already "
                    + "been sent with previous fees!\nClick OK to change them anyways, or Cancel\n")) {
        } else {
            return;
        }
    }
    if ($("#id_final_fee").nval() && $("#id_fee").nval()) {
        var deposit = ($("#id_fee").nval() - $("#id_final_fee").nval());
        $("#id_deposit_fee").val(roundNum(deposit));
        M.updateTextFields();
        $('#id_event_reminders_done').prop("checked", false);
        updateFlags();
    }
});

//------------------------code for jquery-ui dialog boxes
//--------------problem with this is execution doesn't wait
//--------------for user to answer -- would have to rewrite flow
// $( function() {
//   $( "#dialog-confirm" ).dialog({
//     resizable: false,
//     height: "auto",
//     width: 400,
//     modal: true,
//     buttons: {
//       "Delete all items": function() {
//         $( this ).dialog( "close" );
//       },
//       Cancel: function() {
//         $( this ).dialog( "close" );
//       }
//     }
//   });
// } );
  


//function for when a form is clicked in the "more" modal popup:
function moreButtonSubmit(type) {
    $('#special1').remove();
    var input = $("<input id='special1'>")
                    .attr("type", "hidden")
                    .attr("name", type).val("bla");
    $('#form').append(input);
    $('#submitbtn').trigger('click');
}

  
//before submit, enter the event, ensemble, contact, dayofcontact, & location names into the hidden fields
//  so that they can be accessed in the views code
//also, ask if you want to send a contract/deposit request if it's a new event
//also, pop up the "saving event" modal
//also, check if automation or sending any manual emails, are fees/contact email/friendly entered?
//also, check if end time is later than start time?

$("#submitbtn, .ev-submitbtn3, .ev-submitbtn4").click(function(e) {

    //check always, except if:
    // automation is off AND one of these is true:
    //      'this' is _archive_submit or _hold_submit
    //      'this' is '_submit' and 'special1' doesn't exist
    //      'special1' is _hold_submit
    var check = true;
    if (!($('#id_automation').prop("checked"))) {
        if (($(this).attr("name") == '_archive_submit') || ($(this).attr("name") == '_hold_submit')) {
            check = false;
        }
        if (($(this).attr("name") == '_submit') && (!($('#special1').attr("name")))) {
            check = false;
        }
        if ($('#special1').attr("name") == '_hold_submit') {
            check = false;
        }
        if ($(this).attr("name") == '_musicians_submit') {
            check = false;
        }
    }

    if (check) {
        //alert($(this).attr("name"));
        //alert($('#special1').attr("name"));
        //alert('checking required fields...');
        var passed = true;
        var type = '';
        if (isEmptyOrZero($('#id_fee').val()) && (isEmptyOrZero($('#id_deposit_fee').val()) || isEmptyOrZero($('#id_final_fee').val()))) {
            //if fee are not entered, generally a problem except if HOLD type of event!
            var el = document.getElementById("id_type");
            var selected = el.options[el.selectedIndex].text;
            if (selected == "Hold") {
                passed = true;
                type = 'fees';
            } else {
                passed = false;
                type = 'fees';
            }
        }
        if (!($('#id_friendly_name').val())) {
            if (!(passed)) {
                type = type + " & contact's friendly name";
            } else {
                passed = false;
                type = "contact's friendly name";                
            }
        } 
        if (!($('#id_contact_email').val()) && isEmptyOrNbsp($('#contact_show_email').html())) {
            if (!(passed)) {
                type = type + " & contact's email";
            } else {
                passed = false;
                type = "contact's email";                
            }
        }
        if (!($('#id_dayofcontact_email').val()) && isEmptyOrNbsp($('#dayofcontact_show_email').html())) {
            if ($('#id_dayofcontact_0').val()) {
                if (!(passed)) {
                    type = type + " & planner's email";
                } else {
                    passed = false;
                    type = "planner's email";                
                }
            }
        }
        if (!(passed)) {
            var msg = "Before sending a form email or proceeding with automation, \n";
            msg = msg + "you must complete the " + type + " section(s)!";
            alert(msg);
            e.preventDefault(); //this will prevent the default submit
            $('#special1').remove();
            return;
        }
    }
    
    if ($('#id_start_time').val() && $('#id_end_time').val()) {
        //alert($('#id_start_time').val());
        //alert($('#id_end_time').val());
        var a = "11/11/2020 " + $('#id_start_time').val();
        var b = "11/11/2020 " + $('#id_end_time').val();
        var stime = new Date(a).getTime();
        var etime = new Date(b).getTime();
        //alert(stime);
        if (etime < stime) {
            alert('The event end time must be after the event start time!');
            e.preventDefault(); //this will prevent the default submit
            $('#special1').remove();
            return;
        }
    }
    
    
    //ask if new event, not automated, not hold, would you like to send
    //contract and/or payment request (if not waive contract or waive payment)
    if (($('#page_instance').val() == '2') && (!$('#id_automation').prop("checked")) && (!$('#id_flag_hold').prop("checked"))) {
        if ($('#id_start_time').val() && $('#id_end_time').val() && ($('#id_contact_email').val() || !(isEmptyOrNbsp($('#contact_show_email').html())))) {
            if ($('#id_waive_contract').prop("checked") && ($('#id_waive_payment').prop('checked'))) {
                //both contract and payment waived, so don't bother asking anything
            } else if ($('#id_waive_contract').prop("checked")) {
                if (confirm('Would you also like to send a payment request now?')) {
                    //contract waived, so send deposit request only
                    $('#special1').remove();
                    var input = $("<input id='special1'>")
                                    .attr("type", "hidden")
                                    .attr("name", "_deposit_submit").val("bla");
                    $('#form').append(input);
                }
            } else if ($('#id_waive_payment').prop("checked")) {
                if (confirm('Would you also like to send a contract request now?')) {
                    //payment waived, so send contract request only
                    $('#special1').remove();
                    var input = $("<input id='special1'>")
                                    .attr("type", "hidden")
                                    .attr("name", "_contract_submit").val("bla");
                    $('#form').append(input);
                }
            } else {
                if (confirm('Would you also like to send a contract and payment request now?')) {
                    //neither waived, so send contract plus deposit request
                    $('#special1').remove();
                    var input = $("<input id='special1'>")
                                    .attr("type", "hidden")
                                    .attr("name", "_depositcontract_submit").val("bla");
                    $('#form').append(input);
                }
            }
        } 
    }

    var instance = M.Modal.getInstance($("#id_please_wait"));
    instance.open();

    $("#id_please_wait").removeClass('noshow');
//     $("#id_please_wait_2").removeClass('noshow');
    $("#id_event_type_name").val($("#id_event_type_0").val());
    $("#id_ensemble_name").val($("#id_ensemble_0").val());
    $("#id_contact_name").val($("#id_contact_0").val());
    $("#id_dayofcontact_name").val($("#id_dayofcontact_0").val());
    $("#id_location_name").val($("#id_location_0").val());
    //erase dummy musician and instrument fields so nothing is saved
    //$('#id_musician').val('');
    //$('#id_instrument').val('');
});






//generate the edit venue popup
$("#edit_venue").click(function() {
    venue_name = $("#id_location_0").val();
    var data = {
        "venue_name": venue_name
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/venue/ajax/get_venue_id',
        data: data,
        success: function(data) {
            var url = "/venue/" + data['venue_id'] + "/edit/";
            showEditPopup(url);
        },
        error: function(data) {
            alert("Something Went Wrong, likely that venue doesn't exist in database already");
        }
    });
});

//on select or focusout, see if location is in database or new, and hide/show appropriate fields
$("#id_location_0").on('djselectablechange djselectableselect focusout', function(event, ui) {
    venue_name = $("#id_location_0").val();
    var data = {
        "venue_name": venue_name
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/venue/ajax/get_venue_info',
        data: data,
        success: function(data) {
            //             put code here to show this associated data on the screen (with an edit button too)
            if (data['noerror'] == true) {
                $('#location_show_address').html(data['venue_address']);
                $('#location_show_link').html(data['venue_link']);
                $('#location_show_phone').html(data['venue_phone']);
                $('#location_show_email').html(data['venue_email']);
//                 if ($('#location_button').prop("checked") == true) {
                if (!($('#toggle_location_show').hasClass('ev-closed')) || !($('#toggle_location_add').hasClass('ev-closed'))) {
                    $('#toggle_location_show').removeClass("ev-closed");
                    $('#toggle_location_add').addClass("ev-closed");    
                }
//                 $('#toggle_location_show').addClass("ev-closed");
//                 $('#toggle_location_add').addClass("ev-closed");
//                 $('#location_button').prop("checked", false);
                toggle3 = "show";
                
                
            } else {
                //put code here to show "save for future" checkbox and edit boxes for adding associated data
                if (!isEmptyOrSpaces(venue_name)) {
//                     $('#location_button').prop("checked", true);
                    if (!($('#toggle_location_show').hasClass('ev-closed')) || !($('#toggle_location_add').hasClass('ev-closed'))) {
                        $('#toggle_location_show').addClass("ev-closed");
                        $('#toggle_location_add').removeClass("ev-closed");
                    }
                    toggle3 = "add";
                } else {
                    //don't show if entry was blank
                    $('#location_button').prop("checked", false);
                    $('#toggle_location_show').addClass("ev-closed");
                    $('#toggle_location_add').addClass("ev-closed");
                    toggle3 = "";
                }
            }

              $('#hide4').text($('#id_location_0').val());
              if (placeholderActive('#id_location_0')) {
                $('#hide4').text($('#id_location_0').attr('placeholder'));   
              }
              var wide = Number($('#hide4').width());
              wide = wide + 4;
              $('#id_location_0').width(wide);
//               $('#id_location_0').width($('#hide4').width());
//               var wide = Number($('#hide4').width());
//               if (wide > 280) {wide = 280;}
//               wide = wide + 7;
//               $('.evx-btntry3 .ui-combo-button').css("left", wide);


        },
        error: function(data) {
            alert('there was an error getting venue info');
        }
    });
    //$('#form').trigger('rescan.areYouSure');
});

//on select or focusout, see if event_type is in database or new, and do nothing (!)
//$("#id_event_type_0").on('djselectableselect focusout', function(event, ui) {
$("#id_event_type_0").on('djselectablechange djselectableselect', function(event, ui) {
    event_type_name = $("#id_event_type_0").val();
    var data = {
        "event_type_name": event_type_name
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/event_type/ajax/get_event_type_id',
        data: data,
        success: function(data) {
            //             the user select pre-existing event_type, do whatever is necessary?
            if (!data['found']) {
                //alert("not found");
            } else {
//                 if ((event_type_name == 'Background') || (event_type_name == 'Cocktail Hour') || (event_type_name == 'Reception') || (event_type_name == 'Cocktail Hour & Dinner') || (event_type_name == 'Reception & Dinner')) {
//                     $('#id_waive_music_list').prop('checked', true);
//                     $('.waive_music_list_panel').addClass('noshow');
//                     $('#id_event_reminders_done').prop("checked", false);
//                     updateFlags();   
//                 }
            }
            
              $('#hide2').text($('#id_event_type_0').val());
              if (placeholderActive('#id_event_type_0')) {
                $('#hide2').text($('#id_event_type_0').attr('placeholder'));   
              }
              var wide = Number($('#hide2').width());
              wide = wide + 4;
              $('#id_event_type_0').width(wide);
//               $('#id_event_type_0').width($('#hide2').width());
//               var wide = Number($('#hide2').width());
//               if (wide > 300) {wide = 300;}
//               wide = wide + 10;
//               $('.evx-btntry .ui-combo-button').css("left", wide);

            if ($('#id_event_type_0').val().includes('eremony')) {
                $('#cerdiv').attr('style','margin-top:5px;');
            } else {
                $('#cerdiv').attr('style', 'display:none !important;margin-top:5px;');
            }

        },
        error: function(data) {
            alert("there was an error updating event_type_name field");
        }
    });
    //$('#form').trigger('rescan.areYouSure');
});


//on select or focusout, see if ensemble is in database or new, and auto-fill ensemble number
//$("#id_ensemble_0").on('djselectableselect focusout', function(event, ui) {
$("#id_ensemble_0").on('djselectablechange djselectableselect', function(event, ui) {
    ensemble_name = $("#id_ensemble_0").val();
    var data = {
        "ensemble_name": ensemble_name
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/ensemble/ajax/get_ensemble_id',
        data: data,
        success: function(data) {
            if (!data['found']) {
                //alert("not found");
            } else {
                //             the user select pre-existing ensemble, do whatever is necessary?
                $('#id_ensemble_number').val(data['ensemble_number']).trigger('change');
                M.updateTextFields();
            }
            
              $('#hide3').text($('#id_ensemble_0').val());
              if (placeholderActive('#id_ensemble_0')) {
                $('#hide3').text($('#id_ensemble_0').attr('placeholder'));   
              }
              var wide = Number($('#hide3').width());
              wide = wide + 4;
              $('#id_ensemble_0').width(wide);
//               $('#id_ensemble_0').width($('#hide3').width());
//               var wide = Number($('#hide3').width());
//               if (wide > 220) {wide = 220;}
//               wide = wide + 10;
//               $('.evx-btntry2 .ui-combo-button').css("left", wide);
                    
        },
        error: function(data) {
            //             the user types non-existing ensemble, do whatever is necessary?
            //              alert("that ensemble doesn't exist in database already");
            alert("there was an error updating ensemble_name field");
        }
    });
    //$('#form').trigger('rescan.areYouSure');
});


//generate the edit contact popup
$("#edit_contact").click(function() {
    contact_name = $("#id_contact_0").val();
    var data = {
        "contact_name": contact_name
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/contact/ajax/get_contact_id',
        data: data,
        success: function(data) {
            var url = "/contact/" + data['contact_id'] + "/edit/";
            showEditPopup(url);
        },
        error: function(data) {
            alert("Something Went Wrong, likely that contact doesn't exist in database already");
        }
    });
});


//on select or focusout, see if contact is in database or new, and hide/show appropriate fields
$("#id_contact_0").on('djselectablechange djselectableselect focusout', function(event, ui) {
    contact_name = $("#id_contact_0").val();
    var data = {
        "contact_name": contact_name
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/contact/ajax/get_contact_info',
        data: data,
        success: function(data) {
            //             put code here to show this associated data on the screen (with an edit button too)
            ///put data in contact_show fields
            if (data['noerror'] == true) {  //yes, contact is in DB, so fill fields etc... but also clear out unused fields
                $('#contact_show_agency').html(data['contact_agency']);
                $('#contact_show_phone').html(data['contact_phone']);
                $('#contact_show_email').html(data['contact_email']);
                $('#id_friendly_name').val(data['contact_friendlyname'])
                $('#id_contact_agency').val('');
                $('#id_contact_phone').val('');
                $('#id_contact_email').val('');
                if (!($('#toggle_contact_show').hasClass('ev-closed')) || !($('#toggle_contact_add').hasClass('ev-closed'))) {
                    $('#toggle_contact_show').removeClass("ev-closed");
                    $('#toggle_contact_add').addClass("ev-closed"); 
                    $('#contact_email_show').removeClass('noshow');
                    $('#contact_email_add').addClass('noshow');   
                }
                $('#contact_email_show').removeClass('noshow');
                $('#contact_email_add').addClass('noshow'); 
                //$('#contact_email_shaded').addclass('ev-shadedpanel2');  
                //$('#toggle_contact_show').addClass("ev-closed");
                //$('#toggle_contact_add').addClass("ev-closed");
                //$('#contact_button').prop("checked", false);
                toggle = "show";
                //$('#contact_email_show').removeClass('noshow');
                //$('#contact_email_add').addClass('noshow');
            } else {  //No, contact is not in DB, so show correct stuff and clear fields not being used :)
                //             put code here to show "save for future" checkbox and edit boxes for adding associated data
                $('#contact_show_agency').html('&nbsp;');
                $('#contact_show_phone').html('&nbsp;');
                $('#contact_show_email').html('');
                $('#id_friendly_name').val('');
                if (!isEmptyOrSpaces(contact_name)) {
                    if (!($('#toggle_contact_show').hasClass('ev-closed')) || !($('#toggle_contact_add').hasClass('ev-closed'))) {
                        $('#toggle_contact_show').addClass("ev-closed");
                        $('#toggle_contact_add').removeClass("ev-closed");
                        $('#contact_email_show').addClass('noshow');
                        $('#contact_email_add').removeClass('noshow');
                    }
                    $('#contact_email_show').addClass('noshow');
                    $('#contact_email_add').removeClass('noshow');
                    //$('#contact_email_shaded').removeclass('ev-shadedpanel2');
                    //$('#contact_button').prop("checked", true);
                    //$('#toggle_contact_show').addClass("ev-closed");
                    //$('#toggle_contact_add').removeClass("ev-closed");
                    toggle = "add";
                    //$('#contact_email_show').addClass('noshow');
                    //$('#contact_email_add').removeClass('noshow');
                } else {
                    //don't show if entry was blank
                    $('#contact_button').prop("checked", false);
                    $('#toggle_contact_show').addClass("ev-closed");
                    $('#toggle_contact_add').addClass("ev-closed");
                    toggle = "";
                    $('#contact_email_show').addClass('noshow');
                    $('#contact_email_add').removeClass('noshow');
                }
            }
            

              $('#hide8').text($('#id_friendly_name').val());
              if (placeholderActive('#id_friendly_name')) {
                $('#hide8').text($('#id_friendly_name').attr('placeholder'));   
              }
              var wide = Number($('#hide8').width());
              wide = wide + 4;
              $('#id_friendly_name').width(wide);

              $('#hide6').text($('#id_contact_0').val());
              if (placeholderActive('#id_contact_0')) {
                $('#hide6').text($('#id_contact_0').attr('placeholder'));   
              }
              var wide = Number($('#hide6').width());
              wide = wide + 4;
              $('#id_contact_0').width(wide);
//               $('#id_contact_0').width($('#hide6').width());
//               var wide = Number($('#hide6').width());
//               if (wide > 260) {wide = 260;}
//               wide = wide + 7;
//               $('.evx-btntry4 .ui-combo-button').css("left", wide);

              $('#hide9').text($('#id_contact_email').val());
              if (placeholderActive('#id_contact_email')) {
                $('#hide9').text($('#id_contact_email').attr('placeholder'));   
              }
              $('#id_contact_email').width($('#hide9').width());
            
        },
        error: function(data) {
            alert('there was an error retrieving contact data');
        }
    });
    //$('#form').trigger('rescan.areYouSure');
});

//generate the edit dayofcontact popup
$("#edit_dayofcontact").click(function() {
    dayofcontact_name = $("#id_dayofcontact_0").val();
    var data = {
        "dayofcontact_name": dayofcontact_name
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/dayofcontact/ajax/get_dayofcontact_id',
        data: data,
        success: function(data) {
            var url = "/dayofcontact/" + data['dayofcontact_id'] + "/edit/";
            showEditPopup(url);
        },
        error: function(data) {
            alert("Something Went Wrong, likely that dayofcontact doesn't exist in database already");
        }
    });
});


//on select or focusout, see if dayofcontact is in database or new, and hide/show appropriate fields
$("#id_dayofcontact_0").on('djselectablechange djselectableselect focusout', function(event, ui) {
    dayofcontact_name = $("#id_dayofcontact_0").val();
    var data = {
        "dayofcontact_name": dayofcontact_name
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/dayofcontact/ajax/get_dayofcontact_info',
        data: data,
        success: function(data) {
            if (data['noerror'] == true) { //Yes, dayofcontact in in DB, do stuff but also clear out unused fields
                //             put code here to show this associated data on the screen (with an edit button too)
                //             alert(data['dayofcontact_name'] + data['dayofcontact_address'] + data['dayofcontact_link']+ data['dayofcontact_phone'] + data['dayofcontact_email']);
                ///put data in dayofcontact_show fields
                $('#dayofcontact_show_phone').html(data['dayofcontact_phone']);
                $('#dayofcontact_show_email').html(data['dayofcontact_email']);
                $('#id_dayofcontact_email').val('');
                $('#id_dayofcontact_phone').val('');
                
                //if either 'show' or 'add' is open then reveal 'show' no matter what:
                if (!($('#toggle_dayofcontact_show').hasClass('ev-closed')) || !($('#toggle_dayofcontact_add').hasClass('ev-closed'))) {
                    $('#toggle_dayofcontact_show').removeClass("ev-closed");
                    $('#toggle_dayofcontact_add').addClass("ev-closed");
                    $('#toggle_dayofcontact_alone').removeClass("ev-closed");    
                }
                toggle2 = "show";
            } else {  //No, dayofcontact is not in DB, so do stuff but also clear out unused fields
                //             put code here to show "save for future" checkbox and edit boxes for adding associated data
                //             alert("Something Went Wrong, likely that dayofcontact doesn't exist in database already");
                $('#dayofcontact_show_phone').html('&nbsp;');
                $('#dayofcontact_show_email').html('&nbsp;');
                // if name field not empty, then if either is open, reveal 'add' no matter what:
                if (!isEmptyOrSpaces(dayofcontact_name)) {
                    if (!($('#toggle_dayofcontact_show').hasClass('ev-closed')) || !($('#toggle_dayofcontact_add').hasClass('ev-closed'))) {
                        $('#toggle_dayofcontact_show').addClass("ev-closed");
                        $('#toggle_dayofcontact_add').removeClass("ev-closed");
                        $('#toggle_dayofcontact_alone').removeClass("ev-closed");
                    }
                    //$('#dayofcontact_button').prop("checked", true);
                    //$('#toggle_dayofcontact_show').addClass("ev-closed");
                    //$('#toggle_dayofcontact_add').removeClass("ev-closed");
                    toggle2 = "add";
                } else { // if empty then close both and uncheck the button
                    $('#dayofcontact_button').prop("checked", false);
                    $('#toggle_dayofcontact_show').addClass("ev-closed");
                    $('#toggle_daycontact_add').addClass("ev-closed");
                    $('#toggle_dayofcontact_alone').addClass("ev-closed");
                    toggle2 = "";
                }
            }
            
              $('#hide10').text($('#id_dayofcontact_0').val());
              if (placeholderActive('#id_dayofcontact_0')) {
                $('#hide10').text($('#id_dayofcontact_0').attr('placeholder'));   
              }
              var wide = Number($('#hide10').width());
              wide = wide + 4;
              $('#id_dayofcontact_0').width(wide);
//               $('#id_dayofcontact_0').width($('#hide10').width());
//               var wide = Number($('#hide10').width());
//               if (wide > 275) {wide = 275;}
//               wide = wide + 7;
//               $('.evx-btntry5 .ui-combo-button').css("left", wide);
            
            
        },
        error: function(data) {
            alert('there was an error retrieving dayofcontact data');
        }
    });
    //$('#form').trigger('rescan.areYouSure');
});


function updateSidecal(year, month) {
    //alert('here' + year + month);
    var data = {
        "year": year,
        "month": month,
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/sidecalmonth',
        data: data,
        success: function(data) {
            $("#sidecal").html(data['newhttp']);
            //alert(data['newhttp']);
            //init tooltips
            $('.tooltipped').tooltip();
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with the side calendar...");
        }
    });
}
function updateMycal(year, month) {
    //alert('here' + year + month);
    var data = {
        "year": year,
        "month": month,
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/mycalmonth',
        data: data,
        success: function(data) {
            $("#calendar").html(data['newhttp']);
            //alert(data['newhttp']);
            //init tooltips
            $('.tooltipped').tooltip();
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with the calendar...");
        }
    });
}


function updateSidePanels() {
    //update sidepanels for both reminders and activities    
    var data = {
        "dummy": "dummy",
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/sidepanelupdate',
        data: data,
        success: function(data) {
            $("#sidePastDueReminders").html(data['pastdue']);
            $("#sideUpcomingReminders").html(data['upcoming']);
            $("#sideActivities").html(data['activities']);
            $("#sidePaymentsDue").html(data['paymentsdue']);
        },
        error: function(data) {
//             alert("Something Went Wrong, likely something with udpating sidepanel...");
        }
    });
}


$("#id_waive_music_list").click(function() {
    //alert("waive_musiclist clicked");
    $(".waive_music_list_panel").toggleClass('noshow');
    $('#id_event_reminders_done').prop("checked", false);      
    updateFlags();  
});


$("#id_accept_custom").click(function() {
    //alert("accept_custom clicked");
    var data = {
        "music_list": $('#id_music_list').val()
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/check_accept_custom',
        data: data,
        success: function(data) {
            var dollars = Number(data['dollars']);
            if (dollars != 0) {
                //$("#id_accept_custom").addClass("noshow");
                //if now unchecked, SUBTRACT $ from extra_fee
                if ($('#id_accept_custom').prop("checked") == false) {
                    var curr = Number($("#id_extra_fee").val());
                    $("#id_extra_fee").val(curr - dollars);
                    $(".updateFeesExtra").trigger('change');
                    M.updateTextFields();
                } else {
                    //if now checked, ADD $ to extra_fee
                    var curr = Number($("#id_extra_fee").val());
                    $("#id_extra_fee").val(curr + dollars);
                    $(".updateFeesExtra").trigger('change');
                    M.updateTextFields();
                }
                //the below will cause views.py to realize "accept_custom" was checked,
                //and will complete the reminder associated.
                $('#id_event_reminders_done').prop("checked", false);
                updateFlags();
            } else {
                //$("#id_accept_custom").removeClass("noshow");
                //if not already checked, ADD $ to extra_fee
                
            }
        },
        error: function(data) {
            alert("Something went wrong, with check_accept_custom2");
        }   
    });

//     updateFlags();  
});




$("#include_auto_reminders_side").click(function() {
    $(".auto-reminder-side").toggleClass('noshow');
    $(".auto-reminder-side2").toggleClass('noshow');
    $(".auto-reminder-side3").toggleClass('noshow');
    $("#include_auto_reminders_side").toggleClass('auto-pressed'); 
    $("#soonrem_none").toggleClass('noshow'); 
    $("#dummyfocus1").focus(); 
    $("#btn_calendar").focus();
    toggle_auto_side();      
});
function toggle_auto_side() {
    var data = {"dummy": false,};
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/toggle_side_auto',
        data: data,
        success: function(data) {
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with toggling show auto-side...");
        }
    });
}


function trueorfalse(data) {
    if (data == 'true') {
        return true;
    } else {
        return false;
    }
}


function updateFlags() {
    //alert($('#id_event_reminders_done').prop('checked'));
    if (!$('#id_date').val() || ($('#id_date').val() == '')) {
        return;
    }
//     if ($('#id_event_reminders_done').prop('checked')) {
//         xhr = null;
//         return;
//     }
    var data = {"event_reminders_done": $('#id_event_reminders_done').prop('checked'),
                "id": $('#page_instance').val(),
                "ensemble_number": $('#id_ensemble_number').val(),
                "hold_until": $('#id_hold_until').val(),
                "hold_released": $('#id_hold_released').val(),
                "date_entered": $('#id_date_entered').val(),
                "date": $('#id_date').val(),
                "waive_contract": $('#id_waive_contract').prop('checked'),
                "waive_payment": $('#id_waive_payment').prop('checked'),
                "fee": $('#id_fee').val(),
                "deposit_fee": $('#id_deposit_fee').val(),
                "final_fee": $('#id_final_fee').val(),
                "extra_fee": $('#id_extra_fee').val(),
                "automation": $('#id_automation').prop('checked'),
                "accept_custom": $('#id_accept_custom').prop("checked"),
                
                "contract_sentdate": $('#id_contract_sentdate').val(),
                "deposit_sentdate": $('#id_deposit_sentdate').val(),
                "final_sentdate": $('#id_final_sentdate').val(),
                "music_list_sentdate": $('#id_music_list_sentdate').val(),
                "musicians_sentdate": $('#id_musicians_sentdate').val(),
                "confirmation_sentdate": $('#id_confirmation_sentdate').val(),
                "fact_sheets_sentdate": $('#id_fact_sheets_sentdate').val(),
                "hold_sentdate": $('#id_hold_sentdate').val(),
                "extra_sentdate": $('#id_extra_sentdate').val(),
                
                "contract_rcvddate": $('#id_contract_rcvddate').val(),
                "deposit_rcvddate": $('#id_deposit_rcvddate').val(),
                "final_rcvddate": $('#id_final_rcvddate').val(),
                "music_list_rcvddate": $('#id_music_list_rcvddate').val(),
                "musicians_rcvddate": $('#id_musicians_rcvddate').val(),
                "confirmation_rcvddate": $('#id_confirmation_rcvddate').val(),
                "fact_sheets_rcvddate": $('#id_fact_sheets_rcvddate').val(),
                "extra_rcvddate": $('#id_extra_rcvddate').val(),
                
                "contract_rcptdate": $('#id_contract_rcptdate').val(),
                "deposit_rcptdate": $('#id_deposit_rcptdate').val(),
                "final_rcptdate": $('#id_final_rcptdate').val(),
                "extra_rcptdate": $('#id_extra_rcptdate').val(),
                
                "contract_duedate": $('#id_contract_duedate').val(),
                "deposit_duedate": $('#id_deposit_duedate').val(),
                "final_duedate": $('#id_final_duedate').val(),
                "music_list_duedate": $('#id_music_list_duedate').val(),
                "musicians_duedate": $('#id_musicians_duedate').val(),
                "confirmation_duedate": $('#id_confirmation_duedate').val(),
                "fact_sheets_duedate": $('#id_fact_sheets_duedate').val(),
                "extra_duedate": $('#id_extra_duedate').val(),
                
                "contract_senddate": $('#id_contract_senddate').val(),
                "deposit_senddate": $('#id_deposit_senddate').val(),
                "final_senddate": $('#id_final_senddate').val(),
                "music_list_senddate": $('#id_music_list_senddate').val(),
                "musicians_senddate": $('#id_musicians_senddate').val(),
                "confirmation_senddate": $('#id_confirmation_senddate').val(),
                "fact_sheets_senddate": $('#id_fact_sheets_senddate').val(),
                "extra_senddate": $('#id_extra_senddate').val(),
                
                "flag_hold": $('#id_flag_hold').prop('checked'),
                "flag_hold_sent": $('#id_flag_hold_sent').prop('checked'),
                "waive_music_list": $('#id_waive_music_list').prop('checked'),
                "automation": $('#id_automation').prop('checked'),
                "reminderdisable": $('#id_reminderdisable').prop('checked'),
                
                "flag_contract_sent": $('#id_flag_contract_sent').prop('checked'),
                "flag_contract_rcvd": $('#id_flag_contract_rcvd').prop('checked'),
                "flag_contract_rcpt": $('#id_flag_contract_rcpt').prop('checked'),

                "flag_deposit_sent": $('#id_flag_deposit_sent').prop('checked'),
                "flag_deposit_rcvd": $('#id_flag_deposit_rcvd').prop('checked'),
                "flag_deposit_rcpt": $('#id_flag_deposit_rcpt').prop('checked'),

                "flag_music_list_sent": $('#id_flag_music_list_sent').prop('checked'),
                "flag_music_list_rcvd": $('#id_flag_music_list_rcvd').prop('checked'),

                "flag_musicians_sent": $('#id_flag_musicians_sent').prop('checked'),
                "flag_musicians_rcvd": $('#id_flag_musicians_rcvd').prop('checked'),

                "flag_final_payment_sent": $('#id_flag_final_payment_sent').prop('checked'),
                "flag_final_payment_rcvd": $('#id_flag_final_payment_rcvd').prop('checked'),
                "flag_final_payment_rcpt": $('#id_flag_final_payment_rcpt').prop('checked'),

                "flag_extra_sent": $('#id_flag_extra_sent').prop('checked'),
                "flag_extra_rcvd": $('#id_flag_extra_rcvd').prop('checked'),
                "flag_extra_rcpt": $('#id_flag_extra_rcpt').prop('checked'),

                "flag_final_confirmation_sent": $('#id_flag_final_confirmation_sent').prop('checked'),
                "flag_final_confirmation_rcvd": $('#id_flag_final_confirmation_rcvd').prop('checked'),

                "flag_fact_sheets_sent": $('#id_flag_fact_sheets_sent').prop('checked'),
                "flag_fact_sheets_rcvd": $('#id_flag_fact_sheets_rcvd').prop('checked'),
                
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/process_ajax_due_dates',
        data: data,
        success: function(data) {
            //alert('updateDueDatesSuccess');
            //alert(data['flag_hold'] + data['automation']);
            //alert($('#id_contract_senddate').val() + $('#id_flag_contract_sent').prop('checked'))
            
            $('#id_event_reminders_done').prop("checked",trueorfalse(data['event_reminders_done']));
            
            $('#id_contract_sentdate').val(data['contract_sentdate']);
            $('#id_deposit_sentdate').val(data['deposit_sentdate']);
            $('#id_final_sentdate').val(data['final_sentdate']);
            $('#id_music_list_sentdate').val(data['music_list_sentdate']);
            $('#id_musicians_sentdate').val(data['musicians_sentdate']);
            $('#id_confirmation_sentdate').val(data['confirmation_sentdate']);
            $('#id_fact_sheets_sentdate').val(data['fact_sheets_sentdate']);
            $('#id_hold_sentdate').val(data['hold_sentdate']);
            $('#id_extra_sentdate').val(data['extra_sentdate']);
            
            $('#id_contract_rcvddate').val(data['contract_rcvddate']);
            $('#id_deposit_rcvddate').val(data['deposit_rcvddate']);
            $('#id_final_rcvddate').val(data['final_rcvddate']);
            $('#id_music_list_rcvddate').val(data['music_list_rcvddate']);
            $('#id_musicians_rcvddate').val(data['musicians_rcvddate']);
            $('#id_confirmation_rcvddate').val(data['confirmation_rcvddate']);
            $('#id_fact_sheets_rcvddate').val(data['fact_sheets_rcvddate']);
            $('#id_extra_rcvddate').val(data['extra_rcvddate']);
            
            $('#id_contract_rcptdate').val(data['contract_rcptdate']);
            $('#id_deposit_rcptdate').val(data['deposit_rcptdate']);
            $('#id_final_rcptdate').val(data['final_rcptdate']);
            $('#id_extra_rcptdate').val(data['extra_rcptdate']);
            
            $('#id_contract_duedate').val(data['contract_duedate']);
            $('#id_deposit_duedate').val(data['deposit_duedate']);
            $('#id_final_duedate').val(data['final_duedate']);
            $('#id_music_list_duedate').val(data['music_list_duedate']);
            $('#id_musicians_duedate').val(data['musicians_duedate']);
            $('#id_confirmation_duedate').val(data['confirmation_duedate']);
            $('#id_fact_sheets_duedate').val(data['fact_sheets_duedate']);
            $('#id_extra_duedate').val(data['extra_duedate']);
            
            $('#id_contract_senddate').val(data['contract_senddate']);
            $('#id_deposit_senddate').val(data['deposit_senddate']);
            $('#id_final_senddate').val(data['final_senddate']);
            $('#id_music_list_senddate').val(data['music_list_senddate']);
            $('#id_musicians_senddate').val(data['musicians_senddate']);
            $('#id_confirmation_senddate').val(data['confirmation_senddate']);
            $('#id_fact_sheets_senddate').val(data['fact_sheets_senddate']);
            $('#id_extra_senddate').val(data['extra_senddate']);
            
            $('#id_flag_hold').prop("checked",trueorfalse(data['flag_hold']));
            $('#id_flag_hold_sent').prop("checked",trueorfalse(data['flag_hold_sent']));
            $('#id_waive_music_list').prop("checked",trueorfalse(data['waive_music_list']));
            $('#id_automation').prop("checked",trueorfalse(data['automation']));
            
            //alert($('#id_flag_hold').prop("checked") + $('#id_automation').prop("checked"));
            
            $('#id_flag_contract_sent').prop("checked",trueorfalse(data['flag_contract_sent']));
            $('#id_flag_contract_rcvd').prop("checked",trueorfalse(data['flag_contract_rcvd']));
            $('#id_flag_contract_rcpt').prop("checked",trueorfalse(data['flag_contract_rcpt']));

            $('#id_flag_deposit_sent').prop("checked",trueorfalse(data['flag_deposit_sent']));
            $('#id_flag_deposit_rcvd').prop("checked",trueorfalse(data['flag_deposit_rcvd']));
            $('#id_flag_deposit_rcpt').prop("checked",trueorfalse(data['flag_deposit_rcpt']));

            $('#id_flag_music_list_sent').prop("checked",trueorfalse(data['flag_music_list_sent']));
            $('#id_flag_music_list_rcvd').prop("checked",trueorfalse(data['flag_music_list_rcvd']));

            $('#id_flag_musicians_sent').prop("checked",trueorfalse(data['flag_musicians_sent']));
            $('#id_flag_musicians_rcvd').prop("checked",trueorfalse(data['flag_musicians_rcvd']));

            $('#id_flag_final_payment_sent').prop("checked",trueorfalse(data['flag_final_payment_sent']));
            $('#id_flag_final_payment_rcvd').prop("checked",trueorfalse(data['flag_final_payment_rcvd']));
            $('#id_flag_final_payment_rcpt').prop("checked",trueorfalse(data['flag_final_payment_rcpt']));

            $('#id_flag_extra_sent').prop("checked",trueorfalse(data['flag_extra_sent']));
            $('#id_flag_extra_rcvd').prop("checked",trueorfalse(data['flag_extra_rcvd']));
            $('#id_flag_extra_rcpt').prop("checked",trueorfalse(data['flag_extra_rcpt']));

            $('#id_flag_final_confirmation_sent').prop("checked",trueorfalse(data['flag_final_confirmation_sent']));
            $('#id_flag_final_confirmation_rcvd').prop("checked",trueorfalse(data['flag_final_confirmation_rcvd']));

            $('#id_flag_fact_sheets_sent').prop("checked",trueorfalse(data['flag_fact_sheets_sent']));
            $('#id_flag_fact_sheets_rcvd').prop("checked",trueorfalse(data['flag_fact_sheets_rcvd']));
            
            $('#id_deposit_fee').val(data['deposit_fee']);
            $('#id_final_fee').val(data['final_fee']);
            $('#id_date').val(data['date']);
            
            //alert($('#id_contract_senddate').val() + $('#id_flag_contract_sent').prop('checked'))
            
            updateFlags2();
            updateReminders();
           // alert($('#id_event_reminders_done').prop('checked'));
            //$('#form').trigger('checkform.areYouSure');
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with process_ajax_due_dates...");
        }
    });
}

$('#hideleftbar').click(function() {
    $('#sidenav-1').toggleClass('sidebarsizesmall');
    $('#sidenav-1').toggleClass('sidebarsizefull');
    $('#sidecal').toggleClass('nospecialshow');
    $('#sidestuff').toggleClass('nospecialshow');
    $('#headerelement').toggleClass('mainnormal');
    $('#headerelement').toggleClass('mainfull');
    $('#mainelement').toggleClass('mainnormal');
    $('#mainelement').toggleClass('mainfull');
    $('#vstitle').toggleClass('evx-vstitle-move');
    var curr = $('#hideleftbartext').html();
    if (curr == '\u27EA') {
        var newt = '&Rang;';
    } else {
        var newt = '&Lang;';
    }
    $('#hideleftbartext').html(newt);

    var data = {
        "panel": "hide",
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/sidecalpanelclick',
        data: data,
        success: function(data) {
            var nothing = 1;
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with the hide side panel being clicked...");
        }
    });
});




