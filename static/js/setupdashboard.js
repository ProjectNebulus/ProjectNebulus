var courseNames = ["English 7", "History 7", "Biology 7", "Physics 7", "Latin II B", "Algebra & Geometry II", "Health 7"];

var teachers = ["Ms. Nagami", "Mr. Ross", "Ms. Gousia", "Ms. Adams", "Ms. Odell", "Mr. Rocha", "Mr. Floyd"]

var courses = document.getElementById("center");

for (var i = 0; i < courseNames.length; i++) {
  var div = document.createElement("DIV");
  div.className = "dashboardCourse";

  var courseName = document.createElement("H2");
  courseName.innerHTML = courseNames[i];
  div.appendChild(courseName);

  var teacher = document.createElement("H3");
  teacher.innerHTML = teachers[i];
  div.appendChild(teacher);

  courses.appendChild(div);
}