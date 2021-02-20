export function DecryptTab() {
	this.formEl = document.getElementById('form-decrypt');
	this.fileRadioEl = document.getElementById('file-decrypt');
	this.folderRadioEl = document.getElementById('folder-decrypt');
	this.pathEl = document.querySelector('#form-decrypt section.browser > input');
	this.browseBtnEl = document.querySelector('#form-decrypt section.browser button');
	this.removeOptionEl = document.getElementById('option-remove-decrypt');

	this.fileRadioEl.addEventListener('change', this.hideFolderOptions.bind(this));
	this.folderRadioEl.addEventListener('change', this.displayFolderOptions.bind(this));
	this.browseBtnEl.addEventListener('click', showBrowser.bind(this));
	this.formEl.addEventListener('submit', this.handleFormSubmission.bind(this));
}

DecryptTab.prototype.displayFolderOptions = function (e) {
	if (e.target.checked)
		this.pathEl.value = 'No folder chosen...';
}

DecryptTab.prototype.hideFolderOptions = function (e) {
	if (e.target.checked)
		this.pathEl.value = 'No file chosen...';
}

DecryptTab.prototype.handleFormSubmission = function (e) {
	e.preventDefault();
	clearLogs();
	
	const targetType = e.target.targetType.value;
	const password = e.target.password.value.trim();
	const optRm = e.target.optionRemove.checked;

	if (password === '' || password.length < 3 || password.length > 1024) {
		logError('password should be at least 3 characters');
		return;
	}

	disableForm();

	if (targetType === 'file') {
		window.pywebview.api.decrypt_file(password, optRm);
	} else if (targetType === 'folder') {
		window.pywebview.api.decrypt_folder(password, optRm);
	}
}