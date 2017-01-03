var mouse = angular.module('mouse', ['mouse.controllers', 'ngRoute']);

mouse.config(function ($routeProvider, $locationProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'views/mosaic.html',
            controller: 'mosaic'
        })
        .when('/city/', {
            templateUrl: 'views/city.html',
            controller: 'city'
        })
        .when('/event/', {
            templateUrl: 'views/event.html',
            controller: 'event'
        })
        .when('/search/', {
            templateUrl: 'views/search.html',
        })
        .otherwise({
            redirectTo: '/'
        });
    $locationProvider.html5Mode(true);
});

mouse.factory('ServerService', function() {
  return {
      address : 'http://localhost:7000'
  };
});

angular.module('mouse.controllers', [])
    .controller('main', function ($scope, $http, $location, ServerService) {
        $scope.searchString = "";

        $scope.search = function () {
            console.log("Search...");
            var data = {};
            data.searchString = $scope.searchString;

            $http.post(ServerService.address + '/api/search/', data)
                .then(function (response) {
                    console.log(response);
                    $scope.searchResults = response.data;
                    $location.path("/search");
                });
        }
    })
    .controller('mosaic', function ($scope, $http, ServerService) {
        $http.get(ServerService.address + '/api/mosaic/')
            .then(function (response) {
                console.log(response);
                $scope.mosaic = response.data;
            });
    })
    .controller('event', function ($scope, $http, $routeParams, ServerService) {
        var eventId = $routeParams.id;
        $http.get(ServerService.address + '/api/event/' + eventId + '/')
            .then(function (response) {
                console.log(response);
                $scope.event = response.data;
            });
    })
    .controller('city', function ($scope, $http, ServerService) {
        $http.get(ServerService.address + '/api/city/')
            .then(function (response) {
                console.log(response);
                $scope.data = response.data;
            });
    });