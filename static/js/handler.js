function verify_user(data, content) {

    $.ajax({
        type: 'POST',
        url: "{{url_for('verify_user')}}",
        data: data,
        contentType: 'application/json;charset=UTF-8',
        cache: false,
        processData: false,
        success: function(response){
            console.log(response['status']);
        },
        error: function(jqXHR, textStatus, errorThrown){
            // $("#error").html("An unknown error has occurred in processing. Please try again.");
            // $("#error").show();

            // console.log(textStatus);
            // console.log(errorThrown);
        }
    });
}

/* user request */
$(function(){
    $("#submituser").on('click', function(e){
        e.preventDefault(); //prevent reload
        
        var fd = new FormData($('#userdata')[0]);
        console.log("asndksjan")
        
        verify_user(fd, false);
    });
});