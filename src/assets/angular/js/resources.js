app
    /*
     * Auth Resources.
    */
    .factory('Auth', [
        '$resource',
        function ($resource) {
            return $resource(
                '/api/v1/auth', null,
                {
                    login: {
                        url: '/api/v1/auth/login',
                        method: 'POST'
                    },
                    signup: {
                        url: '/api/v1/auth/signup',
                        method: 'POST'
                    }
                }
            );
        }
    ])
    /*
     * Profile Resources.
    */
    .factory('Profile', [
        '$resource',
        function ($resource) {
            return $resource(
                '/api/v1/me', null,
                {
                    changeImage: {
                        url: '/api/v1/me/change-image',
                        method: 'PUT'
                    },
                    deleteImage: {
                        url: '/api/v1/me/delete-image',
                        method: 'DELETE'
                    }
                }
            );
        }
    ])
    .factory('ProfilePost', [
        '$resource',
        function ($resource) {
            return $resource(
                '/api/v1/posts/:id', {id: '@id'},
                {
                    update: {
                        method: 'PATCH'
                    }
                }
            );
        }
    ])

    /*
     * Posts Resources.
    */
    .factory('Area', [
        '$resource',
        function ($resource) {
            return $resource(
                '/api/v1/areas/:id', {id: '@id'}
            );
        }
    ])
    .factory('Subject', [
        '$resource',
        function ($resource) {
            return $resource(
                '/api/v1/areas/:areaId/subjects/:id',
                {
                    areaId: '@areaId',
                    id: '@id'
                }
            );
        }
    ])
    .factory('Post', [
        '$resource',
        function ($resource) {
            return $resource(
                '/api/v1/areas/:areaId/subjects/:subjectId/posts/:id',
                {
                    areaId: '@areaId',
                    subjectId: '@subjectId',
                    id: '@id'
                }
            );
        }
    ]);
