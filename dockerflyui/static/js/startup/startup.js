'use strict';


angular.module('myApp.startup', ['ngRoute','mgcrea.ngStrap.modal', 'angular-underscore', 'startupControllers', 'schemaForm', 'pascalprecht.translate', 'ui.select'])

.config(['$routeProvider', '$modalProvider', '$controllerProvider', '$compileProvider', '$filterProvider', '$provide',
        function ($routeProvider, $modalProvider, $controllerProvider, $compileProvider, $filterProvider, $provide) {
  $routeProvider.when('/startup', {
    templateUrl: 'static/partials/startup.html',
    controller: 'FormController'
  });
  angular.extend($modalProvider.defaults, {html: true});
}])

