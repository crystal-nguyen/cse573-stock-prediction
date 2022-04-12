document.getElementById("getTweetButton").onclick = function() { predictStockDirection() };

function predictStockDirection() {
	var xhr = new XMLHttpRequest();
	// ### Change endpoint ip to localhost:5000 ###
	var predict_endpoint = "http://192.168.0.199:5000/predict";
	xhr.open("POST", predict_endpoint);
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.send(JSON.stringify({
	    tweetURL: document.getElementById("tweetText").value
	}));
	xhr.onreadystatechange=(e)=>{
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

function getTweets() {
var xhr = new XMLHttpRequest();
	// ### Change endpoint ip to localhost ###
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
		// console.log(jsonResponse['result']);
	}
}