// Crypto utilities pour VaultKeeper Chrome Extension
// Utilise Web Crypto API pour AES-256-GCM

class VaultCrypto {
    constructor() {
        this.encoder = new TextEncoder();
        this.decoder = new TextDecoder();
    }

    // Dériver une clé depuis le mot de passe maître
    async deriveKey(masterPassword, salt) {
        const passwordKey = await crypto.subtle.importKey(
            'raw',
            this.encoder.encode(masterPassword),
            'PBKDF2',
            false,
            ['deriveKey']
        );

        return await crypto.subtle.deriveKey(
            {
                name: 'PBKDF2',
                salt: salt,
                iterations: 100000,
                hash: 'SHA-256'
            },
            passwordKey,
            { name: 'AES-GCM', length: 256 },
            false,
            ['encrypt', 'decrypt']
        );
    }

    // Générer un salt aléatoire
    generateSalt() {
        return crypto.getRandomValues(new Uint8Array(16));
    }

    // Générer un IV (Initialization Vector)
    generateIV() {
        return crypto.getRandomValues(new Uint8Array(12));
    }

    // Crypter des données
    async encrypt(data, masterPassword, salt) {
        const key = await this.deriveKey(masterPassword, salt);
        const iv = this.generateIV();
        
        const encryptedData = await crypto.subtle.encrypt(
            { name: 'AES-GCM', iv: iv },
            key,
            this.encoder.encode(JSON.stringify(data))
        );

        // Retourner IV + données cryptées en base64
        const combined = new Uint8Array(iv.length + encryptedData.byteLength);
        combined.set(iv, 0);
        combined.set(new Uint8Array(encryptedData), iv.length);

        return this.arrayBufferToBase64(combined);
    }

    // Décrypter des données
    async decrypt(encryptedBase64, masterPassword, salt) {
        try {
            const key = await this.deriveKey(masterPassword, salt);
            const combined = this.base64ToArrayBuffer(encryptedBase64);
            
            // Extraire IV et données
            const iv = combined.slice(0, 12);
            const data = combined.slice(12);

            const decryptedData = await crypto.subtle.decrypt(
                { name: 'AES-GCM', iv: iv },
                key,
                data
            );

            return JSON.parse(this.decoder.decode(decryptedData));
        } catch (error) {
            throw new Error('Mot de passe incorrect ou données corrompues');
        }
    }

    // Hash du mot de passe maître pour vérification
    async hashPassword(password, salt) {
        // Utiliser PBKDF2 directement pour le hash
        const passwordKey = await crypto.subtle.importKey(
            'raw',
            this.encoder.encode(password),
            'PBKDF2',
            false,
            ['deriveBits']
        );

        const hashBits = await crypto.subtle.deriveBits(
            {
                name: 'PBKDF2',
                salt: salt,
                iterations: 100000,
                hash: 'SHA-256'
            },
            passwordKey,
            256
        );

        return this.arrayBufferToBase64(new Uint8Array(hashBits));
    }

    // Utilitaires de conversion
    arrayBufferToBase64(buffer) {
        let binary = '';
        const bytes = new Uint8Array(buffer);
        for (let i = 0; i < bytes.byteLength; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return btoa(binary);
    }

    base64ToArrayBuffer(base64) {
        const binary = atob(base64);
        const bytes = new Uint8Array(binary.length);
        for (let i = 0; i < binary.length; i++) {
            bytes[i] = binary.charCodeAt(i);
        }
        return bytes;
    }

    // Générer un mot de passe aléatoire
    generatePassword(length = 16, options = {}) {
        const {
            uppercase = true,
            lowercase = true,
            numbers = true,
            symbols = true
        } = options;

        let chars = '';
        if (uppercase) chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        if (lowercase) chars += 'abcdefghijklmnopqrstuvwxyz';
        if (numbers) chars += '0123456789';
        if (symbols) chars += '!@#$%^&*()_+-=[]{}|;:,.<>?';

        if (chars.length === 0) {
            throw new Error('Au moins une option doit être sélectionnée');
        }

        const randomValues = new Uint8Array(length);
        crypto.getRandomValues(randomValues);

        let password = '';
        for (let i = 0; i < length; i++) {
            password += chars[randomValues[i] % chars.length];
        }

        return password;
    }

    // Calculer la force du mot de passe
    calculateStrength(password) {
        if (!password) return { score: 0, text: '', color: '' };

        let score = 0;
        
        // Longueur
        if (password.length >= 8) score += 1;
        if (password.length >= 12) score += 1;
        if (password.length >= 16) score += 1;
        
        // Complexité
        if (/[a-z]/.test(password)) score += 1;
        if (/[A-Z]/.test(password)) score += 1;
        if (/[0-9]/.test(password)) score += 1;
        if (/[^a-zA-Z0-9]/.test(password)) score += 1;
        
        // Variété de caractères
        const uniqueChars = new Set(password).size;
        if (uniqueChars >= password.length * 0.6) score += 1;

        // Déterminer le niveau
        let level, text, color;
        if (score <= 2) {
            level = 25;
            text = '❌ Très faible';
            color = '#ff006e';
        } else if (score <= 4) {
            level = 50;
            text = '⚠️ Faible';
            color = '#ff6b00';
        } else if (score <= 6) {
            level = 75;
            text = '✅ Moyen';
            color = '#00ff88';
        } else {
            level = 100;
            text = '🔐 Fort';
            color = '#00fff9';
        }

        return { score: level, text, color };
    }
}

// Instance globale
const vaultCrypto = new VaultCrypto();
