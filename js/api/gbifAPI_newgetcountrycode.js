function search_gbif(query, api_dfd, results) {
  // call gbif service
  $.ajax({
    // currently gets 5 results
    url: 'http://api.gbif.org/v1/occurrence/search?scientificName=' + query + '&limit=5&offset=0',
  }).done(function(data) {
    // check if there are results
    if (data.results.length != 0) {
      // extract taxonomy from first entry
      var resultObject = data.results[0];
      var taxon = [resultObject.kingdom, resultObject.phylum, resultObject.order, resultObject.family, resultObject.genus];
      var count = data.count;
      
      // update results object
      results['gbif'] = {'name': query, 'taxonomy': taxon.join(), 'count': count, 'database': 'gbif'};
    }

    // notify search complete
    api_dfd.resolve();
  });
}


//image search
function getCountryCode (countryName) {
  // look up ISO 2 letter country code on restcountries.eu
  $.ajax({
    url: 'https://restcountries.eu/rest/v1/name/' + countryName + '?fullText=true' 
  }).done(function(data) {
    // check if there are results
    if (data.length != 0) {
      // extract country code
      var countryCode = data[0].alpha2Code;
      return countryCode
    } else {
      return countryName
    }
  });
}




function search_gbif_location(query, location, api_dfd, results) {
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
          var taxonKey = data.results[0].taxonKey;

      }

      // get 2 letter country code
      countryCode = getCountryCode(location);

      // if country code found, search by location
      if (countryCode != location) {
        $.ajax({
            url: 'http://api.gbif.org/v1/occurrence/count?taxonKey=' + taxonKey + '&country=' + countryCode,
        }).done(function(data) {
            var count = data;
            results['gbif'] = {'name': query, 'taxonomy': taxon.join(), 'count' : count, 'database': 'gbif'};
        })
      }

      // notify search complete
      api_dfd.resolve();
  });
}