app.controller('AuthCtrl', [
    '$scope', '$localStorage', '$state', 'toastr', 'Auth', 'Profile',
    function($scope, $localStorage, $state, toastr, Auth, Profile){

        if ($localStorage.token) {
            return $state.go('panel.areas');
        }

        delete $localStorage.token;
        delete $localStorage.profileInfo;

        $scope.is_login_operation = true;
        $scope.credentials = {};
        $scope.registrationInfo = {};

        $scope.login = function(){
            Auth.login($scope.credentials).$promise.then(function(response){
                $localStorage.token = response.token;

                Profile.get().$promise.then(function(response){
                    $localStorage.profileInfo = response;
                    return $state.go('panel.areas');

                });
            }).catch(function(response){
                toastr.error('Credenciales invalidas', 'Error');
            });
        };

        $scope.register = function(){
            Auth.signup().$promise.then(function(response){
                $scope.areas = response;
            });
        };

        $scope.toggleOperation = function(){
            $scope.is_login_operation = !$scope.is_login_operation;
        };
    }
]);
