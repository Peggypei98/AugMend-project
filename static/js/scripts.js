$("form[name=signup_form").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
  
    $.ajax({
      url: "/user/signup",
      type: "POST",
      data: data,
      dataType: "json",
      success: function(resp) {
        window.location.href = "/questions/";
      },
      error: function(resp) {
        $error.text(resp.responseJSON.error).removeClass("error--hidden");
      }
    });
  
    e.preventDefault();
  });
  
  $("form[name=login_form").submit(function(e) {
  
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
  
    $.ajax({
      url: "/user/login",
      type: "POST",
      data: data,
      dataType: "json",
      success: function(resp) {
        window.location.href = "/questions/";
      },
      error: function(resp) {
        $error.text(resp.responseJSON.error).removeClass("error--hidden");
      }
    });
  
    e.preventDefault();
  });


  document.getElementById('marital_status').addEventListener('change', function() {
    var display = this.value === 'Other' ? 'block' : 'none';
    document.getElementById('other_marital_status').style.display = display;
  });


$('#add_medication').click(function() {
    var newMedInput = $('<input type="text" name="medication_name[]" placeholder="Medication Name">');
    $('#medication_details').append(newMedInput);
});

$('input[name="medication"]').change(function() {
    if (this.value === 'Yes') {
        $('#medication_details').show();
    } else {
        $('#medication_details').hide();
    }
});

document.getElementById('survey_form').addEventListener('submit', function(event) {
  event.preventDefault();
  var email = document.getElementById('email').value;
  fetch('/check_survey', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: 'email=' + encodeURIComponent(email)
  })
  .then(response => response.json())
  .then(data => {
      if (data.exists) {
          if (confirm(data.message)) {
              // User wants to overwrite the existing data
              this.submit();
          } else {
              // User does not want to overwrite
              alert("You have already filled out the survey.");
          }
      } else {
          // No existing data, proceed to submit
          this.submit();
      }
  });
});

