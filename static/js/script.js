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

/* Hide viewall on page load */
$(document).ready(function(){
    $("#category-layout").show();
    $("#viewall-layout").hide();
    $('.collapse').collapse()
});

/* Function to switch page view on Hive */
 $("#btn-categories").click(function(){
    $("#category-layout").show();
    $("#viewall-layout").hide();
    $("#btn-categories").addClass("page-selected")
    $("#btn-viewall").removeClass("page-selected")
  });
  $("#btn-viewall").click(function(){
    $("#viewall-layout").show();
    $("#category-layout").hide();
    $("#btn-viewall").addClass("page-selected")
    $("#btn-categories").removeClass("page-selected")
  });