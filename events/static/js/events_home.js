

$(document).ready(function() {
    
    $(".musicians_feed").each(function(index, value) {
        var event_id = $(this).attr("event_id"); 
        var savedthis = this;
        var data = {"event_id": event_id};
        //alert(data);
        $.ajax({
            type : 'GET',
            url :  '/remind/ajax/get_booked_musicians',
            data : data,
            success : function(data){
                var fullhtml = "";
                var myhtml = "";
                var list = data.split(',');
                var index = 0;
                var nummus = 0;
                if (list.length > 1) {
                    while (index < list.length) {
                        fullhtml = fullhtml + list[index] + " (";
                        index = index + 1;
                        fullhtml = fullhtml + list[index] + ")<br />";
                        if (list[index] != '----') {
                            nummus = nummus + 1;
                        }
                        index = index + 1;
                    }
                }
                $(savedthis).attr("data-tooltip", fullhtml);
                var topline = $(savedthis).html();
                topline = "(" + nummus.toString() + topline;
                $(savedthis).html(topline);
            },
            error: function(data) {
                alert('There was an error 6b!');
            }
        });
    });

    $(".musiclist_feed").each(function(index, value) {
        var event_id = $(this).attr("event_id"); 
        var savedthis = this;
        var data = {"event_id": event_id};
        //alert(data);
        $.ajax({
            type : 'GET',
            url :  '/remind/ajax/get_musiclist',
            data : data,
            success : function(data){
                $(savedthis).attr("data-tooltip", data);
            },
            error: function(data) {
                alert('There was an error 6c!');
            }
        });
    });




    $(".activity_feed").each(function(index, value) {
        var event_id = $(this).attr("event_id"); 
        var savedthis = this;
        var data = {"event_id": event_id};
        //alert(data);
        $.ajax({
            type : 'GET',
            url :  '/remind/ajax/get_5_activities',
            data : data,
            success : function(data){
                var fullhtml = "";
                var myhtml = "";
                var more = 0;
                var rdate;
                var friendlydate = "";
                var week = new Date();
                var today = new Date();
                today.setHours(0,0,0,0);
                week.setHours(0,0,0,0);
                week.setDate(week.getDate() + 6);
                var year, month, day;
                $.each(JSON.parse(data), function (index, object) {
                    year = object.fields.date.substr(0,4);
                    month = object.fields.date.substr(5,2);
                    day = object.fields.date.substr(8,2);
                    year = Number(year);
                    month = Number(month) - 1;
                    day = Number(day);
                    rdate =  new Date(year, month, day);
                    myhtml = '{{ activity.date }}: {{ activity.name }}<br />';
                    month = month + 1;
                    friendlydate = month + "\/" + day;
                    myhtml = myhtml.replace('{{ activity.date }}', friendlydate);
                    myhtml = myhtml.replace('{{ activity.name }}', object.fields.name);
                    if (index == 4) {
                        more = 1;
                    } else {
                        fullhtml = fullhtml + myhtml;
                    }
                });
                if (more == 1) {fullhtml = fullhtml + '....';}
                if (fullhtml == '....' || fullhtml == '') {fullhtml = "No Recent Activity <br />";}
                $(savedthis).attr("data-tooltip", fullhtml);
                var ending = '';
                var index = fullhtml.indexOf("<br />");
                if (index > 30) {index = 30; ending = '...';}
                $(savedthis).html(fullhtml.substring(0,index) + ending);
            },
    
            error: function(data) {
                alert('There was an error 6d!');
            }
            
        });
    });
    

    $(".reminder_feed").each(function(index, value) {
        var event_id = $(this).attr("event_id"); 
        var savedthis = this;
        var data = {"event_id": event_id};
        //alert(data);
        $.ajax({
            type : 'GET',
            url :  '/remind/ajax/get_5_reminders',
            data : data,
            success : function(data){
                var fullhtml = "";
                var myhtml = "";
                var more = 0;
                var rdate;
                var friendlydate = "";
                var week = new Date();
                var today = new Date();
                today.setHours(0,0,0,0);
                week.setHours(0,0,0,0);
                week.setDate(week.getDate() + 6);
                var year, month, day;
                $.each(JSON.parse(data), function (index, object) {
                    year = object.fields.date.substr(0,4);
                    month = object.fields.date.substr(5,2);
                    day = object.fields.date.substr(8,2);
                    year = Number(year);
                    month = Number(month) - 1;
                    day = Number(day);
                    rdate =  new Date(year, month, day);
                    myhtml = '{{ reminder.date }}: {{ reminder.name }}<br />';
                    month = month + 1;
                    friendlydate = month + "\/" + day;
                    myhtml = myhtml.replace('{{ reminder.date }}', friendlydate);
                    myhtml = myhtml.replace('{{ reminder.name }}', object.fields.name);
                    if (index == 4) {
                        more = 1;
                    } else {
                        fullhtml = fullhtml + myhtml;
                    }
                });
                if (more == 1) {fullhtml = fullhtml + '....';}
                if (fullhtml == '....' || fullhtml == '') {fullhtml = "No Upcoming Undone Reminders <br />";}
                $(savedthis).attr("data-tooltip", fullhtml);
                var ending = '';
                var index = fullhtml.indexOf("<br />");
                //if (index > 30) {index = 30; ending = '...';}
                //$(savedthis).html(fullhtml.substring(0,index-1) + ending);
            },
    
            error: function(data) {
                alert('There was an error 6e!');
            }
            
        });
    });







    //update nav bar according to page_flag value    
    var flag = $('#page_flag').val();
    if (flag == 'home') {
        $('#nav_home, #navs_home').addClass("active");
        $('#nav_new, #navs_new').removeClass("active");
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
    if (flag == 'esigs') {
        $('#nav_home, #navs_home').removeClass("active");
        $('#nav_new, #navs_new').removeClass("active");
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
        $('#nav_esigs, #navs_esigs').addClass("active");
        $('#nav_calendar, #navs_calendar').removeClass("active");
        $('#nav_reports, #navs_reports').removeClass("active");
        //add more menu items as necessary?
    }    
    if (flag == 'rates') {
        $('#nav_home, #navs_home').removeClass("active");
        $('#nav_new, #navs_new').removeClass("active");
        $('#nav_arrows').addClass("ev-nav-hide");
        $('#nav_editforms, #navs_editforms').removeClass("active");
        $('#nav_dropdown').removeClass("active");
        $('#nav_archived, #navs_archived').removeClass("active");
        $('#nav_browse, #navs_browse').removeClass("active");
        $('#nav_tasks, #navs_tasks').removeClass("active");
        $('#btn_calendar').addClass("lighten-5");
        $('#btn_calendar').removeClass("lighten-4");
        $('#nav_rates, #navs_rates').addClass("active");
        $('#nav_payments_due, #navs_payments_due').removeClass("active");
        $('#nav_payments_received, #navs_payments_received').removeClass("active");
        $('#nav_syncgcal, #navs_syncgcal').removeClass("active");
        $('#nav_esigs, #navs_esigs').removeClass("active");
        $('#nav_calendar, #navs_calendar').removeClass("active");
        $('#nav_reports, #navs_reports').removeClass("active");
        //add more menu items as necessary?
    }    
    if (flag == 'payments_due') {
        $('#nav_home, #navs_home').removeClass("active");
        $('#nav_new, #navs_new').removeClass("active");
        $('#nav_arrows').addClass("ev-nav-hide");
        $('#nav_editforms, #navs_editforms').removeClass("active");
        $('#nav_dropdown').removeClass("active");
        $('#nav_archived, #navs_archived').removeClass("active");
        $('#nav_browse, #navs_browse').removeClass("active");
        $('#nav_tasks, #navs_tasks').removeClass("active");
        $('#btn_calendar').addClass("lighten-5");
        $('#btn_calendar').removeClass("lighten-4");
        $('#nav_rates, #navs_rates').removeClass("active");
        $('#nav_payments_due, #navs_payments_due').addClass("active");
        $('#nav_payments_received, #navs_payments_received').removeClass("active");
        $('#nav_syncgcal, #navs_syncgcal').removeClass("active");
        $('#nav_esigs, #navs_esigs').removeClass("active");
        $('#nav_calendar, #navs_calendar').removeClass("active");
        $('#nav_reports, #navs_reports').removeClass("active");
        //add more menu items as necessary?
    }  
    if (flag == 'payments_rcvd') {
        $('#nav_home, #navs_home').removeClass("active");
        $('#nav_new, #navs_new').removeClass("active");
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
        $('#nav_payments_received, #navs_payments_received').addClass("active");
        $('#nav_syncgcal, #navs_syncgcal').removeClass("active");
        $('#nav_esigs, #navs_esigs').removeClass("active");
        $('#nav_calendar, #navs_calendar').removeClass("active");
        $('#nav_reports, #navs_reports').removeClass("active");
        //add more menu items as necessary?
    }
    if (flag == 'syncgcal') {
        $('#nav_home, #navs_home').removeClass("active");
        $('#nav_new, #navs_new').removeClass("active");
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
        $('#nav_syncgcal, #navs_syncgcal').addClass("active");
        $('#nav_esigs, #navs_esigs').removeClass("active");
        $('#nav_calendar, #navs_calendar').removeClass("active");
        $('#nav_reports, #navs_reports').removeClass("active");
        //add more menu items as necessary?
    }
    if (flag == 'search') {
        $('#nav_home, #navs_home').removeClass("active");
        $('#nav_new, #navs_new').removeClass("active");
        $('#nav_arrows').addClass("ev-nav-hide");
        $('#nav_editforms, navs_editforms').removeClass("active");
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
    if (flag == 'archived') {
        $('#nav_home, #navs_home').removeClass("active");
        $('#nav_new, #navs_new').removeClass("active");
        $('#nav_arrows').addClass("ev-nav-hide");
        $('#nav_editforms, navs_editforms').removeClass("active");
        $('#nav_dropdown').addClass("active");
        $('#nav_archived, #navs_archived').addClass("active");
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
    if (flag == 'browse') {
        $('#nav_home, #navs_home').removeClass("active");
        $('#nav_new, #navs_new').removeClass("active");
        $('#nav_arrows').removeClass("ev-nav-hide");
        $('#nav_editforms, #navs_editforms').removeClass("active");
        $('#nav_dropdown').removeClass("active");
        $('#nav_archived, #navs_archived').removeClass("active");
        $('#nav_browse, #navs_browse').addClass("active");
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
    if (flag == 'tasks') {
        $('#nav_home, #navs_home').removeClass("active");
        $('#nav_new, #navs_new').removeClass("active");
        $('#nav_arrows').addClass("ev-nav-hide");
        $('#nav_editforms, #navs_editforms').removeClass("active");
        $('#nav_dropdown').removeClass("active");
        $('#nav_archived, #navs_archived').removeClass("active");
        $('#nav_browse, #navs_browse').removeClass("active");
        $('#nav_tasks, #navs_tasks').addClass("active");
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
     if (flag == 'mycal' || flag == 'gcal') {
        $('#nav_home, #navs_home').removeClass("active");
        $('#nav_new, #navs_new').removeClass("active");
        $('#nav_arrows').addClass("ev-nav-hide");
        $('#nav_editforms, #navs_editforms').removeClass("active");
        $('#nav_dropdown').removeClass("active");
        $('#nav_archived, #navs_archived').removeClass("active");
        $('#nav_browse, #navs_browse').removeClass("active");
        $('#nav_tasks, #navs_tasks').removeClass("active");
        $('#btn_calendar').addClass("lighten-4");
        $('#btn_calendar').removeClass("lighten-5");
        $('#nav_rates, #navs_rates').removeClass("active");
        $('#nav_payments_due, #navs_payments_due').removeClass("active");
        $('#nav_payments_received, #navs_payments_received').removeClass("active");
        $('#nav_syncgcal, #navs_syncgcal').removeClass("active");
        $('#nav_esigs, #navs_esigs').removeClass("active");
        $('#nav_calendar, #navs_calendar').addClass("active");
        $('#nav_reports, #navs_reports').removeClass("active");
        //add more menu items as necessary?
    }    
     if (flag == 'reports') {
        $('#nav_home, #navs_home').removeClass("active");
        $('#nav_new, #navs_new').removeClass("active");
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
        $('#nav_reports, #navs_reports').addClass("active");
        //add more menu items as necessary?
    }    
   
    //init tooltips
    $('.tooltipped').tooltip();  
    //init sidebar mobile menu
    $('.sidenav.sidenav-right').sidenav({edge:'right'});
    $('.sidenav.sidenav-left').sidenav({
        edge: 'left'
    });
    //init dropdown trigger
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
    //get last state of sidepanel collapsibles and restore it
//     var data = {
//         "dummy": "dummy",
//     };
//     $.ajax({
//         type: 'GET',
//         url: '/sidecalpanels',
//         data: data,
//         success: function(data) {
//             if (data['pnl1']) {
//                 $('.collapsible').collapsible('open',0);                
//             }
//             if (data['pnl2']) {
//                 $('.collapsible').collapsible('open',1);                
//             }
//             if (data['pnl3']) {
//                 $('.collapsible').collapsible('open',2);                
//             }
//             if (data['pnl4']) {
//                 $('.collapsible').collapsible('open',3);                
//             }
//             if (data['pnl5']) {
//                 $('.collapsible').collapsible('open',4);                
//             }
//         },
//         error: function(data) {
//             alert("Something Went Wrong, likely something with the side panels...");
//         }
//     });



    
//init the selectable tables for rate chart copying  
    $( ".select_table" ).selectable({
        filter: ".select_cell",
        distance: 10,  

        stop: function() {
//             var result = $( "#select-result" ).empty();
            var minhours = 5;
            var minensnum = 5;
            var maxhours = 0;
            var maxensnum = 0;
            var temphours = 0;
            var tempensnum = 0;
            var ratename = "";
            var tempid = 0;
            $( ".ui-selected", this ).each(function() {
//               var index = $( ".select_cell" ).index( this );
//                 var index = $(this).data('rate-start');
//                 result.append( " #" + ( index ) );
                ratename = $(this).data('name');
                temphours = $(this).data('hours');
                tempensnum = $(this).data('ensnum');
                tempid = $(this).data('id');
                if (temphours > maxhours) {
                    maxhours = temphours;
                }
                if (temphours < minhours) {
                    minhours = temphours;
                }
                if (tempensnum > maxensnum) {
                    maxensnum = tempensnum;
                }
                if (tempensnum < minensnum) {
                    minensnum = tempensnum;
                }
            });
            var mode = 2;
            if ($('#radio-hour-'+tempid).prop('checked')) {
                mode = 0;
            }
            if ($('#radio-type-'+tempid).prop('checked')) {
                mode = 1;
            }
            
            processRates(ratename, minhours, maxhours, minensnum, maxensnum, mode);
        }



    });



  
});


//**********************NEWEST*********************

$('input[type=radio]').change(function() {
    var this_id = this.id.substr(11);
//     alert(this_id);
    if ($('#radio-hour-'+this_id).prop('checked')) {
        for(let i = 0; i < 9; i++) {
            $('#label-type-'+this_id+'-col'+i).addClass('noshow');
            $('#label-hour-'+this_id+'-col'+i).removeClass('noshow');
            $('#label-both-'+this_id+'-col'+i).addClass('noshow'); 
        }       
    } else if ($('#radio-type-'+this_id).prop('checked')) {
        for(let i = 0; i < 9; i++) {
            $('#label-type-'+this_id+'-col'+i).removeClass('noshow');
            $('#label-hour-'+this_id+'-col'+i).addClass('noshow');
            $('#label-both-'+this_id+'-col'+i).addClass('noshow'); 
        }       
    } else {
        for(let i = 0; i < 9; i++) {
            $('#label-type-'+this_id+'-col'+i).addClass('noshow');
            $('#label-hour-'+this_id+'-col'+i).addClass('noshow');
            $('#label-both-'+this_id+'-col'+i).removeClass('noshow'); 
        }       
    }
});



$("#id_search").keypress(function(e) {
    if (e.which == '13') {
        if (!$('#id_search').val()) {
            e.preventDefault();
        }
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




//**************************************************
//**************************************************
//automatically make/capo info into correct correct chart when one is clicked
function processRates(chosen, minhours, maxhours, minensnum, maxensnum, mode) {
    var highlight = false;
    if (mode == 5) {
        mode = 2;
        highlight = true;
    }
    if (mode == 4) {
        mode = 1;
        highlight = true;
    }
    if (mode == 3) {
        mode = 0;
        highlight = true;
    }
    var nothing = true;
    if (highlight) {
        nothing = false;
        //add highlighting for appropriate row, column or full chart
        //use minhours, maxhours, minensnum, maxensnum
        //and use chosen (rate name) to select which to highlight  
        for(let i = minhours; i <= maxhours; i++) {
            for (let j = minensnum; j <= maxensnum; j++) {
//                 alert(i + ' ' + j);
                $('.select_cell[data-name="'+chosen+'"][data-hours='+i+'][data-ensnum='+j+']').addClass('ui-selected');
            }
        }
        
    }
    
    var data = {
        "rate_name": chosen,
        "minhours": minhours,
        "minensnum": minensnum,
        "maxhours": maxhours,
        "maxensnum": maxensnum,
        "mode": mode
    };
    
    
    
    var contracting;
    $.ajax({
        type: 'GET',
        url: '/rates/ajax/get_rate_chart',
        data: data,
        success: function(data) {
            var html = data['html'];
            var plain = data['plain'];
            //alert(html);
//             $("#finaltext").val(html);
//             var copyText = document.getElementById("finaltext");
//             copyText.select();
//             copyText.setSelectionRange(0,99999);
//             document.execCommand("copy");
            function listener(e) {
                e.clipboardData.setData("text/html", html);
                e.clipboardData.setData("text/plain", plain);
                e.preventDefault();
            }
            document.addEventListener("copy", listener);
            document.execCommand("copy");
            document.removeEventListener("copy", listener);
            
            alert("Chart copied!");
            
            //clear selection box on screen
            $( ".ui-selected").each(function() {
                $(this).removeClass('ui-selected');   
            });
            
            
            
        },
        error: function(data) {
            alert("Something Went Wrong, processRates charts failed");
        }
    });
}







$("#pnl1").on("click", function(e) {
    var data = {
        "panel": "1",
    };
    $.ajax({
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
    $.ajax({
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
    $.ajax({
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
    $.ajax({
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
    $.ajax({
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
    $.ajax({
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



$("#delete").on("click", function(e) {
    var link = this;

    e.preventDefault();

    $("<div>Are you sure you want to delete this event?</div>").dialog({
        buttons: {
            "Yes": function() {
                window.location = link.href;
            },
            "Cancel": function() {
                $(this).dialog("close");
            }
        }
    });
});





function do_activity_tooltips(i, obj) {
    //TODO needs updated to repeat search for EACH event on page!
    //set activity feed tooltip & innerhtml (for first activity)
    //alert($(this).attr("event_id", event_id));
    var data = {"event_id":"temp"};
    $.ajax({
        type : 'GET',
        url :  '/remind/ajax/get_5_activities',
        data : data,
        success : function(data){
            var fullhtml = "";
            var myhtml = "";
            var rdate;
            var friendlydate = "";
            var week = new Date();
            var today = new Date();
            today.setHours(0,0,0,0);
            week.setHours(0,0,0,0);
            week.setDate(week.getDate() + 6);
            var year, month, day;
            $.each(JSON.parse(data), function (index, object) {
                year = object.fields.date.substr(0,4);
                month = object.fields.date.substr(5,2);
                day = object.fields.date.substr(8,2);
                year = Number(year);
                month = Number(month) - 1;
                day = Number(day);
                rdate =  new Date(year, month, day);
                myhtml = '{{ activity.date }}: {{ activity.name }}<br />';
                month = month + 1;
                friendlydate = month + "\/" + day;
                myhtml = myhtml.replace('{{ activity.date }}', friendlydate);
                myhtml = myhtml.replace('{{ activity.name }}', object.fields.name);
                fullhtml = fullhtml + myhtml;
            });
            fullhtml = fullhtml + '.....';
            if (fullhtml == '.....') {fullhtml = "No Recent Activity <br />";}
            $(this).attr("data-tooltip", fullhtml);
            var ending = '';
            var index = fullhtml.indexOf("<br />");
            if (index > 30) {index = 30; ending = '...';}
            $(this).html(fullhtml.substring(0,index-1) + ending);
        },

        error: function(data) {
            alert('There was an error 6a!');
        }
    });
}    


function updateSidecal(year, month) {
    //alert('here' + year + month);
    var data = {
        "year": year,
        "month": month,
    };
    $.ajax({
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
function updateSidePanels() {
    //update sidepanels for both reminders and activities    
    var data = {
        "dummy": "dummy",
    };
    $.ajax({
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


function updateMycal(year, month) {
    //alert('here' + year + month);
    var data = {
        "year": year,
        "month": month,
    };
    $.ajax({
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


// $("#toggle_pastdue").on("click", function(e) {
//     $("#past_due").toggleClass('noshow');
//     if ($("#toggle_pastdue").html().includes('Show')) {
//         $("#toggle_pastdue").html($("#toggle_pastdue").html().replace('Show','Hide'));  
//     } else {
//         $("#toggle_pastdue").html($("#toggle_pastdue").html().replace('Hide','Show'));   
//     } 
// });
$("#include_pastdue_reminders").on("click", function(e) {
    $("#past_due_home").toggleClass('noshow'); 
    $("#include_pastdue_reminders").toggleClass('auto-pressed'); 
    $("#dummyfocus1").focus(); 
    $("#btn_calendar").focus();
    toggle_pastdue();     
});

$("#include_auto_reminders").click(function() {
    event.stopPropagation();
    $(".auto-reminder").toggleClass('noshow');
    $(".auto-reminder2").toggleClass('noshow');
    $(".auto-reminder3").toggleClass('noshow');
    $("#include_auto_reminders").toggleClass('auto-pressed'); 
    $("#dummyfocus1").focus();
    $("#btn_calendar").focus(); 
    toggle_auto();     
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
    $.ajax({
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
function toggle_auto() {
    var data = {"dummy": false,};
    $.ajax({
        type: 'GET',
        url: '/toggle_auto',
        data: data,
        success: function(data) {
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with toggling show auto...");
        }
    });
}

$("#toggle_home_todo").click(function() {
    var data = {"dummy": 'todo',};
    $.ajax({
        type: 'GET',
        url: '/toggle_home_panels',
        data: data,
        success: function(data) {
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with toggling home todo...");
        }
    });
});
$("#toggle_home_booking").click(function() {
    var data = {"dummy": 'booking',};
    $.ajax({
        type: 'GET',
        url: '/toggle_home_panels',
        data: data,
        success: function(data) {
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with toggling home todo...");
        }
    });
});

$("#toggle_home_payment").click(function() {
    //alert('toggle');
    var data = {"dummy": 'payment',};
    $.ajax({
        type: 'GET',
        url: '/toggle_home_panels',
        data: data,
        success: function(data) {
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with toggling home payment...");
        }
    });
});
$("#toggle_home_history").click(function() {
    var data = {"dummy": 'history',};
    $.ajax({
        type: 'GET',
        url: '/toggle_home_panels',
        data: data,
        success: function(data) {
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with toggling home history...");
        }
    });
});





function toggle_pastdue() {
    var data = {"dummy": false,};
    $.ajax({
        type: 'GET',
        url: '/toggle_show_pd',
        data: data,
        success: function(data) {
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with toggling show past-due...");
        }
    });
}


$("#search_form").on('focusin', function() {
    $('#search_lbl').removeClass("ev_search_lbl");
});
$("#search_form").on('focusout', function() {
    $('#search_lbl').addClass("ev_search_lbl");
});


$(".ratechange").on('change', function() {
    //calculate new contracting amounts whenever a # is changed!
    var num_1s = Number($('#id_solo').val());
    var num_1d = Number($('#id_duo').val());
    var num_1t = Number($('#id_trio').val());
    var num_1q = Number($('#id_quartet').val());
    var mus_1 = Number($('#id_musician').val());
    
    var num_2s = Number($('#id_two_solo').val());
    var num_2d = Number($('#id_two_duo').val());
    var num_2t = Number($('#id_two_trio').val());
    var num_2q = Number($('#id_two_quartet').val());
    var mus_2 = Number($('#id_two_musician').val());

    var num_3s = Number($('#id_three_solo').val());
    var num_3d = Number($('#id_three_duo').val());
    var num_3t = Number($('#id_three_trio').val());
    var num_3q = Number($('#id_three_quartet').val());
    var mus_3 = Number($('#id_three_musician').val());

    var num_4s = Number($('#id_four_solo').val());
    var num_4d = Number($('#id_four_duo').val());
    var num_4t = Number($('#id_four_trio').val());
    var num_4q = Number($('#id_four_quartet').val());
    var mus_4 = Number($('#id_four_musician').val());

    if ((num_1s != 'NaN') && (mus_1 != 'NaN')) {
        $('#id_cont_1s').val(String((num_1s - mus_1).toFixed(2)));
    }
    if ((num_1d != 'NaN') && (mus_1 != 'NaN')) {
        $('#id_cont_1d').val(String((num_1d - (mus_1 * 2)).toFixed(2)));
    }
    if ((num_1t != 'NaN') && (mus_1 != 'NaN')) {
        $('#id_cont_1t').val(String((num_1t - (mus_1 * 3)).toFixed(2)));
    }
    if ((num_1s != 'NaN') && (mus_1 != 'NaN')) {
        $('#id_cont_1q').val(String((num_1q - (mus_1 * 4)).toFixed(2)));
    }

    if ((num_2s != 'NaN') && (mus_2 != 'NaN')) {
        $('#id_cont_2s').val(String((num_2s - mus_2).toFixed(2)));
    }
    if ((num_2d != 'NaN') && (mus_2 != 'NaN')) {
        $('#id_cont_2d').val(String((num_2d - (mus_2 * 2)).toFixed(2)));
    }
    if ((num_2t != 'NaN') && (mus_2 != 'NaN')) {
        $('#id_cont_2t').val(String((num_2t - (mus_2 * 3)).toFixed(2)));
    }
    if ((num_2s != 'NaN') && (mus_2 != 'NaN')) {
        $('#id_cont_2q').val(String((num_2q - (mus_2 * 4)).toFixed(2)));
    }
    
    if ((num_3s != 'NaN') && (mus_3 != 'NaN')) {
        $('#id_cont_3s').val(String((num_3s - mus_3).toFixed(2)));
    }
    if ((num_3d != 'NaN') && (mus_3 != 'NaN')) {
        $('#id_cont_3d').val(String((num_3d - (mus_3 * 2)).toFixed(2)));
    }
    if ((num_3t != 'NaN') && (mus_3 != 'NaN')) {
        $('#id_cont_3t').val(String((num_3t - (mus_3 * 3)).toFixed(2)));
    }
    if ((num_3s != 'NaN') && (mus_3 != 'NaN')) {
        $('#id_cont_3q').val(String((num_3q - (mus_3 * 4)).toFixed(2)));
    }

    if ((num_4s != 'NaN') && (mus_4 != 'NaN')) {
        $('#id_cont_4s').val(String((num_4s - mus_4).toFixed(2)));
    }
    if ((num_4d != 'NaN') && (mus_4 != 'NaN')) {
        $('#id_cont_4d').val(String((num_4d - (mus_4 * 2)).toFixed(2)));
    }
    if ((num_4t != 'NaN') && (mus_4 != 'NaN')) {
        $('#id_cont_4t').val(String((num_4t - (mus_4 * 3)).toFixed(2)));
    }
    if ((num_4s != 'NaN') && (mus_4 != 'NaN')) {
        $('#id_cont_4q').val(String((num_4q - (mus_4 * 4)).toFixed(2)));
    }

});


$(".btn-del").click(function() {
    if (window.confirm("Are you sure you want to delete this rate chart?")) {
        //delete here via ajax
         var chart_id = $(this).attr("chart_id"); 
         var data = {"chart_id": chart_id};
         $.ajax({
             type: 'GET',
             url: '/ratechartdelete',
             data: data,
             success: function(data) {
             },
             error: function(data) {
                 alert("Something Went Wrong, likely something with deleting rate chart...");
             }
         });
        //refresh page
        location.reload(true);
    } else {
        var nothing = 1;
    }
});

$(".btn-delsig").click(function() {
    if (window.confirm("Are you sure you want to delete this signature?")) {
        //delete here via ajax
         var chart_id = $(this).attr("chart_id"); 
         var data = {"chart_id": chart_id};
         $.ajax({
             type: 'GET',
             url: '/esigdelete',
             data: data,
             success: function(data) {
             },
             error: function(data) {
                 alert("Something Went Wrong, likely something with deleting signature...");
             }
         });
        //refresh page
        location.reload(true);
    } else {
        var nothing = 1;
    }
});


$(".paid_check").click(function() {
     var pay_id = $(this).attr("pay_id"); 
     var data = {"pay_id": pay_id};
     $.ajax({
         type: 'GET',
         url: '/markpayduedone',
         data: data,
         success: function(data) {
         },
         error: function(data) {
             alert("Something Went Wrong, likely something with marking payment done...");
         }
     });
    //refresh page
    location.reload(true);
});

// $("#id_sig").change(function() {
//     var text = $("#id_sig").val();
//     $("#sig_preview").html(text);    
// });

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
    $.ajax({
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

$('#reports_details1').click(function() {
    $(".reports_details1_toggle").toggleClass("noshow");
    $("#dummyfocus1").focus();
    $("#btn_calendar").focus();
});

$('#reports_details2').click(function() {
    $(".reports_details2_toggle").toggleClass("noshow");
    $("#dummyfocus1").focus();
    $("#btn_calendar").focus();
});
$('#reports_details3').click(function() {
    $(".reports_details3_toggle").toggleClass("noshow");
    $("#dummyfocus1").focus();
    $("#btn_calendar").focus();
});

$('#reports_details4').click(function() {
    $(".reports_details4_toggle").toggleClass("noshow");
    $("#dummyfocus1").focus();
    $("#btn_calendar").focus();
});
$('#reports_details5').click(function() {
    $(".reports_details5_toggle").toggleClass("noshow");
    $("#dummyfocus1").focus();
    $("#btn_calendar").focus();
});

$('#reports_details6').click(function() {
    $(".reports_details6_toggle").toggleClass("noshow");
    $("#dummyfocus1").focus();
    $("#btn_calendar").focus();
});
$('#reports_details7').click(function() {
    $(".reports_details7_toggle").toggleClass("noshow");
    $("#dummyfocus1").focus();
    $("#btn_calendar").focus();
});

$('#reports_details8').click(function() {
    $(".reports_details8_toggle").toggleClass("noshow");
    $("#dummyfocus1").focus();
    $("#btn_calendar").focus();
});

$('#reports_musicians').click(function() {
    $(".reports_musicians_toggle").toggleClass("noshow");
    $("#dummyfocus1").focus();
    $("#btn_calendar").focus();
});


$("#submitbtn_transition").click(function(e) {
    if ($('#id_signature_date').val() == "") {
        $('#id_signature_date').val('1/1/11');
    }
    if ($('#id_paid_deposit_date').val() == "") {
        $('#id_paid_deposit_date').val('1/1/11');
    }
    if ($('#id_paid_final_date').val() == "") {
        $('#id_paid_final_date').val('1/1/11');
    }
    if ($('#id_paid_total_date').val() == "") {
        $('#id_paid_total_date').val('1/1/11');
    }
    if ($('#id_paid_extra_date').val() == "") {
        $('#id_paid_extra_date').val('1/1/11');
    }
    if ($('#id_music_list_date').val() == "") {
        $('#id_music_list_date').val('1/1/11');
    }
    if ($('#id_verify_info_date').val() == "") {
        $('#id_verify_info_date').val('1/1/11');
    }
});


