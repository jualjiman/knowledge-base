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
                var errorData = prepareErrorMessages(response)
                return toastr.error(errorData.info, errorData.statusText);
            });
        };

        $scope.register = function(){
            Auth.signup($scope.registrationInfo).$promise.then(function(response){
                $scope.registrationInfo = {};
                toastr.success('Registrado correctamente, revisa tu correo electronico para activar tu cuenta');
                $scope.is_login_operation = true;
            }).catch(function(response){
                var errorData = prepareErrorMessages(response)
                return toastr.error(errorData.info, errorData.statusText);
            });
        };

        $scope.toggleOperation = function(){
            $scope.is_login_operation = !$scope.is_login_operation;
        };
    }
]);
