
aleph.factory('Query', ['$route', '$location', function($route, $location) {
  var query = {};

  var submit = function() {
    $location.search(query);
  }

  var ensureArray = function(data) {
    if (!angular.isArray(data)) {
      if (angular.isDefined(data) && data.length) {
        data = [data];
      } else {
        data = [];
      }
    }
    return data;
  };

  var load = function() {
    query = $location.search();
    query.mode = query.mode || 'table';
    query.collection = ensureArray(query.collection);
    query.attribute = ensureArray(query.attribute);
    query.entity = ensureArray(query.entity);
    return query;
  };

  var toggleFilter = function(name, val) {
    var idx = query[name].indexOf(val);
    if (idx == -1) {
      query[name].push(val);
    } else {
      query[name].splice(idx, 1);
    }
    submit();
  };

  var hasFilter = function(name, val) {
    return query[name].indexOf(val) != -1;
  };

  load();

  return {
      state: query,
      submit: submit,
      load: load,
      queryString: function() {
        return queryString(query);
      },
      hasFilter: hasFilter,
      toggleFilter: toggleFilter
  };

}]);
