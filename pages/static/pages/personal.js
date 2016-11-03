(function(){
    var app = angular.module('personalApp',['auth'])
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

    app.controller('personalController', ['$scope', '$http', 'userService', function($scope, $http, userService){

        $scope.institution = null;
        $scope.new_link = '';

        $http.get(urls.profile)//hard code here, we need to fix this later
            .success(function(data){
                console.log("data: ",data);
                $scope.institution = data;
                $http.get(urls.institutions+$scope.institution.initials+urls.services)
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
                userService.logout();
            });

        $scope.addServiceLink = function(){
            if($scope.institution == null) return;
            var data = {
                url: $scope.new_link
            };
            $http.post(urls.institutions+$scope.institution.initials+urls.services, data)
                .success(function(data){
                    console.log('success: ',data);
                    $scope.institution.links.push(data);
                    $scope.new_link = "";
                })
                .error(function(data){
                    console.log('error: ',data);
                    //userService.logout();
                });
        };

        $scope.deleteServiceLink = function(index, link){
            if($scope.institution == null) return;

            $http.delete(urls.institutions+$scope.institution.initials+urls.services+link.id)
                .success(function(){
                    var new_list = [];
                    for(var i=0; i<$scope.institution.links.length; i++){
                        if(i!=index) {
                            new_list.push($scope.institution.links[i]);
                        }
                    }
                    $scope.institution.links = new_list;
                    console.log('success to delete', $scope.institution.links);
                })
                .error(function(data){
                    console.log('error: ', data);
                    //userService.logout();
                });
        }
    }]);
})();