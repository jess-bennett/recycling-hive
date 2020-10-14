/* https://stackoverflow.com/questions/21727317/how-to-check-confirm-password-field-in-form-without-reloading-page/21727518 */
$('#password, #confirm_password').on('keyup', function () {
  if ($('#password').val() == $('#confirm_password').val()) {
    $('#passwordMatch').html('Passwords match').css('color', '#888C1B');
  } else 
    $('#passwordMatch').html('Passwords do not match').css('color', '#8C0A06');
    stopSubmission();
});

$("#registrationSubmit").click(function(event) {
    if ($('#password').val() != $('#confirm_password').val()) {
        event.preventDefault();
    }           
});

 $("#btn-categories").click(function(){
    $(".category-layout").show();
  });
  $("#btn-viewall").click(function(){
    $(".category-layout").hide();
  });