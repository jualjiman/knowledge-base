app.config([
    '$stateProvider', '$urlRouterProvider', '$contentProvider', '$httpProvider', '$locationProvider', 'toastrConfig', 'markedProvider',
    function($stateProvider, $urlRouterProvider, $contentProvider, $httpProvider, $locationProvider, toastrConfig, markedProvider) {
        // Configure content base url.
        $contentProvider.urlPrefix = staticUrl;
        
        // Markdown library setup.
        markedProvider.setOptions({
            gfm: true,
            highlight: function (code, lang) {
                if (lang) {
                    return hljs.highlight(lang, code, true).value;
                } else {
                    return hljs.highlightAuto(code).value;
                }
            }
        });

        // Toastr configurations.
        angular.extend(toastrConfig, {
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
         * 
         * Home states.
         */
        $stateProvider
            .state('panel', {
                url: '/panel',
                abstract: true,
                views: {
                    "": {
                        templateUrl: $contentProvider.url('angular/views/panel/main.html'),
                    },
                    "header@panel": {
                        templateUrl: $contentProvider.url('angular/views/panel/header.html'),
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
                        controller: "AreaCtrl"
                    }
                }
            })
            .state('panel.subjects', {
                url: '/areas/:areaId/subjects',
                views: {
                    "content": {
                        templateUrl: $contentProvider.url('angular/views/catalogues/subjects.html'),
                        controller: "SubjectCtrl"
                    }
                }
            })
            .state('panel.posts', {
                url: '/areas/:areaId/subjects/:subjectId/posts',
                views: {
                    "content": {
                        templateUrl: $contentProvider.url('angular/views/catalogues/posts.html'),
                        controller: "PostsCtrl"
                    }
                }
            })
            .state('panel.post', {
                url: '/areas/:areaId/subjects/:subjectId/posts/:id',
                views: {
                    "content": {
                        templateUrl: $contentProvider.url('angular/views/catalogues/post.html'),
                        controller: "PostCtrl"
                    }
                }
            })
            /*
             * Login states
             */
            .state('login', {
                url: '/login',
                templateUrl: $contentProvider.url('angular/views/login/main.html'),
                controller: "AuthCtrl"
            });

        return $urlRouterProvider.otherwise('/panel/areas');
    }
]).run(['$rootScope', '$content', 
    function($rootScope, $content){
        // Importing vo-content provider to the entire project.
        $rootScope.$content = $content;
    }
]);
