$(document).ready(function() {
  $("#input-typeOfWaste").hide(); /* Hide additional forms on page load */
  $("#instructions-addTypeOfWaste").hide();
  $("#select-itemCategory").hide();
  $("#instructions-addItemCategory").hide();
  $("#member-details").hide();
  $("#location-details").hide();
  $("#collection-details").hide();
});

/* REGISTER.HTML */

/* https://stackoverflow.com/questions/21727317/how-to-check-confirm-password-field-in-form-without-reloading-page/21727518 */
/* Check passwords match on Registration page */
$("#password, #confirm-password").on("keyup", function() {
  if ($("#password").val() == $("#confirm-password").val()) {
    $("#password-match").html("Passwords match").css("color", "#888C1B");
  } else
    $("#password-match").html("Passwords do not match").css("color",
      "#8C0A06");
  stopSubmission();
});

/* Prevent submission if passwords do not match on Registration page */
$("#submit-registration").click(function(event) {
  if ($("#password").val() != $("#confirm-password").val()) {
    event.preventDefault();
  }
});

/* HIVE-COLLECTION.HTML */

/* Initialize all tooltips on a page */
$(function() {
  $("[data-toggle='tooltip']").tooltip()
})

/* FORMS IN ADD NEW COLLECTION MODAL */

/* Change category if type of waste changed */

$("select#select-typeOfWaste").change(function() {
  selectedTypeOfWaste = $(this).find(":selected").val();
  selectedTypeOfWasteCategory = $(this).find(":selected").data("id");
  if (selectedTypeOfWaste == "Add New Type of Waste...") {
    $("#select-typeOfWaste").hide();
    $("#select-typeOfWaste").attr("name", "select-typeOfWaste");
    $("#input-typeOfWaste").show();
    $("#input-typeOfWaste").attr("name", "newTypeOfWaste");
    $("#input-typeOfWaste").attr("required", true);
    $("#instructions-addTypeOfWaste").show();
    $("#input-itemCategory").hide();
    $("#select-itemCategory").show();
    $("#select-itemCategory").prop('required',true);
  } else {
    $("#input-itemCategory").attr("placeholder", selectedTypeOfWasteCategory);
  }
});

$("select#select-itemCategory").change(function() {
  selectedItemCategory = $(this).find(":selected").val();
  if (selectedItemCategory == "Add New Item Category...") {
    $("#select-itemCategory").hide();
    $("#select-itemCategory").attr("name", "select-itemCategory");
    $("#select-itemCategory").prop('required',false);
    $("#input-itemCategory").show();
    $("#input-itemCategory").attr("name", "newItemCategory");
    $("#input-itemCategory").prop("disabled", false);
    $("#input-itemCategory").prop('required',true);
    $("#instructions-addItemCategory").show();
  }
});

$("select#locationID").change(function() {
  selectedLocationID = $(this).find(":selected").data("id");
  $("#locationAddress").attr("placeholder", selectedLocationID);
});

/* FORMS IN EDIT COLLECTION MODAL */
$("select#editLocation").change(function() {
  selectedEditLocation = $(this).find(":selected").data("id");
  $("#editLocationAddress").attr("placeholder", selectedEditLocation);
});

/* HIVE-MANAGEMENT.HTML */
$("#btn-manage-requests").click(function() {
  $("#btn-manage-members").addClass("inactive");
  $("#btn-manage-requests").removeClass("inactive");
  $("#membership-requests").show();
  $("#workerbee-requests").show();
  $("#member-details").hide();
  $("#location-details").hide();
  $("#collection-details").hide();
});

$("#btn-manage-members").click(function() {
  $("#btn-manage-members").removeClass("inactive");
  $("#btn-manage-requests").addClass("inactive");
  $("#membership-requests").hide();
  $("#workerbee-requests").hide();
  $("#member-details").show();
  $("#location-details").show();
  $("#collection-details").show();
});