var app = angular.module("myApp", ["ngRoute"]);
app.config(function ($routeProvider) {
  $routeProvider
    .when("/", {
      templateUrl: "index.html",
    })
});
var url = "http://127.0.0.1:8000/api/products/";

app.controller("controller", function ($scope, $http) {
  $http.get("http://127.0.0.1:8000/api/category/").then(function (response) {
    // console.log($scope.category.data);
    $scope.category = response;
  });
  var current_page = "http://127.0.0.1:8000/api/products/";

  $scope.next = function () {
    current_page = $scope._page.next;
    if (current_page != null) {
      $http.get(current_page).then(function (response) {
        $scope._page = response.data.pagination;
        $scope.products = response.data.results;
        // current_page = $scope._page.current;
      });
    }
  };
  $scope.prev = function () {
    current_page = $scope._page.previous;
    if (current_page != null) {
      $http.get(current_page).then(function (response) {
        $scope._page = response.data.pagination;
        $scope.products = response.data.results;
        // current_page = $scope._page.current;
      });
    }
  };

  $http.get(current_page).then(function (response) {
    $scope._page = response.data.pagination;
    $scope.products = response.data.results;
    $scope.dene = $scope._page.current.split("=")[1];
    // current_page = $scope._page.current;
  });

  $scope.categoryBtn = function (slug) {
    $http
      .get("http://127.0.0.1:8000/api/category/" + slug + "/products")
      .then(function (response) {
        $scope.products = response.data;
        $scope.isActive = function (viewLocation) {
          return viewLocation === window.location.hash;
        };
      });
  };

  $scope.mainpage = function () {
    $http.get("http://127.0.0.1:8000/api/products/").then(function (response) {
      $scope.products = response.data.results;
      console.log(($scope._page = response.data.pagination.next));
    });
  };
});
