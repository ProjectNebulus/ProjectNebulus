// Set up trick or treat
var zipCode = ["Caroline"];
var city = ["Sally", "Peter", "John"];
var state = [];
var country = [];
var international = [];
var stateUnlocked = false;
var countryUnlocked = false;
var internUnlocked = false;

var leftBar = document.getElementsByTagName("center")[0];

for (name of zipCode) {
  var namep = document.createElement("p");
  namep.innerHTML = "🏠 " + name;
  leftBar.appendChild(namep);
}

var newArea = document.createElement("h4");
newArea.innerHTML = "Same city";
leftBar.appendChild(newArea);

for (name of city) {
  var namep = document.createElement("p");
  namep.innerHTML = "🏠 " + name;
  leftBar.appendChild(namep);
}

newArea = document.createElement("h4");
newArea.innerHTML = "Same Province/State";
leftBar.appendChild(newArea);

if (stateUnlocked) {
  for (name of state) {
    var namep = document.createElement("p");
    namep.innerHTML = "🏠 " + name;
    leftBar.appendChild(namep);
  }
} else {
  var message = document.createElement("p");
  message.innerHTML = "🔒 You must finish everyone in your city!";
  leftBar.appendChild(message);
}

newArea = document.createElement("h4");
newArea.innerHTML = "Same country";
leftBar.appendChild(newArea);

if (countryUnlocked) {
  for (name of country) {
    var namep = document.createElement("p");
    namep.innerHTML = "🏠 " + name;
    leftBar.appendChild(namep);
  }
} else {
  var message = document.createElement("p");
  message.innerHTML = "🔒 You must finish everyone of your province or state!";
  leftBar.appendChild(message);
}

newArea = document.createElement("h4");
newArea.innerHTML = "International";
leftBar.appendChild(newArea);

if (internUnlocked) {
  for (name of international) {
    var namep = document.createElement("p");
    namep.innerHTML = "🏠 " + name;
    leftBar.appendChild(namep);
  }
} else {
  var message = document.createElement("p");
  message.innerHTML = "🔒 You must finish everyone in your country!";
  leftBar.appendChild(message);
}

// Set up courses
var courseNames = ["Testing"];
var teachers = ["rhyley"];

var courses = document.getElementsByTagName("center")[1];

for (var i = 0; i < courseNames.length; i++) {
  var a = document.createElement("a");
  a.className = "dashboardCourse";

  var courseName = document.createElement("h2");
  courseName.innerHTML = courseNames[i];
  a.appendChild(courseName);

  var teacher = document.createElement("h3");
  teacher.innerHTML = teachers[i];
  a.appendChild(teacher);

  courses.appendChild(a);
}
