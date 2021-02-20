import { EncryptTab } from '/encrypt.js';
import { DecryptTab } from '/decrypt.js';

const navLinkEncrypt = document.getElementById('nav-link-encrypt');
const navLinkDecrypt = document.getElementById('nav-link-decrypt');
const tabEncrypt = document.getElementById('tab-encrypt');
const tabDecrypt = document.getElementById('tab-decrypt');

const encryptTab = new EncryptTab();
const decryptTab = new DecryptTab();
tabDecrypt.setAttribute('hidden', '');

navLinkEncrypt.addEventListener('click', e => {
	activateTabLink(navLinkEncrypt, navLinkDecrypt);
	tabDecrypt.setAttribute('hidden', '');
	tabEncrypt.removeAttribute('hidden');
	flash(tabEncrypt);
});

navLinkDecrypt.addEventListener('click', e => {
	activateTabLink(navLinkDecrypt, navLinkEncrypt);
	tabEncrypt.setAttribute('hidden', '');
	tabDecrypt.removeAttribute('hidden');
	flash(tabDecrypt);
});

function activateTabLink(currLink, otherLink) {
	if (otherLink.classList.contains('active')) {
		otherLink.classList.remove('active');
		currLink.classList.add('active');
	}
}

function flash(el) {
	const currBgColor = el.style.backgroundColor;
	el.style.backgroundColor = 'rgba(30, 30, 30, 0.5)';
	setTimeout(() => {
		el.style.backgroundColor = currBgColor;
	}, 100);
}