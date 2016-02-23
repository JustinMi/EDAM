var clean_data = {};
var clean_data2 = {};
var taxon_id;
var myurl;

$.ajax({
  // search taxonomy
  url: 'http://api.speciesplus.net/api/v1/taxon_concepts.json?name=Puma concolor',
  headers: {'X-Authentication-Token': 'WYjddmVCPlzeonLKsf39rwtt'}
}).done(function(data) {
    var extract_results = [];
  // extract common names, higher taxa, and taxon ID
    var data_extract = {
      'common_names': data.taxon_concepts[0].common_names,
      'higher_taxa': data.taxon_concepts[0].higher_taxa,
    };
   
    extract_results.push(data_extract);
    taxon_id = data.taxon_concepts[0].id;
    myurl = 'http://api.speciesplus.net/api/v1/taxon_concepts/'+taxon_id+'/distributions.json';

  // add cleaned results to object
  clean_data['results'] = extract_results;
  //console.log(clean_data);
//});

	$.ajax({
	  // search taxonomy
	  url: myurl,
	  headers: {'X-Authentication-Token': 'WYjddmVCPlzeonLKsf39rwtt'}
	}).done(function(data2) {

	  var extract_results2 = [];
	 // extract location and references
	  for (var i = 0; i < data2.length; i++) {
	    var data_extract2 = {
	      'location': data2[i].name,
	      'references': data2[i].references
	    };
	    extract_results2.push(data_extract2);
	  }

	  // add cleaned results to object
	  clean_data['results2'] = extract_results2;
	  console.log(clean_data);
	});
});


