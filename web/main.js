/**
 * Called when the user chooses an image. If the user doesn't actually choose a file
 * the python return value will be used to continue on the same page rather than change to choose.html.
 */
async function process_img() {
	let flag = await eel.process_img()();
	if (flag != 1) {
		window.location.href = "home.html";
	}
}

/**
 * Called when the user adjusts the slider threshold.
 */
function reprocess() {
	var threshold = document.getElementById('thresh').value;
	eel.change_thresh(threshold);
	document.getElementById('img').src = 'temp/.temp.png';
}

/**
 * Called when the user wants to save their image. If they don't go through
 * with saving the image then nothing happens and we continue in the same page.
 */
async function save_img() {
	let flag = await eel.save_final_image()();
	if (flag != 1) {
		window.location.href = "choose.html";
	}
}
