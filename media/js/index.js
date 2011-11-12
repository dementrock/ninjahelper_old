$(function(){
    $("#import-form").submit(function(){
        fetch_data();  
        return false;
    });
});

function fetch_data(){
    //alert(url_import_form);
    $.post(url_import_form, $('#import-form').serialize(), function(data){
        output_str = '<h3>According to your friend list, </h3><ul>';
        for (var i = 0; i < data.length; ++i) {
            output_str += '<li>You will attend ' + data[i][0] + ' with ';
            if (!data[i][1].length) {
                output_str += 'none of your friends.</li>'; 
            } else {
                for (var j = 0; j < data[i][1].length; ++j) {
                    if (j == data[i][1].length - 1 && data[i][1].length > 1) {
                        if (data[i][1].length > 2) {
                            output_str += 'and ';
                        } else {
                            output_str += ' and ';
                        }
                    }
                    output_str += '<a href="http://ninjacourses.com' + data[i][1][j][1] + '">' + data[i][1][j][0] + '</a>';
                    if (j < data[i][1].length - 1){
                        if (data[i][1].length > 2) {
                            output_str += ', ';
                        }
                    } else {
                        output_str += '.</li>';
                    }
                }
            }
        }
        output_str += '</ul>';
        $('#output-field').html(output_str);
        
        /*for (var i = 0; i < data.length; ++i) {
            alert(data[i][0] + data[i][1]);
        }*/
    }, 'json');
}
