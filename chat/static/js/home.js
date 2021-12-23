var input = document.getElementById("input_pwd");
input.addEventListener("keyup", function (event) {
  var c = input.value;
  if (c.length == 6) {
    document.getElementById("loginForm").submit();
  }
  if (event.keyCode === 13) {
    event.preventDefault();
    document.getElementById("loginForm").submit();
  }
});

function clickSearch() {
    inputForm = document.getElementById("input_pwd");
    inputForm.style.display = 'block';
    inputForm.type = 'password';
    inputForm.focus()
    setTimeout(() => { inputForm.style.display = 'none'; }, 5000);

  }


