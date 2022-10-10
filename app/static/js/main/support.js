const {isSupported} = require("dompurify");

if (window.isPopup)
    document.getElementById("navbar").style.display = "hidden";

async function sendForm() {
    const email = document.getElementById('useremail').value;
    const msg = document.getElementById('usermessage').value;
    //const userCategory = document.getElementById('userCategory').value;
    const title = document.getElementById('usertitle').value;
    //const file = get the file somehow

    console.log(email, msg, title)

    const webhookmsg = {
        username: 'Nebulus Bugs',
        content: 'Incoming Support Ticket: ' + title,
        avatar_url: "https://nebulus.app/static/images/NebulusSpecialLogo.png",
        embeds: [{
            title: 'New Support Form:',
            fields: [
                {email: 'Email:', value: email},
                //{ category: 'Category: ', value: userCategory },
                {title: 'Title: ', value: title},
                {message: 'Message: ', value: msg}
            ]
        }],
    };

    const webhookurl = 'https://discord.com/api/webhooks/1019052484423069738/Fk9oxCPKQsde0i2kuwRWjJV7UoIpjqaNi1hl3Y2ATOkAUTkf0bygksS2h_GUKiWwfCT3';

    const response = await fetch(webhookurl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(webhookmsg),
    });

    console.log(response)

    if (response.ok) {
        alert('Message sent! We should reply back in about 2 hours.');
        console.log('Worked')
    } else {
        alert('There was an error sending your form. Please try again later.');
        console.log('failed')
    }
}