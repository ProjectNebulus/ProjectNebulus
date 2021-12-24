var courseNames = ["English 7", "History 7", "Biology 7", "Physics 7", "Latin II B", "Algebra & Geometry II", "Health 7"];

var teachers = ["Ms. Nagami", "Mr. Ross", "Ms. Gousia", "Ms. Adams", "Ms. Odell", "Mr. Rocha", "Mr. Floyd"]

var courses = document.getElementById("center");

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