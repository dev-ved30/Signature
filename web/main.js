async function process_img() {
	let flag = await eel.process_img()();
	if (flag != 1) {
		window.location.href = "home.html";
	}
}
function reprocess() {
	var threshold = document.getElementById('thresh').value;
	eel.change_thresh(threshold);
	document.getElementById('img').src = 'temp/.temp.png';
}
async function save_img() {
	let flag = await eel.save_final_image()();
	if (flag != 1) {
		window.location.href = "choose.html";
	}
}
