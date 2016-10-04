(function(){
    var app = angular.module('personalApp',[])
        .config(function ($interpolateProvider) {
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
        });

    var url_base = '/idehco3/servicemanager/';
    app.controller('personalController', ['$scope', '$http', function($scope, $http){
        $scope.institution = null;
        $http.get(url_base+'institutions/ibge/')
            .success(function(data){
                console.log("data: ",data);
                $scope.institution = data;
                $http.get(url_base+'institutions/ibge/services')
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
    }]);
})();