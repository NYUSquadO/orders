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

        var cust_id =  $("#cust_id").val() + "";

        var data = {
            "cust_id": cust_id,
            "order_items":[]
        };

        var item_id = $("#item_id").val() + "";
        var item_name = $("#item_name").val() + "";
        var item_qty = $("#item_qty").val() + "";
        var item_price = $("#item_price").val() + "";

        var item = {};
        item["item_id"] = item_id;
        item["item_name"] = item_name;
        item["item_qty"] = item_qty;
        item["item_price"] = item_price;
        data["order_items"].push(item);


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
    
    // ****************************************
    // Retrieve an Order
    // ****************************************

    $("#retrieve-btn").click(function () {

        var order_id = $("#order_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/orders/" + order_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message(`Success. Order:${order_id} retrieved.`)
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });


    // Delete an Order
    $("#delete-btn").click(function () {

        var order_id = $("#order_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/orders/" + order_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Order has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("No orders found!")
        });
    });

     // Cancel an Order
    $("#cancel-btn").click(function () {

        var order_id = $("#order_id").val().trim();

        if (order_id == "" || order_id == "undefined")
        {
            flash_message("Please enter order id")
            return
        }

        var ajax = $.ajax({
            type: "PUT",
            url: "/orders/" + order_id + "/cancel",
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Order has been Cancelled!")
        });

        ajax.fail(function(res){
            flash_message("No orders found!")
        });
    });


    // ****************************************
    // Clear the form
    // ****************************************
    $("#clear-btn").click(function () {
        $("#order_id").val("");
        clear_form_data()
    });

})
