(function () {
    "use strict";
    angular
      .module("myApp", [ui.router,"ngRoute", "ngMessages", "ngStorage", "ngMockE2E"])
      .config(config)
      .run(run);
  
    function config($stateProvider, $urlRouterPrevider) {
      $urlRouterPrevider.otherwise("/");
      $stateProvider
        .state("home", {
          url: "/",
          templateUrl: "../../index.html",
          controller: "Home.IndexController",
          controllerAs: "vm",
        })
        .state("login", {
          url: "/login",
          templateUrl: "../../templates/user/login.html",
          controller: "Login.IndexController",
          controllerAs: "vm",
        });
    }
  
    function run($rootscope, $http, $location, $localStorage) {
      if ($localStorage.currentUser) {
        $http.defaults.headers.common.Authorization =
          "Bearer" + $localStorage.currentUser.token;
      }
  
      $rootscope.$on("$locationChangeStart", function (event, next, curent) {
        var publicPages = ["/login"];
        var restrictedPage = publicPages.indexOf($location.path()) === -1;
        if (restrictedPage && !$localStorage.currentUser) {
          $location.path("/login");
        }
      });
    }
  });
  