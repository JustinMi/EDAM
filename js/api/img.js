
 $.ajax({
    // currently gets 5 results
    type: "POST",
    dataType: 'jsonp',
    
    url: 'https://www.googleapis.com/customsearch/v1?q='+'puma concolor'+'&key=AIzaSyB9GKaKX2TRnMH8M28bVD8BfG-rR7H7RJs&cx=006284769470110551168:rbgx9geslba',
  }).done(function(data) {
    // check if there are results
    if (data.length != 0) {
      console.log(data);
      alert(data.items[0].pagemap.cse_image[0].src);
    }

    // notify search complete
   
  });
