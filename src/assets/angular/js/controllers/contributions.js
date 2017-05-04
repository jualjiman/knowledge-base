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
    '$scope', '$stateParams', '$filter','$localStorage', 'ProfileContribution', 'Subject',
    function($scope, $stateParams, $filter, $localStorage, ProfileContribution, Subject){

        $scope.profileInfo = $localStorage.profileInfo;

        ProfileContribution.get({id: $stateParams.postId}).$promise.then(function(response){
            $scope.post = response;
            $scope.hasEditPermissions = $filter('hasEditPermissions')(
                $scope.post,
                $scope.profileInfo.id
            );

            Subject.get(
                {
                    areaId: response.subject.category.area.id,
                    categoryId: response.subject.category.id,
                    id: response.subject.id
                }
            ).$promise.then(function(response){
                $scope.subject = response;
            });
        });    
    }
])

.controller('CreatePostCtrl', [
    '$scope', '$state', '$stateParams','Area', 'Category', 'Subject', 'User', 'ProfileContribution', 'toastr', 'marked',
    function($scope, $state, $stateParams, Area, Category, Subject, User, ProfileContribution, toastr, marked){
        $scope.post = {
            isActive: true
        };

        Area.get().$promise.then(function(response){
            $scope.areas = response.results;

            //
            // Adding preloaded fields.
            //
            reloadSelectFields();
            $scope.post.area = parseInt($stateParams.areaId);

            $scope.loadCategories();
            $scope.post.category = parseInt($stateParams.categoryId);

            $scope.loadSubjects();
            $scope.post.subject = parseInt($stateParams.subjectId);
        });

        $scope.loadCategories = function(){
            if($scope.post.area){
                Category.get(
                    {
                        areaId: $scope.post.area
                    }
                ).$promise.then(function(response){
                    $scope.categories = response.results;
                    //
                    // this function should be executed here, because
                    // material select field should be updated when data is ready.
                    //
                    reloadSelectFields();
                });
            } else {
                $scope.categories = null;
                reloadSelectFields();
            }
        };

        $scope.loadSubjects = function(){
            if($scope.post.category){
                Subject.get(
                    {
                        areaId: $scope.post.area,
                        categoryId: $scope.post.category
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
        // Autocomplete fields.
        //
        // Available to
        $scope.availableTo = angular.element('#availableToField').materialize_autocomplete({
            limit: 5,
            multiple: {
                enable: true
            },
            appender: {
                el: '.aac-users'
            },
            dropdown: {
                el: '#availableMultipleDropdown'
            },
            getData: function(value, callback){
                User.get({q: value}).$promise.then(function(response){
                    var data = response.results;
                    callback(value, data);
                });
            }
        });

        // Editable to
        $scope.editableTo = angular.element('#editableToField').materialize_autocomplete({
            limit: 5,
            multiple: {
                enable: true
            },
            appender: {
                el: '.eac-users'
            },
            dropdown: {
                el: '#editableMultipleDropdown'
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
            $scope.post.listEditableTo = [];

            angular.forEach($scope.availableTo.value, function(item){
                $scope.post.listAvailableTo.push(item.id);
            });

            angular.forEach($scope.editableTo.value, function(item){
                $scope.post.listEditableTo.push(item.id);
            });

            ProfileContribution.save($scope.post).$promise.then(function(){
                toastr.success('Publicación creada correctamente');
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

        function reloadSelectFields(){
            setTimeout(function(){
                angular.element('select').material_select();
            }, 300);
        }

        function goToPreviousState(){
            if($state.previous.state.name !== ''){
                return $state.go($state.previous.state.name, $state.previous.params);
            }
            return $state.go('panel.contributions');
        }

        angular.element('#content').keydown(textareaAllowTabs);

        // Initializing materialize fields.
        angular.element('ul.tabs').tabs();

    }
])

.controller('CreateContributionCtrl', [
    '$scope', '$state', 'Area', 'Category', 'Subject', 'User', 'ProfileContribution', 'toastr', 'marked',
    function($scope, $state, Area, Category, Subject, User, ProfileContribution, toastr, marked){
        $scope.post = {
            isActive: true  
        };

        Area.get().$promise.then(function(response){
            $scope.areas = response.results;
            reloadSelectFields();
        });

        $scope.loadCategories = function(){
            if($scope.post.area){
                Category.get(
                    {
                        areaId: $scope.post.area
                    }
                ).$promise.then(function(response){
                    $scope.categories = response.results;
                    //
                    // this function should be executed here, because
                    // material select field should be updated when data is ready.
                    //
                    reloadSelectFields();
                });
            } else {
                $scope.categories = null;
                reloadSelectFields();
            }
        };

        $scope.loadSubjects = function(){
            if($scope.post.category){
                Subject.get(
                    {
                        areaId: $scope.post.area,
                        categoryId: $scope.post.category
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
        // Autocomplete fields.
        //
        // Available to
        $scope.availableTo = angular.element('#availableToField').materialize_autocomplete({
            limit: 5,
            multiple: {
                enable: true
            },
            appender: {
                el: '.aac-users'
            },
            dropdown: {
                el: '#availableMultipleDropdown'
            },
            getData: function(value, callback){
                User.get({q: value}).$promise.then(function(response){
                    var data = response.results;
                    callback(value, data);
                });
            }
        });

        // Editable to
        $scope.editableTo = angular.element('#editableToField').materialize_autocomplete({
            limit: 5,
            multiple: {
                enable: true
            },
            appender: {
                el: '.eac-users'
            },
            dropdown: {
                el: '#editableMultipleDropdown'
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
            $scope.post.listEditableTo = [];

            angular.forEach($scope.availableTo.value, function(item){
                $scope.post.listAvailableTo.push(item.id);
            });

            angular.forEach($scope.editableTo.value, function(item){
                $scope.post.listEditableTo.push(item.id);
            });

            ProfileContribution.save($scope.post).$promise.then(function(){
                toastr.success('Publicación creada correctamente');
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

        function reloadSelectFields(){
            setTimeout(function(){
                angular.element('select').material_select();
            }, 300);
        }

        function goToPreviousState(){
            if($state.previous.state.name !== ''){
                return $state.go($state.previous.state.name, $state.previous.params);
            }
            return $state.go('panel.contributions');
        }

        angular.element('#content').keydown(textareaAllowTabs);

        // Initializing materialize fields.
        angular.element('ul.tabs').tabs();
    }
])

.controller('EditContributionCtrl', [
    '$scope', '$state', '$stateParams', 'Area', 'Subject', 'Category', 'User', 'ProfileContribution', 'toastr', 'marked',
    function($scope, $state, $stateParams, Area, Subject, Category, User, ProfileContribution, toastr, marked){

        Area.get().$promise.then(function(response){
            $scope.areas = response.results;

            ProfileContribution.get({id: $stateParams.postId}).$promise.then(function(response){
                $scope.post = {
                    id: response.id,
                    area: response.subject.category.area.id,
                    category: response.subject.category.id,
                    subject: response.subject.id,
                    content: response.content,
                    resume: response.resume,
                    name: response.name,
                    isActive: response.isActive
                };

                $scope.loadCategories();
                $scope.post.category = response.subject.category.id;

                $scope.loadSubjects();
                $scope.post.subject = response.subject.id;

                //
                // Autocomplete fields.
                //
                // Available to
                $scope.availableTo = angular.element('#availableToField').materialize_autocomplete({
                    limit: 5,
                    multiple: {
                        enable: true
                    },
                    appender: {
                        el: '.aac-users'
                    },
                    dropdown: {
                        el: '#availableMultipleDropdown'
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

                // Editable to
                $scope.editableTo = angular.element('#editableToField').materialize_autocomplete({
                    limit: 5,
                    multiple: {
                        enable: true
                    },
                    appender: {
                        el: '.eac-users'
                    },
                    dropdown: {
                        el: '#editableMultipleDropdown'
                    },
                    getData: function(value, callback){
                        User.get({q: value}).$promise.then(function(response){
                            var data = response.results;
                            callback(value, data);
                        });
                    }
                });

                angular.forEach(response.editableTo, function(item){
                    $scope.editableTo.setValue(item);
                });
                // Initializing select fields.
                reloadSelectFields();
                angular.element('ul.tabs').tabs();
            });
        });

        $scope.save = function(){
            $scope.post.listAvailableTo = [];
            $scope.post.listEditableTo = [];

            angular.forEach($scope.availableTo.value, function(item){
                $scope.post.listAvailableTo.push(item.id);
            });

            angular.forEach($scope.editableTo.value, function(item){
                $scope.post.listEditableTo.push(item.id);
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

        $scope.loadCategories = function(){
            if($scope.post.area){
                Category.get(
                    {
                        areaId: $scope.post.area
                    }
                ).$promise.then(function(response){
                    $scope.categories = response.results;
                    //
                    // this function should be executed here, because
                    // material select field should be updated when data is ready.
                    //
                    reloadSelectFields();
                });
            } else {
                $scope.categories = null;
                reloadSelectFields();
            }
        };

        $scope.loadSubjects = function(){
            if($scope.post.category){
                Subject.get(
                    {
                        areaId: $scope.post.area,
                        categoryId: $scope.post.category
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
                angular.element('select').material_select();
                Materialize.updateTextFields();
            }, 300);
        }

        function goToPreviousState(){
            if($state.previous.state.name !== ''){
                return $state.go($state.previous.state.name, $state.previous.params);
            }
            return $state.go('panel.contributions');
        }

        angular.element('#content').keydown(textareaAllowTabs);
    }
]);
