$(function(){
    $("#form").submit(function(){
        shortname = $("#form :input[name=shortname]").val();
        url = $("#form :input[name=url]").val();
        if (shortname == "" || url == "") {
            $("#note").html("Must provide both shortname and url.");
        }
        processing("Processing...");
        $.post(url_add_shortlink, $("#form").serialize(), function(data) {
            alert(data.status);
            if (data.status == 'error') {
                $("#note").html(data.message);
            } else {
                $("#note").html("Shortlink is successfully added.")
                window.location.replace(url_next);
            }
        }, 'json');
        return false;
    });
    function processing(msg) {
        $("#note").html("<img id='processing' src='/media/processing.gif' />" + msg);
    }

});


