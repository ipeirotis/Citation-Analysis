var app = angular.module('datamgmt', ['ngResource', 'ngRoute', 'datamgmt.controllers', 'datamgmt.services']);

app.config(function ($routeProvider) {
  $routeProvider.when('/organization', {
    controller: 'RootOrganizationListCtrl',
    templateUrl: '/partials/organizations/list-root.html'
  }).when('/organization/:id/tree', {
    controller: 'OrganizationTreeCtrl',
    templateUrl: '/partials/organizations/list-tree.html'
  }).when('/organization/new', {
    controller: 'OrganizationCreateCtrl',
    templateUrl: '/partials/organizations/create.html',
  }).when('/organization/:id/new', {
    controller: 'OrganizationCreateCtrl',
    templateUrl: '/partials/organizations/create.html',
  }).when('/organization/:id/edit', {
    controller: 'OrganizationEditCtrl',
    templateUrl: '/partials/organizations/edit.html'
  }).when('/author', {
    controller: 'AuthorListCtrl',
    templateUrl: '/partials/authors/list.html'
  }).when('/author/new', {
    controller: 'AuthorCreateCtrl',
    templateUrl: '/partials/authors/create.html',
  }).when('/author/:id/edit', {
    controller: 'AuthorEditCtrl',
    templateUrl: '/partials/authors/edit.html'
  }).otherwise({
    redirectTo: '/organization'
  })
});
