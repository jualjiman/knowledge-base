app.filter('hasEditPermissions',[
    function() {
        return function(post, userId) {
            //
            // Returns true if user has edit permissions.
            //
            var hasPermissions = false,
                i;

            for(i=0; i < post.editableTo.length; i++){
                var user = post.editableTo[i];
                if(user.id === userId){
                    hasPermissions = true;
                    break;
                }
            }

            return hasPermissions;
        };
    }
]);
