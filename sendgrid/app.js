const sgMail = require('@sendgrid/mail');

// This is your real test secret API key.
const API_KEY = "";

sgMail.setApiKey(API_KEY);

const message = {
    to: 'glenlow12374@gmail.com',
    // to: ['reciever1@gmail.com', 'reciever2@gmail.com'],
    from: {
        name: 'BOSS Finder',
        email: 'glen.low.2021@scis.smu.edu.sg',
    },
    subject: 'New Jobs This Month!',
    text: 'Here is the list of new jobs this month!',
    html: '<h1>Job List below</h1>',
};

sgMail
    .send(message)
    .then(response => console.log('Email sent successfully'))
    .catch(error => console.log(error.message));


// Run 2 commands first
// npm install @sendgrid/mail
// node app.js