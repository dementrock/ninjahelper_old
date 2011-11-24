$(function(){
    var form_submitted = false;
    $("#form").submit(function(){
        if (form_submitted) {
            return false;
        }
        form_submitted = true;
        shortname = $("#form :input[name=shortname]").val();
        url = $("#form :input[name=url]").val();
        processing("Processing...");
        $.post(url_edit_shortlink, $("#form").serialize(), function(data) {
            if (data.status == 'error') {
                $("#note").html(data.message);
                form_submitted = false;
            } else {
                $("#note").html(data.message);
                form_submitted = false;
            }
        }, 'json');
        return false;
    });
    function processing(msg) {
        $("#note").html("<img id='processing' src='/media/processing.gif' />" + msg);
    }

});


