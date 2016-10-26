(function() {
    var base = "/idehco3/servicemanager/";
    var urls = {
        home : base,
        authetication : "/idehco3/universaluser/authentication/index",
        authentication_me : "/idehco3/universaluser/authentication/me",
    };
    var app = angular.module("auth", [])
        .config(function ($interpolateProvider) {
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
        });

    app.factory('authInterceptor', function ($rootScope, $q, $window) {
        return {
            request: function (config) {
                config.headers = config.headers || {};
                if ($window.sessionStorage.token) {
                    config.headers.Authorization = 'JWT ' + $window.sessionStorage.token;
                }
                return config;
            },
            response: function (response) {
                if (response.status === 401) {
                    // handle the case where the user is not authenticated
                }
                return response || $q.when(response);
            }
        };
    });

    app.config(function ($httpProvider) {
        $httpProvider.interceptors.push('authInterceptor');
    });

    app.controller("UserController", ['$http', '$scope', '$window', function ($http, $scope, $window) {

        $scope.user = {username: "unknown", first_name: "Unknown"};
        var url_authentication_me = urls.authentication_me+"/";
        $scope.authenticated = false;

        if ($window.sessionStorage.token != null) {
            $http.get(url_authentication_me)
                .success(function (data) {
                    $scope.user = data;
                    $scope.authenticated = true;
                })
                .error(function (data) {
                    console.log(data);
                    delete $window.sessionStorage.token;
                });
        }

        $scope.logout = function () {
            if ($window.sessionStorage.token != null) {
                delete $window.sessionStorage.token;
            }

            $window.location = urls.home;
        };

        $scope.login = function(){
            path = $window.location.pathname;
            $window.location = urls.authetication+'/?next='+path;
        };
    }]);

})();