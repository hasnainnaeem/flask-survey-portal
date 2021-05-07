function send_study2_form(data, content) {

    $.ajax({
        type: 'POST',
        url: "{{url_for('submit_study2')}}",
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
    $("#submit-study2-button").on('click', function(e){
        e.preventDefault(); //prevent reload
        
        var fd = new FormData($('#study2-form-data')[0]);
        console.log(fd)
        send_study2_form(fd, false);
    });
});