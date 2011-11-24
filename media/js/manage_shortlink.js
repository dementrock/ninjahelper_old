$(function(){
    $("#form").submit(submit_form({'submit_url': url_add_shortlink, 'success_action': function(){location.reload()}}));
});
