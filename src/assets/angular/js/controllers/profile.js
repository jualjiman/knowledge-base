app
.controller('EditProfileCtrl', [
    '$scope', '$state', '$stateParams', '$localStorage', 'Area', 'Profile', 'toastr',
    function($scope, $state, $stateParams, $localStorage, Area, Profile, toastr){


        Area.get().$promise.then(function(response){
            $scope.areas = response.results;

            Profile.get().$promise.then(function(response){

                updateProfileObject(response); 

                // Initializing select fields.
                reloadSelectFields();
                $('ul.tabs').tabs();
            });

            $scope.deleteImage = function($event){
                $event.preventDefault();

                mbox.confirm('¿Eliminar imagen de perfil?', function(yes) {
                    if (yes) {
                        Profile.deleteImage().$promise.then(function(){
                            $scope.profile.thumbnail = "http://placehold.it/200x200";
                            toastr.success('Imagen eliminada correctamente');
                        }).catch(function(response){
                            toastr.error(prepareErrorMessagesWithTitles(response));
                        });
                    }
                });
            };

            $scope.save = function(){
                Profile.update($scope.profile).$promise.then(function(response){
                    updateProfileObject(response); 
                    toastr.success('Perfil actualizado correctamente');
                    return $state.go('panel.areas', {}, { reload: true });
                }).catch(function(response){
                    toastr.error(prepareErrorMessagesWithTitles(response));
                    return $state.go('panel.areas', {}, { reload: true });
                });
            };

        });

        function updateProfileObject(response){
            $localStorage.profileInfo = response;

            $scope.profile = {
                id: response.id,
                name: response.name,
                description: response.description,
                email: response.email,
                thumbnail: response.thumbnail
            };

            // Area is not a mandatory field.
            if(response.area){
                $scope.profile.area = response.area.id;
            }

            if(!response.thumbnail){
                $scope.profile.thumbnail = "http://placehold.it/200x200";
            }

            return $scope.profile;
            
        };

        function reloadSelectFields(){
            setTimeout(function(){
                $('select').material_select();
                Materialize.updateTextFields();
            }, 100);
        }
     }
]);
