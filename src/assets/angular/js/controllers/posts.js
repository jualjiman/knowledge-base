app.controller('PostsCtrl', [
    '$scope', '$stateParams', '$localStorage', 'Post', 'Subject',
    function($scope, $stateParams, $localStorage, Post, Subject){
        $scope.profileInfo = $localStorage.profileInfo;
        Post.get(
            {
                areaId: $stateParams.areaId,
                categoryId: $stateParams.categoryId,
                subjectId: $stateParams.subjectId
            }
        ).$promise.then(function(response){
            $scope.posts = response.results;
        });

        Subject.get(
            {
                areaId: $stateParams.areaId,
                categoryId: $stateParams.categoryId,
                id: $stateParams.subjectId
            }
        ).$promise.then(function(response){
            $scope.subject = response;
        });
    }
])

.controller('PostCtrl', [
    '$scope', '$stateParams', '$filter', '$localStorage', 'Post', 'Subject',
    function($scope, $stateParams, $filter, $localStorage, Post, Subject){

        $scope.profileInfo = $localStorage.profileInfo;

        Post.get(
            {
                areaId: $stateParams.areaId,
                categoryId: $stateParams.categoryId,
                subjectId: $stateParams.subjectId,
                id: $stateParams.id
            }
        ).$promise.then(function(response){
            $scope.post = response;
            $scope.hasEditPermissions = $filter('hasEditPermissions')(
                $scope.post,
                $scope.profileInfo.id
            );
        });

        Subject.get(
            {
                areaId: $stateParams.areaId,
                categoryId: $stateParams.categoryId,
                id: $stateParams.subjectId
            }
        ).$promise.then(function(response){
            $scope.subject = response;
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
