var containerControllers = angular.module('containerControllers', []);

$('.collapse').collapse({toggle:true});

containerControllers.controller('ContainerListCtrl', ['$scope', 'Container', function($scope, Container) {
  $scope.containers = Container.query();
  $scope.orderProp = 'last_modify_time';
}]);

