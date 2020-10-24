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

  /* Change list of recycling items on dropdown change */
  $("#itemCategory").change(function () {
        let itemCategory = this.value;
    });

    /* Initialize all tooltips on a page */
    $(function () {
  $('[data-toggle="tooltip"]').tooltip()
})


/* Hide additional forms on page load */
$(document).ready(function(){
    $("#addNewTypeOfWaste").hide();
    $("#addNewCategory").hide();
});

/* Show 'add type of waste' form if option selected on dropdown */
$(function () {
            $("#typeOfWaste").on("change", function () {
                let selectedTypeOfWaste = $('#typeOfWaste').find("option:selected").val();
                if (selectedTypeOfWaste == 'Add New Type of Waste...') {
                    $("#addLocation").hide();
                    $("#addNewTypeOfWaste").show();
                } 
            });
        });

 /* Show 'add category' form if option selected on dropdown */
$(function () {
    $("#itemCategory").on("change", function () {
        let selectedCategory = $('#itemCategory').find("option:selected").val();
        if (selectedCategory == 'Add New Category...') {
            $("#addNewTypeOfWaste").hide();
            $("#addNewCategory").show();
        } 
    });
});

/* Hide 'add type of waste' form if closed */
$("#close-typeOfWaste").click(function(){
  $("#addLocation").show();
  $("#addNewTypeOfWaste").hide();
  $('#typeOfWaste>option:eq(0)').prop('selected', true);
});

/* Hide 'add category' form if closed */
$("#close-category").click(function(){
  $("#addNewTypeOfWaste").show();
  $("#addNewCategory").hide();
  $('#itemCategory>option:eq(0)').prop('selected', true);
});

