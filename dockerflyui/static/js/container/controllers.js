var containerControllers = angular.module('containerControllers', []);

containerControllers.controller('ContainerListCtrl', ['$scope', 'Container', function($scope, Container) {
  $scope.containers = Container.query();
  $scope.orderProp = 'last_modify_time';
}]);

