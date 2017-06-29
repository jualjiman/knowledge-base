app.config([
    '$stateProvider', '$urlRouterProvider', '$contentProvider', '$httpProvider', '$locationProvider', 'toastrConfig', 'markedProvider',
    function($stateProvider, $urlRouterProvider, $contentProvider, $httpProvider, $locationProvider, toastrConfig, markedProvider) {
        // Configure content base url.
        $contentProvider.urlPrefix = staticUrl;
        
        // Markdown library setup.
        markedProvider.setOptions({
            gfm: true,
            tables: true,
            highlight: function (code, lang) {
                if (lang) {
                    return hljs.highlight(lang, code, true).value;
                } else {
                    return hljs.highlightAuto(code).value;
                }
            }
        });

        markedProvider.setRenderer({
            link: function(url, title, text) {
                var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*/;
                var match = url.match(regExp);

                if(!match){
                    return "<a href='" + url + "'" + (title ? " title='" + text + "'" : '') + " target='_blank'>" + text + "</a>";
                }

                return (
                    '<a href="' + url + '" target="_blank"><p><strong>' + text + '</p></a>' +
                    '<div style="position:relative;height:0;padding-bottom:56.25%">' +
                    '<iframe src="https://www.youtube.com/embed/' + match[7] + '?ecver=2" width="640" height="360" frameborder="0" style="position:absolute;width:100%;height:100%;left:0" allowfullscreen></iframe>' +
                    '</div>'
                );
            }
        });

        // Toastr configurations.
        angular.extend(toastrConfig, {
            target: 'body',
            allowHtml: false,
            closeButton: false,
            closeHtml: '<button>&times;</button>',
            extendedTimeOut: 1000,
            iconClasses: {
                error: 'toast-error',
                info: 'toast-info',
                success: 'toast-success',
                warning: 'toast-warning'
            },  
            messageClass: 'toast-message',
            onHidden: null,
            onShown: null,
            onTap: null,
            progressBar: false,
            tapToDismiss: true,
            templates: {
                toast: $contentProvider.url('angular/directives/toast/toast.html'),
                progressbar: $contentProvider.url('angular/directives/toast/progressbar.html'),
            },
            timeOut: 5000,
            titleClass: 'toast-title',
            toastClass: 'toast'
        });

        // Token interceptor.
        $httpProvider.interceptors.push(function($q, $localStorage, $rootScope) {
            return {
                request: function(config) {
                    config.headers = config.headers || {};
                    if ($localStorage.token) {
                        config.headers.Authorization = "jwt " + $localStorage.token;
                    }
                    return config;
                },
                responseError: function(response) {
                    if (response.status === 401 || response.status === 403) {
                        $rootScope.$emit("unauthorized");
                    }
                    return $q.reject(response);
                }
            };
        });

        /*
         * States.
         */
        $stateProvider
            /*
             * Login states
             */
            .state('login', {
                url: '/login',
                templateUrl: $contentProvider.url('angular/views/login/main.html'),
                controller: "AuthCtrl"
            })
            /*
             * Panel states
             */
            .state('panel', {
                url: '/panel',
                abstract: true,
                views: {
                    "": {
                        templateUrl: $contentProvider.url('angular/views/panel/main.html'),
                    },
                    "header@panel": {
                        templateUrl: $contentProvider.url('angular/views/panel/header.html'),
                        controller: "HeaderSearchCtrl"
                    },
                    "sidenav@panel": {
                        templateUrl: $contentProvider.url('angular/views/panel/sidenav.html'),
                    }
                }
            })
            .state('panel.areas', {
                url: '/areas',
                views: {
                    "content": {
                        templateUrl: $contentProvider.url('angular/views/catalogues/areas.html'),
                        controller: "AreasCtrl"
                    }
                }
            })
            .state('panel.categories', {
                url: '/areas/:areaId/categories',
                views: {
                    "content": {
                        templateUrl: $contentProvider.url('angular/views/catalogues/categories.html'),
                        controller: "CategoriesCtrl"
                    }
                }
            })
            .state('panel.subjects', {
                url: '/areas/:areaId/categories/:categoryId/subjects',
                views: {
                    "content": {
                        templateUrl: $contentProvider.url('angular/views/catalogues/subjects.html'),
                        controller: "SubjectsCtrl"
                    }
                }
            })
            .state('panel.posts', {
                url: '/areas/:areaId/categories/:categoryId/subjects/:subjectId/posts',
                views: {
                    "content": {
                        templateUrl: $contentProvider.url('angular/views/catalogues/posts.html'),
                        controller: "PostsCtrl"
                    }
                }
            })
            .state('panel.post', {
                url: '/areas/:areaId/subjects/:subjectId/categories/:categoryId/posts/:id',
                views: {
                    "content": {
                        templateUrl: $contentProvider.url('angular/views/catalogues/post.html'),
                        controller: "PostCtrl"
                    }
                }
            })

            .state('panel.searchPosts', {
                url: '/posts/search?:q',
                views: {
                    "content": {
                        templateUrl: $contentProvider.url('angular/views/catalogues/searchPosts.html'),
                        controller: "SearchPostsCtrl"
                    }
                }
            })

            .state('panel.addPost', {
                url: '/areas/:areaId/categories/:categoryId/subjects/:subjectId/add-contribution',
                views: {
                    "content": {
                        templateUrl: $contentProvider.url('angular/views/contributions/action.html'),
                        controller: "CreatePostCtrl"
                    }
                }
            })

            .state('panel.contributions', {
                url: '/contributions',
                views: {
                    "content": {
                        templateUrl: $contentProvider.url('angular/views/contributions/list.html'),
                        controller: "ContributionsCtrl"
                    }
                }
            })

            .state('panel.contribution', {
                url: '/contribution/:postId',
                views: {
                    "content": {
                        templateUrl: $contentProvider.url('angular/views/contributions/detail.html'),
                        controller: "ContributionCtrl"
                    }
                }
            })
            .state('panel.addContribution', {
                url: '/add-contribution',
                views: {
                    "content": {
                        templateUrl: $contentProvider.url('angular/views/contributions/action.html'),
                        controller: "CreateContributionCtrl"
                    }
                }
            })
            .state('panel.editContribution', {
                url: '/edit-contribution/:postId',
                views: {
                    "content": {
                        templateUrl: $contentProvider.url('angular/views/contributions/action.html'),
                        controller: "EditContributionCtrl"
                    }
                }
            })

            .state('panel.editProfile', {
                url: '/edit-profile',
                views: {
                    "content": {
                        templateUrl: $contentProvider.url('angular/views/profile/edit.html'),
                        controller: "EditProfileCtrl"
                    }
                }
            });


        return $urlRouterProvider.otherwise('/login');
    }
]).run(['$rootScope', '$content', '$state', '$localStorage', 'Profile',
    function($rootScope, $content, $state, $localStorage, Profile){
        // Importing vo-content provider to the entire project.
        $rootScope.$content = $content;

        $rootScope.$on('$stateChangeStart', function(evt, toState, toParams, fromState, fromParams) {
            // Loading user info.
            if($localStorage.token){
                Profile.get().$promise.then(function(response){
                    $localStorage.profileInfo = response;
                });
            }

            // Loading information from previous state.
            $state.previous = {
                state: fromState,
                params: fromParams
            };
        });

        $rootScope.$on('unauthorized', function() {
            $state.transitionTo('login');
        });
    }
]);
