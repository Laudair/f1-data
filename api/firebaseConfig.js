import firebase from 'firebase/app';
import 'firebase/database';

const firebaseConfig = {
    apiKey: "AIzaSyCXVMYCPmpB5SsNf1CLAhnp65rBRbHau3w",
    authDomain: "f1-data-6fee2.firebaseapp.com",
    databaseURL: "https://f1-data-6fee2-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "f1-data-6fee2",
    storageBucket: "f1-data-6fee2.appspot.com",
    messagingSenderId: "415011868876",
    appId: "1:415011868876:web:534755544d821ef90db269",
    measurementId: "G-VMYB2XSHKF"
}

firebase.initializeApp(firebaseConfig);

const database = firebase.database();

export default database;
