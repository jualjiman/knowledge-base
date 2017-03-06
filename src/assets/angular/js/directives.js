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

            return scope;
          }
        };
    }
])

.directive('navigationMenu', [
    '$localStorage', '$content', '$state', 'Profile',
    function($localStorage, $content, $state, Profile) {
        return {
          restrict: 'E',
          templateUrl: $content.url('angular/directives/navigation-menu.html'),
          link: function(scope) {

            scope.editProfile = function(){
                return $state.go('panel.editProfile');
            };

            scope.logout = function(){
                delete $localStorage.token;
                delete $localStorage.profileInfo;
                return $state.go('login');
            };

            $(".dropdown-button").dropdown();
            return scope;
          }
        };
    }
])

.directive('profileImageUpload', [
    'Profile', 'toastr', '$localStorage',
    function (Profile, toastr, $localStorage) {
    return {
        restrict: 'A',
        scope: {
            value: "="
        },
        link: function (scope, element, attr) {

            element.bind('change', function () {
                var formData = new FormData();
                formData.append('photo', element[0].files[0]);

                Profile.changeImage(formData).$promise.then(function(response){
                    $localStorage.profileInfo = response;
                    scope.value = response.thumbnail;
                    toastr.success('Imagen reemplazada correctamente');
                }).catch(function(response){
                    toastr.error('Error al reemplazar la imagen');
                });
            });

        }
    };
}]);
