app.controller('ContributionsCtrl', [
    '$scope', 'ProfileContributions',
    function($scope, ProfileContributions){
        ProfileContributions.get().$promise.then(function(response){
            $scope.contributions = response.results;
            console.log($scope.contributions);
        });
    }
]);
