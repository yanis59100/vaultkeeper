// VaultKeeper Chrome Extension - Popup Script

let currentFilter = 'all';
let allPasswords = [];
let currentEditId = null;
let isUnlocked = false;
let masterPassword = '';

// Initialisation
document.addEventListener('DOMContentLoaded', async () => {
    initializeParticles();
    await checkLoginStatus();
    setupEventListeners();
});

// Vérifier si déjà connecté
async function checkLoginStatus() {
    const result = await chrome.storage.local.get(['vaultInitialized', 'sessionToken']);
    
    if (!result.vaultInitialized) {
        showScreen('loginScreen');
    } else if (result.sessionToken) {
        // Session active
        showScreen('mainScreen');
        isUnlocked = true;
        await loadPasswords();
    } else {
        showScreen('loginScreen');
    }
}

// Configuration des événements
function setupEventListeners() {
    // Login
    document.getElementById('loginBtn').addEventListener('click', login);
    document.getElementById('createAccountBtn').addEventListener('click', createVault);
    document.getElementById('masterPassword').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') login();
    });
    
    // Main screen
    document.getElementById('addPasswordBtn').addEventListener('click', () => openEditModal());
    document.getElementById('generateBtn').addEventListener('click', () => openGeneratorModal());
    document.getElementById('lockBtn').addEventListener('click', lock);
    document.getElementById('searchInput').addEventListener('input', filterPasswords);
    
    // Filtres
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            currentFilter = e.target.dataset.filter;
            filterPasswords();
        });
    });
    
    // Modal edit
    document.getElementById('saveBtn').addEventListener('click', savePassword);
    document.getElementById('togglePassword').addEventListener('click', togglePasswordVisibility);
    document.getElementById('generatePassword').addEventListener('click', () => {
        const password = vaultCrypto.generatePassword(16, {
            uppercase: true,
            lowercase: true,
            numbers: true,
            symbols: true
        });
        document.getElementById('editPassword').value = password;
        updateStrengthIndicator();
    });
    
    document.getElementById('editPassword').addEventListener('input', updateStrengthIndicator);
    
    // Modal generator
    document.getElementById('lengthSlider').addEventListener('input', (e) => {
        document.getElementById('lengthValue').textContent = e.target.value;
        regeneratePassword();
    });
    
    ['genUppercase', 'genLowercase', 'genNumbers', 'genSymbols'].forEach(id => {
        document.getElementById(id).addEventListener('change', regeneratePassword);
    });
    
    document.getElementById('regenerateBtn').addEventListener('click', regeneratePassword);
    document.getElementById('copyGenerated').addEventListener('click', () => {
        const password = document.getElementById('generatedPassword').value;
        navigator.clipboard.writeText(password);
        showNotification('Copié!');
    });
    
    // Fermeture modals
    document.querySelectorAll('.close-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.getElementById('editModal').style.display = 'none';
            document.getElementById('generatorModal').style.display = 'none';
        });
    });
}

// Créer un nouveau coffre
async function createVault() {
    const password = document.getElementById('masterPassword').value;
    
    if (password.length < 8) {
        showError('Le mot de passe doit contenir au moins 8 caractères');
        return;
    }
    
    const strength = vaultCrypto.calculateStrength(password);
    if (strength.score < 50) {
        showError('Mot de passe trop faible. Utilisez un mot de passe plus fort.');
        return;
    }
    
    // Générer salt et hasher le mot de passe
    const salt = vaultCrypto.generateSalt();
    const passwordHash = await vaultCrypto.hashPassword(password, salt);
    
    // Sauvegarder
    await chrome.storage.local.set({
        vaultInitialized: true,
        passwordHash: passwordHash,
        salt: vaultCrypto.arrayBufferToBase64(salt),
        passwords: [],
        sessionToken: Date.now().toString()
    });
    
    masterPassword = password;
    isUnlocked = true;
    showScreen('mainScreen');
    showNotification('✅ Coffre créé avec succès!');
}

// Connexion
async function login() {
    const password = document.getElementById('masterPassword').value;
    
    if (!password) {
        showError('Entrez votre mot de passe maître');
        return;
    }
    
    const result = await chrome.storage.local.get(['passwordHash', 'salt']);
    
    if (!result.passwordHash || !result.salt) {
        showError('Aucun coffre trouvé. Créez-en un d\'abord.');
        return;
    }
    
    // Vérifier le mot de passe
    const salt = vaultCrypto.base64ToArrayBuffer(result.salt);
    const passwordHash = await vaultCrypto.hashPassword(password, salt);
    
    if (passwordHash !== result.passwordHash) {
        showError('❌ Mot de passe incorrect');
        return;
    }
    
    // Connexion réussie
    masterPassword = password;
    isUnlocked = true;
    
    await chrome.storage.local.set({ sessionToken: Date.now().toString() });
    await loadPasswords();
    showScreen('mainScreen');
}

