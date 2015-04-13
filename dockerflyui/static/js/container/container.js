'use strict';

angular.module('myApp.container', ['ngRoute', 'containerControllers', 'containerServices'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/container', {
    templateUrl: 'static/partials/container.html',
    controller: 'ContainerListController'
  });
}]);

