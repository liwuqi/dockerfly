$('.collapse').collapse({toggle:true});
var startupControllers = angular.module('startupControllers', []);

startupControllers.controller('StartupCtrl', ['$scope', '$http', '$timeout', 'Container', function($scope, $http, $timeout, Container) {
  if (!Date.now) {
      Date.now = function() { return new Date().getTime(); }
  }
  $scope.container_template =  [
      {
        "gateway": "172.16.13.1",
        "eths": [
            [
                "v"+ Math.floor(Date.now()/1000),
                "em2",
                "172.16.13.254/24"
            ]
        ],
        "image_name": "docker-registry.dev.netis.com.cn:5000/crossflow/bpc3",
        "run_cmd": "/usr/bin/svscan /etc/dockerservices",
        "id":null,
        "pid":null,
        "status":"running",
        "container_name":"yourname_crossflowname_for_xxx",
        "last_modify_time":0,
        "desc":"testfor crossflow"
    }
  ];

  $scope.createContainer = function(container_template) {
    console.log("create container")
    console.log(container_template);
    $http.post('/api/containers', data=container_template)
    .success(function(data, status, headers, config){
        alert("OK.\nstatus:" + status.toString() + "\n" + JSON.stringify(data, null, 2));
    })
    .error(function(data, status, headers, config){
        alert("Error.\n" + status.toString() + "\n" + JSON.stringify(data, null, 2));
    });
  };

  $scope.$on('json-updated', function(msg, value) {
    $scope.container_template = value;
    console.log(value);
  });

}])

