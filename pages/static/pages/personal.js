(function(){
    var app = angular.module('personalApp',['auth'])
        .config(function ($interpolateProvider) {
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
        });

    var urls ={
        base: '/idehco3/servicemanager/',
        institutions: 'institutions/',
        services: 'services/'
    };

    app.controller('personalController', ['$scope', '$http', function($scope, $http){
        $scope.institution = null;
        $scope.new_link = '';
        $http.get(urls.base+urls.institution+'ibge/')//hard code here, we need to fix this later
            .success(function(data){
                console.log("data: ",data);
                $scope.institution = data;
                $http.get(urls.base+urls.institutions+'ibge/'+urls.services) //hard code here, we need to fix this later
                    .success(function(data){
                        $scope.institution.links = data;
                        console.log("data2: ", data);
                    })
                    .error(function(data){
                        $scope.institution.links = [];
                        console.log("error2: ", data);
                    });
            })
            .error(function(data){
                console.log("error: ",data);
            });

        $scope.addService = function(){
            if($scope.institution == null) return;
            var data = {
                url: $scope.new_link
            };
            $http.post(urls.base+urls.institutions+$scope.institution.initials+'/'+urls.services, data) //this doesn't look good!
                .success(function(data){
                    console.log('success: ',data);
                })
                .error(function(data){
                    console.log('error: ',data);
                });
        };
    }]);
})();