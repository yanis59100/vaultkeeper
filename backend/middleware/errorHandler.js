const errorHandler = (err, req, res, next) => {
    console.error('Error:', err);

    // CORS errors
    if (err.message === 'Not allowed by CORS') {
        return res.status(403).json({ error: 'Origine non autorisée' });
    }

    // JWT errors
    if (err.name === 'JsonWebTokenError') {
        return res.status(401).json({ error: 'Token invalide' });
    }

    if (err.name === 'TokenExpiredError') {
        return res.status(401).json({ error: 'Token expiré' });
    }

    // Database errors
    if (err.code === '23505') { // Unique violation
        return res.status(409).json({ error: 'Cette ressource existe déjà' });
    }

    if (err.code === '23503') { // Foreign key violation
        return res.status(400).json({ error: 'Référence invalide' });
    }

    // Default error
    res.status(err.status || 500).json({
        error: err.message || 'Erreur interne du serveur'
    });
};

module.exports = { errorHandler };
