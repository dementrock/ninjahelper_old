$(function(){
    $("#cellform").submit(submit_form({'submit_url': url_set_phone, 'form_id': '#cellform', }));
    $("#codeform").submit(submit_form({'submit_url': url_set_phone, 'form_id': '#codeform', }));
});
