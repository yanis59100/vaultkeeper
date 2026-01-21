// VaultKeeper - Content Script (injection dans les pages web)

// Écouter les messages de la popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'fillPassword') {
        fillPasswordFields(request.username, request.password);
        sendResponse({ success: true });
    }
});

// Remplir automatiquement les champs de formulaire
function fillPasswordFields(username, password) {
    // Chercher les champs username/email
    const usernameFields = document.querySelectorAll('input[type="email"], input[type="text"][autocomplete*="username"], input[name*="user"], input[name*="email"], input[id*="user"], input[id*="email"]');
    
    // Chercher les champs password
    const passwordFields = document.querySelectorAll('input[type="password"]');
    
    // Remplir le champ username si trouvé
    if (username && usernameFields.length > 0) {
        const usernameField = usernameFields[0];
        usernameField.value = username;
        usernameField.dispatchEvent(new Event('input', { bubbles: true }));
        usernameField.dispatchEvent(new Event('change', { bubbles: true }));
        
        // Animation visuelle
        animateField(usernameField);
    }
    
    // Remplir le champ password
    if (password && passwordFields.length > 0) {
        const passwordField = passwordFields[0];
        passwordField.value = password;
        passwordField.dispatchEvent(new Event('input', { bubbles: true }));
        passwordField.dispatchEvent(new Event('change', { bubbles: true }));
        
        // Animation visuelle
        animateField(passwordField);
    }
    
    // Notification
    showPageNotification('✅ Rempli par VaultKeeper');
}

// Animation du champ rempli
function animateField(field) {
    const originalBorder = field.style.border;
    field.style.border = '2px solid #00fff9';
    field.style.boxShadow = '0 0 10px rgba(0, 255, 249, 0.5)';
    
    setTimeout(() => {
        field.style.border = originalBorder;
        field.style.boxShadow = '';
    }, 1000);
}

// Notification sur la page
function showPageNotification(message) {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #00fff9, #b537ff);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        font-weight: 600;
        z-index: 999999;
        box-shadow: 0 5px 20px rgba(0, 255, 249, 0.4);
        animation: slideIn 0.3s ease;
    `;
    
    // Ajouter animation CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => notification.remove(), 300);
    }, 2500);
}

// Détecter les formulaires de connexion et proposer de sauvegarder
document.addEventListener('submit', (e) => {
    if (e.target.tagName === 'FORM') {
        const passwordFields = e.target.querySelectorAll('input[type="password"]');
        if (passwordFields.length > 0) {
            // Potentiellement un formulaire de connexion
            // On pourrait proposer de sauvegarder le mot de passe ici
            console.log('Formulaire de connexion détecté');
        }
    }
});
