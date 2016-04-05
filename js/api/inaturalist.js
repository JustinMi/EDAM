

 //this function is used for keyword search
function search_inat(query, api_dfd, results) {
var cleaned=[];

var jqXHR=$.ajax({
	url: "http://api.inaturalist.org/v1/observations?q=puma%20concolor&per_page=500&order=desc&order_by=created_at"


}

	).done(function(data){
    
		if(data.results.length!= 0) {
		
		results['iNaturalist'] = {'name': query, 'taxonomy': null, 'database': 'iNaturalist'};
		}
		api_dfd.resolve();

	});
}

function count_inat(query, api_dfd, results) {


var jqXHR=$.ajax({
	url: "http://api.inaturalist.org/v1/observations?q=puma%20concolor&per_page=500&order=desc&order_by=created_at"


}

	).done(function(data){
    var headers = jqXHR.getResponseHeader('X-Total-Entries');
    results['iNaturalist'] = {'count': headers, 'database': 'iNaturalist'};
	api_dfd.resolve();

	});
}
		
