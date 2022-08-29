var app = angular.module("myApp", []);

app.controller("userCtrl", function ($scope, $http) {
  const form = document.getElementById("loginForm");


  form.addEventListener("submit", (event) => {

    
        var formEl = document.forms.loginForm
        var formData = new FormData(formEl);
        formData.append('username',document.getElementById('username').value);
        var name = formData.get('username')
        var password = formData.get('password')
        event.preventDefault();
//   // (B2) APPEND FIELDS
//   data.append("name", document.getElementById("user_name").value);
//   data.append("email", document.getElementById("user_email").value);
        console.log(formData)
        console.log(name)
        console.log(password)


  });
});
