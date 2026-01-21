// VaultKeeper API Client
// Gère la communication avec le backend

class VaultKeeperAPI {
    constructor() {
        this.baseURL = 'http://localhost:3000/api'; // Change in production
        this.token = null;
    }

    // Set auth token
    setToken(token) {
        this.token = token;
        chrome.storage.local.set({ apiToken: token });
    }

    // Get auth token
    async getToken() {
        if (this.token) return this.token;
        
        const result = await chrome.storage.local.get(['apiToken']);
        this.token = result.apiToken || null;
        return this.token;
    }

    // Clear token
    async clearToken() {
        this.token = null;
        await chrome.storage.local.remove(['apiToken', 'cloudEmail']);
    }

    // Make API request
    async request(endpoint, options = {}) {
        const token = await this.getToken();
        
        const headers = {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` }),
            ...options.headers
        };

        const response = await fetch(`${this.baseURL}${endpoint}`, {
            ...options,
            headers
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Erreur API');
        }

        return data;
    }

    // Register
    async register(email, password) {
        const data = await this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });

        this.setToken(data.token);
        await chrome.storage.local.set({ cloudEmail: email, syncEnabled: true });
        
        return data;
    }

    // Login
    async login(email, password) {
        const data = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });

        this.setToken(data.token);
        await chrome.storage.local.set({ cloudEmail: email, syncEnabled: true });
        
        return data;
    }

    // Logout
    async logout() {
        await this.clearToken();
        await chrome.storage.local.set({ syncEnabled: false });
    }

    // Verify token
    async verify() {
        try {
            return await this.request('/auth/verify');
        } catch (error) {
            await this.clearToken();
            throw error;
        }
    }

    // Get vault from cloud
    async getVault() {
        return await this.request('/vault');
    }

    // Sync vault to cloud
    async syncVault(encryptedData, salt) {
        return await this.request('/vault/sync', {
            method: 'POST',
            body: JSON.stringify({ encryptedData, salt })
        });
    }

    // Delete vault from cloud
    async deleteVault() {
        return await this.request('/vault', {
            method: 'DELETE'
        });
    }

    // Get sync history
    async getSyncHistory() {
        return await this.request('/vault/history');
    }

    // Check if sync is enabled
    async isSyncEnabled() {
        const result = await chrome.storage.local.get(['syncEnabled']);
        return result.syncEnabled || false;
    }
}

// Instance globale
const vaultAPI = new VaultKeeperAPI();
