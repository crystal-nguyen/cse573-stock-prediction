document.getElementById("predictButton").onclick = function() { predictStockDirection() };

function predictStockDirection() {
	var xhr = new XMLHttpRequest();
	var predict_endpoint = "http://10.0.2.15:5000/predict";
	xhr.open("POST", predict_endpoint);
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.send(JSON.stringify({
	    tweet: document.getElementById("tweetText").value
	}));
	xhr.onreadystatechange=(e)=>{
		var jsonResponse = JSON.parse(xhr.responseText);

		/*
		if (jsonResponse['direction'] == 'up') {
			var arrow = document.getElementById('up_arrow');
			arrow.style.visibility = ('visible');
		} else {
			var arrow = document.getElementById('down_arrow');
			arrow.style.visibility = ('visible');
		}
		*/
	}
}
