$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#customer_id").val(res.id);
        $("#name").val(res.name);
        $("#user_name").val(res.user_name);
        $("#password").val(res.password);
        if (res.locked == true) {
            $("#customer_available").val("true");
        } else {
            $("#customer_available").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#name").val("");
        $("#user_name").val("");
        $("#password").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Customer & PUSH 
    // ****************************************

    $("#create-btn").click(function () {

        var name = $("#name").val();
        var user_name = $("#user_name").val();
        var password = $("#password").val();
        var locked = $("#customer_available").val() == "true";

        //create json file same way as postman
        var data = {
            "name": name,
            "user_name": user_name,
            "password": password, 
            "locked": locked
        };
        //same as the tests in postman
        var ajax = $.ajax({
            type: "POST",
            url: "/customers",
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
    // Update a Customer & PUT
    // ****************************************

    $("#update-btn").click(function () {

        var customer_id = $("#customer_id").val();
        var name = $("#name").val();
        var user_name = $("#user_name").val();
        var password = $("#password").val();
        var locked = $("#customer_available").val() == "true";

        var data = {
            "name": name,
            "user_name": user_name,
            "password": password,
            "locked": locked
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/customers/" + customer_id,
                contentType: "application/json",
                data: JSON.stringify(data),
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Customer
    // ****************************************

    $("#retrieve-btn").click(function () {

        var customer_id = $("#customer_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/customers/" + customer_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Customer
    // ****************************************

    $("#delete-btn").click(function () {

        var customer_id = $("#customer_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/customers/" + customer_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Customer has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#customer_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a Customer
    // ****************************************

    $("#search-btn").click(function () {

        var name = $("#name").val();
        var user_name = $("#user_name").val();
        var locked = $("#customer_available").val() == "true";

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (user_name) {
            if (queryString.length > 0) {
                queryString += '&user_name=' + user_name
            } else {
                queryString += 'user_name=' + user_name
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/customers?" + queryString,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">User Name</th>'
            header += '<th style="width:10%">Locked</th></tr>'
            $("#search_results").append(header);
            var firstCustomer = "";
            for(var i = 0; i < res.length; i++) {
                var customer = res[i];
                var row = "<tr><td>"+customer.id+"</td><td>"+customer.name+"</td><td>"+customer.user_name+"</td><td>"+customer.locked+"</td><td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstCustomer = customer;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstCustomer != "") {
                update_form_data(firstCustomer)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
