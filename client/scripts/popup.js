// const buttons = document.getElementsByClassName("close_button");
Array.from(document.getElementsByClassName("close_button")).forEach(
  (button) => {
    button.addEventListener("click", () => {
      document.body.removeChild(document.getElementById("alert-div"));
    });
  }
);

// Popup screen 'Terms of use' collapse/expand functionality
document.getElementById("terms-link").addEventListener("click", () => {
  const ele = document.getElementById("termsOfUseContent");
  const terms_chev = document.getElementById("terms_chev");
  if (ele.classList.contains("hide")) {
    ele.classList.remove("hide");
    terms_chev.classList.remove("fa-chevron-down");
    terms_chev.classList.add("fa-chevron-up");
  } else {
    ele.classList.add("hide");
    terms_chev.classList.remove("fa-chevron-up");
    terms_chev.classList.add("fa-chevron-down");
  }
});
