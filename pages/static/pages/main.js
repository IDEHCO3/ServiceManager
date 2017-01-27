(function(){
    var app = angular.module('searchApp', ['auth'])
        .config(function ($interpolateProvider) {
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
        });

    var urls ={
        base: '/servicemanager/',
        profile: '/servicemanager/institutions/profile/',
        institutions: '/servicemanager/institutions/',
        links: '/links/'
    };

    app.controller('serviceController', ['$scope', '$http', 'userService', function($scope, $http, userService){
        $scope.institutions = [];
        var that = this;
        $http.get(urls.institutions)
            .success(function(data){
                $scope.institutions = data;
            })
            .error(function(data){
                console.log('Error: ',data);
            });

        $scope.openLinks = function(institution){

            if(institution.links != undefined){
                if(institution.activated){
                    institution.activated = false;
                }
                else{
                    institution.activated = true;
                }
                return;
            }

            var url = urls.institutions + institution.initials + urls.links;
            $http.get(url)
                .success(function(data){
                    institution.links = data;
                    institution.activated = true;
                })
                .error(function(data){
                    console.log("Error: ",data);
                });
        };

        this.getServicesInOptions = function(data){
            var services = [];
            var context = data['@context'];
            for(var key in context){
                if( key in data && context[key]['@type'] == '@id'){
                    services.push({
                        name: key,
                        url: data[key]
                    });
                }
            }
            return services;
        };

        $scope.openServices = function(institution, index, link_object){
            if(link_object.services != undefined){
                if(link_object.activated){
                    institution.links[index].activated = false;
                }
                else{
                    institution.links[index].activated = true;
                }
                return;
            }

            $http({
                method: "OPTIONS",
                url: link_object.url
            })
            .success(function(data){
                institution.links[index].services = that.getServicesInOptions(data);
                institution.links[index].activated = true;
            })
            .error(function(data){
                console.log("Error: ",data);
            });
        };
    }]);
})();