$('.collapse').collapse({toggle:true});
var startupControllers = angular.module('startupControllers', []);

startupControllers.controller('FormController', ['$scope', '$http', '$timeout',
    function($scope, $http, $timeout) {
      if (!Date.now) {
          Date.now = function() { return new Date().getTime(); }
      }

      $scope.schema = {
        type: 'object',
        properties: {
          container_name: {
              type: 'string',
              title: 'Name',
              default: 'yourname_projectname_for_xxx',
              description: 'set your container name'
          },
          gateway: {
              type: 'string',
              title: 'Gateway',
              default: '172.16.13.1',
              pattern: '^(\\d|[1-9]\\d|1\\d\\d|2([0-4]\\d|5[0-5]))\\.(\\d|[1-9]\\d|1\\d\\d|2([0-4]\\d|5[0-5]))\\.(\\d|[1-9]\\d|1\\d\\d|2([0-4]\\d|5[0-5]))\\.(\\d|[1-9]\\d|1\\d\\d|2([0-4]\\d|5[0-5]))$',
              description: 'please set the gateway',
              validationMessage: " "
          },
          desc: {
              type: 'string',
              title: 'Description',
              default: 'integration test',
              description: 'please add desc for you container'
          },
          run_cmd: {
              type: 'string',
              title: 'container run cmd',
              default: '/usr/bin/svscan /etc/dockerservices',
              description: 'set your container run command'
          },
          image_name: {
              type: 'string',
              title: 'base image',
              enum: [
                    "docker-registry.dev.netis.com.cn:5000/crossflow/bpc2",
                    "docker-registry.dev.netis.com.cn:5000/crossflow/bpc3",
                    "docker-registry.dev.netis.com.cn:5000/crossflow/npm3",
                    "docker-registry.dev.netis.com.cn:5000/crossflow/centos6",
                    "docker-registry.dev.netis.com.cn:5000/crossflow/smartprobe",
                  ],
              default: "docker-registry.dev.netis.com.cn:5000/crossflow/bpc3",
              description: 'select your base image of container'
          },
          eths: {
              type: 'array',
              title: 'add eths',
              items: {
                  type: 'object',
                  properties: {
                      eth_name: {
                        type: 'string',
                        title: 'new eth',
                        default: 'v' + Math.floor(Date.now()/1000),
                      },
                      attach_to: {
                        type: 'string',
                        title: 'attach to which mother eth',
                        default: 'eth1'
                      },
                      ip: {
                        type: 'string',
                        title: 'set ip',
                        default: '172.16.13.100/24',
                        pattern: '^(\\d|[1-9]\\d|1\\d\\d|2([0-4]\\d|5[0-5]))\\.(\\d|[1-9]\\d|1\\d\\d|2([0-4]\\d|5[0-5]))\\.(\\d|[1-9]\\d|1\\d\\d|2([0-4]\\d|5[0-5]))\\.(\\d|[1-9]\\d|1\\d\\d|2([0-4]\\d|5[0-5]))/([1-2]\\d|3[0-2]|\\d)$',
                        validationMessage: " "
                      }
                  }
              }
          },
        },
        required: [
            'container_name',
            'image_name',
            'run_cmd',
            'desc',
            'gateway',
            'eths'
        ]
      };

      $scope.form = [
        {
            type: 'help',
            helpvalue: '<div class="alert alert-info">set up your container</div>'
        },
        {
            htmlClass: 'row',
            type: 'section',
            items: [
                {
                    type: 'section',
                    htmlClass: 'col-xs-12',
                    items: [
                        'container_name',
                        'image_name',
                        'run_cmd',
                        'desc',
                    ]
                }
            ]
        },
        {
            type: 'help',
            helpvalue: '<div class="alert alert-info">custom your container network</div>'
        },
        {
            htmlClass: 'row',
            type: 'section',
            items: [
                {
                    type: 'section',
                    htmlClass: 'col-xs-12',
                    items: [
                        'gateway',
                        'eths',
                    ]
                }
            ]
        },
        {
            type: 'submit',
            title: 'Create'
        }
      ];

      $scope.containerModel= {};

      $scope.onSubmit = function(form) {
        $scope.$broadcast('schemaFormValidate');

        if(form.$valid) {
            console.log("create container");

            //normalize post params
            var post_params = angular.copy($scope.containerModel);
            post_params.eths = new Array();
            for (i=0; i<$scope.containerModel.eths.length; i++) {
                    post_params.eths[i] = new Array();
                    post_params.eths[i][0] = $scope.containerModel.eths[i]['eth_name'];
                    post_params.eths[i][1] = $scope.containerModel.eths[i]['attach_to'];
                    post_params.eths[i][2] = $scope.containerModel.eths[i]['ip'];
            }

            post_params['status'] = 'running';
            console.log(post_params);
            var post_params_wrapper = new Array(post_params);

            $http.post('/api/containers', data=post_params_wrapper)
                .success(function(data, status, headers, config){
                    alert("status:" + status.toString() + "\n" + JSON.stringify(data, null, 2));
                })
                .error(function(data, status, headers, config){
                    alert("status" + status.toString() + "\n" + JSON.stringify(data, null, 2));
                });
        } else {
            alert('invalid params, please check your input');
        }
      };
  }]
)
