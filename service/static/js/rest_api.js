$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#order_id").val(res.id);
        $("#cust_id").val(res.cust_id);
        $("#status").val(res.status);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#order_id").val("");
        $("#cust_id").val("");
        $("#status").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }


    // ****************************************
    // Create an order
    // ****************************************

    $("#create-btn").click(function () {

        var cust_id =  $("#cust_id").val();
        var status = $("#status").val();
        var item_id = $("#item_id").val();
        var item_name = $("#item_name").val()
        var item_qty = $("#item_qty").val()
        var item_price = $("#item_price").val()


        var data = {
            "cust_id": cust_id,
            "status": status,
            order_items: [
                {
                    "item_id": item_id,
                    "item_name": item_name,
                    "item_qty": item_qty,
                    "item_price": item_price
                }
            ]
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/orders",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

})
