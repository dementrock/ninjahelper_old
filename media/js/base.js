function signOut() {
    $.post(url_signout, '{}', function(data) {
       outputhtml = "";
       outputhtml += "<a id='signin' href='#signin-form-container'>Sign In</a> ";
       outputhtml += "<a id='signup' href='#signup-form-container'>Register</a>"; 
    });
}
