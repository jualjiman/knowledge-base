app.controller('SubjectsCtrl', [
    '$scope', '$stateParams', '$localStorage', 'Subject', 'Category',
    function($scope, $stateParams, $localStorage, Subject, Category){
        $scope.profileInfo = $localStorage.profileInfo;
        Subject.get(
            {
                areaId: $stateParams.areaId,
                categoryId: $stateParams.categoryId
            }
        ).$promise.then(function(response){
            $scope.subjects = response.results;
        });

        Category.get(
            {
                areaId: $stateParams.areaId,
                id: $stateParams.categoryId
            }
        ).$promise.then(function(response){
            $scope.category = response;
        });
    }
]);
