'use strict';

describe('myApp.container.module', function() {

  beforeEach(module('myApp.container'));

  describe('container controller', function(){

    it('should ....', inject(function($controller) {
      //spec body
      var ContainerCtrl = $controller('ContainerCtrl');
      expect(ContainerCtrl).toBeDefined();
    }));

  });
});
