function process_img() {
	eel.process();
	console.log('Initial processing is complete');
	console.log('Redirecting to edit page');
}
function reprocess() {
	var threshold = document.getElementById('thresh').value;
	eel.change_thresh(threshold);
	console.log('Threshold re-processing is complete');
}
function save_img() {
	eel.save_final_image();
	console.log('Final image is now saved');
}
