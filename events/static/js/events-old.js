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
var flag_empty = "#eeeeee";
var flag_started = "#fff176";
var flag_done = "#a5d6a7";
var flag_late = "#ffcdd2";
var flag_hold = "#ffcc80";
var flag_white = "#ffffff";


//helper to see if actually empty or null
function isEmptyOrSpaces(str) {
    return str === null || str.match(/^ *$/) !== null;
}


$(document).ready(function() {
    $('.collapsible').collapsible({
        accordion: false,
    });

    //unknown?
    $('select').formSelect();
    //set Type hidden fields when choice changes (regular/hold/agency)
    var today = new Date();
    today.setHours(0, 0, 0, 0);
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
    });
    //when hold date is changed, updateFlags
    $('#id_hold_until').change(function() {
        //alert($('#id_hold_until').val());
        $('#id_event_reminders_done').prop("checked", false);
        updateFlags();
        M.updateTextFields();
    });
    //when date is changed, clear event_reminders_done flag!
    $('#id_date').change(function() {
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
        } else if (toggle2 == "show") {
            $('#toggle_dayofcontact_show').toggleClass("ev-closed");
        } else {
            //do nothing in reponse to button click if neither should be open
            $('#dayofcontact_button').prop("checked", false);
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
    
    
    
    
    
    $('.modal').modal();

    $('#reminders_bar_header').click(function() {
        //alert("clicked"); 
        //$('#form').trigger('rescan.areYouSure');
        if ($('#id_reminders_bar_hidden').prop("checked")) { 
            $('#id_reminders_bar_hidden').prop("checked", false);
        } else {
            $('#id_reminders_bar_hidden').prop("checked", true);
        }
        $('#form').trigger('checkform.areYouSure');
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
    var parts = $('#eventdate_norm').val().split('-');
    var mydate = new Date(parts[2],parts[0]-1,parts[1]);
    $(function() {
        $('#id_date').datepicker({
            autoClose: 'True',
            showDaysInNextAndPreviousMonths: 'True',
            format: 'dddd, mmmm d, yyyy',
            firstDay: 1,
            setDefaultDate: 'True',
            defaultDate: mydate,
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
    
    //update badges/flags
    updateFlags();
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









    if ($('#id_event_type_0').val().includes('eremony')) {
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





    
    
});

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

$( window ).resize(function() {
    //alert("change");
    M.textareaAutoResize($("#id_location_details"));
    M.textareaAutoResize($("#id_contact_details"));
    M.textareaAutoResize($("#id_dayofcontact_details"));
    //M.textareaAutoResize($("#id_contact_email"));
    
});

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
    $('#flag_contract').attr("data-badge-caption", "contract");
    $('#flag_contract').addClass('badge ev-badge-norm flag-empty');
    $('#id_color_contract').val(flag_empty);

    $('#btn_factsheet').removeClass();
    $('#btn_musicians').removeClass();
    $('#btn_confirmation').removeClass();
    $('#btn_receipt_finalpay').removeClass();
    $('#btn_receipt_finalpay').addClass('noshow');
    $('#btn_finalpay').removeClass();
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

    if (selected == 'Hold') {
        $('#flag_contract').removeClass();
        $('#flag_contract').attr("data-badge-caption", "HOLD");
        $('#flag_contract').addClass('badge ev-badge-norm flag-hold');
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
        $('#btn_hold').removeClass();
        //make red if hold past-due
        if (hold_pastdue) {
            $('#flag_contract').removeClass();
            $('#flag_contract').addClass('badge ev-badge-norm flag-late');
            $('#id_color_contract').val(flag_late);
        }
        return;
    }

    if ($('#id_waive_contract').prop('checked')) {
        $('#flag_contract').removeClass();
        $('#flag_contract').attr("data-badge-caption", "contract");
        $('#flag_contract').addClass('badge ev-badge-norm flag-white');
        $('#id_color_contract').val(flag_white);
        $('#flag_contract').attr("style", "text-decoration:line-through");
        //hide all contract buttons
        $('#btn_contract').addClass('noshow');
        $('#btn_depositcontract').addClass('noshow');
    } else {
        $('#flag_contract').attr("style", "text-decoration:none");
        if ($('#id_flag_contract_sent').prop('checked')) {
            $('#flag_contract').removeClass();
            $('#flag_contract').attr("data-badge-caption", "contract");
            $('#flag_contract').addClass('badge ev-badge-norm flag-started');
            $('#id_color_contract').val(flag_started);
            //hide contract btns
            $('#btn_contract').addClass('noshow');
            $('#btn_depositcontract').addClass('noshow');
        }
        if ($('#id_flag_contract_rcvd').prop('checked')) {
            $('#flag_contract').removeClass();
            $('#flag_contract').attr("data-badge-caption", "contract");
            $('#flag_contract').addClass('badge ev-badge-norm flag-done');
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
            $('#flag_contract').attr("data-badge-caption", "contract");
            $('#flag_contract').addClass('badge ev-badge-norm flag-late');
            $('#id_color_contract').val(flag_late);
        }
    }

    if ($('#id_waive_payment').prop('checked') || ($("#id_deposit_senddate").val() && ($("#id_deposit_senddate").val() == $("#id_final_senddate").val())) || ($("#id_deposit_fee").val() == '0') || ($("#id_deposit_fee").val() == '0.00')) {
        $('#flag_deposit').removeClass();
        $('#flag_deposit').addClass('badge ev-badge-norm flag-white');
        $('#id_color_deposit').val(flag_white);
        $('#flag_deposit').attr("style", "text-decoration:line-through");
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
        $('#flag_deposit').attr("style", "text-decoration:none");
        $('#flag_deposit').removeClass();
        $('#flag_deposit').addClass('badge ev-badge-norm flag-empty');
        if ($('#id_flag_deposit_sent').prop('checked')) {
            $('#flag_deposit').removeClass();
            $('#flag_deposit').addClass('badge ev-badge-norm flag-started');
            $('#id_color_deposit').val(flag_started);
            //hide deposit btns
            $('#btn_deposit').addClass('noshow');
            $('#btn_depositcontract').addClass('noshow');
        }
        if ($('#id_flag_deposit_rcvd').prop('checked')) {
            $('#flag_deposit').removeClass();
            $('#flag_deposit').addClass('badge ev-badge-norm flag-done');
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
            $('#flag_deposit').addClass('badge ev-badge-norm flag-late');
            $('#id_color_deposit').val(flag_late);
        }
    }


    if ($('#id_waive_music_list').prop('checked')) {
        $('#flag_music_list').removeClass();
        $('#flag_music_list').addClass('badge ev-badge-norm flag-white');
        $('#id_color_music_list').val(flag_white);
        $('#flag_music_list').attr("style", "text-decoration:line-through");
        //hide musiclist button
        $('#btn_musiclist').addClass('noshow');
    } else {
        $('#flag_music_list').attr("style", "text-decoration:none");
        $('#flag_music_list').removeClass();
        $('#flag_music_list').addClass('badge ev-badge-norm flag-empty');
        if ($('#id_flag_music_list_sent').prop('checked')) {
            $('#flag_music_list').removeClass();
            $('#flag_music_list').addClass('badge ev-badge-norm flag-started');
            $('#id_color_music_list').val(flag_started);
            //hide musiclist button
            $('#btn_musiclist').addClass('noshow');
        }
        if ($('#id_flag_music_list_rcvd').prop('checked')) {
            $('#flag_music_list').removeClass();
            $('#flag_music_list').addClass('badge ev-badge-norm flag-done');
            $('#id_color_music_list').val(flag_done);
            //hide musiclist button
            $('#btn_musiclist').addClass('noshow');
        }
        if (music_list_pastdue) {
            $('#flag_music_list').removeClass();
            $('#flag_music_list').addClass('badge ev-badge-norm flag-late');
            $('#id_color_music_list').val(flag_late);
        }
    }

    if ($('#id_flag_musicians_sent').prop('checked')) {
        $('#flag_musicians').removeClass();
        $('#flag_musicians').addClass('badge ev-badge-norm flag-started');
        $('#id_color_musicians').val(flag_started);
        //don't yet hide musicians button
        //$('#btn_musicians').addClass('noshow');
        //also include xbtn_musicians
        //var dummy;
        //dummy =  setTimeout(updateMusiciansAskedList, 1000);
    }
    if ($('#id_flag_musicians_rcvd').prop('checked')) {
        $('#flag_musicians').removeClass();
        $('#flag_musicians').addClass('badge ev-badge-norm flag-done');
        $('#id_color_musicians').val(flag_done);
        //now hide musicians button, cause all hired
        $('#btn_musicians').addClass('noshow');
    }
    if (musicians_pastdue) {
        $('#flag_musicians').removeClass();
        $('#flag_musicians').addClass('badge ev-badge-norm flag-late');
        $('#id_color_musicians').val(flag_late);
    }

    if ($('#id_waive_payment').prop('checked')) {
        $('#flag_final_pay').removeClass();
        $('#flag_final_pay').addClass('badge ev-badge-norm flag-white');
        $('#id_color_final_payment').val(flag_white);
        $('#flag_final_pay').attr("style", "text-decoration:line-through");
        //hide finalpay button
        $('#btn_finalpay').addClass('noshow');
    } else {
        $('#flag_final_pay').attr("style", "text-decoration:none");
        $('#flag_final_pay').removeClass();
        $('#flag_final_pay').addClass('badge ev-badge-norm flag-empty');
        if ($('#id_flag_final_payment_sent').prop('checked')) {
            $('#flag_final_pay').removeClass();
            $('#flag_final_pay').addClass('badge ev-badge-norm flag-started');
            $('#id_color_final_payment').val(flag_started);
            //hide finalpay button
            $('#btn_finalpay').addClass('noshow');
        }
        if ($('#id_flag_final_payment_rcvd').prop('checked')) {
            $('#flag_final_pay').removeClass();
            $('#flag_final_pay').addClass('badge ev-badge-norm flag-done');
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
            $('#flag_final_pay').addClass('badge ev-badge-norm flag-late');
            $('#id_color_final_payment').val(flag_late);
        }
    }

    if ($('#id_flag_final_confirmation_sent').prop('checked')) {
        $('#flag_confirm').removeClass();
        $('#flag_confirm').addClass('badge ev-badge-norm flag-started');
        $('#id_color_final_confirmation').val(flag_started);
        //hide confirmation button
        $('#btn_confirmation').addClass('noshow');
    }
    if ($('#id_flag_final_confirmation_rcvd').prop('checked')) {
        $('#flag_confirm').removeClass();
        $('#flag_confirm').addClass('badge ev-badge-norm flag-done');
        $('#id_color_final_confirmation').val(flag_done);
        //hide confirmation button
        $('#btn_confirmation').addClass('noshow');
    }
    if (confirmation_pastdue) {
        $('#flag_confirm').removeClass();
        $('#flag_confirm').addClass('badge ev-badge-norm flag-late');
        $('#id_color_final_confirmation').val(flag_late);
    }

    if ($('#id_flag_fact_sheets_sent').prop('checked')) {
        $('#flag_fact_sheets').removeClass();
        $('#flag_fact_sheets').addClass('badge ev-badge-norm flag-started');
        $('#id_color_fact_sheets').val(flag_started);
        //hide factsheet button
        $('#btn_factsheet').addClass('noshow');
    }
    if ($('#id_flag_fact_sheets_rcvd').prop('checked')) {
        $('#flag_fact_sheets').removeClass();
        $('#flag_fact_sheets').addClass('badge ev-badge-norm flag-done');
        $('#id_color_fact_sheets').val(flag_done);
        //hide factsheet button
        $('#btn_factsheet').addClass('noshow');
    }
    if (fact_sheets_pastdue) {
        $('#flag_fact_sheets').removeClass();
        $('#flag_fact_sheets').addClass('badge ev-badge-norm flag-late');
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
                updateFlags();
            },
            error: function(data) {
                alert('There was an checking disable built-in');
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
            var fullhtml = "";
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

                myhtml = '<span class="ev-activity-list">{{ activity.date|date:"n/j" }}: {{ activity.name }}</span><br />';

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
            $('#reminders_bar').html("Reminders, Activity, Notes");

            //also important, rebind event handlers to new list of reminders!
            $(".ev-remind-check").on('click', evRemindCheck);
            $(".edit_automation").click(evEditAutomated);
            $(".edit_regular").click(evEditRegular);
            $("#show_disabled_reminders").click(function() {
                $('#show_disabled').toggleClass("noshow");
                $('#show_disabled_buffer').toggleClass("noshow");
            });
            updateSidePanels();
            
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
    //  User will need to SAVE event because of this...
    
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
    if (lastsplit == 'deposit') {
        $("#id_flag_deposit_sent").prop("checked", true);
        if ($("#id_deposit_sentdate").val()) {
            addActivity(remind_id, "Deposit request was sent manually");    
        }
    }
    if (lastsplit == 'depositcontract') {
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
    if (lastsplit == 'musiclist') {
        $("#id_flag_music_list_sent").prop("checked", true);
        if ($("#id_music_list_sentdate").val()) {
            addActivity(remind_id, "Music list request was sent manually");    
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
    if (lastsplit == 'invoice') {
        addActivity(remind_id, "Invoice (full) was sent manually");    
    }
    if (lastsplit == 'invoice_deposit') {
        addActivity(remind_id, "Invoice (deposit) was sent manually");    
    }
    if (lastsplit == 'invoice_final') {
        addActivity(remind_id, "Invoice (final) was sent manually");    
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
function closePopup3(win) {
    //same as above, except called after *email* popup
    //so process new info, like musicians invited
    //win.onbeforeunload = popupclosed2(win);
//     dummy = setTimeout(updateFlags, 2500);
//     dummy =  setTimeout(updateActivities, 4500);
//     dummy =  setTimeout(updateValues, 5250);
//     dummy =  setTimeout(updateMusiciansAskedList, 6000);
    win.close();
    var dummy = setTimeout(resaveevent, 400);
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
            if (num != ensnum) {
                if (confirm("The selection you made does not match the form's Ensemble Number.\nWould you like to proceed anyways?")) {
                    //do nothing
                } else {
                    return;
                }
            }
            if (ensnum == "1") {
                $("#id_fee").val(data['ens1']);
                $("#id_musician_fee").val(data['ensm']);
                contracting = data['ens1'] - (data['ensm'] * ensnum);
                $("#id_contracting_fee").val(contracting);
                $("#id_deposit_fee").val($("#id_fee").val() / 2);
                $("#id_final_fee").val($("#id_fee").val() / 2);
                M.updateTextFields();
            }
            if (ensnum == "2") {
                $("#id_fee").val(data['ens2']);
                $("#id_musician_fee").val(data['ensm']);
                contracting = data['ens2'] - (data['ensm'] * ensnum);
                $("#id_contracting_fee").val(contracting);
                $("#id_deposit_fee").val($("#id_fee").val() / 2);
                $("#id_final_fee").val($("#id_fee").val() / 2);
                M.updateTextFields();
            }
            if (ensnum == "3") {
                $("#id_fee").val(data['ens3']);
                $("#id_musician_fee").val(data['ensm']);
                contracting = data['ens3'] - (data['ensm'] * ensnum);
                $("#id_contracting_fee").val(contracting);
                $("#id_deposit_fee").val($("#id_fee").val() / 2);
                $("#id_final_fee").val($("#id_fee").val() / 2);
                M.updateTextFields();
            }
            if (ensnum == "4") {
                $("#id_fee").val(data['ens4']);
                $("#id_musician_fee").val(data['ensm']);
                contracting = data['ens4'] - (data['ensm'] * ensnum);
                $("#id_contracting_fee").val(contracting);
                $("#id_deposit_fee").val($("#id_fee").val() / 2);
                $("#id_final_fee").val($("#id_fee").val() / 2);
                M.updateTextFields();
            }
            $('#id_used_ratechart').prop("checked", true);
            $('#id_event_reminders_done').prop("checked", false);
            updateFlags();
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
    var data = {
        "mus": mus,
        "event": $("#page_instance").val(),
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
    var data = {
        "mus": mus,
        "event": $("#page_instance").val(),
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
$(document).on('change', '.musinputinst', function() {
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
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/updatelistofmusicians',
        data: data,
        success: function(data) {
            $("#musicianslist").html(data['mlist']);
            //dummy = setTimeout(updateFlags, 500);
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with udpating musicianslist...");
        }
    });    
}



//update the fees when ensemble_number, fee, or musician_fee is changed
$(".updateFees").on('change', function(event, ui) {
    if ($("#id_fee").val() && $("#id_musician_fee").val() && $("#id_ensemble_number").val()) {
        var contracting = $("#id_fee").val() - ($("#id_musician_fee").val() * $("#id_ensemble_number").val());
        $("#id_contracting_fee").val(contracting);
        $("#id_deposit_fee").val($("#id_fee").val() / 2);
        $("#id_final_fee").val($("#id_fee").val() / 2);
        M.updateTextFields();
        if ($("#id_deposit_fee").val() == '0') {
            $('#id_event_reminders_done').prop("checked", false);
            updateFlags();
        }
    }
});
//update musician_fee if contracting fee is changed manually
$(".updateFeesContracting").on('change', function(event, ui) {
    if ($("#id_fee").val() && $("#id_musician_fee").val() && $("#id_ensemble_number").val()) {
        var musicians = ($("#id_fee").val() - $("#id_contracting_fee").val()) / $("#id_ensemble_number").val();
        $("#id_musician_fee").val(musicians);
        M.updateTextFields();
        //updateFlags();
    }
});
//update deposit/final fees upon manual change
$(".updateFeesDeposit").on('change', function(event, ui) {
    if ($("#id_deposit_fee").val() && $("#id_fee").val()) {
        var final = ($("#id_fee").val() - $("#id_deposit_fee").val());
        $("#id_final_fee").val(final);
        M.updateTextFields();
        //check for deposit_fee = 0, if so set flag to redo reminder in py.
        // next time event is updated the flags will update, reminders for final
        //  will be deleted if deposit already receieved, etc. 
        if ($("#id_deposit_fee").val() == '0') {
            $('#id_event_reminders_done').prop("checked", false);
            updateFlags();
        }
        //updateFlags();
    }
});
$(".updateFeesFinal").on('change', function(event, ui) {
    if ($("#id_final_fee").val() && $("#id_fee").val()) {
        var deposit = ($("#id_fee").val() - $("#id_final_fee").val());
        $("#id_deposit_fee").val(deposit);
        M.updateTextFields();
        //check for deposit_fee = 0, if so set flag to redo reminder in py.
        // next time event is updated the flags will update, reminders for final
        //  will be deleted if deposit already receieved, etc. 
        if ($("#id_deposit_fee").val() == '0') {
            $('#id_event_reminders_done').prop("checked", false);
            updateFlags();
        }
        //updateFlags();
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
    }

    if (check) {
        //alert($(this).attr("name"));
        //alert($('#special1').attr("name"));
        //alert('checking required fields...');
        var passed = true;
        var type = '';
        if ($('#id_fee').val() && ($('#id_deposit_fee').val() || $('#id_final_fee').val())) {
            //nothing
        } else { //if fee are not entered, generally a problem except if HOLD type of event!
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
            passed = false;
            type = "contact's friendly name";
        }
        if (!($('#id_contact_email').val()) && !($('#contact_show_email').val())) {
            passed = false;
            type = "contact's email";
        }
        if (!(passed)) {
            var msg = "Before proceeding with automation or sending a form email, \n";
            msg = msg + "you must fill in at least the " + type + " section!";
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
        if ($('#id_start_time').val() && $('#id_end_time').val() && ($('#id_contact_email').val() || $('#contact_show_email').val())) {
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
            if (data['noerror'] == true) {
                $('#contact_show_agency').html(data['contact_agency']);
                $('#contact_show_phone').html(data['contact_phone']);
                $('#contact_show_email').html(data['contact_email']);
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
            } else {
                //             put code here to show "save for future" checkbox and edit boxes for adding associated data
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
            if (data['noerror'] == true) {
                //             put code here to show this associated data on the screen (with an edit button too)
                //             alert(data['dayofcontact_name'] + data['dayofcontact_address'] + data['dayofcontact_link']+ data['dayofcontact_phone'] + data['dayofcontact_email']);
                ///put data in dayofcontact_show fields
                $('#dayofcontact_show_phone').html(data['dayofcontact_phone']);
                $('#dayofcontact_show_email').html(data['dayofcontact_email']);
                //$('#toggle_dayofcontact_show').addClass("ev-closed");
                //$('#toggle_dayofcontact_add').addClass("ev-closed");
                //$('#dayofcontact_button').prop("checked", false);
                if (!($('#toggle_dayofcontact_show').hasClass('ev-closed')) || !($('#toggle_dayofcontact_add').hasClass('ev-closed'))) {
                    $('#toggle_dayofcontact_show').removeClass("ev-closed");
                    $('#toggle_dayofcontact_add').addClass("ev-closed");    
                }
                toggle2 = "show";
            } else {
                //             put code here to show "save for future" checkbox and edit boxes for adding associated data
                //             alert("Something Went Wrong, likely that dayofcontact doesn't exist in database already");
                if (!isEmptyOrSpaces(dayofcontact_name)) {
                    if (!($('#toggle_dayofcontact_show').hasClass('ev-closed')) || !($('#toggle_dayofcontact_add').hasClass('ev-closed'))) {
                        $('#toggle_dayofcontact_show').addClass("ev-closed");
                        $('#toggle_dayofcontact_add').removeClass("ev-closed");
                    }
                    //$('#dayofcontact_button').prop("checked", true);
                    //$('#toggle_dayofcontact_show').addClass("ev-closed");
                    //$('#toggle_dayofcontact_add').removeClass("ev-closed");
                    toggle2 = "add";
                } else {
                    $('#dayofcontact_button').prop("checked", false);
                    $('#toggle_dayofcontact_show').addClass("ev-closed");
                    $('#toggle_daycontact_add').addClass("ev-closed");
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
            alert("Something Went Wrong, likely something with udpating sidepanel...");
        }
    });
}


$("#id_waive_music_list").click(function() {
    $(".waive_music_list_panel").toggleClass('noshow');
    $('#id_event_reminders_done').prop("checked", false);      
    updateFlags();  
});


$("#include_auto_reminders_side").click(function() {
    $(".auto-reminder-side").toggleClass('noshow');
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
                "hold_until": $('#id_hold_until').val(),
                "hold_released": $('#id_hold_released').val(),
                "date_entered": $('#id_date_entered').val(),
                "date": $('#id_date').val(),
                "waive_contract": $('#id_waive_contract').prop('checked'),
                "waive_payment": $('#id_waive_payment').prop('checked'),
                "fee": $('#id_fee').val(),
                "deposit_fee": $('#id_deposit_fee').val(),
                "final_fee": $('#id_final_fee').val(),
                "automation": $('#id_automation').prop('checked'),
                
                "contract_sentdate": $('#id_contract_sentdate').val(),
                "deposit_sentdate": $('#id_deposit_sentdate').val(),
                "final_sentdate": $('#id_final_sentdate').val(),
                "music_list_sentdate": $('#id_music_list_sentdate').val(),
                "musicians_sentdate": $('#id_musicians_sentdate').val(),
                "confirmation_sentdate": $('#id_confirmation_sentdate').val(),
                "fact_sheets_sentdate": $('#id_fact_sheets_sentdate').val(),
                "hold_sentdate": $('#id_hold_sentdate').val(),
                
                "contract_rcvddate": $('#id_contract_rcvddate').val(),
                "deposit_rcvddate": $('#id_deposit_rcvddate').val(),
                "final_rcvddate": $('#id_final_rcvddate').val(),
                "music_list_rcvddate": $('#id_music_list_rcvddate').val(),
                "musicians_rcvddate": $('#id_musicians_rcvddate').val(),
                "confirmation_rcvddate": $('#id_confirmation_rcvddate').val(),
                "fact_sheets_rcvddate": $('#id_fact_sheets_rcvddate').val(),
                
                "contract_rcptdate": $('#id_contract_rcptdate').val(),
                "deposit_rcptdate": $('#id_deposit_rcptdate').val(),
                "final_rcptdate": $('#id_final_rcptdate').val(),
                
                "contract_duedate": $('#id_contract_duedate').val(),
                "deposit_duedate": $('#id_deposit_duedate').val(),
                "final_duedate": $('#id_final_duedate').val(),
                "music_list_duedate": $('#id_music_list_duedate').val(),
                "musicians_duedate": $('#id_musicians_duedate').val(),
                "confirmation_duedate": $('#id_confirmation_duedate').val(),
                "fact_sheets_duedate": $('#id_fact_sheets_duedate').val(),
                
                "contract_senddate": $('#id_contract_senddate').val(),
                "deposit_senddate": $('#id_deposit_senddate').val(),
                "final_senddate": $('#id_final_senddate').val(),
                "music_list_senddate": $('#id_music_list_senddate').val(),
                "musicians_senddate": $('#id_musicians_senddate').val(),
                "confirmation_senddate": $('#id_confirmation_senddate').val(),
                "fact_sheets_senddate": $('#id_fact_sheets_senddate').val(),
                
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
            
            $('#id_contract_rcvddate').val(data['contract_rcvddate']);
            $('#id_deposit_rcvddate').val(data['deposit_rcvddate']);
            $('#id_final_rcvddate').val(data['final_rcvddate']);
            $('#id_music_list_rcvddate').val(data['music_list_rcvddate']);
            $('#id_musicians_rcvddate').val(data['musicians_rcvddate']);
            $('#id_confirmation_rcvddate').val(data['confirmation_rcvddate']);
            $('#id_fact_sheets_rcvddate').val(data['fact_sheets_rcvddate']);
            
            $('#id_contract_rcptdate').val(data['contract_rcptdate']);
            $('#id_deposit_rcptdate').val(data['deposit_rcptdate']);
            $('#id_final_rcptdate').val(data['final_rcptdate']);
            
            $('#id_contract_duedate').val(data['contract_duedate']);
            $('#id_deposit_duedate').val(data['deposit_duedate']);
            $('#id_final_duedate').val(data['final_duedate']);
            $('#id_music_list_duedate').val(data['music_list_duedate']);
            $('#id_musicians_duedate').val(data['musicians_duedate']);
            $('#id_confirmation_duedate').val(data['confirmation_duedate']);
            $('#id_fact_sheets_duedate').val(data['fact_sheets_duedate']);
            
            $('#id_contract_senddate').val(data['contract_senddate']);
            $('#id_deposit_senddate').val(data['deposit_senddate']);
            $('#id_final_senddate').val(data['final_senddate']);
            $('#id_music_list_senddate').val(data['music_list_senddate']);
            $('#id_musicians_senddate').val(data['musicians_senddate']);
            $('#id_confirmation_senddate').val(data['confirmation_senddate']);
            $('#id_fact_sheets_senddate').val(data['fact_sheets_senddate']);
            
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

            $('#id_flag_final_confirmation_sent').prop("checked",trueorfalse(data['flag_final_confirmation_sent']));
            $('#id_flag_final_confirmation_rcvd').prop("checked",trueorfalse(data['flag_final_confirmation_rcvd']));

            $('#id_flag_fact_sheets_sent').prop("checked",trueorfalse(data['flag_fact_sheets_sent']));
            $('#id_flag_fact_sheets_rcvd').prop("checked",trueorfalse(data['flag_fact_sheets_rcvd']));
            
            $('#id_deposit_fee').val(data['deposit_fee']);
            $('#id_final_fee').val(data['final_fee']);
            
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




