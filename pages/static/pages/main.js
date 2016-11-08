(function(){
    var app = angular.module('searchApp', ['auth'])
        .config(function ($interpolateProvider) {
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
        });

    var urls ={
        base: '/idehco3/servicemanager/',
        profile: '/idehco3/servicemanager/institutions/profile/',
        institutions: '/idehco3/servicemanager/institutions/',
        services: '/services/'
    };

    app.controller('serviceController', ['$scope', '$http', 'userService', function($scope, $http, userService){
        $scope.institutions = [];
        $http.get(urls.institutions)
            .success(function(data){
                $scope.institutions = data;
            })
            .error(function(data){
                console.log('Error: ',data);
            });

        $scope.openServices = function(url){
            $http({
                method: "OPTIONS",
                url: url
            })
            .success(function(data){
                console.log("success: ",data);
            })
            .error(function(data){
                console.log("Error: ",data);
            });
        };
    }]);
})();