app.controller('PostsCtrl', [
        '$scope', '$stateParams', 'Post', 'Subject', 'Area',
        function($scope, $stateParams, Post, Subject, Area){
            Post.get(
                {
                    areaId: $stateParams.areaId,
                    subjectId: $stateParams.subjectId
                }
            ).$promise.then(function(response){
                $scope.posts = response.results;
            });

            Subject.get(
                {
                    areaId: $stateParams.areaId,
                    id: $stateParams.subjectId
                }
            ).$promise.then(function(response){
                $scope.subject = response;
            });

            Area.get(
                {id: $stateParams.areaId}
            ).$promise.then(function(response){
                $scope.area = response;
            });
        }
    ])

    .controller('PostCtrl', [
        '$scope', '$stateParams', 'Post', 'Subject', 'Area',
        function($scope, $stateParams, Post, Subject, Area){

            Post.get(
                {
                    areaId: $stateParams.areaId,
                    subjectId: $stateParams.subjectId,
                    id: $stateParams.id
                }
            ).$promise.then(function(response){
                $scope.post = response;
            });

            Subject.get(
                {
                    areaId: $stateParams.areaId,
                    id: $stateParams.subjectId
                }
            ).$promise.then(function(response){
                $scope.subject = response;
            });

            Area.get(
                {id: $stateParams.areaId}
            ).$promise.then(function(response){
                $scope.area = response;
            });
        }
    ]);
