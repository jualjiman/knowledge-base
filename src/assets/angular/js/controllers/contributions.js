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
            mbox.confirm('¿Eliminar publicación?', function(yes) {
                if (yes) {
                    ProfileContribution.remove({id: postId}).$promise.then(function(){
                        toastr.success('Publicación eliminada correctamente.');
                        loadContributions()
                    });
                }
            });
        };
        
        loadContributions();
    }
])

.controller('ContributionCtrl', [
    '$scope', '$stateParams', 'ProfileContribution', 'Subject', 'Area',
    function($scope, $stateParams, ProfileContribution, Subject, Area){

        ProfileContribution.get({id: $stateParams.postId}).$promise.then(function(response){
            $scope.post = response;

            response.subject.parentIds.areaId,
            Subject.get(
                {
                    areaId: response.subject.parentIds.areaId,
                    id: response.subject.id
                }
            ).$promise.then(function(response){
                $scope.subject = response;
            });

            Area.get(
                {id: response.subject.parentIds.areaId}
            ).$promise.then(function(response){
                $scope.area = response;
            });
        });    
    }
])

.controller('CreatePostCtrl', [
    '$scope', '$state', '$stateParams','Area', 'Subject', 'User', 'ProfileContribution', 'toastr',
    function($scope, $state, $stateParams, Area, Subject, User, ProfileContribution, toastr){
        $scope.post = {
            isActive: true
        };

        Area.get().$promise.then(function(response){
            $scope.areas = response.results;

            reloadSelectFields();
            $scope.post.area = parseInt($stateParams.areaId);
            $scope.loadSubjects();
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
        
        //
        // Adding preloaded subject field.
        //
        $scope.loadSubjects();
        $scope.post.subject = parseInt($stateParams.subjectId);

        //
        // Autocomplete field.
        //
        $scope.availableTo = $('#multipleInput').materialize_autocomplete({
            multiple: {
                enable: true
            },
            appender: {
                el: '.ac-users'
            },
            dropdown: {
                el: '#multipleDropdown'
            },
            getData: function(value, callback){
                User.get({q: value}).$promise.then(function(response){
                    var data = response.results;
                    callback(value, data);
                });
            }
        });

        $scope.save = function(){
            $scope.post.listAvailableTo = [];

            angular.forEach($scope.availableTo.value, function(item){
                $scope.post.listAvailableTo.push(item.id);
            });

            ProfileContribution.save($scope.post).$promise.then(function(){
                toastr.success('Publicación creada correctamente');
                return $state.go('panel.contributions');
            }).catch(function(response){
                toastr.error('Error al crear la publicación');
                return $state.go('panel.contributions');
            });
        };

        function reloadSelectFields(){
            setTimeout(function(){
                $('select').material_select();
            }, 300);
        }

        $('#content').keydown(textareaAllowTabs);

        // Initializing materialize fields.
        $('ul.tabs').tabs();

    }
])

.controller('CreateContributionCtrl', [
    '$scope', '$state', 'Area', 'Subject', 'User', 'ProfileContribution', 'toastr',
    function($scope, $state, Area, Subject, User, ProfileContribution, toastr){
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

        //
        // Autocomplete field.
        //
        $scope.availableTo = $('#multipleInput').materialize_autocomplete({
            multiple: {
                enable: true
            },
            appender: {
                el: '.ac-users'
            },
            dropdown: {
                el: '#multipleDropdown'
            },
            getData: function(value, callback){
                User.get({q: value}).$promise.then(function(response){
                    var data = response.results;
                    callback(value, data);
                });
            }
        });

        $scope.save = function(){
            $scope.post.listAvailableTo = [];

            angular.forEach($scope.availableTo.value, function(item){
                $scope.post.listAvailableTo.push(item.id);
            });

            ProfileContribution.save($scope.post).$promise.then(function(){
                toastr.success('Publicación creada correctamente');
                return $state.go('panel.contributions');
            }).catch(function(response){
                toastr.error('Error al crear la publicación');
                return $state.go('panel.contributions');
            });
        };

        function reloadSelectFields(){
            setTimeout(function(){
                $('select').material_select();
            }, 300);
        }

        $('#content').keydown(textareaAllowTabs);

        // Initializing materialize fields.
        $('ul.tabs').tabs();
    }
])

.controller('EditContributionCtrl', [
    '$scope', '$state', '$stateParams', 'Area', 'Subject', 'User', 'ProfileContribution', 'toastr',
    function($scope, $state, $stateParams, Area, Subject, User, ProfileContribution, toastr){

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

                //
                // Autocomplete field.
                //
                $scope.availableTo = $('#multipleInput').materialize_autocomplete({
                    multiple: {
                        enable: true
                    },
                    appender: {
                        el: '.ac-users'
                    },
                    dropdown: {
                        el: '#multipleDropdown'
                    },
                    getData: function(value, callback){
                        User.get({q: value}).$promise.then(function(response){
                            var data = response.results;
                            callback(value, data);
                        });
                    }
                });

                angular.forEach(response.availableTo, function(item){
                    $scope.availableTo.setValue(item);
                });


                // Initializing select fields.
                reloadSelectFields();
                $('ul.tabs').tabs();
            });
        });

        $scope.save = function(){
            $scope.post.listAvailableTo = [];

            angular.forEach($scope.availableTo.value, function(item){
                $scope.post.listAvailableTo.push(item.id);
            });

            ProfileContribution.update({id: $stateParams.postId}, $scope.post).$promise.then(function(){
                toastr.success('Publicación actualizada correctamente');
                return $state.go('panel.contributions');
            }).catch(function(response){
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
            }, 300);
        }

        $('#content').keydown(textareaAllowTabs);
    }
]);
