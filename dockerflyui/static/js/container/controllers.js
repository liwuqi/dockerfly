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

  /* for refresh scroll position */
  /*
  $scope.addNewItem = function() {
    var wrapper = document.getElementById('dockerflyui-accordion');
    var scrollRemaining = wrapper.scrollHeight - wrapper.scrollTop;

    $scope.containers = $scope.containers.concat({
      id: $scope.containers.length,
      name: "container " + $scope.containers.length
    });
    // will fail if you observe the item 0 because we scroll before the view is updated;
    $timeout(function(){
      wrapper.scrollTop = wrapper.scrollHeight - scrollRemaining;
    },0);
  }
  */

  /* auto refresh */
  (function update() {
    $timeout(update, 15000);
    $scope.containers = Container.query();

    if (!$scope.collapsed) {
      angular.forEach($scope.containers, function(value, key) {
        $scope.collapsed[value.id] = true;
      });
    }
  }());
}])

