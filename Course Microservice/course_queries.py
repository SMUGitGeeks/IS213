from course_models import Course, CourseSkill, db


# We need to have a resolver for each query and mutation we have defined in course.graphql
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


def resolve_courses(obj, info):
    try:
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


def resolve_update_course(obj, info, course_id, course_name, course_link):
    try:
        course = Course.query.get(course_id)
        if course:
            course.course_name = course_name
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


def resolve_delete_course(obj, info, course_id):
    try:
        course = Course.query.get(course_id)
        db.session.delete(course)
        db.session.commit()
        payload = {"success": True}

    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_course_skills(obj, info):
    try:
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


def resolve_course_skills_by_id(obj, info, course_id):
    try:
        # course_skills = CourseSkill.query.filter_by(course_id=course_id)
        # course_skills = [course_skill.to_dict() for course_skill in CourseSkill.query.all()]
        course_skills = [course_skill.to_dict() for course_skill in CourseSkill.query.filter_by(course_id=course_id).all()]
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


def resolve_update_course_skill(obj, info, course_id, skill_name):
    try:
        course_skill = CourseSkill.query.get(course_id, skill_name)
        if course_skill:
            course_skill.course_skill = course_skill

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


def resolve_delete_course_skill(obj, info, course_id, course_skill):
    try:
        course_skill = CourseSkill.query.get(course_id, course_skill)
        db.session.delete(course_skill)
        db.session.commit()
        payload = {"success": True}

    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload
