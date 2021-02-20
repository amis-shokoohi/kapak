export function EncryptTab() {
	this.formEl = document.getElementById('form-encrypt');
	this.fileRadioEl = document.getElementById('file-encrypt');
	this.folderRadioEl = document.getElementById('folder-encrypt');
	this.pathEl = document.querySelector('#form-encrypt section.browser > input');
	this.browseBtnEl = document.querySelector('#form-encrypt section.browser button');
	this.removeOptionEl = document.getElementById('option-remove-encrypt');
	this.zipOptionEl = document.getElementById('option-zip-encrypt');

	// Hide folder options on initialization
	this.zipOptionEl.style.display = 'none';

	this.fileRadioEl.addEventListener('change', this.hideFolderOptions.bind(this));
	this.folderRadioEl.addEventListener('change', this.displayFolderOptions.bind(this));
	this.browseBtnEl.addEventListener('click', showBrowser.bind(this));
	this.formEl.addEventListener('submit', this.handleFormSubmission.bind(this));
}

EncryptTab.prototype.displayFolderOptions = function (e) {
	if (e.target.checked) {
		this.pathEl.value = 'No folder chosen...';
		this.zipOptionEl.style.display = 'flex';
	}
}

EncryptTab.prototype.hideFolderOptions = function (e) {
	if (e.target.checked) {
		this.pathEl.value = 'No file chosen...';
		this.zipOptionEl.style.display = 'none';
	}
}

EncryptTab.prototype.handleFormSubmission = function (e) {
	e.preventDefault();
	clearLogs();
	
	const targetType = e.target.targetType.value;
	const password = e.target.password.value.trim();
	const password2 = e.target.retypePassword.value.trim();
	const optRm = e.target.optionRemove.checked;
	const optZip = e.target.optionZip.checked;

	if (password === '' || password.length < 3 || password.length > 1024) {
		logError('password should be at least 3 characters');
		return;
	}
	if (password !== password2) {
		logError('passwords do not match');
		return;
	}

	disableForm();

	if (targetType === 'file') {
		window.pywebview.api.encrypt_file(password, optRm);
	} else if (optZip && targetType === 'folder') {
		window.pywebview.api.zip_folder_then_encrypt(password, optRm);
	} else if (targetType === 'folder') {
		window.pywebview.api.encrypt_folder(password, optRm);
	}
}