import { displayFolderOptions, hideFolderOptions, showBrowser, showError } from '/util.js';

export function initEncryptTab() {
	const encryptTab = {
		formEl: document.getElementById('form-encrypt'),
		fileRadioEl: document.getElementById('file-encrypt'),
		folderRadioEl: document.getElementById('folder-encrypt'),
		pathEl: document.querySelector('#form-encrypt section.browser > input'),
		browseBtnEl: document.querySelector('#form-encrypt section.browser button'),
		removeOptionEl: document.getElementById('option-remove-encrypt'),
		zipOptionEl: document.getElementById('option-zip-encrypt'),
		isFile: true
	}

	encryptTab.zipOptionEl.style.display = 'none';

	encryptTab.fileRadioEl.addEventListener('change', hideFolderOptions(encryptTab));
	encryptTab.folderRadioEl.addEventListener('change', displayFolderOptions(encryptTab));
	encryptTab.browseBtnEl.addEventListener('click', showBrowser(encryptTab));
	encryptTab.formEl.addEventListener('submit', handleEncryptFormSubmission(encryptTab));
}

function handleEncryptFormSubmission(tab) {
	return e => {
		e.preventDefault();
		const targetType = e.target.targetType.value;
		const password = e.target.password.value.trim();
		const optRm = e.target.optionRemove.checked;
		const optZip = e.target.optionZip.checked;

		if (password === '' || password.length < 3 || password.length > 1024) {
			showError('password should be at least 3 characters');
			return;
		}

		if (targetType === 'file') {
			window.pywebview.api.encrypt_file(password, optRm);
		} else if (optZip && targetType === 'folder') {
			window.pywebview.api.zip_folder_then_encrypt(password, optRm);
		} else if (targetType === 'folder') {
			window.pywebview.api.encrypt_folder(password, optRm);
		}
	}
}