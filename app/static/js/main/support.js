const { isSupported } = require("dompurify");

async function sendform() {
    //ev.preventDefault();

    const useremail = document.getElementById('useremail').value;
    const usermsg = document.getElementById('usermessage').value;
    //const usercategory = document.getElementById('usercategory').value;
    const usertitle = document.getElementById('usertitle').value;
    //const userfile = get the file somehow

    console.log(useremail, usermsg, usertitle)

    const webhookmsg = {
        username: 'Nebulus Bugs',
        content: 'Incoming Support Ticker: ',
        avatar_url: 'https://nebulus.app/static/images/NebulusSpecialLogo.png',
        embeds: [{
            title: 'New Support Form:',
            fields: [
                {name: 'Email:', value: useremail},
                //{ name: 'Category: ', value: usercategory },
                {name: 'Title: ', value: usertitle},
                {name: 'Message: ', value: usermsg}
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