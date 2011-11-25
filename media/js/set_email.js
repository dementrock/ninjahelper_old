$(function(){
    $("#emailform").submit(submit_form({
        'submit_url': url_set_email,
        'form_id': '#emailform'
    }));
    $("#codeform").submit(submit_form({
        'submit_url': url_set_email,
        'form_id': '#codeform',
        'success_action': function(){
            window.location.replace('/');
        }
    }));
});
