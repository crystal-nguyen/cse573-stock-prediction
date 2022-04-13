document.getElementById("getTweetButton").onclick = function() { predictStockDirection() };

function predictStockDirection() {
var xhr = new XMLHttpRequest();

	// ### ! change endpoint to your own localhost ip ! ###
	var predict_endpoint = "http://192.168.0.199:5000/tweets";
	xhr.open("POST", predict_endpoint);
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.send(JSON.stringify({
	    tweetURL: document.getElementById("tweetText").value
	}));
	xhr.onreadystatechange=(e)=>{
		var jsonResponse = JSON.parse(xhr.responseText);
		document.getElementById('tweetResult').innerHTML = jsonResponse['result'];
	}
}