$(function(){
    $("#form").submit(submit_form({'submit_url': url_add_monitor_course, 'success_action': function(){location.reload()}}));
});
