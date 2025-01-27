

paypal.Buttons({
  createOrder: function(data, actions) {
    // This function sets up the details of the transaction, including the amount and line item details.
    var amount_to_pay = $("#amount_to_pay").val();
    var my_custom_id = $('#payment_type').val() + '#' + $('#event_id').val();
    var my_custom_name = $('#eventname').val() + ' - ' + $('#eventtype').val() + ' - ' + $('#eventdate').val();
    var my_custom_description = $('#payment_type').val() + ' payment';
    var my_custom_sku = 'id#' + $('#event_id').val();
    var amount_base = $("#thisfeebase").val();
    var amount_fee = $("#thisfeefee").val();
    return actions.order.create({
      purchase_units: [{
        custom_id: my_custom_id,
        items: [{
            name: my_custom_name,
            description: my_custom_description,
            sku: my_custom_sku,
            unit_amount: {
                currency_code: "USD",
                value: amount_base
                },
            quantity: "1"
        }],
        amount: {
          value: amount_to_pay,
          breakdown: {
              item_total: {
                  currency_code: "USD",
                  value: amount_base
              },
              shipping: {
                  currency_code: "USD",
                  value: "0"
              },
              handling: {
                  currency_code: "USD",
                  value: amount_fee
              }
          }
        }
      }]
    });
  },
  onApprove: function(data, actions) {
    // This function captures the funds from the transaction.
    return actions.order.capture().then(function(details) {
      // This function shows a transaction success message to your buyer.
      //alert('Transaction completed by ' + details.payer.name.given_name);
      process_done(details);  
    });
  },
  onCancel: function(data) {
    // Show a cancel page, or return to cart
    process_not_done();
  },
  onError: function(err) {
    // Show an error page here, when an error occurs
    process_not_done();
  }
}).render('#paypal-button-container');
//This function displays Smart Payment Buttons on your web page.



function process_done(details) {
    var data = {
        "name": details.payer.name.given_name,
        "amount": details.purchase_units[0].payments.captures[0].amount.value,
        "event": $("#event_id").val(),
        "type": $("#payment_type").val(),
        "client": $("#client").val(),
        "mode": $("#mode").val(),
        "id": details.purchase_units[0].payments.captures[0].id
    };
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/events/savepaypalid',
        data: data,
        success: function(data) {
            //nothing
        },
        error: function(date) {
            alert("Hmmm... something didn't process as expected in our new system, excuse our construction debris and dust!\nYour payment is safe and completed, all taken care of.  But if you get a chance, let us know about this cautionary message!");
        }
    });   
    
    
    var old = $("#paypal-page-container").html();
    var wait = '<div class="progress"><div class="indeterminate"></div></div>';
    $("#paypal-page-container").html(wait);
    $("#goto_home2").addClass("client-noshow");
    $.ajaxq("MyQueue", {
        type: 'GET',
        url: '/updatepaypal',
        data: data,
        success: function(data) {
            $("#paypal-page-container").html(data['newhttp']);
            $("#goto_home2").removeClass("client-noshow");
//             $("#goto_home2").removeClass("ev-col4");
//             $("#goto_home2").addClass("ccol4");
//             $("#goto_home2").addClass("cbtn-orange");
        },
        error: function(data) {
            alert("Hmmm... something didn't process as expected in our new system, excuse our construction debris and dust!\nYour payment is safe and completed, all taken care of.  But if you get a chance, let us know about this cautionary message!");
            $("paypal-page-container").html(data['newhttp']);
            $("goto_home2").removeClass("client-noshow");
//             $("#goto_home2").removeClass("ev-col4");
//             $("#goto_home2").addClass("ccol4");
//             $("#goto_home2").addClass("cbtn-orange");
        }
    });
    
}

function process_not_done() {
    alert("Paypal reported an error,\n or the process did not complete.\n\nPlease try again!");
//     $("#goto_home2").removeClass("ev-col4");
//     $("#goto_home2").addClass("ccol4");
//     $("#goto_home2").addClass("cbtn-orange");
}


