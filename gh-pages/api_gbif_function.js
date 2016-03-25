function searchGbif(species) {
// input: scientific name as a string (genus species)
// output: object with dictionary containing
            //a) species: string(genus species)
            //b) taxonomy: array[kingdom, phylum, order, family, genus]
        // or null if search found no results

    var api_data = [];
    var dfd = $.Deferred();
    // only search first page (change index for more pages)
    var index = 1;

    $.ajax({
        // search species and taxonomy by scientific name (max limit allowed = 300 entries per page)
        url: 'http://api.gbif.org/v1/occurrence/search?scientificName='+species+'&limit=300&offset='+index,
    }).done(function(data) {
        // extract species and taxonomy from first entry (change i for more entries)
        for (var i = 0; i < 1; i++) {
            if (data.results.length != 0) {
                var results = {
                    'species': data.results[i].species,
                    'taxonomy': [data.results[i].kingdom, data.results[i].phylum, data.results[i].order, data.results[i].family, data.results[i].genus]
                };
                api_data.push(results)
            }
        }
        dfd.resolve();
    });

    // after dfd is resolved
    dfd.done(function() {
        $.when.apply(this).done(function() {
            if (api_data.length == 0) {
                // search found no results
                console.log(null)
                return null
            } else {
                // print results to console
                console.log(api_data)
                return api_data;
            }
        });
    });
}

// test search function
searchGbif('Puma concolor');



function getCountGbif(species) {
// input: scientific name as a string (genus species)
// output: a count for the number of entries found by the search

    var api_data = [];
    var dfd = $.Deferred();
    // only search first page (change index for more pages)
    var index = 1;

    $.ajax({
        // search count by scientific name (max limit allowed = 300 entries per page)
        url: 'http://api.gbif.org/v1/occurrence/search?scientificName='+species+'&limit=300&offset='+index,
    }).done(function(data) {
        // extract count
        if (data.results.length != 0) {
            var count = data.count;
        } else {
            var count = 0;
        }

        api_data.push(count)
        dfd.resolve();
    });

    // after dfd is resolved
    dfd.done(function() {
        $.when.apply(this).done(function() {
            if (api_data.length == 0) {
                // search found no results
                console.log(null)
                return null
            } else {
                // print results to console
                console.log(api_data)
                return api_data;
            }
        });
    });
}

// test get count function
getCountGbif('Puma concolor');


