function searchVertNet(species) {
	var api_data = [];
	var dfd = $.Deferred();


	$.ajax({
		// search taxonomy
		url: 'http://api.vertnet-portal.appspot.com/api/search?q={"q":'+species+'"}'
	}).done(function(data) {
		console.log(data)
		// extract species and taxonomy
		var total_entries = data.matching_records;
		if (total_entries != 0) {
			var results = {
				'species': data.recs[0].specificepithet,
				'taxonomy': data.recs[0].higherclassification
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
searchVertNet('Puma concolor');

