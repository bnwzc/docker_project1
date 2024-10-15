const express = require('express');
const mysql = require('mysql2');
const { MongoClient } = require('mongodb');

const app = express();
const PORT = 5002;




const mysqlConnection = mysql.createConnection({
    host: "mysql_db",
    user: "root",
    password: "root",
    database: "project"
});

function getHealthData() {
    return new Promise((resolve, reject) => {
        const query = "SELECT height, weight FROM height_weight";
        mysqlConnection.query(query, (err, results) => {
            if (err) return reject(err);
            resolve(results);
        });
    });
}


function calculateStatistics(data) {
    if (data.length === 0) {
        return { max_height: 0, max_weight: 0, avg_height: 0, avg_weight: 0 };
    }

    const heights = data.map(row => row.height);
    const weights = data.map(row => row.weight);

    return {
        max_height: Math.max(...heights),
        max_weight: Math.max(...weights),
        avg_height: heights.reduce((a, b) => a + b, 0) / heights.length,
        avg_weight: weights.reduce((a, b) => a + b, 0) / weights.length
    };
}


async function writeToMongoDB(statistics) {
    const client = new MongoClient('mongodb://root:root@mongo_db:27017/');
    try {
        await client.connect();
        const db = client.db('project');
        const collection = db.collection('health_weight');

        const query = { _id: 'statistics' };
        const update = { _id: 'statistics', ...statistics };

        await collection.replaceOne(query, update, { upsert: true });
    } finally {
        await client.close();
    }
}


app.post('/analytics', async (req, res) => {
    try {
        const healthData = await getHealthData();
        const statistics = calculateStatistics(healthData);
        await writeToMongoDB(statistics);
        res.send("Data processed and written to MongoDB!");
    } catch (error) {
        console.error(error);
        res.status(500).send("Error processing data.");
    }
});


app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});




