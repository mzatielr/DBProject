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

angular.module('mouse.controllers', [])
    .controller('main', function ($scope, $http, $location) {
        $scope.searchString = "";

        $scope.search = function () {
            console.log("Search...");
            var data = {};
            data.searchString = $scope.searchString;

            $http.post('http://localhost:7000/api/search/', data)
                .then(function (response) {
                    console.log(response);
                    $scope.searchResults = response.data;
                    $location.path("/search");
                });
        }
    })
    .controller('mosaic', function ($scope, $http) {
        $http.get('http://localhost:7000/api/mosaic/')
            .then(function (response) {
                console.log(response);
                $scope.mosaic = response.data;
            });
    })
    .controller('event', function ($scope, $http, $routeParams) {
        var eventId = $routeParams.id;
        $http.get('http://localhost:7000/api/event/' + eventId + '/')
            .then(function (response) {
                console.log(response);
                $scope.event = response.data;
            });
    })
    .controller('city', function ($scope, $http) {
        $http.get('http://localhost:7000/api/city/')
            .then(function (response) {
                console.log(response);
                $scope.data = response.data;
            });
    });