const express = require('express');
const { exec } = require('child_process');
const cors = require('cors');
const db = require('./firebaseAdminConfig'); 

const app = express();
const port = 3000;

app.use(cors());


app.get('/get-f1-data', (req, res) => {
    const { year, race, driver } = req.query;

    const ref = db.ref(`f1data/${year}_${race}_${driver}`);
    ref.once('value', (snapshot) => {
        if (snapshot.exists()) {
            console.log('Data found in Firebase. Sending data...');
            res.json(snapshot.val());
        } else {
            console.log('Data not found in Firebase. Running Python script...');
            const pythonCommand = `python ../scripts/data_visualization.py ${year} ${race} ${driver}`;
            exec(pythonCommand, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Exec error: ${error}`);
                    return res.status(500).send(stderr);
                }
                console.log('Python script executed. Fetching new data from Firebase...');
                ref.once('value', (newSnapshot) => {
                    if (newSnapshot.exists()) {
                        res.json(newSnapshot.val());
                    } else {
                        res.status(500).send('Error fetching new data');
                    }
                });
            });
        }
    }, (error) => {
        console.error('Firebase read error:', error);
        res.status(500).send('Error fetching data from Firebase');
    });
});

app.get('/get-f1-session', (req, res) => {
    const { year, race } = req.query;

    const ref = db.ref(`f1data/${year}_${race}`);
    ref.once('value', (snapshot) => {

        if (snapshot.exists()) {
            console.log('Data found in Firebase. Sending data...');
            res.json(snapshot.val());
        } else {
            console.log('Data not found in Firebase. Running Python script to get sesion...');
            const getSessionCommand = `python ../scripts/session_results.py ${year} ${race}`;
            exec(getSessionCommand, (error, stdout, stderr) => {
                if(error) {
                    console.error(`Exec error: ${error}`);
                    return res.status(500).send(stderr);
                }
                console.log('Python script executed. Fetching new data from Firebase to get sessions...');
                ref.once('value', (newSnapshot) => {
                    if (newSnapshot.exists()) {
                        res.json(newSnapshot.val());
                    } else {
                        res.status(500).send('Error fetching new data');
                    }
                });
            })
        }

    }, (error) => {
        console.error('Firebase read error:', error);
        res.status(500).send('Error fetching data from Firebase');
    })

});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
