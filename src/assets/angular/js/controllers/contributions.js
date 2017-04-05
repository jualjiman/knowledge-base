app.controller('ContributionsCtrl', [
    '$scope', '$localStorage', 'ProfileContribution', 'toastr',
    function($scope, $localStorage, ProfileContribution, toastr){

        $scope.profileInfo = $localStorage.profileInfo;

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
    '$scope', '$stateParams', '$localStorage', 'ProfileContribution', 'Subject', 'Area',
    function($scope, $stateParams, $localStorage, ProfileContribution, Subject, Area){

        $scope.profileInfo = $localStorage.profileInfo;

        ProfileContribution.get({id: $stateParams.postId}).$promise.then(function(response){
            $scope.post = response;

            Subject.get(
                {
                    areaId: response.subject.area.id,
                    id: response.subject.id
                }
            ).$promise.then(function(response){
                $scope.subject = response;
            });

            Area.get(
                {id: response.subject.area.id}
            ).$promise.then(function(response){
                $scope.area = response;
            });
        });    
    }
])

.controller('CreatePostCtrl', [
    '$scope', '$state', '$stateParams','Area', 'Subject', 'User', 'ProfileContribution', 'toastr', 'marked',
    function($scope, $state, $stateParams, Area, Subject, User, ProfileContribution, toastr, marked){
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
                    //
                    // this function should be executed here, because
                    // material select field should be updated when data is ready.
                    //
                    reloadSelectFields();
                });
            } else {
                $scope.subjects = null;
                reloadSelectFields();
            }
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
                return $state.go(
                    'panel.posts',
                    {
                        areaId: $scope.post.area,
                        subjectId: $scope.post.subject
                    }
                );
            }).catch(function(response){
                var errorData = prepareErrorMessages(response)
                toastr.error(errorData.info, errorData.statusText);
                return $state.go('panel.contributions');
            });
        };

        $scope.generatePreview = function(){
            angular.element("#post-preview").html(marked($scope.post.content));
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
    '$scope', '$state', 'Area', 'Subject', 'User', 'ProfileContribution', 'toastr', 'marked',
    function($scope, $state, Area, Subject, User, ProfileContribution, toastr, marked){
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
                    //
                    // this function should be executed here, because
                    // material select field should be updated when data is ready.
                    //
                    reloadSelectFields();
                });
            } else {
                $scope.subjects = null;
                reloadSelectFields();
            }
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
                var errorData = prepareErrorMessages(response)
                toastr.error(errorData.info, errorData.statusText);
                return $state.go('panel.contributions');
            });
        };

        $scope.generatePreview = function(){
            angular.element("#post-preview").html(marked($scope.post.content));
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
    '$scope', '$state', '$stateParams', 'Area', 'Subject', 'User', 'ProfileContribution', 'toastr', 'marked',
    function($scope, $state, $stateParams, Area, Subject, User, ProfileContribution, toastr, marked){

        Area.get().$promise.then(function(response){
            $scope.areas = response.results;

            ProfileContribution.get({id: $stateParams.postId}).$promise.then(function(response){
                $scope.post = {
                    id: response.id,
                    area: response.subject.area.id,
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
                goToPreviousState();
            }).catch(function(response){
                var errorData = prepareErrorMessages(response)
                toastr.error(errorData.info, errorData.statusText);
                goToPreviousState();
            });
        };

        $scope.generatePreview = function(){
            angular.element("#post-preview").html(marked($scope.post.content));
        };

        $scope.loadSubjects = function(){
            if($scope.post.area){
                Subject.get(
                    {
                        areaId: $scope.post.area
                    }
                ).$promise.then(function(response){
                    $scope.subjects = response.results;
                    //
                    // this function should be executed here, because
                    // material select field should be updated when data is ready.
                    //
                    reloadSelectFields();
                });
            } else {
                $scope.subjects = null;
                reloadSelectFields();
            }
        };

        function reloadSelectFields(){
            setTimeout(function(){
                $('select').material_select();
                Materialize.updateTextFields();
            }, 300);
        }

        function goToPreviousState(){
            if($state.previous.state.name !== ''){
                return $state.go($state.previous.state.name, $state.previous.params);
            }
            return $state.go('panel.contributions');
        }

        $('#content').keydown(textareaAllowTabs);
    }
]);
