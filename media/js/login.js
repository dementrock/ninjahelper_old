$(function(){
    $("form").submit(submit_form({
        'submit_url': url_login,
        'success_action': function(){
            window.location.replace(url_next);
        },
        'processing_msg': 'Logging in...',
    }));
});


