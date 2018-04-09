function validateForm() {
    var x = document.forms["myForm"]["email"].value;
    if (x == "") {
        alert("Email must be filled out");
        return false;
    }
}