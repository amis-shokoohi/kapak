import { displayFolderOptions, hideFolderOptions, showBrowser, showError } from '/util.js';

export function initDecryptTab() {
	const decryptTab = {
		formEl: document.getElementById('form-decrypt'),
		fileRadioEl: document.getElementById('file-decrypt'),
		folderRadioEl: document.getElementById('folder-decrypt'),
		pathEl: document.querySelector('#form-decrypt section.browser > input'),
		browseBtnEl: document.querySelector('#form-decrypt section.browser button'),
		removeOptionEl: document.getElementById('option-remove-decrypt'),
		zipOptionEl: document.getElementById('option-zip-decrypt'),
		isFile: true
	}

	decryptTab.zipOptionEl.style.display = 'none';

	decryptTab.fileRadioEl.addEventListener('change', hideFolderOptions(decryptTab));
	decryptTab.folderRadioEl.addEventListener('change', displayFolderOptions(decryptTab));
	decryptTab.browseBtnEl.addEventListener('click', showBrowser(decryptTab));
	decryptTab.formEl.addEventListener('submit', handleDecryptFormSubmission(decryptTab));
}

function handleDecryptFormSubmission(tab) {
	return e => {
		e.preventDefault();
		console.log(e.target);
	}
}