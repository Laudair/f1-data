const admin = require('firebase-admin');
const serviceAccount = require('path/to/your/firebase-adminsdk.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://f1-data-6fee2-default-rtdb.asia-southeast1.firebasedatabase.app'
});

const db = admin.database();

module.exports = db;
