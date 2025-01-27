
$(document).ready(function(){

    //update nav bar according to page_flag value    
    var flag = $('#page_flag').val();
//     if (flag == 'home') {
//         $('#nav_home').addClass("active");
//         $('#nav_new').removeClass("active");
//         $('#nav_arrows').addClass("ev-nav-hide");
//         $('#nav_arrows_small_bar').addClass("hide");
//         $('#nav_editforms').removeClass("active");
//         //add more menu items as necessary?
//     }    
//     if (flag == 'new') {
//         $('#nav_new').addClass("active");
//         $('#nav_home').removeClass("active");
//         $('#nav_arrows').addClass("ev-nav-hide");
//         $('#nav_arrows_small_bar').addClass("hide");
//         $('#nav_editforms').removeClass("active"); 
//         //add more menu items as necessary?
//     }
    if (flag == 'email') {
        $('#nav_arrows').addClass("ev-nav-hide");
        $('#nav_arrows_small_bar').addClass("hide");
        $('#nav_editforms, #navs_editforms').addClass("active");
        $('#nav_home, #navs_home').removeClass("active");
        $('#nav_new, #navs_new').removeClass("active");
        $('#nav_dropdown').addClass("active");
    }
    //prevent user from leaving changed form
    $('form').areYouSure( {'message':'These event details are not saved!'} );
    //init floating action bar
    //$('.sidenav').sidenav({edge:'right'});
    //init tooltips
    $('.tooltipped').tooltip();  
    //init sidebar collapsibles
    $('.collapsible').collapsible({
        accordion: false,
    });
    //init dropdown
    $(".dropdown-trigger").dropdown({alignment:'bottom',});
//     var body = $('#this_body').val();
//     $("id_body").val(body);

    
//     window.onbeforeunload = function() {
//         var test = $("#formname").val();
//         popupwasclosed(test);
//         //return "onbeforeunload";
//         return null;
//     };   



});


//will call ajax routine to undo everything done before
//window was opened..
// function popupwasclosed(test) {
//     console.log(test);
//     opener.popupclosed();    
// }


$("#submitbtn").click( function() {
   //var test = $("#formname").val(); 
   opener.popupclosed();
});

$('#showkey').click( function() {
    $('#key').toggleClass('noshow');
});

$('#sigs').click( function() {
//     var contents = $('#id_body').val();
//     var contentssplit = contents.split("<!-- sigstart -->", 2);
//     var contentsnosig = contentssplit[0];
// 
//     var newsig = "--Jni";
//     var newcontents = contentsnosig + newsig;

    //open a div that shows all sigs, allowing clicking
    //on one of them to choose.
    //in second js routine, capture click and sub signature out
    //email & emailpdf routines get sig data,
    //email.html & email_pdf.html render it hidden

    $('#sig_panel').toggleClass("noshow");

});

$('.click_sig').click( function() {
    var contents = $('#id_body').val();
    var contentssplit = contents.split("<!-- sigstart -->", 2);
    var contentsnosig = contentssplit[0];
    var thishtml = $(this).attr("sig_html");
    //alert(thishtml);
    var newsig = thishtml;
    var newcontents = contentsnosig + newsig;
    tinyMCE.get('id_body').setContent(newcontents);
    
});





