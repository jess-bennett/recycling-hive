/* https://stackoverflow.com/questions/21727317/how-to-check-confirm-password-field-in-form-without-reloading-page/21727518 */
/* Check passwords match */
$('#password, #confirm_password').on('keyup', function () {
  if ($('#password').val() == $('#confirm_password').val()) {
    $('#passwordMatch').html('Passwords match').css('color', '#888C1B');
  } else 
    $('#passwordMatch').html('Passwords do not match').css('color', '#8C0A06');
    stopSubmission();
});

/* Prevent submission if passwords do not match */
$("#registrationSubmit").click(function(event) {
    if ($('#password').val() != $('#confirm_password').val()) {
        event.preventDefault();
    }           
});


  /* Change list of recycling items on dropdown change */
  $("#itemCategory").change(function () {
        let itemCategory = this.value;
    });