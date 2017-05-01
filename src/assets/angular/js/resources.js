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
                        method: 'post'
                    },
                    signup: {
                        url: '/api/v1/auth/signup',
                        method: 'post'
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
                    update: {
                        method: 'patch'
                    },
                    changeImage: {
                        url: '/api/v1/me/change-image',
                        method: 'put',
                        headers: {
                            'Content-Type': void 0
                        }
                    },
                    deleteImage: {
                        url: '/api/v1/me/delete-image',
                        method: 'delete'
                    }
                }
            );
        }
    ])

    .factory('User', [
        '$resource',
        function ($resource) {
            return $resource(
                '/api/v1/users/search',
                {
                    q: '@q'
                }
            );
        }
    ])

    .factory('ProfileContribution', [
        '$resource',
        function ($resource) {
            return $resource(
                '/api/v1/me/posts/:id', {id: '@id'},
                {
                    update: {
                        method: 'patch'
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

    .factory('Category', [
        '$resource',
        function ($resource) {
            return $resource(
                '/api/v1/areas/:areaId/categories/:id',
                {
                    areaId: '@areaId',
                    id: '@id'
                }
            );
        }
    ])

    .factory('Subject', [
        '$resource',
        function ($resource) {
            return $resource(
                '/api/v1/areas/:areaId/categories/:categoryId/subjects/:id',
                {
                    areaId: '@areaId',
                    categoryId: '@categoryId',
                    id: '@id'
                }
            );
        }
    ])

    .factory('Post', [
        '$resource',
        function ($resource) {
            return $resource(
                '/api/v1/areas/:areaId/categories/:categoryId/subjects/:subjectId/posts/:id',
                {
                    areaId: '@areaId',
                    categoryId: '@categoryId',
                    subjectId: '@subjectId',
                    id: '@id',
                    q: '@q'
                },
                {
                    search: {
                        url: '/api/v1/posts/search',
                        method: 'get'
                    }
                }
            );
        }
    ]);
