

 //this function is used for keyword search
function search_inat(query, api_dfd, results) {
var cleaned=[];

var jqXHR=$.ajax({
	url: "http://api.inaturalist.org/v1/observations?q="+query+"&per_page=500&order=desc&order_by=created_at"


}

	).done(function(data){
    
		if(data.results.length!= 0) {
		
		results['iNaturalist'] = {'name': query, 'taxonomy': null, 'database': 'iNaturalist'};
		}
		api_dfd.resolve();

	});
}

function count_inat(query,api_dfd, results) {


var jqXHR=$.ajax({
	url: "http://api.inaturalist.org/v1/observations/species_counts?q="+query



}

	).done(function(data){
   	var count = 0;
   	if (data.results.length == 0) {
    	
    }
    else {
    var count = data.results[0].count
    }
    results['iNaturalist'] = {'count': count, 'database': 'iNaturalist'};
	api_dfd.resolve();

	});
}
		
function locationsearch_iucn(query, location, api_dfd, results) {
	var jqXHR=$.ajax({
	url: "https://www.inaturalist.org/places.json?place_type=country&q="+location


}
).done(function(data){
		$.each
});

}
