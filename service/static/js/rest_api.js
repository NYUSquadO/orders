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

})
