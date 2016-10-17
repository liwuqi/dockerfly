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
                  default: 'bpc_for_cups',
                  title : '设置你的项目名字，只支持英文'
              },
              gateway: {
                  type: 'string',
                  default: '172.16.13.1',
                  pattern: '^(\\d|[1-9]\\d|1\\d\\d|2([0-4]\\d|5[0-5]))\\.(\\d|[1-9]\\d|1\\d\\d|2([0-4]\\d|5[0-5]))\\.(\\d|[1-9]\\d|1\\d\\d|2([0-4]\\d|5[0-5]))\\.(\\d|[1-9]\\d|1\\d\\d|2([0-4]\\d|5[0-5]))$',
                  title : '设置网关',
                  validationMessage: " "
              },
              desc: {
                  type: 'string',
                  default: 'xx银行\nhttp://kb.netis.com.cn:8090/pages/xxxxx',
                  title : '对这个项目简要描述一下'
              },
              run_cmd: {
                  type: 'string',
                  default: '/usr/bin/svscan /etc/dockerservices',
                  title: '镜像启动命令，默认不用修改'
              },
              image_name: {
                  type: 'string',
                  format: 'uiselect',
                  uiClass: 'short_select',
                  items: images,
                   options: {
                     refreshDelay: 100,
                     callback: $scope.refreshSelect
                   },
                  title: '选择合适的镜像',
              },
              eths: {
                  type: 'array',
                  items: {
                      type: 'object',
                      properties: {
                          eth_name: {
                            type: 'string',
                            default: 'veth1',
                            title: '新建一个虚拟网卡 (veth1--veth100)',
                          },
                          attach_to: {
                            type: 'string',
                            default: 'eth1',
                            title: '虚拟网卡的物理母卡，默认不用修改',
                          },
                          ip: {
                            type: 'string',
                            default: '0.0.0.0/24',
                            pattern: '^(\\d|[1-9]\\d|1\\d\\d|2([0-4]\\d|5[0-5]))\\.(\\d|[1-9]\\d|1\\d\\d|2([0-4]\\d|5[0-5]))\\.(\\d|[1-9]\\d|1\\d\\d|2([0-4]\\d|5[0-5]))\\.(\\d|[1-9]\\d|1\\d\\d|2([0-4]\\d|5[0-5]))/([1-2]\\d|3[0-2]|\\d)$',
                            validationMessage: " ",
                            title: '虚拟网卡IP，如果设置为0.0.0.0/24则代表不分配IP,用于回放流量'
                          },
                          promisc : {
                            type: 'boolean',
                            title: '是否设为混杂模式',
                            default: false,
                            enum: [true, false]
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
                helpvalue: '<div class="alert alert-info">定制Docker虚机</div>'
            },
            {
                htmlClass: 'row',
                type: 'section',
                items: [
                    {
                        type: 'section',
                        htmlClass: 'col-md-12',
                        items: [
                            'container_name',
                        ]
                    },
                    {
                        type: 'section',
                        htmlClass: 'col-md-12',
                        items: [
                            'run_cmd',
                        ]
                    },
                ]
            },
            {
                key: 'desc',
                type: 'textarea',
            },
            {
               key: 'image_name',
               placeholder: 'please select your docker image',
            },
            {
                type: 'help',
                helpvalue: '<div class="alert alert-info">定制虚拟网络</div>'
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

          $scope.onSubmit = function(form) {
            $scope.$broadcast('schemaFormValidate');

            if(form.$valid) {
                //ok, let's do creat a container
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
                        postParams.eths[i][3] = $scope.containerModel.eths[i]['promisc'];
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
                                             'info:' + JSON.stringify(data, null, 2).replace(/\n/g, '<br />'),
                                    show: false, backdrop: false});
                        alertModal.$promise.then(alertModal.show);

                    })
                    .error(function(data, status, headers, config){
                        var alertModal = $modal({
                                    title: 'Error',
                                    content: 'That something was not right here! <br /> <br />' +
                                             'status:' + status.toString() + '<br />' +
                                             'info:' + JSON.stringify(data, null, 2).replace(/\n/g, '<br />'),
                                    show: false, backdrop: false});
                        alertModal.$promise.then(alertModal.show);
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
.directive('ngEnter', function () {
    return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if(event.which === 13) {
                scope.$apply(function (){
                    scope.$eval(attrs.ngEnter);
                });

                event.preventDefault();
            }
        });
    };
});
