var mouse = angular.module('mouse', ['mouse.controllers', 'ngRoute']);

mouse.config(function ($routeProvider, $locationProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'views/mosaic.html',
            controller: 'query',
            resolve: {
                queryName: function ($route) {
                    $route.current.params.queryName = "mosaic";
                }
            }
        })
        .when('/hottest_city/', {
            templateUrl: 'views/hottest_city.html',
            controller: 'query',
            resolve: {
                queryName: function ($route) {
                    $route.current.params.queryName = "hottest_city";
                }
            }
        })
        .when('/highest_attending/', {
            templateUrl: 'views/highest_attending.html',
            controller: 'query',
            resolve: {
                queryName: function ($route) {
                    $route.current.params.queryName = "highest_attending";
                }
            }
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

mouse.factory('ServerService', ['$location', function ($location) {
    return {
        address: 'http://' + $location.host() + ':' + $location.port()
    };
}]);

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
    .controller('event', function ($scope, $http, $routeParams, ServerService) {
        var eventId = $routeParams.id;
        $http.get(ServerService.address + '/api/event/' + eventId + '/')
            .then(function (response) {
                console.log(response);
                $scope.event = response.data;
            });

        $http.get(ServerService.address + '/api/event/' + eventId + '/comments/')
            .then(function (response) {
                console.log(response);
                $scope.comments = response.data;
            });

        $scope.updateEvent = function () {
            $http.get(ServerService.address + '/api/event/' + eventId + '/update/')
                .then(function (response) {
                    $http.get(ServerService.address + '/api/event/' + eventId + '/')
                        .then(function (response) {
                            console.log(response);
                            $scope.event = response.data;

                            $('#updateNotify').modal();
                        });
                });
        }

        $scope.sendComment = function () {
            var data = {};
            data.newComment = $scope.newComment;

            $http.post(ServerService.address + '/api/event/' + eventId + '/comments/add/', data)
                .then(function (response) {
                    console.log(response);
                    $http.get(ServerService.address + '/api/event/' + eventId + '/comments/')
                        .then(function (response) {
                            console.log(response);
                            $scope.comments = response.data;

                            $('#addCommentNotify').modal();
                        });
                });
        }
    })
    .controller('query', function ($scope, $http, ServerService, $routeParams) {
        $http.get(ServerService.address + '/api/query/' + $routeParams.queryName + '/')
            .then(function (response) {
                console.log(response);
                $scope.data = response.data;
            });
    });