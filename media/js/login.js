$(function(){
    $("#login-form").submit(function(){
        username = $("#login-form :input[name=username]").val();
        password = $("#login-form :input[name=password]").val();
        if (username == "" || password == "") {
            $("#note").html("Must provide both username and password.");
        }
        $.post(url_login, $("#login-form").serialize(), function(data) {
            if (data.status == 'error') {
                $("#note").html(data.message);
            } else {
                $("#note").html("Log in success. Redirecting...")
                location.reload();
            }
        }, 'json');
        return false;
    });
});

