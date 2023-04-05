from course_models import Course, CourseSkill, db


# We need to have a resolver for each query and mutation we have defined in course.graphql

########################################## Course ##########################################
# get 1 specific course based on course_id
def resolve_course(obj, info, course_id):
    try:
        course = Course.query.get(course_id)
        payload = {
            "success": True,
            "course": course.to_dict()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


# get all courses
def resolve_courses(obj, info, skill_name=None):
    try:
        if skill_name:
            # get courses from Course table based on skill_name from CourseSkill table
            courses = [course.to_dict() for course in
                       Course.query.join(CourseSkill).filter(CourseSkill.skill_name == skill_name).all()]
            payload = {
                "success": True,
                "courses": courses
            }
        else:
            courses = [course.to_dict() for course in Course.query.all()]
            payload = {
                "success": True,
                "courses": courses
            }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


# create a course
def resolve_create_course(obj, info, course_id, course_name, course_link):
    try:
        course = Course(
            course_id=course_id, course_name=course_name, course_link=course_link
        )
        db.session.add(course)
        db.session.commit()
        payload = {
            "success": True,
            "course": course.to_dict()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


# update a course
def resolve_update_course(obj, info, course_id, course_name=None, course_link=None):
    try:
        course = Course.query.get(course_id)
        if course_name:
            course.course_name = course_name
        if course_link:
            course.course_link = course_link
        db.session.commit()
        payload = {
            "success": True,
            "course": course.to_dict()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


# delete a course
def resolve_delete_course(obj, info, course_id):
    try:
        course = Course.query.get(course_id)
        courseskills = CourseSkill.query.filter_by(course_id=course_id).all()
        for courseskill in courseskills:
            db.session.delete(courseskill)
        db.session.delete(course)
        db.session.commit()
        payload = {"success": True}

    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


########################################## CourseSkill ##########################################

# get all course skills
def resolve_course_skills(obj, info, course_id=None):
    try:
        # get all course skills based on courseid
        if course_id:
            course_skills = [course_skill.to_dict() for course_skill in
                             CourseSkill.query.filter_by(course_id=course_id).all()]
            payload = {
                "success": True,
                "course_skills": course_skills
            }
        else:
            course_skills = [course_skill.to_dict() for course_skill in CourseSkill.query.all()]
            payload = {
                "success": True,
                "course_skills": course_skills
            }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


# create a course skill
def resolve_create_course_skill(obj, info, course_id, skill_name):
    try:
        course_skill = CourseSkill(
            course_id=course_id, skill_name=skill_name
        )
        db.session.add(course_skill)
        db.session.commit()
        payload = {
            "success": True,
            "course_skill": course_skill.to_dict()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


# update a course skill
def resolve_update_course_skill(obj, info, course_id, new_skill, old_skill):
    # payload = {"success": False, "errors": [str(error)]}
    try:
        course_skill = CourseSkill.query.get((course_id, old_skill))
        course_skill.skill_name = new_skill
        db.session.commit()
        payload = {
            "success": True,
            "course_skill": course_skill.to_dict()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


# delete a course skill
def resolve_delete_course_skill(obj, info, course_id, skill_name):
    try:
        course_skill = CourseSkill.query.get((course_id, skill_name))
        db.session.delete(course_skill)
        db.session.commit()
        payload = {"success": True}

    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload
