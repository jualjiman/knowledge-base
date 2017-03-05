app.directive('profileInfo', [
    '$localStorage', '$content', '$state', 'Profile',
    function($localStorage, $content, $state, Profile) {
        return {
          restrict: 'E',
          templateUrl: $content.url('angular/directives/profile-info.html'),
          link: function(scope) {
            
            // Placing a placeholder, when thumbnail is not given.
            var thumbnail = $localStorage.profileInfo.thumbnail;
            if(!thumbnail){
                thumbnail = 'http://placehold.it/100x100'
            }
            scope.profileInfo = {
                name: $localStorage.profileInfo.name,
                email: $localStorage.profileInfo.email,
                thumbnail: thumbnail
            };

            scope.logout = function(){
                delete $localStorage.token;
                delete $localStorage.profileInfo;
                return $state.go('login');
            };

            return scope;
          }
        };
    }
]);
