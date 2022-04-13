document.getElementById("getTweetButton").onclick = function() { predictStockDirection() };

function predictStockDirection() {
var xhr = new XMLHttpRequest();
var m1prediction = ''
var m2prediction = ''
var m3prediction = ''


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
		document.getElementById('tweetResult').innerHTML = jsonResponse['result']
		// console.log(jsonResponse['m1prediction']);
		// console.log(jsonResponse['m2prediction']);
		// console.log(jsonResponse['m3prediction']);
		m1prediction = parseInt(JSON.stringify(jsonResponse['m1prediction']).charAt(1))
		m2prediction = JSON.stringify(jsonResponse['m2prediction'])
		m2prediction = parseInt(m2prediction.charAt(2))
		m3prediction = parseInt(JSON.stringify(jsonResponse['m3prediction']).charAt(1))
		overallPrediction = m1prediction + m2prediction + m3prediction
		console.log(m1prediction);
		console.log(m2prediction);
		console.log(m3prediction);
		computeM1prediction(m1prediction);
		computeM2prediction(m2prediction);
		computeM3prediction(m3prediction);
		computeOverallPrediction(overallPrediction);
	}
}

function computeOverallPrediction(overallPrediction){
	var img = document.getElementById("arrowOverall");
	// show up
	if (overallPrediction >= 2){
		document.getElementById("arrowOverall").src="./up_arrow.png";
		img.style.visibility = 'visible';
	}
	// show down
	else if (overallPrediction == 1 || overallPrediction == 0) {
		document.getElementById("arrowOverall").src="./down_arrow.png";
		img.style.visibility = 'visible';
	}
	// stay hidden
	else{
		img.style.visibility = 'hidden';
	}
}

function computeM1prediction(m1){
	var img = document.getElementById("arrow1");
	// show up
	if (overallPrediction >= 2){
		document.getElementById("arrow1").src="./up_arrow.png";
		img.style.visibility = 'visible';
	}
	// show down
	else if (overallPrediction == 1 || overallPrediction == 0) {
		document.getElementById("arrow1").src="./down_arrow.png";
		img.style.visibility = 'visible';
	}
	// stay hidden
	else{
		img.style.visibility = 'hidden';
	}
}
function computeM2prediction(m2){
	var img = document.getElementById("arrow2");
	// show up
	if (overallPrediction >= 2){
		document.getElementById("arrow2").src="./up_arrow.png";
		img.style.visibility = 'visible';
	}
	// show down
	else if (overallPrediction == 1 || overallPrediction == 0) {
		document.getElementById("arrow2").src="./down_arrow.png";
		img.style.visibility = 'visible';
	}
	// stay hidden
	else{
		img.style.visibility = 'hidden';
	}
}
function computeM3prediction(m3){
	var img = document.getElementById("arrow3");
	// show up
	if (overallPrediction >= 2){
		document.getElementById("arrow3").src="./up_arrow.png";
		img.style.visibility = 'visible';
	}
	// show down
	else if (overallPrediction == 1 || overallPrediction == 0) {
		document.getElementById("arrow3").src="./down_arrow.png";
		img.style.visibility = 'visible';
	}
	// stay hidden
	else{
		img.style.visibility = 'hidden';
	}
}