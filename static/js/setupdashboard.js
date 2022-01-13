// Set up trick or treat
let zipCode = ['Caroline'];
let city = ['Sally', 'Peter', 'John'],
    state = [],
    country = [],
    international = [],
    stateUnlocked = false,
    countryUnlocked = false,
    internUnlocked = false;

let leftBar = document.getElementsByTagName('center')[0];

// TODO(kev): refactor duplicate code

for (name of zipCode) {
    let namep = document.createElement('p');
    namep.innerHTML = '🏠 ' + name;
    leftBar.appendChild(namep);
}

let newArea = document.createElement('h4');
newArea.innerHTML = 'Same city';
leftBar.appendChild(newArea);

for (name of city) {
    let namep = document.createElement('p');
    namep.innerHTML = '🏠 ' + name;
    leftBar.appendChild(namep);
}

newArea = document.createElement('h4');
newArea.innerHTML = 'Same Province/State';
leftBar.appendChild(newArea);

if (stateUnlocked) {
    for (name of state) {
        let namep = document.createElement('p');
        namep.innerHTML = '🏠 ' + name;
        leftBar.appendChild(namep);
    }
} else {
    let message = document.createElement('p');
    message.innerHTML = '🔒 You must finish everyone in your city!';
    leftBar.appendChild(message);
}

newArea = document.createElement('h4');
newArea.innerHTML = 'Same country';
leftBar.appendChild(newArea);

if (countryUnlocked) {
    for (name of country) {
        let namep = document.createElement('p');
        namep.innerHTML = '🏠 ' + name;
        leftBar.appendChild(namep);
    }
} else {
    let message = document.createElement('p');
    message.innerHTML = '🔒 You must finish everyone of your province or state!';
    leftBar.appendChild(message);
}

newArea = document.createElement('h4');
newArea.innerHTML = 'International';
leftBar.appendChild(newArea);

if (internUnlocked) {
    for (name of international) {
        let namep = document.createElement('p');
        namep.innerHTML = '🏠 ' + name;
        leftBar.appendChild(namep);
    }
} else {
    let message = document.createElement('p');
    message.innerHTML = '🔒 You must finish everyone in your country!';
    leftBar.appendChild(message);
}
