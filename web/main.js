var x = 10;

function process_img() {
	eel.process_img();
	console.log('Initial processing is complete');
	console.log('Redirecting to edit page');
}
function reprocess() {
	var threshold = document.getElementById('thresh').value;
	eel.change_thresh(threshold);
	console.log('Threshold re-processing is complete. Threshold is set to ' + threshold);
	location.reload();
}
function save_img() {
	eel.save_final_image();
	console.log('Final image is now saved');
}
function get_thresh() {
	var x = 200;
	eel.get_thresh_val()(function(ret) {
		console.log(ret);
		x = ret;
	});
	return x;
}
