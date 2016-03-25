var api_data = [];
var searchGbif = function(species, index) {
    var dfd = $.Deferred();
    var limit = 300;
    var offset = 0;
    if (index != 0) {
        offset = index*limit
  }

    $.ajax({
        url: 'http://api.gbif.org/v1/occurrence/search?scientificName='+species+'&limit='+limit+'&offset='+offset,
    }).done(function(data) {

        for (var i = 0; i < data.results.length; i++) {
            var results = {
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
            api_data.push(results);
        }

        if (data.endOfRecords == true) {
            console.log(api_data);
            dfd.resolve(api_data);
        } else {
            searchGbif(species, index+1)
        }
    });
    
    return dfd.promise();
}

searchGbif('Puma concolor', 0);