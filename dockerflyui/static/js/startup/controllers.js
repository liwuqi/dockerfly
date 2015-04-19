$('.collapse').collapse({toggle:true});
var startupControllers = angular.module('startupControllers', []);

startupControllers.controller('FormController', ['$scope', '$http', '$timeout', '$modal',
    function($scope, $http, $timeout, $modal) {
      if (!Date.now) {
          Date.now = function() { return new Date().getTime(); }
      }

      images = new Array();
      $http.get('/api/images').success(function(data, status, headers, config) {
          for (var i = 0; i < data['images'].length; i++) {
                images[i] = {
                                value: data['images'][i],
                                label: data['images'][i],
                            };
          };

          $scope.refreshSelect = function(schema, options, search) {
            console.log('refreshSelect is called');
            return images;
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
                  format: 'uiselect',
                  uiClass: 'short_select',
                  items: images,
                   options: {
                     refreshDelay: 100,
                     callback: $scope.refreshSelect
                   },
                  description: 'select your base image of container',
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
                        htmlClass: 'col-md-4',
                        items: [
                            'container_name',
                        ]
                    },
                    {
                        type: 'section',
                        htmlClass: 'col-md-4',
                        items: [
                            'run_cmd',
                        ]
                    },
                    {
                        type: 'section',
                        htmlClass: 'col-md-4',
                        items: [
                            'desc',
                        ]
                    },
                ]
            },
             {
               key: 'image_name',
               placeholder: 'please select your docker image',
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
                        htmlClass: 'col-md-12',
                        items: [
                            'gateway',
                        ]
                    },
                    {
                        type: 'section',
                        htmlClass: 'col-md-12',
                        items: [
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

          //ok, let's do creat a container
          $scope.onSubmit = function(form) {
            $scope.$broadcast('schemaFormValidate');

            if(form.$valid) {
                console.log("create container");

                //check if ip and eth name is unique
                var eths = $scope.map($scope.containerModel.eths, function(eth){return eth['eth_name']});
                var ips = $scope.map($scope.containerModel.eths, function(eth){return eth['ip']});
                if (DockerflyUI.checkDuplicates(eths)) {
                    var alertModal = $modal({
                                title: 'Error',
                                content: 'You set duplicate eth!',
                                show: false, backdrop: false});
                    alertModal.$promise.then(alertModal.show);
                    return;
                }
                if (DockerflyUI.checkDuplicates(ips)) {
                    var alertModal = $modal({
                                title: 'Error',
                                content: 'You set duplicate IP!',
                                show: false, backdrop: false});
                    alertModal.$promise.then(alertModal.show);
                    return;
                }

                //normalize post params
                var postParams = angular.copy($scope.containerModel);
                postParams.eths = new Array();
                for (i=0; i<$scope.containerModel.eths.length; i++) {
                        postParams.eths[i] = new Array();
                        postParams.eths[i][0] = $scope.containerModel.eths[i]['eth_name'];
                        postParams.eths[i][1] = $scope.containerModel.eths[i]['attach_to'];
                        postParams.eths[i][2] = $scope.containerModel.eths[i]['ip'];
                }

                postParams['status'] = 'running';
                console.log(postParams);
                var postParamsWrapper = new Array(postParams);

                $http.post('/api/containers', data=postParamsWrapper)
                    .success(function(data, status, headers, config){
                        var alertModal = $modal({
                                    title: 'Success',
                                    content: 'You set a new container! <br /> <br />' +
                                             'status:' + status.toString() + '<br />' +
                                             'info:' + JSON.stringify(data, null, 2),
                                    show: false, backdrop: false});
                        alertModal.$promise.then(alertModal.show);

                    })
                    .error(function(data, status, headers, config){
                        var alertModal = $modal({
                                    title: 'Error',
                                    content: 'That something was not right here! <br /> <br />' +
                                             'status:' + status.toString() + '<br />' +
                                             'info:' + JSON.stringify(data, null, 2),
                                    show: false, backdrop: false});
                        alertModal.$promise.then(alertModal.show);

                        alert("status" + status.toString() + "\n" + JSON.stringify(data, null, 2));
                    });
            } else {
                var alertModal = $modal({
                            title: 'Error',
                            content: 'Invalid params, please check your input!',
                            show: false, backdrop: false});
                alertModal.$promise.then(alertModal.show);
            }
          };
      });
  }]
)
