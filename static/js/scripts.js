$(document).ready(function() {
  // Form submission handlers for signup and login
  $("form[name=signup_form], form[name=login_form]").submit(function(e) {
      e.preventDefault();
      var $form = $(this);
      var $error = $form.find(".error");
      var url = $form.attr("name") === "signup_form" ? "/user/signup" : "/user/login";
      
      $.ajax({
          url: url,
          type: "POST",
          data: $form.serialize(),
          dataType: "json",
          success: function(resp) {
              window.location.href = "/questions/";
          },
          error: function(resp) {
              $error.text(resp.responseJSON.error).removeClass("error--hidden");
          }
      });
  });

  // Handling display of 'other marital status' field
  document.getElementById('marital_status').addEventListener('change', function() {
      var isVisible = this.value === 'Other';
      document.getElementById('other_marital_status').style.display = isVisible ? 'block' : 'none';
  });

  // Add medication input dynamically
  $('#add_medication').click(function() {
      $('#medication_details').append('<input type="text" name="medication_name[]" placeholder="Medication Name">');
  });

  // Toggle medication details visibility
  $('input[name="medication"]').change(function() {
      $('#medication_details').toggle(this.value === 'Yes');
  });

  // Check if survey has been filled out before submitting
  document.getElementById('survey_form').addEventListener('submit', function(event) {
      event.preventDefault();
      var email = document.getElementById('email').value;
      
      fetch('/check_survey', {
          method: 'POST',
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          body: 'email=' + encodeURIComponent(email)
      }).then(response => response.json()).then(data => {
          if (data.exists) {
              if (confirm(data.message)) {
                  this.submit();
              } else {
                  alert("You have already filled out the survey.");
              }
          } else {
              this.submit();
          }
      });
  });
});
