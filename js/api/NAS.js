function search_nas(query, api_dfd, results) {
var cleaned=[];
var space = query.indexOf(" ");
var genus = "";
var species = "";
if (space > 0) {
	genus = query.substring(0,space);
	species = query.substring(space + 1);
}
else {
	alert("call invalid, roy do whatever you want to handle this exception");
}
var jqXHR=$.ajax({
	url: "http://nas.er.usgs.gov/api/v1/occurrence/search?genus="+genus+"&species="+species+"&api_key=7F0F12B9-BFF1-4266-A0B5-77C4115CA7B8"


}

	).done(function(data){
    
   
		
		if(data.results.length>0) {
				var info = data.results[0];
		 var taxon = [info.group, info.family, info.genus, info.species];
		results['NAS'] = {'name': query, 'taxonomy': taxon.join(), 'database': 'NAS'};
		
		}
	
	api_dfd.resolve();
	});

}

function count_nas(query, api_dfd, results) {
	var space = query.indexOf(" ");
var genus = "";
var species = "";
if (space > 0) {
	genus = query.substring(0,space);
	species = query.substring(space + 1);
}
else {
	alert("call invalid, roy do whatever you want to handle this exception");
}
	var jqXHR=$.ajax({
	url: "http://nas.er.usgs.gov/api/v1/occurrence/search?genus="+genus+"&species="+species+"&api_key=7F0F12B9-BFF1-4266-A0B5-77C4115CA7B8"



}

	).done(function(data){
    
    
		var count = data.count;
		
		results['NAS'] = {'count': count, 'database': 'NAS'};
		
		
			results['NAS'] = {'count': count, 'database': 'NAS'};
		
		api_dfd.resolve();
	});
	
}

function locationsearchnas(query, location, api_dfd, results) {
	var space = query.indexOf(" ");
var genus = "";
var species = "";
if (space > 0) {
	genus = query.substring(0,space);
	species = query.substring(space + 1);
}
else {
	alert("call invalid, roy do whatever you want to handle this exception");
}
	if (location === "USA" || location === "United States") {
	var jqXHR=$.ajax({
	url: "http://nas.er.usgs.gov/api/v1/occurrence/search?genus="+genus+"&species="+species+"&api_key=7F0F12B9-BFF1-4266-A0B5-77C4115CA7B8"



	}

	).done(function(data){
    
    
		var count = data.count;
		if (count > 0) {
		results['NAS'] = {'location':location,'count': count, 'database': 'NAS'};
		
		
		}
		else {
			results['NAS'] = {'location':location,'count': 0, 'database': 'NAS'};
		}
		api_dfd.resolve();
	});


	}
	else {
		results['NAS'] = {'location':location,'count': 0, 'database': 'NAS'};
		api_dfd.resolve();
	}
}
