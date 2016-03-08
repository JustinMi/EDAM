var clean_data = {};
var extract_results = [];

//added limit (number of results per page) = 300 and offset (1 to 50)
for (var index = 1; index < 2; index++) {
  $.ajax({
    // search taxonomy, location, and references
    url: 'http://api.gbif.org/v1/occurrence/search?scientificName=Puma concolor&limit=200&offset='+index,
  }).done(function(data) {
      //var extract_results = []
      // extract taxa (kingdom, phylum, order, family, genus, and species),
      //  location (country, latitude, and longitude),
      //  and references (excluding data from inaturalist)
      for (var i = 0; i < data.results.length; i++) {
        var ref = data.results[i].datasetName;
        // only data from inaturalist has a field labeled datasetName
        if (typeof ref == "undefined") {
            var data_extract = {
              'kingdom': data.results[i].kingdom,
              'phylum': data.results[i].phylum,
              'order': data.results[i].order,
              'family': data.results[i].family,
              'genus': data.results[i].genus,
              'species': data.results[i].species,
              'country': data.results[i].country,
              'latitude': data.results[i].decimalLatitude,
              'longitude': data.results[i].decimalLongitude,
              'references': data.results[i].institutionCode
              };
          //console.log(data_extract);
            extract_results.push(data_extract);
          }
        }

      if (index == 49) {
      // add cleaned results to object
        clean_data['results'] = extract_results;
        console.log(clean_data);
      }
    });
}
