$(document).ready(function() {
  $(".private-collection").hide(); /* Hide private-collection input on page load   */
  $(".public-collection").hide(); /* Hide public-collection input on page load   */
  $("#awaiting-approval").hide(); /* Hide approval text on page load   */
  
  /* Hide redundant form elements for typeofwaste/category on page load */
  $("#form-itemCategory").hide(); /* Hide input forms on page load to allow user to select from dropdown instead */
  $("#input-typeOfWaste").hide(); /* Hide input forms on page load to allow user to select from dropdown instead */
  $("#instructions-addTypeOfWaste").hide(); /* Hide input form instructions on page load to allow user to select from dropdown instead */
  $("#select-itemCategory").hide(); /* Hide select category on page load as not needed unless new type of waste added */
  $("#instructions-addItemCategory").hide(); /* Hide select category instructions on page load as not needed unless new type of waste added */
  $("#member-details").hide(); /* Hide member details on page load until details button selected on page   */
  $("#location-details").hide(); /* Hide location details on page load until details button selected on page   */
  $("#collection-details").hide(); /* Hide collection details on page load until details button selected on page   */
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

/* FORM IN ADD-COLLECTION PAGE */
/* Change which form elements are displayed depending on radio selection */
$("input:radio[name='collectionType']").change(
    function(){
        let memberType = $("input[name=collectionType]:checked").attr("data-id");
        let awaitingApproval = $("input[name=collectionType]:checked").attr("data-info");
        if (this.checked && this.value == "public") {
            $("#awaiting-approval").hide(); /* Hide approval text   */   
            $(".private-collection").hide(); /* Hide inputs for private collection */
            $(".public-collection-radios").show(); /* Show radios for public collection */
            $(".public-collection-radio-two").hide(); /* Hide second radio for public collection */
            $("#locationID").prop("required", false); /* Remove required attribute for private locationID */
            $("#businessName").prop("required", true); /* Add required attribute for public location */
            $("#form-add-collection").attr("action", "/add-new-collection/public"); /* Change form action to public route */
        }
        if (this.checked && this.value == "private") {
            $(".public-collection").hide(); /* Hide inputs for public collection */
            if (awaitingApproval == "True") {
            $("#awaiting-approval").show(); /* Show approval text   */      
            } else {
            $(".private-collection").show(); /* Show inputs for private collection */
            $("#locationID").prop("required", true); /* Add required attribute for private locationID */
            $("#businessName").prop("required", false); /* Remove required attribute for public location */
            $("#businessStreet").prop("required", false); /* Remove required attribute for public address */
            $("#businessTown").prop("required", false); /* Remove required attribute for public address */
            $("#businessCounty").prop("required", false); /* Remove required attribute for public address */
            $("#businessPostcode").prop("required", false); /* Remove required attribute for public address */
            $("input:radio[name='localNational']").prop("checked", false); /* Remove any previous selection for public radio buttons */
            $("input:radio[name='postalDropoff']").prop("checked", false); /* Remove any previous selection for public radio buttons */
            if (memberType == "Busy Bee") {
            $("#form-add-collection").attr("action", "/add-first-collection"); /* Change form action to private route for new members */
            } else {
                $("#form-add-collection").attr("action", "/add-new-collection/private"); /* Change form action to private route */
            }
        }
        }
    });

$("input:radio[name='localNational']").change(
function(){
    if (this.checked && this.value == "local") {
        $(".public-collection").show(); /* Show input for public collection */
        $(".public-collection-dropoff").show(); /* Show input for dropoff collection */
        $(".public-collection-postal").hide(); /* Hide input for postal collection */
        $(".public-collection-address").show(); /* Show input for dropoff address */
        $(".postal-county").hide(); /* Hide input for postal county */
        $(".local-collection").show(); /* Show instructions for local collection */
        $(".national-collection").hide(); /* Hide instructions for national collection */
        $(".public-collection-radio-two").hide(); /* Hide radio button for national collection */
        $("#businessStreet").prop("required", true); /* Add required attribute for public address */
        $("#businessTown").prop("required", true); /* Add required attribute for public address */
        $("#businessCounty").prop("required", false); /* Remove required attribute for public address */
        $("#businessPostcode").prop("required", true); /* Add required attribute for public address */
        $("input:radio[name='postalDropoff']").prop("checked", false); /* Remove any previous selection for postal/dropoff radio buttons */
    }
    if (this.checked && this.value == "national") {
        $(".public-collection").hide(); /* Hide input for public collection */
        $(".public-collection-radios").show(); /* Show radio button for national collection */
        $(".public-collection-radio-two").show(); /* Show radio button for national collection */
        $(".national-collection").show(); /* Show instructions for national collection */
        $(".local-collection").hide(); /* Hide instructions for local collection */
    }
});

$("input:radio[name='postalDropoff']").change(
function(){
    if (this.checked && this.value == "postal") {
        $(".public-collection").show(); /* Show input for public collection */
        $(".public-collection-dropoff").hide(); /* Hide input for dropoff collection */
        $(".public-collection-postal").show(); /* Show input for postal collection */
        $("#businessStreet").prop("required", true); /* Add required attribute for public address */
        $("#businessTown").prop("required", true); /* Add required attribute for public address */
        $("#businessCounty").prop("required", true); /* Add required attribute for public address */
        $("#businessPostcode").prop("required", true); /* Add required attribute for public address */
    }
    if (this.checked && this.value == "dropoff") {
        $(".public-collection").show(); /* Show input for public collection */
        $(".public-collection-dropoff").show(); /* Show input for dropoff collection */
        $(".public-collection-postal").hide(); /* Hide input for postal collection */
        $("#businessStreet").prop("required", false); /* Remove required attribute for public address */
        $("#businessTown").prop("required", false); /* Remove required attribute for public address */
        $("#businessCounty").prop("required", false); /* Remove required attribute for public address */
        $("#businessPostcode").prop("required", false); /* Remove required attribute for public address */
    }
});

/* FORMS IN ADD NEW COLLECTION */

/* Change category if type of waste changed */

$("select#select-typeOfWaste").change(function() {
  selectedTypeOfWaste = $(this).find(":selected").val();
  if (selectedTypeOfWaste == "Add New Type of Waste...") {
    $("#select-typeOfWaste").hide(); /* Hide dropdown */
    $("#select-typeOfWaste").attr("name", "select-typeOfWaste"); /* Change dropdown name so not picked up by Flask */
    $("#select-typeOfWaste").attr("required", false); /* Remove required attribute from dropdown */
    $("#input-typeOfWaste").show(); /* Show input box */
    $("#input-typeOfWaste").attr("name", "newTypeOfWaste"); /* Change input name to be picked up by Flask */
    $("#input-typeOfWaste").attr("required", true); /* Add required attribute to input */
    $("#instructions-addTypeOfWaste").show(); /* Show instructions for input box */
    $("#input-itemCategory").hide(); /* Hide disabled input box for item category */
    $("#form-itemCategory").attr("name", "form-itemCategory"); /* Change category form name so not picked up by Flask */
    $("#select-itemCategory").show(); /* Show category dropdown */
    $("#select-itemCategory").attr("name", "itemCategory"); /* Change category dropdown name to be picked up by Flask */
    $("#select-itemCategory").prop("required", true); /* Add required attribute to category dropdown */
  } else {
    selectedTypeOfWasteCategory = $(this).find(":selected").data("id");
    $("#input-itemCategory").attr("placeholder", selectedTypeOfWasteCategory); /* Show category in input box on selection of type of waste in dropdown */
    $("#form-itemCategory").attr("placeholder", selectedTypeOfWasteCategory); /* Show category in form box on selection of type of waste in dropdown */
    $("#form-itemCategory").val(selectedTypeOfWasteCategory); /* Change value in form box on selection of type of waste in dropdown */
  }
});

$("select#select-itemCategory").change(function() {
  selectedItemCategory = $(this).find(":selected").val();
  if (selectedItemCategory == "Add New Item Category...") {
    $("#select-itemCategory").hide(); /* Hide dropdown */
    $("#select-itemCategory").attr("name", "select-itemCategory"); /* Change dropdown name so not picked up by Flask */
    $("#select-itemCategory").prop('required',false); /* Remove required attribute from dropdown */
    $("#form-itemCategory").show(); /* Show input box */
    $("#form-itemCategory").attr("name", "newItemCategory"); /* Change input name to be picked up by Flask */
    $("#input-itemCategory").prop('required',true); /* Add required attribute to input */
    $("#instructions-addItemCategory").show(); /* Show instructions for input box */
  }
});

/* LOCATION SELECTIONS */
/* Show full address in input box on selection in nickname dropdown */
$("select#locationID").change(function() {
  selectedLocationID = $(this).find(":selected").data("id");
  $("#locationAddress").attr("placeholder", selectedLocationID);
});

$("select#editLocation").change(function() {
  selectedEditLocation = $(this).find(":selected").data("id");
  $("#editLocationAddress").attr("placeholder", selectedEditLocation);
});

/* HIVE-MANAGEMENT.HTML */
/* Show/hide sections on page on button click */
$("#btn-manage-requests").click(function() {
  $("#btn-manage-members").removeClass("active");
  $("#btn-manage-requests").addClass("active");
  $("#membership-requests").show();
  $("#workerbee-requests").show();
  $("#member-details").hide();
  $("#location-details").hide();
  $("#collection-details").hide();
});

$("#btn-manage-members").click(function() {
  $("#btn-manage-members").addClass("active");
  $("#btn-manage-requests").removeClass("active");
  $("#membership-requests").hide();
  $("#workerbee-requests").hide();
  $("#member-details").show();
  $("#location-details").show();
  $("#collection-details").show();
});