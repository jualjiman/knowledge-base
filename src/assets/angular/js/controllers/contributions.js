app.controller('ContributionsCtrl', [
    '$scope', 'ProfileContribution', 'toastr',
    function($scope, ProfileContribution, toastr){

        // Loading contributions.
        function loadContributions(){
            ProfileContribution.get().$promise.then(function(response){
                $scope.contributions = response.results;
            });
        }

        $scope.confirmDelete = function(postId){
            mbox.confirm('Drugs are bad, are you sure you want to use them?', function(yes) {
                if (yes) {
                    ProfileContribution.remove({id: postId}).$promise.then(function(){
                        toastr.success('Publicación eliminada correctamente.');
                        loadContributions()
                    });
                }
            });
        };
        
        loadContributions();
        //Initializing modal.
        $('.modal').modal();
    }
])

.controller('CreateContributionCtrl', [
    '$scope', '$state', 'Area', 'Subject', 'ProfileContribution', 'toastr',
    function($scope, $state, Area, Subject, ProfileContribution, toastr){
        $scope.post = {
            isActive: true  
        };

        Area.get().$promise.then(function(response){
            $scope.areas = response.results;
            reloadSelectFields();
        });

        $scope.loadSubjects = function(){
            if($scope.post.area){
                Subject.get(
                    {
                        areaId: $scope.post.area
                    }
                ).$promise.then(function(response){
                    $scope.subjects = response.results;
                });
            } else {
                $scope.subjects = null;
            }
            reloadSelectFields();
        };
        
        $scope.save = function(){
            ProfileContribution.save($scope.post).$promise.then(function(){
                toastr.success('Publicación creada correctamente');
                return $state.go('panel.contributions');
            }).catch(function(response){
                console.log(response);
                toastr.error('Error al crear la publicación');
            });
        };

        function reloadSelectFields(){
            setTimeout(function(){
                $('select').material_select();
            }, 100);
        }

        // Initializing select fields.
        $('ul.tabs').tabs();
    }
])

.controller('EditContributionCtrl', [
    '$scope', '$state', '$stateParams', 'Area', 'Subject', 'ProfileContribution', 'toastr',
    function($scope, $state, $stateParams, Area, Subject, ProfileContribution, toastr){

        Area.get().$promise.then(function(response){
            $scope.areas = response.results;

            ProfileContribution.get({id: $stateParams.postId}).$promise.then(function(response){
                $scope.post = {
                    id: response.id,
                    area: response.subject.parentIds.areaId,
                    content: response.content,
                    resume: response.resume,
                    name: response.name,
                    isActive: response.isActive
                };

                $scope.loadSubjects();
                $scope.post.subject = response.subject.id;

                // Initializing select fields.
                reloadSelectFields();
                $('ul.tabs').tabs();
            });
        });

        $scope.save = function(){
            ProfileContribution.update({id: $stateParams.postId}, $scope.post).$promise.then(function(){
                toastr.success('Publicación actualizada correctamente');
                return $state.go('panel.contributions');
            }).catch(function(response){
                console.log(response);
                toastr.error('Error al actualizar la publicación');
            });
        };

        $scope.loadSubjects = function(){
            if($scope.post.area){
                Subject.get(
                    {
                        areaId: $scope.post.area
                    }
                ).$promise.then(function(response){
                    $scope.subjects = response.results;
                });
            } else {
                $scope.subjects = null;
            }
            reloadSelectFields();
        };

        function reloadSelectFields(){
            setTimeout(function(){
                $('select').material_select();
                Materialize.updateTextFields();
            }, 100);
        }
    }
]);
