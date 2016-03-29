

 //this function is used for keyword search
function search_inat(query, api_dfd, results) {
var cleaned=[];

var jqXHR=$.ajax({
	url: "http://api.inaturalist.org/v1/observations?q=puma%20concolor&per_page=500&order=desc&order_by=created_at"


}

	).done(function(data){
    var headers = jqXHR.getResponseHeader('X-Total-Entries');
    console.log(headers);
    console.log(data);
	console.log(data.results);
		if(data.results.length!= 0) {
		
		results['inaturalist'] = {'name': query, 'taxonomy': null, 'database': 'inaturalist'};
		}
		api_dfd.resolve();

	});
}


		
