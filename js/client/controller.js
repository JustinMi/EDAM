var app = angular.module('edamApp', []);

var databases = {
                'idigbio': {'basic': search_idigbio, 'location': search_idigbio_location},
                'gbif': {'basic': search_gbif, 'location': search_gbif_location},
                'iucn': {'basic': search_iucn, 'location': search_iucn_location},
                'inaturalist': {'basic': search_inat, 'location': search_inat_location}
                };
var autoTags = ['Puma', 'Puma concolor', "Puma concolor mayensis"]; 

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
    //autoTags = autoComplete($('#form-control').text());
    var q = $('#form-control').text();  
    //autoTags = autoComplete(q);
    autoTage = autoComplete("Puma");
    console.log(autoTags);

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

$(function() {
    var availableTags = [
      "ActionScript",
      "AppleScript",
      "Asp",
      "Puma",
      "Puma concolor"
    ];
    var autocompletedTags = autoComplete($("Puma").text());
    console.log($('#form-control').text());
    $(".form-control").autocomplete({
      source: autoTags
    });
  });

autoComplete = function(query) {
  $.ajax({
    url: 'http://api.gbif.org/v1/species/suggest?q=' + query,
  }).done(function(data) {
    // check if there are results
    if (data.length != 0) {
      // extract taxonomy from first entry  
      var taxons = []; 
       $.each(data, function(i, animalObj) {
        taxons.push (animalObj.canonicalName); 
      }); 
      console.log(taxons);
      return (taxons); 
    }
  });
}


