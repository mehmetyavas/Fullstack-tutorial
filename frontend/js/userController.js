var app = angular.module("myApp", []);

app.controller("userCtrl", function ($scope, $http) {
  app.$inject = ['$window', 'loginSrv', 'notify'];

  const form = document.getElementById("loginForm");

  form.addEventListener("submit", (event) => {
    var formEl = document.forms.loginForm;
    var formData = new FormData(formEl);
    formData.append("username", document.getElementById("username").value);
    formData.append("password", document.getElementById("password").value);
    var name = formData.get("username");
    var password = formData.get("password");
    event.preventDefault();
    //   // (B2) APPEND FIELDS"
    //   data.append("name", document.getElementById("user_name").value);
    //   data.append("email", document.getElementById("user_email").value);

    const deneme = {
      username: name,
      password,
    };
    $http
      .post("http://127.0.0.1:8000/api/token/", deneme)
      .then(function (response) {
          token = localStorage.setItem("token", response.data.access);
          console.log(response.data);
          if (localStorage.key('token')!=null) {
            window.location.href= "../../index.html"         
          }

      });
  });
});
