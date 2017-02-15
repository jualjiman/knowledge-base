app.config([
    '$stateProvider', '$urlRouterProvider', '$contentProvider', '$httpProvider', '$locationProvider', '$mdThemingProvider',
    function($stateProvider, $urlRouterProvider, $contentProvider, $httpProvider, $locationProvider, $mdThemingProvider) {
        // Configure content base url.
        $contentProvider.urlPrefix = staticUrl;

        // Theme configurations.
        $mdThemingProvider.theme('default').primaryPalette('indigo').accentPalette('indigo');
        
        // Token interceptor.
        $httpProvider.interceptors.push(function($q, $localStorage, $rootScope) {
            return {
                request: function(config) {
                    config.headers = config.headers || {};
                    if ($localStorage.token) {
                        config.headers.Authorization = 'jwt ' + $localStorage.token;
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

        // States.
        $stateProvider.state('home', {
            url: '/',
            controller: 'HomeCtrl',
            views: {
                "header": {
                    templateUrl: $contentProvider.url('angular/views/common/header.html')
                },
                "content": {
                    templateUrl: $contentProvider.url('angular/views/home/home.html'),
                    controller: 'HomeCtrl',
                    controllerAs: 'ctrl',
                    resolve: {
                        home: function() {
                            return "placeHolder";
                        }
                    }
                },
                "sidenav": {
                    templateUrl: $contentProvider.url('angular/views/common/sidenav.html')
                },
                "footer": {
                    templateUrl: $contentProvider.url('angular/views/common/footer.html')
                }
            }
        });

        return $urlRouterProvider.otherwise('/');
    }
]).run(['$rootScope', '$content', 
    function($rootScope, $content){
        // Importing vo-content provider to the entire project.
        $rootScope.$content = $content;
    }
]);
