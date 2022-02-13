import schoolopy, json
def getcourse(courseid, sc):
  print("Getting Course")
  course = {}
  #Main

  section = sc.get_section(courseid)
  #print(section)
  section = dict(section)
  course["id"] = section["id"]
  course["name"] = section["course_title"]
  course["image"] = section["profile_url"]
  #Updates
  #updates = sc.get_updates(section_id = courseid)
  scupdates = sc.get_section_updates(courseid)
  updates = []
  for i in scupdates:
    theupdate = {}
    theupdate["body"] = i["body"]
    theupdate["id"] = i["id"]
    theupdate["likes"] = i["likes"]
    theupdate["liked"] = i["user_like_action"]
    theupdate["comments"] = i["num_comments"]
    updates.append(theupdate)
  course["updates"] = updates
  print(updates)
  #Documents

  #Grades

  #Events

  #Members

  #Assignments
  scassignments = sc.get_assignments(courseid)
  assignments = []
  for scassignment in scassignments:
    assignment = {}
    assignment["id"] = scassignment["id"]
    assignment["name"] = scassignment["title"]
    assignment["info"] = scassignment["description"]
    assignment["url"] = scassignment["web_url"]
    assignment["completed"] = scassignment["completed"]
    assignment["due"] = scassignment["due"]
    assignments.append(assignment)
  
  print(assignments)
  course["assignments"] = assignments

  #Final
  with open("schoology.json", "w") as out:
    json.dump(course, out, indent=4)
  