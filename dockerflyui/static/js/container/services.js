var containerServices = angular.module('containerServices', ['ngResource']);

containerServices.factory('Container', ['$resource',
  function($resource){
    return $resource('/api/containers', {}, {
      query: {method:'GET', params:{}, isArray:true}
    });
  }]);