// Charger les mots de passe
async function loadPasswords() {
    const result = await chrome.storage.local.get(['passwords', 'salt', 'encryptedData']);
    
    if (result.encryptedData) {
        // Déchiffrer les données
        const salt = vaultCrypto.base64ToArrayBuffer(result.salt);
        try {
            allPasswords = await vaultCrypto.decrypt(result.encryptedData, masterPassword, salt);
        } catch (error) {
            console.error('Erreur de déchiffrement:', error);
            allPasswords = [];
        }
    } else {
        allPasswords = result.passwords || [];
    }
    
    displayPasswords();
}

// Afficher les mots de passe
function displayPasswords() {
    const container = document.getElementById('passwordsList');
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    
    let filtered = allPasswords.filter(p => {
        const matchesSearch = !searchTerm || 
            p.name.toLowerCase().includes(searchTerm) ||
            (p.username && p.username.toLowerCase().includes(searchTerm)) ||
            (p.url && p.url.toLowerCase().includes(searchTerm));
        
        const matchesFilter = currentFilter === 'all' || 
            (currentFilter === 'favorites' && p.favorite);
        
        return matchesSearch && matchesFilter;
    });
    
    // Trier: favoris en premier
    filtered.sort((a, b) => {
        if (a.favorite && !b.favorite) return -1;
        if (!a.favorite && b.favorite) return 1;
        return a.name.localeCompare(b.name);
    });
    
    if (filtered.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🔐</div>
                <p>${allPasswords.length === 0 ? 'Aucun mot de passe enregistré' : 'Aucun résultat'}</p>
            </div>
        `;
    } else {
        container.innerHTML = filtered.map(p => `
            <div class="password-item" data-id="${p.id}">
                <div class="password-item-header">
                    <span class="password-item-name">${escapeHtml(p.name)}</span>
                    ${p.favorite ? '<span class="password-item-favorite">⭐</span>' : ''}
                </div>
                ${p.username ? `<div class="password-item-username">${escapeHtml(p.username)}</div>` : ''}
                <span class="password-item-category">${getCategoryDisplay(p.category)}</span>
                <div class="password-item-actions">
                    <button onclick="copyPassword('${p.id}')">📋 Copier</button>
                    <button onclick="fillPassword('${p.id}')">✏️ Remplir</button>
                    <button onclick="editPassword('${p.id}')">📝 Éditer</button>
                    <button onclick="deletePassword('${p.id}')">🗑️</button>
                </div>
            </div>
        `).join('');
    }
    
    document.getElementById('passwordCount').textContent = `${allPasswords.length} mot${allPasswords.length > 1 ? 's' : ''} de passe`;
}

// Filtrer les mots de passe
function filterPasswords() {
    displayPasswords();
}

// Ouvrir modal d'édition
function openEditModal(passwordId = null) {
    currentEditId = passwordId;
    const modal = document.getElementById('editModal');
    const title = document.getElementById('modalTitle');
    
    if (passwordId) {
        const password = allPasswords.find(p => p.id === passwordId);
        title.textContent = 'Modifier le mot de passe';
        document.getElementById('editName').value = password.name;
        document.getElementById('editUsername').value = password.username || '';
        document.getElementById('editPassword').value = password.password;
        document.getElementById('editUrl').value = password.url || '';
        document.getElementById('editCategory').value = password.category || 'Other';
        document.getElementById('editNotes').value = password.notes || '';
        document.getElementById('editFavorite').checked = password.favorite || false;
    } else {
        title.textContent = 'Ajouter un mot de passe';
        document.getElementById('editName').value = '';
        document.getElementById('editUsername').value = '';
        document.getElementById('editPassword').value = '';
        document.getElementById('editUrl').value = '';
        document.getElementById('editCategory').value = 'Other';
        document.getElementById('editNotes').value = '';
        document.getElementById('editFavorite').checked = false;
    }
    
    updateStrengthIndicator();
    modal.style.display = 'flex';
}

// Sauvegarder un mot de passe
async function savePassword() {
    const name = document.getElementById('editName').value.trim();
    const password = document.getElementById('editPassword').value;
    
    if (!name || !password) {
        alert('Le nom et le mot de passe sont requis');
        return;
    }
    
    const passwordData = {
        id: currentEditId || Date.now().toString(),
        name,
        username: document.getElementById('editUsername').value.trim(),
        password,
        url: document.getElementById('editUrl').value.trim(),
        category: document.getElementById('editCategory').value,
        notes: document.getElementById('editNotes').value.trim(),
        favorite: document.getElementById('editFavorite').checked,
        created: currentEditId ? allPasswords.find(p => p.id === currentEditId).created : new Date().toISOString(),
        modified: new Date().toISOString()
    };
    
    if (currentEditId) {
        const index = allPasswords.findIndex(p => p.id === currentEditId);
        allPasswords[index] = passwordData;
    } else {
        allPasswords.push(passwordData);
    }
    
    await saveToStorage();
    displayPasswords();
    document.getElementById('editModal').style.display = 'none';
    showNotification('✅ Enregistré!');
}

// Sauvegarder dans le storage (chiffré)
async function saveToStorage() {
    const result = await chrome.storage.local.get(['salt']);
    const salt = vaultCrypto.base64ToArrayBuffer(result.salt);
    const encryptedData = await vaultCrypto.encrypt(allPasswords, masterPassword, salt);
    
    await chrome.storage.local.set({ 
        encryptedData,
        passwords: [] // Garder vide, tout est chiffré
    });
}

// Copier un mot de passe
window.copyPassword = async function(id) {
    const password = allPasswords.find(p => p.id === id);
    await navigator.clipboard.writeText(password.password);
    showNotification('📋 Mot de passe copié!');
};

// Remplir le mot de passe sur la page
window.fillPassword = async function(id) {
    const password = allPasswords.find(p => p.id === id);
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    await chrome.tabs.sendMessage(tab.id, {
        action: 'fillPassword',
        username: password.username,
        password: password.password
    });
    
    showNotification('✏️ Rempli!');
};

// Éditer un mot de passe
window.editPassword = function(id) {
    openEditModal(id);
};

// Supprimer un mot de passe
window.deletePassword = async function(id) {
    if (!confirm('Supprimer ce mot de passe?')) return;
    
    allPasswords = allPasswords.filter(p => p.id !== id);
    await saveToStorage();
    displayPasswords();
    showNotification('🗑️ Supprimé!');
};

// Ouvrir le générateur
function openGeneratorModal() {
    regeneratePassword();
    document.getElementById('generatorModal').style.display = 'flex';
}

// Régénérer un mot de passe
function regeneratePassword() {
    const length = parseInt(document.getElementById('lengthSlider').value);
    const options = {
        uppercase: document.getElementById('genUppercase').checked,
        lowercase: document.getElementById('genLowercase').checked,
        numbers: document.getElementById('genNumbers').checked,
        symbols: document.getElementById('genSymbols').checked
    };
    
    const password = vaultCrypto.generatePassword(length, options);
    document.getElementById('generatedPassword').value = password;
}

// Basculer visibilité mot de passe
function togglePasswordVisibility() {
    const input = document.getElementById('editPassword');
    const btn = document.getElementById('togglePassword');
    
    if (input.type === 'password') {
        input.type = 'text';
        btn.textContent = '🙈';
    } else {
        input.type = 'password';
        btn.textContent = '👁️';
    }
}

// Mettre à jour l'indicateur de force
function updateStrengthIndicator() {
    const password = document.getElementById('editPassword').value;
    const strength = vaultCrypto.calculateStrength(password);
    
    const fill = document.getElementById('strengthFill');
    const text = document.getElementById('strengthText');
    
    fill.style.width = strength.score + '%';
    fill.style.background = strength.color;
    text.textContent = strength.text;
    text.style.color = strength.color;
}

// Verrouiller
async function lock() {
    await chrome.storage.local.remove('sessionToken');
    masterPassword = '';
    isUnlocked = false;
    allPasswords = [];
    document.getElementById('masterPassword').value = '';
    showScreen('loginScreen');
}

// Utilitaires
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.style.display = 'none');
    document.getElementById(screenId).style.display = 'block';
}

function showError(message) {
    const errorEl = document.getElementById('loginError');
    errorEl.textContent = message;
    errorEl.style.display = 'block';
    setTimeout(() => errorEl.style.display = 'none', 3000);
}

function showNotification(message) {
    // Simple notification (peut être amélioré)
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        background: linear-gradient(135deg, #00fff9, #b537ff);
        color: white;
        padding: 10px 15px;
        border-radius: 8px;
        font-size: 12px;
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 2000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function getCategoryDisplay(category) {
    const categories = {
        'Banking': '💳 Banque',
        'Email': '📧 Email',
        'Social': '👥 Social',
        'Work': '💼 Travail',
        'Gaming': '🎮 Gaming',
        'Other': '📁 Autre'
    };
    return categories[category] || categories['Other'];
}

// Particules canvas
function initializeParticles() {
    const canvas = document.getElementById('particles');
    const ctx = canvas.getContext('2d');
    
    canvas.width = 380;
    canvas.height = 600;
    
    const particles = [];
    const colors = ['#00fff9', '#ff006e', '#b537ff', '#00ff88', '#ff6b00'];
    
    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2 + 1;
            this.speedX = Math.random() * 0.3 - 0.15;
            this.speedY = Math.random() * 0.3 - 0.15;
            this.color = colors[Math.floor(Math.random() * colors.length)];
        }
        
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            
            if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
            if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
        }
        
        draw() {
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }
    
    for (let i = 0; i < 30; i++) {
        particles.push(new Particle());
    }
    
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => {
            p.update();
            p.draw();
        });
        requestAnimationFrame(animate);
    }
    
    animate();
}
