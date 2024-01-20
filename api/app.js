const express = require('express');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const app = express();
const port = 3000;

app.get('/get-f1-data', (req, res) => {
    const { year, race, driver } = req.query;
    console.log(`Request received for year: ${year}, race: ${race}, driver: ${driver}`);

    const cacheFile = `../cache/${year}_${race}_${driver}.json`;

    // Check if cache exists
    if (fs.existsSync(path.join(__dirname, cacheFile))) {
        console.log('Cache found. Sending cached data...');
        res.sendFile(path.join(__dirname, cacheFile));
    } else {
        console.log('Cache not found. Running Python script...');
        // Construct the Python command
        const pythonCommand = `python ../scripts/data_visualization.py ${year} ${race} ${driver}`;

        exec(pythonCommand, (error, stdout, stderr) => {
            if (error) {
                console.error(`Exec error: ${error}`);
                return res.status(500).send(stderr);
            }
            console.log('Python script executed. Sending new data...');
            res.sendFile(path.join(__dirname, cacheFile));
        });
    }
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
