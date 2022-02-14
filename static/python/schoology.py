import schoolopy, json

def getcourse(courseid, sc, user):
  # print("Getting Course")
  course = {}
  #Main

  section = dict(sc.get_section(courseid))
  #print(section)
  course["id"] = section["id"]
  course["name"] = section["course_title"]
  course["image"] = section["profile_url"]
  #Updates
  #updates = sc.get_updates(section_id = courseid)
  scupdates = sc.get_section_updates(courseid)
  updates = []
  for update in scupdates:
    updates.append({
      "body": update["body"],
      "id": update["id"],
      "likes": update["likes"],
      "liked": update["user_like_action"],
      "comments": update["num_comments"]
    })
  course["updates"] = updates

  # print("Updates:\n")

  # for update in updates:
  #   for key in update:
  #     print(key + ":", update[key])
  #   print()

  #Documents
  scdocuments= sc.get_section_documents(courseid)
  documents = []
  for scdocument in scdocuments:
    document = {}
    document["id"] = scdocument["id"]
    document["name"] = scdocument["title"]
    document["attachment"] = scdocument["attachments"]
    documents.append(document)
  course["documents"] = documents
  

  #Grades
  scgrades= sc.get_user_grades_by_section(user, courseid)
  print(scgrades)

  #Events
  scevents = sc.get_section_events(courseid)
  print(scevents)
  #Members

  #Unavailable

  #Assignments
  scassignments = sc.get_assignments(courseid)
  assignments = []
  for assignment in scassignments:
    assignments.append({
      "id": assignment["id"],
      "name": assignment["title"],
      "info": assignment["description"],
      "url": assignment["web_url"],
      "completed": assignment["completed"],
      "due": assignment["due"]
    })
  
    # print("\nAssignments:")

    # for assignment in assignments:
    #   for key in assignment:
    #     print(key + ":", assignment[key])
    #   print()

  course["assignments"] = assignments

  #Final
  with open("schoology.json", "w") as out:
    json.dump(course, out, indent=4)
  