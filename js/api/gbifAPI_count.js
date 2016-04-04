function get_count_gbif(query, api_dfd, results) {
  // call gbif service
  $.ajax({
    // currently gets 5 results
    url: 'http://api.gbif.org/v1/occurrence/search?scientificName=' + query + '&limit=5&offset=0',
  }).done(function(data) {
    // check if there are results
    if (data.results.length != 0) {
      // extract count
      var count = data.count;
     
      // update results object
      results['gbif'] = {'count': count, 'database': 'gbif'};
    }

    // notify search complete
    api_dfd.resolve();
  });
}
