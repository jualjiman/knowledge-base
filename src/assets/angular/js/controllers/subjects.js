app.controller('SubjectCtrl', [
        '$scope', '$stateParams', 'Subject', 'Area',
        function($scope, $stateParams, Subject, Area){
            Subject.get(
                {areaId: $stateParams.areaId}
            ).$promise.then(function(response){
                $scope.subjects = response.results;
            });

            Area.get(
                {id: $stateParams.areaId}
            ).$promise.then(function(response){
                $scope.area = response;
            });
        }
    ]);
