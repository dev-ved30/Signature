function process_img() {
	eel.process_img();
	console.log('Initial processing is complete');
	console.log('Redirecting to edit page');
}
function reprocess() {
	var threshold = document.getElementById('thresh').value;
	eel.change_thresh(threshold);
	document.getElementById('img').src = 'temp/.temp.png';
	console.log('Threshold re-processing is complete. Threshold is set to ' + threshold);
}
function save_img() {
	eel.save_final_image();
}
