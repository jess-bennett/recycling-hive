/* https://stackoverflow.com/questions/21727317/how-to-check-confirm-password-field-in-form-without-reloading-page/21727518 */
/* Check passwords match on Registration page */
$('#password, #confirm-password').on('keyup', function () {
  if ($('#password').val() == $('#confirm-password').val()) {
    $('#password-match').html('Passwords match').css('color', '#888C1B');
  } else 
    $('#password-match').html('Passwords do not match').css('color', '#8C0A06');
    stopSubmission();
});

/* Prevent submission if passwords do not match on Registration page */
$("#submit-registration").click(function(event) {
    if ($('#password').val() != $('#confirm-password').val()) {
        event.preventDefault();
    }           
});

/* Collapse accordion on page load on Hive category page  */
$(document).ready(function(){
    $('.collapse').collapse()
});

/* Select category in dropdown on page change */
$("#select-category").click(function(event) {
    $("select#itemCategory option").filter(function() {
                    return $(this).val() == $(this).val(); 
                }).prop('selected', true);         
});

  /* Change list of recycling items on dropdown change */
  $("#itemCategory").change(function () {
        let itemCategory = this.value;
    });