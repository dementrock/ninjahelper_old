$(function(){
    Function.prototype.defaults = function(){
        var _f = this;
        var _a = Array(_f.length-arguments.length).concat(Array.prototype.slice.apply(arguments));
        return function(){
            return _f.apply(_f, Array.prototype.slice.apply(arguments).concat(_a.slice(arguments.length, _a.length)));
        }
    }
    submit_form = function() {
        var form_submitted = false;
        return function(args) {
            if ('submit_url' in args) {
                var submit_url = args['submit_url'];    
            } else {
                alert('Need to specify submit url!');
            }
            var processing_msg = 'processing_msg' in args ? args['processing_msg'] : 'Processing...';
            var form_id = 'form_id' in args ? args['form_id'] : '#form';
            var note_id = 'note_id' in args ? args['note_id'] : '#note';
            var error_action = 'error_action' in args ? args['error_action'] : function(){};
            var success_action = 'success_action' in args ? args['success_action'] : function(){};
            return function(){
                if (form_submitted) {
                    return false;
                }
                form_submitted = true;
                $(note_id).html("<img id='processing' src='/media/processing.gif' />" + processing_msg);
                $.post(submit_url, $(form_id).serialize(), function(data){
                    if (data.status == 'error') {
                        $(note_id).html(data.message);
                        form_submitted = false;
                        error_action();
                    } else {
                        $(note_id).html(data.message);
                        form_submitted = false;
                        success_action();
                    }
                }, 'json');
                return false;
            }
        }
    }();
});
