var clean_data = {};
var string = "inaturalist"

$.ajax({
  // search taxonomy
  url: 'http://api.gbif.org/v1/species/search?q=Puma concolor',
}).done(function(data) {
  // print all results from API
  //console.log(data);
  var extract_results = []

  // extract kingdom, phylum, order, family, genus, species, common names,
  for (var i = 0; i < data.results.length; i++) {
    if data.results[i].references.indexOf(string) > -1:
      var data_extract = {
        'kingdom': data.results[i].kingdom,
        'phylum': data.results[i].phylum,
        'order': data.results[i].order,
        'family': data.results[i].family,
        'genus': data.results[i].genus,
        'species': data.results[i].species,
        'common_names': data.results[i].vernacularNames,
      };
      console.log(data_extract);
    else:
      console.log("i");
    //console.log(data_extract);
    extract_results.push(data_extract);
  }

  // add cleaned results to object
  clean_data['results'] = extract_results;
  console.log(clean_data);
});