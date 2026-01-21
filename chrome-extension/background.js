// VaultKeeper - Background Service Worker

// Installation
chrome.runtime.onInstalled.addListener(() => {
    console.log('VaultKeeper installé!');
});

// Écouter les messages
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getPasswords') {
        // Récupérer les mots de passe pour le domaine actuel
        chrome.storage.local.get(['passwords', 'encryptedData'], (result) => {
            sendResponse({ passwords: result.passwords || [] });
        });
        return true;
    }
});

// Auto-lock après 15 minutes d'inactivité
let lockTimer;

function resetLockTimer() {
    clearTimeout(lockTimer);
    lockTimer = setTimeout(() => {
        chrome.storage.local.remove('sessionToken');
        console.log('Session verrouillée automatiquement');
    }, 15 * 60 * 1000); // 15 minutes
}

// Réinitialiser le timer à chaque activité
chrome.tabs.onActivated.addListener(resetLockTimer);
chrome.tabs.onUpdated.addListener(resetLockTimer);

resetLockTimer();
