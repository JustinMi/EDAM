//NOTE: use Safari instead of Google Chrome

function searchSpeciesplus(species) {
	var api_data = [];
	var dfd = $.Deferred();


	$.ajax({
		// search taxonomy
		url: 'http://api.speciesplus.net/api/v1/taxon_concepts.json?name='+species,
		headers: {'X-Authentication-Token': 'WYjddmVCPlzeonLKsf39rwtt'}
	}).done(function(data) {
		// extract species and taxonomy
		var total_entries = data.pagination.total_entries;
		if (total_entries != 0) {
			var higher_taxa = data.taxon_concepts[0].higher_taxa;
			var results = {
				'species': data.taxon_concepts[0].full_name,
				'taxonomy': [higher_taxa['kingdom'], higher_taxa['phylum'], higher_taxa['order'], higher_taxa['family']]
			};
			api_data.push(results)	
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
searchSpeciesplus('Turbinaria ornata');

