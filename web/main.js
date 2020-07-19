async function process_img() {
	let x = await eel.process_img()();
	if (x != 1) {
		//document.getElementById("home_form").action = "home.html";
		window.location.href = "home.html";
	} else {
		//document.getElementById("home_form").action = "choose.html";
		window.location.href = "choose.html";
	}
	console.log('Initial processing is complete');
}
function reprocess() {
	var threshold = document.getElementById('thresh').value;
	eel.change_thresh(threshold);
	document.getElementById('img').src = 'temp/.temp.png';
	console.log('Threshold re-processing is complete. Threshold is set to ' + threshold);
}
function save_img() {
	eel.save_final_image();
	console.log('Final Image Saved');
}
