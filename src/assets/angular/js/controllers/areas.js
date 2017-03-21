app.controller('AreaCtrl', [
    '$scope', 'Area',
    function($scope, Area){
        Area.get().$promise.then(function(response){
            $scope.areas = response.results;
            setTimeout(function(){
                $(".button-collapse").sideNav();
            }, 200);
        });
    }
]);
