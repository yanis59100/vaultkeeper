const express = require('express');
const router = express.Router();
const { body, validationResult } = require('express-validator');
const db = require('../config/database');
const { authenticateToken } = require('../middleware/auth');

// All vault routes require authentication
router.use(authenticateToken);

// Get user's vault
router.get('/', async (req, res) => {
    try {
        const result = await db.query(
            'SELECT encrypted_data, salt, version, updated_at FROM vaults WHERE user_id = $1',
            [req.user.userId]
        );

        if (result.rows.length === 0) {
            return res.status(404).json({ error: 'Aucun coffre trouvé' });
        }

        const vault = result.rows[0];

        // Log sync
        await db.query(
            'INSERT INTO sync_logs (user_id, action, ip_address, user_agent) VALUES ($1, $2, $3, $4)',
            [req.user.userId, 'download', req.ip, req.get('user-agent')]
        );

        res.json({
            encryptedData: vault.encrypted_data,
            salt: vault.salt,
            version: vault.version,
            updatedAt: vault.updated_at
        });
    } catch (error) {
        console.error('Get vault error:', error);
        res.status(500).json({ error: 'Erreur lors de la récupération du coffre' });
    }
});

// Upload/sync vault
router.post('/sync', [
    body('encryptedData').notEmpty().withMessage('Données cryptées requises'),
    body('salt').notEmpty().withMessage('Salt requis')
], async (req, res) => {
    try {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }

        const { encryptedData, salt } = req.body;

        // Check if vault exists
        const existing = await db.query(
            'SELECT id, version FROM vaults WHERE user_id = $1',
            [req.user.userId]
        );

        let result;

        if (existing.rows.length === 0) {
            // Create new vault
            result = await db.query(
                'INSERT INTO vaults (user_id, encrypted_data, salt, version) VALUES ($1, $2, $3, 1) RETURNING id, version, updated_at',
                [req.user.userId, encryptedData, salt]
            );
        } else {
            // Update existing vault
            const newVersion = existing.rows[0].version + 1;
            result = await db.query(
                'UPDATE vaults SET encrypted_data = $1, salt = $2, version = $3 WHERE user_id = $4 RETURNING id, version, updated_at',
                [encryptedData, salt, newVersion, req.user.userId]
            );
        }

        // Log sync
        await db.query(
            'INSERT INTO sync_logs (user_id, action, ip_address, user_agent) VALUES ($1, $2, $3, $4)',
            [req.user.userId, 'upload', req.ip, req.get('user-agent')]
        );

        res.json({
            message: 'Coffre synchronisé avec succès',
            version: result.rows[0].version,
            updatedAt: result.rows[0].updated_at
        });
    } catch (error) {
        console.error('Sync vault error:', error);
        res.status(500).json({ error: 'Erreur lors de la synchronisation' });
    }
});

// Delete vault
router.delete('/', async (req, res) => {
    try {
        await db.query('DELETE FROM vaults WHERE user_id = $1', [req.user.userId]);

        res.json({ message: 'Coffre supprimé avec succès' });
    } catch (error) {
        console.error('Delete vault error:', error);
        res.status(500).json({ error: 'Erreur lors de la suppression du coffre' });
    }
});

// Get sync history (last 10 syncs)
router.get('/history', async (req, res) => {
    try {
        const result = await db.query(
            'SELECT action, timestamp, ip_address FROM sync_logs WHERE user_id = $1 ORDER BY timestamp DESC LIMIT 10',
            [req.user.userId]
        );

        res.json({ history: result.rows });
    } catch (error) {
        console.error('Get history error:', error);
        res.status(500).json({ error: 'Erreur lors de la récupération de l\'historique' });
    }
});

module.exports = router;
