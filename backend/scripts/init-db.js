const db = require('../config/database');
const fs = require('fs');
const path = require('path');

async function initializeDatabase() {
    try {
        console.log('🔧 Initializing database...');

        // Read schema SQL
        const schemaPath = path.join(__dirname, '../database/schema.sql');
        const schema = fs.readFileSync(schemaPath, 'utf8');

        // Execute schema
        await db.query(schema);

        console.log('✅ Database initialized successfully!');
        console.log('📊 Tables created: users, vaults, sync_logs');

        process.exit(0);
    } catch (error) {
        console.error('❌ Database initialization failed:', error);
        process.exit(1);
    }
}

initializeDatabase();
