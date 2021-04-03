


// function makes sure user accepts Terms and conditions
function accept_terms(checkbox) {
  if(checkbox.checked == true) {
    document.getElementById("register").disabled = false;
  } else {
    document.getElementById("register").disabled = true;
  }
}
//popup function for Terms and conditions
function togglePopup() {
  document.getElementById("popup-1").classList.toggle("active");
}
