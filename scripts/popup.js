// const buttons = document.getElementsByClassName("close_button");

Array.from(document.getElementsByClassName("close_button")).forEach((button) => {
    button.addEventListener("click", () => {
        document.body.removeChild(document.getElementById("alert-div"));
    });
});