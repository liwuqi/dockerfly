'use strict';


angular.module('myApp.startup', ['ngRoute', 'startupControllers', 'ngPrettyJson'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/startup', {
    templateUrl: 'static/partials/startup.html',
    controller: 'StartupCtrl'
  });
}]);

