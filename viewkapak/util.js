function showBrowser(e) {
	e.preventDefault();
	if (this.fileRadioEl.checked) {
		window.pywebview.api.open_file_dialog().then(result => {
			this.pathEl.value = shortPath(result.toString('utf8'));
		});
	} else {
		window.pywebview.api.open_folder_dialog().then(result => {
			this.pathEl.value = shortPath(result.toString('utf8'));
		});
	}
}

function shortPath(path) {
	if (path.length > 27) {
		const sub = path.substring(13, path.length - 13);
		return path.replace(sub, '...');
	}
	return path;
}

function disableForm() {
	const disableEl = document.getElementById('disable');
	disableEl.style.width = '100%';
	disableEl.style.height = '100%';
}

function enableForm() {
	const disableEl = document.getElementById('disable');
	disableEl.style.width = '0%';
	disableEl.style.height = '0%';
}

function logMsg(msg) {
	const msgEl = document.getElementById('message');
	msgEl.innerText = msg;
}

function logError(err) {
	const errEl = document.getElementById('error');
	errEl.innerText = 'Error: ' + err;
}

function showProgress(percentage) {
	const logsDiv = document.querySelector('#logs > div');
	logsDiv.innerHTML = `
		<div id="progressbar" class="w-100">
			<div role="progressbar" aria-valuenow="${percentage}" 
				aria-valuemin="0" aria-valuemax="100" style="width:${percentage}%;">
			</div>
		</div>
		<p id="percentage">${percentage}%</p>
	`;
}

function clearLogs() {
	const msgEl = document.getElementById('message');
	msgEl.innerText = '';
	const errEl = document.getElementById('error');
	errEl.innerText = '';
	const logsDiv = document.querySelector('#logs > div');
	logsDiv.innerHTML = '';
}

function resetForm(id) {
	const form = document.getElementById(id);
	if (form.optionZip) {
		form.optionZip.parentElement.style.display = 'none';
	}
	form.reset();
}