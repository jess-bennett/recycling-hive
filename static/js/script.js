$(document).ready(function() {
  $("#local-national").hide(); /* Hide local-national question on page load   */
  $(".private-collection").hide(); /* Hide private-collection input on page load   */
  $(".public-collection").hide(); /* Hide public-collection input on page load   */
  $(".form-public-collection").hide(); /* Hide public-collection input on page load   */
  $(".form-public-collection-address").hide(); /* Hide public-collection input on page load   */
  $(".form-public-collection-postal").hide(); /* Hide public-collection input on page load   */
  $(".form-public-collection-dropoff").hide(); /* Hide public-collection input on page load   */
  $(".national-collection").hide(); /* Hide national-collection text on page load   */
  $(".all-collection").hide(); /* Hide all-collection input on page load   */
  $("#input-typeOfWaste").hide(); /* Hide input forms on page load to allow user to select from dropdown instead */
  $("#input-businessTypeOfWaste").hide(); 
  $("#instructions-addTypeOfWaste").hide(); /* Hide input form instructions on page load to allow user to select from dropdown instead */
  $("#instructions-addBusinessTypeOfWaste").hide();
  $("#select-itemCategory").hide(); /* Hide select category on page load as not needed unless new type of waste added */
  $("#select-businessItemCategory").hide();
  $("#instructions-addItemCategory").hide(); /* Hide select category instructions on page load as not needed unless new type of waste added */
  $("#instructions-addBusinessItemCategory").hide();
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

$("input:radio[name='collectionType']").change(
    function(){
        
        if (this.checked && this.value == "public") {
            $("#local-national").show();
            $(".all-collection").hide();
            $(".private-collection").hide();
            $("#locationID").prop("required", false);
            $("#businessName").prop("required", true);
            $("#form-add-collection").attr("action", "/add-new-collection/public");
        }
        if (this.checked && this.value == "private") {
            $(".form-public-collection").hide();
            $(".private-collection").show();
            $(".all-collection").show();
            $(".public-collection").hide();
            $("#local-national").hide();
            $("#locationID").prop("required", true);
            $("#businessName").prop("required", false);
            $("#businessStreet").prop("required", false);
            $("#businessTown").prop("required", false);
            $("#businessPostcode").prop("required", false);
            $("input:radio[name='localNational']").prop("checked", false);
            $("input:radio[name='dropoffPosted']").prop("checked", false);
            let memberType = '{{ member_type }}';
            console.log(memberType)
            if (memberType == "Busy Bee") {
            $("#form-add-collection").attr("action", "/add-first-collection");
            } else {
                $("#form-add-collection").attr("action", "/add-new-collection/private");
            }
        }
    });

$("input:radio[name='localNational']").change(
function(){
    if (this.checked && this.value == "local") {
        $("#dropoff-posted").hide();
        $(".national-collection").hide();
        $(".form-public-collection").show();
        $(".form-public-collection-address").show();
        $("#businessStreet").prop("required", true);
        $("#businessTown").prop("required", true);
        $("#businessPostcode").prop("required", true);
        $(".form-public-collection-dropoff").show();
        $(".form-public-collection-postal").hide();
        $(".all-collection").show();
        $("input:radio[name='dropoffPosted']").prop("checked", false);
    }
    if (this.checked && this.value == "national") {
        $("#dropoff-posted").show();
        $(".national-collection").show();
        $(".form-public-collection").hide();
        $(".form-public-collection-dropoff").hide();
        $(".all-collection").hide();
    }
});

$("input:radio[name='dropoffPosted']").change(
function(){
    if (this.checked && this.value == "postal") {
        $(".form-public-collection").show();
        $(".all-collection").show();
        $("#businessStreet").prop("required", true);
        $("#businessTown").prop("required", true);
        $("#businessPostcode").prop("required", true);
        $(".form-public-collection-address").show();
        $(".form-public-collection-postal").show();
        $(".form-public-collection-dropoff").hide();
    }
    if (this.checked && this.value == "dropoff") {
        $(".form-public-collection").show();
        $(".all-collection").show();
        $("#businessStreet").prop("required", false);
        $("#businessTown").prop("required", false);
        $("#businessPostcode").prop("required", false);
        $(".form-public-collection-postal").hide();
        $(".form-public-collection-address").hide();
        $(".form-public-collection-dropoff").show();
    }
});

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

/* FORMS IN NATIONAL COLLECTION MODAL */

/* Change category if type of waste changed */

$("select#select-businessTypeOfWaste").change(function() {
  selectedBusinessTypeOfWaste = $(this).find(":selected").val();
  selectedBusinessTypeOfWasteCategory = $(this).find(":selected").data("id");
  if (selectedBusinessTypeOfWaste == "Add New Type of Waste...") {
    $("#select-businessTypeOfWaste").hide();
    $("#select-businessTypeOfWaste").attr("name", "select-businessTypeOfWaste");
    $("#input-businessTypeOfWaste").show();
    $("#input-businessTypeOfWaste").attr("name", "newBusinessTypeOfWaste");
    $("#input-businessTypeOfWaste").attr("required", true);
    $("#instructions-addBusinessTypeOfWaste").show();
    $("#input-businessItemCategory").hide();
    $("#select-businessItemCategory").show();
    $("#select-businessItemCategory").prop('required',true);
  } else {
    $("#input-businessItemCategory").attr("placeholder", selectedBusinessTypeOfWasteCategory);
  }
});

$("select#select-businessItemCategory").change(function() {
  selectedBusinessItemCategory = $(this).find(":selected").val();
  if (selectedBusinessItemCategory == "Add New Item Category...") {
    $("#select-businessItemCategory").hide();
    $("#select-businessItemCategory").attr("name", "select-businessItemCategory");
    $("#select-businessItemCategory").prop('required',false);
    $("#input-businessItemCategory").show();
    $("#input-businessItemCategory").attr("name", "newItemCategory");
    $("#input-businessItemCategory").prop("disabled", false);
    $("#input-businessItemCategory").prop('required',true);
    $("#instructions-addBusinessItemCategory").show();
  }
});

$("select#locationID").change(function() {
  selectedLocationID = $(this).find(":selected").data("id");
  $("#locationAddress").attr("placeholder", selectedLocationID);
});

/* FORMS IN EDIT COLLECTION-LOCATION MODAL */
$("select#editLocation").change(function() {
  selectedEditLocation = $(this).find(":selected").data("id");
  $("#editLocationAddress").attr("placeholder", selectedEditLocation);
});

/* HIVE-MANAGEMENT.HTML */
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