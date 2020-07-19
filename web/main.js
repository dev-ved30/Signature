function process_img() {
	eel.process_img();
	console.log('Initial processing is complete');
	console.log('Redirecting to edit page');
}
function reprocess() {
	var threshold = document.getElementById('thresh').value;
	eel.change_thresh(threshold);
	document.cookie = document.getElementById('thresh').value;
	console.log('Threshold re-processing is complete. Threshold is set to ' + threshold);
	location.reload();
}
function save_img() {
	eel.save_final_image();
}
/* function get_cookie_value() {
	var x = document.cookie;
	var val = x.split(';');
	console.log(val[1]);
	return val[1];
} */
