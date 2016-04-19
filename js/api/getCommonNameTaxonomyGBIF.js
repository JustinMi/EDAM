function getCommonNameTaxonomy(query, api_dfd, results) {
  // call gbif service
  $.ajax({
      // currently gets 5 results
      url: 'http://api.gbif.org/v1/occurrence/search?scientificName=' + query + '&limit=5&offset=0',
  }).done(function(data) {
      // check if there are results
      if (data.results.length != 0) {
          // extract taxonomy and taxonKey from first entry
          var resultObject = data.results[0];
          var taxon = [resultObject.kingdom, resultObject.phylum, resultObject.order, resultObject.family, resultObject.genus];
          var taxonKey = data.results[0].taxonKey; //2435099
      }

      // search for commonNames using taxonKey
      $.ajax({
          url: 'http://api.gbif.org/v1/species/' + taxonKey +'/vernacularNames',
      }).done(function(data) {
          var commonNamesSet = new Set();
          // loop through results array an extract commonNames without repetition
          for (var i = 0; i < data.results.length; i++) {
            if (data.results[i].language == "eng") {
              commonNamesSet.add(data.results[i].vernacularName)
            }
          }
          var commonNames = Array.from(commonNamesSet);
          results['gbif'] = {'name': query, 'taxonomy': taxon.join(), 'common names' : commonNames, 'database': 'gbif'};
      });

      // notify search complete
      api_dfd.resolve();
  });
}
