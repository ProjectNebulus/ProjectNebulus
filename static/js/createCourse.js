// set up templates
var divs = document.getElementsByClassName("scroll");
var screens = document.getElementsByClassName("CourseBtn");

// set up button
var modal = document.getElementById("CourseModal");
var btn = document.getElementById("create");


btn.onclick = function() {
  modal.style.display = "block";

  for (var screen of screens)
    screen.style.display = "none";
  screens[0].style.display = "block";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

//set up close button
for (var close of document.getElementsByClassName("close")) {
  close.className += " material-icons";
  close.innerHTML = "close";
  close.onclick = function() { modal.style.display = "none"; }
}

/*

To create a new template, add a new dictionary and put the parameters:

name (e.g. Science)
icon (e.g. science.svg)
description (e.g. Physics, Chemistry, Biology)

as demonstrated below.

*/
var templates = [
  {
    name: "Science",
    icon: "science.svg",
    subtemplates: ['Science', 'Physics', 'Chemistry', 'Biology', 'Astronomy', 'Life Science', 'Earth Science', 'Physical Science', 'Physical Geography', 'Computer Science', 'Programming', 'Coding']
  },

  {
    name: "Mathematics",
    icon: "math.svg",
    subtemplates: ['K-8th Math', 'Pre-Algebra', 'Algebra I', 'Algebra II', 'Pre-Calculus A/B/AB', 'Calculus AB/BC', 'AP Statistics', 'AP Calculus', 'Competitive Math']
  },

  {
    name: "History",
    icon: "history.svg",
    subtemplates: ['Social Studies', 'World History I/II', 'US History', 'AP World History', 'AP US History']
  },

  {
    name: "Art",
    icon: "art.svg",
    subtemplates: ['Visual Arts', 'Music', 'Drama']
  },

  {
    name: "Language",
    icon: "language.svg",
    subtemplates: ['English', 'Latin', 'Spanish', 'French', 'Mandarin', 'German']
  },

  {
    name: "Sports",
    icon: "sport.svg",
    subtemplates: ['PE', 'Basketball', 'Soccer', 'Ice Hockey', 'Volleyball', 'Track and Field', 'Football', 'Tennis', 'Dance']
  }
]

for (var template of templates) {
  const t = template;

  var button = document.createElement("span");
  button.className = "button";
  button.onclick = function() { step2(t) }
  
  var imageSpan = document.createElement("span");
  imageSpan.style.float = "left";

  var image = document.createElement("img");
  image.style.float = "right";
  image.height = 20;
  image.width = 20;
  image.src = "static/images/icons/" + template.icon;
  imageSpan.appendChild(image);

  button.appendChild(imageSpan);

  var templateName = document.createElement("span");
  templateName.innerHTML = template.name;
  button.appendChild(templateName);
  
  var next = document.createElement("span");
  next = document.createElement("img");
  next.style.float = "right";
  next.height = 20;
  next.width = 20;
  next.src = "static/images/icons/next.svg";
  button.appendChild(next);

  button.appendChild(document.createElement("br"));

  var description = document.createElement("span");
  description.style.color = "gray";
  description.style.fontSize = "0.8em";
  description.innerHTML = "(";

  for (var subtemplate of template.subtemplates)
    description.innerHTML += subtemplate + ", ";
  description.innerHTML += "etc.)"

  button.appendChild(description);

  divs[0].appendChild(button);
}


function step2(template) {
  screens[0].style.display = "none";
  screens[1].style.display = "block";

  divs[1].innerHTML = "";

  for (var subtemplate of template.subtemplates) {  
    var button = document.createElement("span");
    button.className = "button";
    
    var imageSpan = document.createElement("span");
    imageSpan.style.float = "left";

    var image = document.createElement("img");
    image.style.float = "right";
    image.height = 20;
    image.width = 20;
    image.src = "static/images/icons/" + template.icon;
    imageSpan.appendChild(image);

    button.appendChild(imageSpan);

    var templateName = document.createElement("span");
    templateName.innerHTML = subtemplate;
    button.appendChild(templateName);
    
    var next = document.createElement("span");
    next = document.createElement("img");
    next.style.float = "right";
    next.height = 20;
    next.width = 20;
    next.src = "static/images/icons/next.svg";
    button.appendChild(next);

    divs[1].appendChild(button);
  }

  document.getElementsByTagName("h1")[2].innerHTML.replace("[replace this]", template.name)
}

function step3(template) {
  screens[0].style.display = "none";
  screens[1].style.display = "block";

  divs[1].innerHTML = "";

  for (var subtemplate of template.subtemplates) {  
    var button = document.createElement("span");
    button.className = "button";
    
    var imageSpan = document.createElement("span");
    imageSpan.style.float = "left";

    var image = document.createElement("img");
    image.style.float = "right";
    image.height = 20;
    image.width = 20;
    image.src = "static/images/icons/" + template.icon;
    imageSpan.appendChild(image);

    button.appendChild(imageSpan);

    var templateName = document.createElement("span");
    templateName.innerHTML = subtemplate;
    button.appendChild(templateName);
    
    var next = document.createElement("span");
    next = document.createElement("img");
    next.style.float = "right";
    next.height = 20;
    next.width = 20;
    next.src = "static/images/icons/next.svg";
    button.appendChild(next);

    divs[1].appendChild(button);
  }

  document.getElementsByTagName("h1")[2].innerHTML.replace("[replace this]", template.name)
}