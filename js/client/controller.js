var autoTags = ['cat', 'dog', 'fish'];  //default drop-downs. 

var app = angular.module('edamApp', []);

var databases = {
                'idigbio': {'basic': search_idigbio, 'location': search_idigbio_location},
                'gbif': {'basic': search_gbif, 'location': search_gbif_location},
                'iucn': {'basic': search_iucn, 'location': search_iucn_location},
                'inaturalist': {'basic': search_inat, 'location': search_inat_location}
                };

searchDatabase = function(query, locationQuery, search_dfd, results) {

  var all_dfd = [];

  // search each database
  $.each(databases, function(db, func) {
    // search complete notifier
    var api_dfd = $.Deferred();

    // add deferred to list of deferreds
    all_dfd.push(api_dfd);

    // run search to upate results
    if (locationQuery != null && locationQuery.length > 0) {
      func['location'](query, locationQuery, api_dfd, results);
    } else {
      func['basic'](query, api_dfd, results);
    }
  });

  // return results after all searches complete
  $.when.apply(this, all_dfd).done(function() {
    if ($.isEmptyObject(results)) {
      results['null'] = {'name': 'no results', 'taxonomy': 'no results', 'count': 'no results', 'database': 'no results'};
    }
    search_dfd.resolve();
  });
};

app.controller('searchController', function($scope) {

  $scope.updateAutoComplete = function() {
    var q = $('.form-control').val();
    autoComplete(q); // update auto complete 
    console.log("array is " + autoTags);

    $(".form-control").autocomplete({
      source: autoTags
    });
  }

  // data model for results table
  $scope.searchResult = {};

  $scope.search = function(query, locationQuery){
    // all search complete notifier
    var search_dfd = $.Deferred();

    // container object to modify
    var results = {};


    // start database searches
    searchDatabase(query, locationQuery, search_dfd, results);

    // return when all searches are complete
    search_dfd.done(function() {
      // force update
      $scope.$apply(function() {
        $scope.searchResult = results;
        console.log(results)
      });
    });
  }
});


autoComplete = function(query) {
  $.ajax({
    url: 'http://api.gbif.org/v1/species/suggest?q=' + query,
  }).done(function(data) {
    // check if there are results
    if (data.length != 0) {
      //only want the first ten  records. 
      data = data.splice(0, 10); 
      // extract taxonomy from first entry  
      autoTags = []; 
       $.each(data, function(i, animalObj) {
        autoTags.push (animalObj.canonicalName); 
      }); 
      //console.log("taxons are " +);
      //console.log("array is  " + autoTags);
      //return taxons; 
    }
  });
}


