$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#order_id").val(res.id);
        $("#cust_id").val(res.cust_id);
        $("#status").val(res.status);
        $("#item_id").val(res.order_items[0].item_id);
        $("#item_name").val(res.order_items[0].item_name);
        $("#item_qty").val(res.order_items[0].item_qty);
        $("#item_price").val(res.order_items[0].item_price);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#order_id").val("");
        $("#cust_id").val("");
        $("#status").val("");
        $("#item_id").val("");
        $("#item_name").val("");
        $("#item_qty").val("");
        $("#item_price").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Retrieve an Order
    // ****************************************

    $("#retrieve-btn").click(function () {

        var order_id = $("#order_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/api/orders/" + order_id,
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
        
        if (!cust_id){
            flash_message(`Cust_id is required for creating an order.`);
        } else if (!item_id){
            flash_message(`Item_id is required for creating an order.`);
        } else if (!item_name){
            flash_message(`Item_name is required for creating an order.`);
        } else if (!item_qty){
            flash_message(`Item_qty is required for creating an order.`);
        } else if (!item_price){
            flash_message(`Item_price is required for creating an order.`);
        } else {
            var item = {};
            item["item_id"] = item_id;
            item["item_name"] = item_name;
            item["item_qty"] = item_qty;
            item["item_price"] = item_price;
            data["order_items"].push(item);

            var ajax = $.ajax({
                type: "POST",
                url: "/api/orders",
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

        }
        
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
            url: "api/orders/" + order_id + "/cancel", data: '',
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
    // Query an Order by cust_id
    // ****************************************
    $("#search-btn").click(function () {

        var cust_id = $("#cust_id").val();
        
        var ajax = $.ajax({
            type: "GET",
            url: "/api/orders?cust_id=" + cust_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">order_id</th>'
            header += '<th style="width:10%">cust_id</th>'
            header += '<th style="width:20%">status</th>'
            header += '<th style="width:10%">item_id</th>'
            header += '<th style="width:20%">item_name</th>'
            header += '<th style="width:20%">item_qty</th>'
            header += '<th style="width:20%">item_price</th></tr>'
            $("#search_results").append(header);
            var firstOrder = "";
            for(var i = 0; i < res.length; i++) {
                var order = res[i];
                first_order_items = order.order_items[0]
                var row = "<tr><td>"+order.id+"</td><td>"+order.cust_id+"</td><td>"+order.status+"</td><td>"+first_order_items.item_id+"</td><td>"+first_order_items.item_name+"</td><td>"+first_order_items.item_qty+"</td><td>"+first_order_items.item_price+"</td><tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstOrder = order;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstOrder != "") {
                update_form_data(firstOrder)
            }

            flash_message(`Success. Query returns ${res.length} order(s).`)
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });


    // ****************************************
    // Query an Order by item_id
    // ****************************************
    $("#search-item-btn").click(function () {

        var item_id = $("#item_id").val();
        
        var ajax = $.ajax({
            type: "GET",
            url: "/api/orders?item_id=" + item_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">order_id</th>'
            header += '<th style="width:10%">cust_id</th>'
            header += '<th style="width:20%">status</th>'
            header += '<th style="width:10%">item_id</th>'
            header += '<th style="width:20%">item_name</th>'
            header += '<th style="width:20%">item_qty</th>'
            header += '<th style="width:20%">item_price</th></tr>'
            $("#search_results").append(header);
            var firstOrder = "";
            for(var i = 0; i < res.length; i++) {
                var order = res[i];
                first_order_items = order.order_items[0]
                var row = "<tr><td>"+order.id+"</td><td>"+order.cust_id+"</td><td>"+order.status+"</td><td>"+first_order_items.item_id+"</td><td>"+first_order_items.item_name+"</td><td>"+first_order_items.item_qty+"</td><td>"+first_order_items.item_price+"</td><tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstOrder = order;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstOrder != "") {
                update_form_data(firstOrder)
            }

            flash_message(`Success. Query returns ${res.length} order(s).`)
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete an Order
    // ****************************************
    $("#delete-btn").click(function () {

        var order_id = $("#order_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/api/orders/" + order_id,
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


    const listOrders = (res) => {
        $("#search_results").empty();
        $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">order_id</th>'
            header += '<th style="width:10%">cust_id</th>'
            header += '<th style="width:20%">status</th></tr>'
            $("#search_results").append(header);
            for(var i = 0; i < res.length; i++) {
                var order = res[i];
                var row = "<tr><td>"+order.id+"</td><td>"+order.cust_id+"</td><td>"+order.status+"</td><tr>";
                $("#search_results").append(row);
            }
            $("#search_results").append('</table>');
    };


    // ****************************************
    // List all orders
    // ****************************************
    $("#list-btn").click(function () {
        
        const ajax = $.ajax({
            type: "GET",
            url: "/api/orders",
            contentType: "application/json",
            data: "",
        });

        ajax.done((res) => {
            listOrders(res);
            flash_message(`Success. List returns ${res.length} order(s).`);
        });

    });


    const listItems = (res) => {
        $("#search_results").empty();
        $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">item_id</th>'
            header += '<th style="width:20%">item_name</th>'
            header += '<th style="width:20%">item_qty</th>'
            header += '<th style="width:20%">item_price</th></tr>'
            $("#search_results").append(header);
            for(var i = 0; i < res.length; i++) {
                var item = res[i];
                var row = "<tr><td>"+item.item_id+"</td><td>"+item.item_name+"</td><td>"+item.item_qty+"</td><td>"+item.item_price+"</td><tr>";
                $("#search_results").append(row);
            }
            $("#search_results").append('</table>');
    };

    
    // ****************************************
    // List all items in the order
    // ****************************************
    $("#list-item-btn").click(function () {
        
        var order_id = $("#order_id").val();
        
        if (order_id) {
            const ajax = $.ajax({
                type: "GET",
                url: "/api/orders/" + order_id + '/items',
                contentType: "application/json",
                data: "",
            });
    
            ajax.done((res) => {
                listItems(res);
                flash_message(`Success. List returns ${res.length} item(s).`);
            });

            ajax.fail(function(res){
                flash_message(`Order was not found for order_id = ${order_id}.`)
            });
        }
        else {
            flash_message(`Order_id is required to list the items in it`);
        }

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
        
    });


    // ****************************************
    // Clear the form
    // ****************************************
    $("#clear-btn").click(function () {
        $("#order_id").val("");
        flash_message()
        clear_form_data()
        $("#search_results").empty();
    });


    // ****************************************
    // Update Order
    // ****************************************

    $("#update-btn").click(function () {

        var order_id = $("#order_id").val();
        var cust_id = $("#cust_id").val();
        var item_id = $("#item_id").val();
        var item_name = $("#item_name").val();
        var item_qty = $("#item_qty").val();
        var item_price = $("#item_price").val();
        

        
        var data = {
            "cust_id": cust_id,
            "order_items" : [{
                "item_id" : item_id,
                "item_name" : item_name,
                "item_qty" : item_qty,
                "item_price" : item_price
            }]
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/api/orders/" + order_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });
})
