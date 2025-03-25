import express from 'express';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import fs from 'fs';

const app = express();
const port = 3000;

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

app.get('/', async (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.get('/logs', async (req, res) => {
    const files = fs.readdirSync(`${__dirname}/logs`);
    res.json(files);
});

app.get('/logs/:filename', async (req, res) => {
    const filename = req.params.filename;
    const data = fs.readFileSync(`${__dirname}/logs/${filename}`, 'utf8');
    res.json(data);
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});