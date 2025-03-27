import express from 'express';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import fs from 'fs';

const app = express();
const port = 3000;

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

app.use(express.json());

if (!fs.existsSync(`${__dirname}/logs`)) fs.mkdirSync(`${__dirname}/logs`);

const processesFile = `${__dirname}/processes.json`;

app.get('/', async (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.get('/logs', async (req, res) => {
    const files = fs.readdirSync(`${__dirname}/logs`);
    res.json(files);
});

app.get('/logs/:filename', async (req, res) => {
    const filename = req.params.filename;
    let data;

    try {
        const raw = fs.readFileSync(`${__dirname}/logs/${filename}`, 'utf8');
        data = JSON.parse(raw);
    } catch (err) {
        console.error(err);
        return res.status(500).json({ message: err.message });
    }

    res.json(data.filtered || {});
});

app.get('/processes', async (req, res) => {
    try {
        if (!fs.existsSync(processesFile)) return res.json([]);

        const data = fs.readFileSync(processesFile, 'utf8');
        const processes = JSON.parse(data);
        res.json(processes);
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: err.message });
    }
});

app.post('/processes', async (req, res) => {
    const { processName } = req.body;
    if (!processName) return res.status(400).json({ message: 'Process name is required' });

    try {
        let processes = [];
        if (fs.existsSync(processesFile)) {
            const data = fs.readFileSync(processesFile, 'utf8');
            processes = JSON.parse(data);
        }

        processes.push(processName);
        fs.writeFileSync(processesFile, JSON.stringify(processes, null, 2));

        res.json(processes);
    }
    catch (err) {
        console.error(err);
        res.status(500).json({ message: err.message });
    }
});

app.delete('/processes', async (req, res) => {
    const { processName } = req.body;
    if (!processName) return res.status(400).json({ message: 'Process name is required' });

    try {
        if (!fs.existsSync(processesFile)) return res.json([]);

        const data = fs.readFileSync(processesFile, 'utf8');
        let processes = JSON.parse(data);
        processes = processes.filter(p => p !== processName);
        fs.writeFileSync(processesFile, JSON.stringify(processes, null, 2));

        res.json(processes);
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: err.message });
    }
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});