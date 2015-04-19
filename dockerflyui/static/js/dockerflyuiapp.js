'use strict';

// Declare app level module which depends on views, and components
angular.module('myApp', [
  'ngRoute',
  'ngPrettyJson',
  'myApp.container',
  'myApp.startup',
  'myApp.version'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/container'});
}]);


//for custom utils
var DockerflyUI = DockerflyUI || {};

DockerflyUI.checkDuplicates = function(arr) {
    var arr = angular.copy(arr);
    var sorted_arr = arr.sort();
    for (var i = 0; i < arr.length - 1; i++) {
        if (sorted_arr[i + 1] == sorted_arr[i]) {
            return true;
        }
    }
    return false;
};


