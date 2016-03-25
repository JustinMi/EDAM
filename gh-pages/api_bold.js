function searchBold(species) {
    var api_data = [];
    var dfd = $.Deferred();
    // only search first page (change index for more pages)
    var index = 1;

    $.ajax({
        // search taxonomy
        url: 'http://www.boldsystems.org/index.php/API_Public/specimen?taxon=Puma concolor&format=xml',
    }).done(function(data) {
        console.log(data)
        // extract species and taxonomy from first entry (change i for more entries)
        // for (var i = 0; i < 1; i++) {
        //     // removed the filtering out of entries from inaturalist for now
        //     // var ref = data.results[i].datasetName;
        //     // if (typeof ref == "undefined") {
        //     if (results != null) {
        //         var results = {
        //             'species': data.results[i].species,
        //             'taxonomy': [data.results[i].kingdom, data.results[i].phylum, data.results[i].order, data.results[i].family, data.results[i].genus]
        //         };
        //         api_data.push(results)
        //     }
        // }
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
searchBold('Puma concolor');


