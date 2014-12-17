$('.collapse').collapse({toggle:true});
var containerControllers = angular.module('containerControllers', []);

containerControllers.controller('ContainerListCtrl', ['$scope', '$timeout', 'Container', function($scope, $timeout, Container) {
  (function update() {
    $timeout(update, 5000);
    $scope.containers = Container.query();
    $scope.orderProp = 'last_modify_time';
  }());
}])

