function sorto(o1, o2) {
  if (o1.name > o2.name) {
    return 1;
  }
  if (o1.name < o2.name) {
    return -1;
  }
  return 0;
}

angular.module('datamgmt.controllers', []).controller('RootOrganizationListCtrl', function ($scope, $location, Organization, RootOrganization, $timeout) {

  $scope.resultsPerPage = 10;
  $scope.currentPage = 1;

  $scope.query = function () {
    RootOrganization.get({
      per_page: $scope.resultsPerPage,
      page: $scope.currentPage
    }).$promise.then(function (result) {
      $scope.organizations = result.roots;
      $scope.totalPages = result.total_pages;
      $scope.totalResults = result.total;
    });
  };

  $timeout(function () {
    $scope.query();
  }, 2000);

  $scope.nextPage = function () {
    if ($scope.currentPage < $scope.totalPages) {
      $scope.currentPage = $scope.currentPage + 1;
    }
    $scope.query();
  };

  $scope.previousPage = function () {
    if ($scope.currentPage > 1) {
      $scope.currentPage = $scope.currentPage - 1;
    }
    $scope.query();
  };

  $scope.deleteOrganization = function (id) {
    Organization.delete({
      id: id
    }).$promise.then(function (result) {
      $scope.totalResults = $scope.totalResults - 1;
      if ($scope.totalResults == 0) {
        $scope.currentPage = 1;
      }
      $scope.query();
    });
  };

  $scope.editOrganization = function (id) {
    $location.path('/organization/' + id + '/edit');
  };

  $scope.createOrganization = function () {
    $location.path('/organization/new');
  };

  $scope.viewOrganizationTree = function (id) {
    $location.path('/organization/' + id + '/tree');
  };

  $scope.query();

}).controller('OrganizationTreeCtrl', function ($scope, $location, Organization, OrganizationTree, $timeout, $routeParams) {

  $scope.query = function () {

    Organization.query({
      q: angular.toJson({
        "filters": [{
          "name": "id",
          "op": "eq",
          "val": $routeParams.id
        }]
      })
    }).$promise.then(function (result) {
      $scope.organization = result.data.objects[0];
      OrganizationTree.get({
        id: $routeParams.id
      }).$promise.then(function (result) {
        $scope.tree = result.tree;
      });
    });
  };

  $timeout(function () {
    $scope.query();
  }, 2000);

  $scope.deleteOrganization = function (id) {
    Organization.delete({
      id: id
    }).$promise.then(function (result) {
      $scope.query();
    });
  };

  $scope.editOrganization = function (id) {
    $location.path('/organization/' + id + '/edit');
  };

  $scope.createOrganization = function () {
    $location.path('/organization/new');
  };

  $scope.addChildOrganization = function (id) {
    $location.path('/organization/' + id + '/new');
  };

  $scope.query();

}).controller('OrganizationCreateCtrl', function ($scope, $location, $routeParams, Organization) {

  var id = $routeParams.id;

  $scope.organization = new Organization();

  Organization.query({
    q: angular.toJson({
      "filters": [{
        "name": "parent",
        "op": "is_null"
      }],
      "order_by": [{
        "field": "name",
        "direction": "asc"
      }]
    })
  }).$promise.then(function (result) {
    $scope.organizations_1 = result.data.objects;
    if (id) {
      $scope.organization.parent_id = id;
      Organization.get({
        id: $routeParams.id
      }).$promise.then(function (result) {
        var ancestors = [result.id];
        for (var i = 0; i < result.ancestor_ids.length; i++) {
          ancestors.push(result.ancestor_ids[i]);
        }
        $scope.top = ancestors[ancestors.length - 1];
        if (ancestors.length > 0) {
          for (var i = 0; i < $scope.organizations_1.length; i++) {
            var organization_1 = $scope.organizations_1[i];
            if (organization_1.id == ancestors[ancestors.length - 1]) {
              $scope.organization_1 = organization_1;
            }
          }
        }
        for (var i = ancestors.length - 1; i >= 0; i--) {
          $scope.getChildren(ancestors[i], ancestors.length - i + 1, i > 0 ? ancestors[i - 1] : null);
        }
      });
    }
  });

  $scope.getChildren = function (id, level, pre) {
    if (!id) {
      $scope['organizations_' + level] = null;
      return;
    }
    for (var i = level + 1; i <= 4; i++) {
      $scope['organizations_' + i] = null;
    }
    Organization.query({
      q: angular.toJson({
        "filters": [{
          "name": "parent_id",
          "op": "eq",
          "val": id
        }],
        "order_by": [{
          "field": "name",
          "direction": "asc"
        }]
      })
    }).$promise.then(function (result) {
      $scope['organizations_' + level] = result.data.objects;
      if (pre) {
        for (var i = 0; i < $scope['organizations_' + level].length; i++) {
          var organization = $scope['organizations_' + level][i];
          if (organization.id == pre) {
            $scope['organization_' + level] = organization;
          }
        }
      }
    });
  };

  $scope.createOrganization = function () {
    Organization.save($scope.organization);
    $location.path('/organization/' + $scope.top + '/tree');
  };

  $scope.cancel = function () {
    $location.path('/organization');
  };

}).controller('OrganizationEditCtrl', function ($scope, $location, $routeParams, Organization) {

  $scope.updateOrganization = function (id) {
    Organization.update($scope.organization);
    $location.path('/organization');
  };

  Organization.query({
    q: angular.toJson({
      "filters": [{
        "name": "parent",
        "op": "is_null"
      }],
      "order_by": [{
        "field": "name",
        "direction": "asc"
      }]
    })
  }).$promise.then(function (result) {
    $scope.organizations_1 = result.data.objects;
    Organization.get({
      id: $routeParams.id
    }).$promise.then(function (result) {
      $scope.organization = result;
      if (result.ancestor_ids.length > 0) {
        for (var i = 0; i < $scope.organizations_1.length; i++) {
          var organization_1 = $scope.organizations_1[i];
          if (organization_1.id == result.ancestor_ids[result.ancestor_ids.length - 1]) {
            $scope.organization_1 = organization_1;
          }
        }
      }
      for (var i = result.ancestor_ids.length - 1; i >= 0; i--) {
        $scope.getChildren(result.ancestor_ids[i], result.ancestor_ids.length - i + 1, i > 0 ? result.ancestor_ids[i - 1] : null);
      }
    });
  });

  $scope.getChildren = function (id, level, pre) {
    if (!id) {
      $scope['organizations_' + level] = null;
      return;
    }
    for (var i = level + 1; i <= 4; i++) {
      $scope['organizations_' + i] = null;
    }
    Organization.query({
      q: angular.toJson({
        "filters": [{
          "name": "parent_id",
          "op": "eq",
          "val": id
        }],
        "order_by": [{
          "field": "name",
          "direction": "asc"
        }]
      })
    }).$promise.then(function (result) {
      $scope['organizations_' + level] = result.data.objects;
      if (pre) {
        for (var i = 0; i < $scope['organizations_' + level].length; i++) {
          var organization = $scope['organizations_' + level][i];
          if (organization.id == pre) {
            $scope['organization_' + level] = organization;
          }
        }
      }
    });
  };

  $scope.editOrganization = function (id) {
    $location.path('/organization/' + id + '/edit');
  };

  $scope.cancel = function () {
    $location.path('/organization');
  };

}).controller('AuthorListCtrl', function ($scope, $location, Author, $timeout) {

  $scope.resultsPerPage = 10;
  $scope.currentPage = 1;

  $scope.query = function () {
    Author.query({
      q: angular.toJson({
        "filters": [{
          "or": [{
            "name": "retrieved_at",
            "op": "is_not_null"
      }, {
            "name": "scholar_id",
            "op": "is_null"
            }]
          }],
        "order_by": [{
          "field": "name",
          "direction": "asc"
      }]
      }),
      results_per_page: $scope.resultsPerPage,
      page: $scope.currentPage
    }).$promise.then(function (result) {
      $scope.authors = result.data.objects;
      $scope.currentPage = result.data.page;
      $scope.totalPages = result.data.total_pages;
      $scope.numResults = result.data.num_results;
    });
  };

  $timeout(function () {
    $scope.query();
  }, 2000);

  $scope.nextPage = function () {
    if ($scope.currentPage < $scope.totalPages) {
      $scope.currentPage = $scope.currentPage + 1;
    }
    $scope.query();
  };

  $scope.previousPage = function () {
    if ($scope.currentPage > 1) {
      $scope.currentPage = $scope.currentPage - 1;
    }
    $scope.query();
  };

  $scope.deleteAuthor = function (id) {
    Author.delete({
      id: id
    }).$promise.then(function (result) {
      $scope.numResults = $scope.numResults - 1;
      if ($scope.numResults == 0) {
        $scope.currentPage = 1;
      }
      $scope.query();
    })
  };

  $scope.editAuthor = function (id) {
    $location.path('/author/' + id + '/edit');
  };

  $scope.createAuthor = function () {
    $location.path('/author/new');
  };

  $scope.query();

}).controller('AuthorCreateCtrl', function ($scope, $location, $http, Author, Organization) {

  $scope.author = new Author();

  Organization.query({
    q: angular.toJson({
      "filters": [{
        "name": "parent",
        "op": "is_null"
      }],
      "order_by": [{
        "field": "name",
        "direction": "asc"
      }]
    })
  }).$promise.then(function (result) {
    $scope.organizations_1 = result.data.objects;
  });

  $scope.getChildren = function (id, level, pre) {
    if (!id) {
      $scope['organizations_' + level] = null;
      return;
    }
    for (var i = level + 1; i <= 4; i++) {
      $scope['organizations_' + i] = null;
    }
    Organization.query({
      q: angular.toJson({
        "filters": [{
          "name": "parent_id",
          "op": "eq",
          "val": id
        }],
        "order_by": [{
          "field": "name",
          "direction": "asc"
        }]
      })
    }).$promise.then(function (result) {
      $scope['organizations_' + level] = result.data.objects;
      if (pre) {
        for (var i = 0; i < $scope['organizations_' + level].length; i++) {
          var organization = $scope['organizations_' + level][i];
          if (organization.id == pre) {
            $scope['organization_' + level] = organization;
          }
        }
      }
    });
  };

  $scope.createAuthor = function () {
    if ($scope.author.scholar_id) {
      Author.query({
        q: angular.toJson({
          "filters": [{
            "and": [{
              "name": "scholar_id",
              "op": "==",
              "val": $scope.author.scholar_id
            }, {
              "name": "retrieved_at",
              "op": "is_null"
            }]
      }]
        })
      }).$promise.then(function (result) {
        if (result.data.objects && result.data.objects.length) {
          var author = result.data.objects[0];
          author.name = $scope.author.name;
          author.title = $scope.author.title;
          author.university_id = $scope.author.university_id;
          author.department_id = $scope.author.department_id;
          author.year_of_hd = $scope.author.year_of_phd;
          author.tenured = $scope.author.tenured;
          author.scholar_id = $scope.author.scholar_id;
          Author.update(author);
        } else {
          Author.save($scope.author);
        }
        Author.query({
          q: angular.toJson({
            "filters": [{
              "name": "scholar_id",
              "op": "==",
              "val": $scope.author.scholar_id
            }],
            "single": true
          })
        });
        $location.path('/author');
      });
    } else {
      Author.save($scope.author);
      $location.path('/author');
    }
  };

  $scope.cancel = function () {
    $location.path('/author');
  };

}).controller('AuthorEditCtrl', function ($scope, $location, $routeParams, Author, Organization) {

  $scope.updateAuthor = function (id) {
    Author.update($scope.author);
    $location.path('/author');
  };

  Organization.query({
    q: angular.toJson({
      "filters": [{
        "name": "parent",
        "op": "is_null"
      }],
      "order_by": [{
        "field": "name",
        "direction": "asc"
      }]
    })
  }).$promise.then(function (result) {
    $scope.organizations_1 = result.data.objects;
    Author.get({
      id: $routeParams.id
    }).$promise.then(function (result) {
      $scope.author = result;
      if (result.organization_ids.length > 0) {
        for (var i = 0; i < $scope.organizations_1.length; i++) {
          var organization_1 = $scope.organizations_1[i];
          if (organization_1.id == result.organization_ids[0]) {
            $scope.organization_1 = organization_1;
          }
        }
      }
      for (var i = 0; i < result.organization_ids.length; i++) {
        $scope.getChildren(result.organization_ids[i], i + 2, i < result.organization_ids.length - 1 ? result.organization_ids[i + 1] : null);
      }
    });
  });

  $scope.getChildren = function (id, level, pre) {
    if (!id) {
      $scope['organizations_' + level] = null;
      return;
    }
    for (var i = level + 1; i <= 4; i++) {
      $scope['organizations_' + i] = null;
    }
    Organization.query({
      q: angular.toJson({
        "filters": [{
          "name": "parent_id",
          "op": "eq",
          "val": id
        }],
        "order_by": [{
          "field": "name",
          "direction": "asc"
        }]
      })
    }).$promise.then(function (result) {
      $scope['organizations_' + level] = result.data.objects;
      if (pre) {
        for (var i = 0; i < $scope['organizations_' + level].length; i++) {
          var organization = $scope['organizations_' + level][i];
          if (organization.id == pre) {
            $scope['organization_' + level] = organization;
          }
        }
      }
    });
  };

  $scope.cancel = function () {
    $location.path('/author');
  };
});
