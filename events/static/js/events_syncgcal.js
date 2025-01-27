$(document).ready(function() {
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
    $(".dropdown-trigger").dropdown({alignment:'right',constrainWidth:false,coverTrigger:false,});
    //init sidebar collapsibles
    $('.collapsible').collapsible({
        accordion: false,
    });
    
    $('#nav_new, #navs_new').removeClass("active");
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
    $('#nav_syncgcal, #navs_syncgcal').addClass("active");
    $('#nav_esigs, #navs_esigs').removeClass("active");
    $('#nav_calendar, #navs_calendar').removeClass("active");
    $('#nav_reports, #navs_reports').removeClass("active");
    
    
   
    
    
    
    
});

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




//do the re-sync gcal stuff
$("#btn_syncgcal").click(function() {
    $('#btn_syncgcal').addClass('noshow');
    $('#wait1_syncgcal').removeClass('noshow');
    var data = {
        "dummy": "dummy"
    };
    $.ajax({
        type: 'GET',
        url: '/syncgcal_deleteold',
        data: data,
        success: function(data) {
            var newinfo = "Deleted " + data['count'] + " events...";
            $('#wait1_syncgcal').addClass('noshow');
            $('#info_syncgcal').html(newinfo);
            $('#info_syncgcal').removeClass('noshow');
            $('#wait2_syncgcal').removeClass('noshow');
            syncgcal_savenew();       
        },
        error: function(data) {
            alert("Something Went Wrong, likely with gcal sync delete");
        }
    });
});
function syncgcal_savenew()
{
    var data = {
        "dummy": "dummy"
    };
    $.ajax({
        type: 'GET',
        url: '/syncgcal_savenew',
        data: data,
        success: function(data) {
            var newinfo = "Re-saved " + data['count'] + " events...";
            $('#wait2_syncgcal').addClass('noshow');
            $('#saveinfo_syncgcal').html(newinfo);
            $('#saveinfo_syncgcal').removeClass('noshow');
            $('#done_syncgcal').removeClass('noshow');
        },
        error: function(data) {
            alert("Something Went Wrong, likely with gcal sync savenew");
        }
    });
}


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
        },
        error: function(data) {
            alert("Something Went Wrong, likely something with udpating sidepanel...");
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


$("#search_form").on('focusin', function() {
    $('#search_lbl').removeClass("ev_search_lbl");
});
$("#search_form").on('focusout', function() {
    $('#search_lbl').addClass("ev_search_lbl");
});
