(function(){
    var personal_app = angular.module('personalApp',[]);

    personal_app.controler('personalController', ['$scope', '$http', function($scope, $http){
        $scope.institution = null;
    }]);
});