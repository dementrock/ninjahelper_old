var is_importing = false;

function import_data() {
    if (is_importing) {
        return;
    }
    is_importing = true;
    processing("#note", "Importing...");
    $.post(url_import_all, $("#csrf-form").serialize(), function(data) {
        if (data.status == 'error') {
            $('#note').html(data.message);
            is_importing = false;
        } else {
            $('#note').html("Successfully imported. Redirecting...");
            is_importing = false;
            location.reload();
        }
    }, 'json');
}

function compare_schedule(){
    $.post(url_compare_schedule, $('#csrf-form').serialize(), function(data){
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
        $('#note').html(output_str);
        
    }, 'json');
}
