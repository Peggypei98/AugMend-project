$("form[name=signup_form]").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            // console.log(resp);
            window.location.href = "/questions/";
        },
        error: function(resp) {
            // console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});
