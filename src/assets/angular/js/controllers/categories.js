app.controller('CategoriesCtrl', [
        '$scope', '$stateParams', 'Category', 'Area',
        function($scope, $stateParams, Category, Area){
            Category.get(
                {areaId: $stateParams.areaId}
            ).$promise.then(function(response){
                $scope.categories = response.results;
            });

            Area.get(
                {id: $stateParams.areaId}
            ).$promise.then(function(response){
                $scope.area = response;
            });
        }
    ]);
