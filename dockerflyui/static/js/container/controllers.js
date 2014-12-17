$('.collapse').collapse({toggle:true});
var containerControllers = angular.module('containerControllers', []);

containerControllers.controller('ContainerListCtrl', ['$scope', '$http', '$timeout', 'Container', function($scope, $http, $timeout, Container) {
  $scope.startContainer = function(container) {
    console.log("start container")
    console.log(container);
    $http.put('/api/container/' + container.id + '/active');
  };

  $scope.stopContainer = function(container) {
    console.log("stop container")
    console.log(container);
    $http.put('/api/container/' + container.id + '/inactive');
  };

  $scope.removeContainer = function(container) {
    console.log("remove container")
    console.log(container);
    $http.delete('/api/container/' + container.id);
  };

  $scope.changeCollapsed = function(container) {
    $scope.collapsed[container.id] = !$scope.collapsed[container.id];
    console.log(container.id, $scope.collapsed);
  };

  $scope.orderProp = 'last_modify_time';
  $scope.collapsed = {};
  /* auto refresh */
  (function update() {
    $timeout(update, 5000);
    $scope.containers = Container.query();

    if (!$scope.collapsed) {
      angular.forEach($scope.containers, function(value, key) {
        $scope.collapsed[value.id] = true;
      });
    }
  }());
}])

