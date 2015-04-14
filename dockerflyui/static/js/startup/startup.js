'use strict';


angular.module('myApp.startup', ['ngRoute', 'startupControllers', 'schemaForm'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/startup', {
    templateUrl: 'static/partials/startup.html',
    controller: 'FormController'
  });
}]);

