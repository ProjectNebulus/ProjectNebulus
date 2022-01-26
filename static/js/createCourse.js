// set up button
var modal = document.getElementById("CourseModal");
var btn = document.getElementById("CourseBtn");

btn.onclick = function() {
  modal.style.display = "block";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

//set up close button
document.getElementById("close").onclick = function() {
  modal.style.display = "none";
}

// set up templates
var divs = document.getElementsByClassName("scroll");

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
    description: "(Science, Physics, Chemistry, Biology, Astronomy, Life Science, Earth Science, Physical Science, Physical Geography, Computer Science (Coding) etc.)"
  },

  {
    name: "Mathematics",
    icon: "math.svg",
    description: "(K-8th Math, Pre-Algebra, Algebra I, Algebra II, Pre-Calculus A/B/AB, Calculus AB/BC, AP Statistics, AP Calculus, Competitive Math etc.)"
  },

  {
    name: "History",
    icon: "history.svg",
    description: "(Social Studies, World History I/II, US History, AP World History, AP US History, etc.)"
  },

  {
    name: "Art",
    icon: "art.svg",
    description: "(Visual Arts, Music, Drama, etc.)"
  },

  {
    name: "Language",
    icon: "language.svg",
    description: "(English, Latin, Spanish, French, Mandarin, German, etc.)"
  },

  {
    name: "Sports",
    icon: "sport.svg",
    description: "(PE, Basketball, Soccer, Ice Hockey, Volleyball, Track and Field, Football, Tennis, Dance, etc.)"
  }
]

for (var template of templates) {
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
  description.innerHTML = template.description;

  button.appendChild(description);

  divs[0].appendChild(button);
}

function step2(courseName) {

}