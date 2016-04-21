//function used in aggregate general data and finding mode
function mode(array) {
    if(array.length == 0)
      return null;
    var modeMap = {};
    var maxEl = array[0], maxCount = 1;

    for(var i = 0; i < array.length; i++)
    {
      var el = array[i];
      if(el = "undefined") continue;
      if(modeMap[el] == null) modeMap[el] = 1;
      else modeMap[el]++;  
      if(modeMap[el] > maxCount) {
        maxEl = el;
        maxCount = modeMap[el];
      }
    }
    return maxEl;
  }

function searchIDigBio(species){
  var taxon = [];
  var scientificname = [];
  var dfd = $.Deferred();

  // initial request to get total entries
  $.ajax("https://search.idigbio.org/v2/search/records/", 
  {
    dataType: 'json',
    contentType: 'application/json',
    type: "POST",
    data: JSON.stringify({limit:50000, rq:{scientificname: species}})
  }).done(function(data) {
    for (var i = 0; i < data.items.length; i++) {
      var data_extract = {
        'scientific name': data.items[i].indexTerms.scientificname,
        'higher taxonomy': data.items[i].indexTerms.highertaxon
      };

      //aggregating individiual attributes to different arrays
      if(data_extract['higher taxonomy'] != undefined)
        taxon.push(data_extract['higher taxonomy']);

      scientificname.push(data_extract['scientific name']);
    }
    dfd.resolve();
    console.log(data);
  });

  //after dfd is resolved from deferred, run
  dfd.done(function() {
    // wait for all data to load
    $.when.apply(this).done(function() {
      var api_data = {'species': mode(scientificname), 'taxonomy': mode(taxon) };
      if(api_data.length ==  0){

        return null
      }
      return console.log(api_data);
    });
  });
}

searchIDigBio("puma concolor");