var input = document.getElementById("input_pwd");
var logout = document.getElementsByName("logoutClick")
var allImages = document.getElementsByTagName("img");
for( var i=0,il = logout.length; i< il; i ++ ){
  logout[i].onclick = function (){
    document.getElementById('logoutBTN').click()
  };
 }

input.addEventListener("keyup", function (event) {
  var c = input.value;
  if (event.keyCode === 13) {
    event.preventDefault();
    document.getElementById("loginForm").submit();
  }
});

function focusInput(){
  input.focus()
}