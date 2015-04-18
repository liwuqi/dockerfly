'use strict';


angular.module('myApp.startup', ['ngRoute', 'angular-underscore/filters', 'startupControllers', 'schemaForm', 'pascalprecht.translate', 'ui.select'])

.config(['$routeProvider', '$controllerProvider', '$compileProvider', '$filterProvider', '$provide', function ($routeProvider, $controllerProvider, $compileProvider, $filterProvider, $provide) {
  $routeProvider.when('/startup', {
    templateUrl: 'static/partials/startup.html',
    controller: 'FormController'
  });
}]);

