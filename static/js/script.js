$(document).ready(function() {
  $("#input-typeOfWaste").hide(); /* Hide additional forms on page load */
  $("#instructions-addTypeOfWaste").hide();
  $("#select-itemCategory").hide();
  $("#instructions-addItemCategory").hide();
  $("#profile-page").hide(); /* Hide profile page on page load */
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

/* INDEX.HTML */
$("#btn-profile").click(function() {
  $("#profile-page").show();
  $("#home-hexagons").hide();
});

/* Change list of recycling items on dropdown change */
/*  $("#itemCategory").change(function () {
       let itemCategory = this.value;
   }); */

/* HIVE-COLLECTION.HTML */

/* Initialize all tooltips on a page */
$(function() {
  $("[data-toggle='tooltip']").tooltip()
})

/* FORMS IN ADD NEW COLLECTION MODAL */

/* Change category if type of waste changed */

$("select#select-typeOfWaste").change(function() {
  selectedTypeOfWaste = $(this).find(":selected").val();
  console.log(selectedTypeOfWaste)
  selectedTypeOfWasteCategory = $(this).find(":selected").data("id");
  console.log(selectedTypeOfWasteCategory)
  if (selectedTypeOfWaste == "Add New Type of Waste...") {
    console.log("YES");
    $("#select-typeOfWaste").hide();
    $("#select-typeOfWaste").attr("name", "select-typeOfWaste");
    $("#input-typeOfWaste").show();
    $("#input-typeOfWaste").attr("name", "newTypeOfWaste");
    $("#instructions-addTypeOfWaste").show();
    $("#input-itemCategory").hide();
    $("#select-itemCategory").show();
  } else {
    $("#itemCategory").attr("placeholder", selectedTypeOfWasteCategory);
  }
});

$("select#select-itemCategory").change(function() {
  selectedItemCategory = $(this).find(":selected").val();
  if (selectedItemCategory == "Add New Item Category...") {
    $("#select-itemCategory").hide();
    $("#select-itemCategory").attr("name", "select-itemCategory");
    $("#input-itemCategory").show();
    $("#input-itemCategory").attr("name", "newItemCategory");
    $("#input-itemCategory").prop("disabled", false);
    $("#instructions-addItemCategory").show();
  }
});

$("select#locationID").change(function() {
  selectedLocationID = $(this).find(":selected").data("id");
  $("#locationAddress").attr("placeholder", selectedLocationID);
});

/* Show 'add type of waste' form if option selected on dropdown */
/* $(function () {
            $("#typeOfWaste").on("change", function () {
                let selectedTypeOfWaste = $("#typeOfWaste").find("option:selected").val();
                console.log(selectedTypeOfWaste);
                if (selectedTypeOfWaste == "Add New Type of Waste...") {
                    $("#formCollection").hide();
                    $("#formNewTypeOfWaste").show();
                } 
            });
        }); */

/* Show 'add category' form if option selected on dropdown */
/* $(function () {
    $("#itemCategory").on("change", function () {
        let selectedCategory = $("#itemCategory").find("option:selected").val();
        if (selectedCategory == "Add New Category...") {
            $("#formNewTypeOfWaste").hide();
            $("#formNewCategory").show();
        } 
    });
}); */

/* Hide 'add type of waste' form if closed */
/* $("#close-typeOfWaste").click(function(){
  $("#formCollection").show();
  $("#formNewTypeOfWaste").hide();
  $("#typeOfWaste>option:eq(0)").prop("selected", true);
}); */

/* Hide 'add category' form if closed */
/* $("#close-category").click(function(){
  $("#formNewTypeOfWaste").show();
  $("#formNewCategory").hide();
  $("#itemCategory>option:eq(0)").prop("selected", true);
}); */