function getBathValue() {
  var uiBathrooms = document.getElementsByName("uiBathrooms");
  for(var i in uiBathrooms) {
    if(uiBathrooms[i].checked) {
        return parseInt(i)+1;
    }
  }
  return -1;
}

function getBHKValue() {
  var uiBHrooms = document.getElementsByName("uiBHK");
  for(var i in uiBHrooms) {
    if(uiBHrooms[i].checked) {
        return parseInt(i)+1;
    }
  }
  return -1;
}

function onClickedEstimatePrice() {
  console.log("Estimate price button clicked");
  var sqft = document.getElementById("uiSqft");
  var bhk = getBHKValue();
  var bathrooms = getBathValue();
  var location = document.getElementById("uiLocations");
  var estPrice = document.getElementById("uiEstimatedPrice");

  // Update the URL to match your server port
  var url = "http://127.0.0.1:8000/predict_home_price";

  // Send data as JSON
  fetch(url, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          total_sqft: parseFloat(sqft.value),
          bhk: bhk,
          bath: bathrooms,
          location: location.value
      })
  })
  .then(response => response.json())
  .then(data => {
      if (data.error) {
          estPrice.innerHTML = "<h2>Error: " + data.error + "</h2>";
      } else {
          estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " Lakh</h2>";
      }
  })
  .catch(error => {
      console.error('Error:', error);
      estPrice.innerHTML = "<h2>Error: Unable to get estimated price</h2>";
  });
}

function onPageLoad() {
  console.log("document loaded");
  // Update the URL to match your server port
  var url = "http://127.0.0.1:8000/get_location_names";
  
  fetch(url)
      .then(response => response.json())
      .then(data => {
          console.log("got response for get_location_names request");
          if(data && data.locations) {
              var locations = data.locations;
              var uiLocations = document.getElementById("uiLocations");
              uiLocations.innerHTML = '<option value="" disabled="disabled" selected="selected">Choose a Location</option>';
              
              locations.forEach(location => {
                  var opt = document.createElement('option');
                  opt.value = location;
                  opt.innerHTML = location;
                  uiLocations.appendChild(opt);
              });
          }
      })
      .catch(error => {
          console.error('Error:', error);
      });
}

window.onload = onPageLoad;