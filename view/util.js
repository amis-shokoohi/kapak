export function displayFolderOptions(tab) {
	return e => {
		if (e.target.checked)
			tab.isFile = false;
		tab.pathEl.value = 'No folder chosen...';
		tab.zipOptionEl.style.display = 'flex';
	}
}

export function hideFolderOptions(tab) {
	return e => {
		if (e.target.checked)
			tab.isFile = true;
		tab.pathEl.value = 'No file chosen...';
		tab.zipOptionEl.style.display = 'none';
	}
}

export function showBrowser(tab) {
	return e => {
		e.preventDefault();
		if (tab.isFile) {
			window.pywebview.api.open_file_dialog().then(result => {
				alert(typeof result);
				tab.pathEl.value = shortPath(result.toString('utf8'));
			});
		} else {
			window.pywebview.api.open_folder_dialog().then(result => {
				tab.pathEl.value = shortPath(result.toString('utf8'));
			});
		}
	}
}

function shortPath(path) {
	if (path.length > 29) {
		const sub = path.substring(14, path.length - 14);
		return path.replace(sub, '...');
	}
	return path;
}

export function showError(msg) {
	const duration = 3000;
	const card = document.createElement('div');
	card.innerText = msg;
	card.classList.add('err-card');
	const logo = document.getElementById('logo');
	document.body.insertBefore(card, logo);
	setTimeout(() => card.style.top = '3rem', 100);
	setTimeout(() => card.style.top = '-3rem', duration);
	setTimeout(() => card.remove(), duration + 200);
}