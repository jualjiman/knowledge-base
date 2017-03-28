app.controller('PostsCtrl', [
        '$scope', '$stateParams', '$localStorage', 'Post', 'Subject', 'Area',
        function($scope, $stateParams, $localStorage, Post, Subject, Area){
            $scope.profileInfo = $localStorage.profileInfo;
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
        '$scope', '$stateParams', '$localStorage', 'Post', 'Subject', 'Area',
        function($scope, $stateParams, $localStorage, Post, Subject, Area){

            $scope.profileInfo = $localStorage.profileInfo;

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
    ])

    .controller('HeaderSearchCtrl', [
        '$scope','$state' ,'$stateParams', 'Post',
        function($scope, $state, $stateParams, Post){
            $scope.q = '';

            $scope.submit = function(){
                $state.go('panel.searchPosts', {q: $scope.q});
                $scope.q = '';
            };
        }
    ])

    .controller('SearchPostsCtrl', [
        '$scope', '$stateParams', 'Post',
        function($scope, $stateParams, Post){

            $scope.q = $stateParams.q;

            Post.search(
                {
                    q: $stateParams.q,
                }
            ).$promise.then(function(response){
                $scope.matches = response.results;
                $scope.totalMatches = response.count;
            });
        }
    ]);
