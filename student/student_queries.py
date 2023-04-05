from student_models import Student, StudentModule, db


# We need to have a resolver for each query and mutation we have defined in module.graphql
def resolve_student(obj, info, student_id):
    try:
        student = Student.query.get(student_id)
        payload = {
            "success": True,
            "student": student.to_dict()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_students(obj, info):
    try:
        students = [student.to_dict() for student in Student.query.all()]
        payload = {
            "success": True,
            "students": students
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_create_student(obj, info, student_id, student_name, email, is_graduated, is_subscribed):
    try:
        student = Student(
            student_id=student_id,
            student_name=student_name,
            email=email,
            is_graduated=is_graduated,
            is_subscribed=is_subscribed
        )
        db.session.add(student)
        db.session.commit()
        payload = {
            "success": True,
            "student": student.to_dict()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_update_student(obj, info, student_id, student_name=None, email=None, is_graduated=None, is_subscribed=None):
    try:
        student = Student.query.get(student_id)
        if student:
            if student_name:
                student.student_name = student_name

            if email:
                student.email = email

            if (is_graduated != None):
                student.is_graduated = is_graduated

            if (is_subscribed != None):
                student.is_subscribed = is_subscribed

            db.session.commit()
            payload = {
                "success": True,
                "student": student.to_dict()
            }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_delete_student(obj, info, student_id):
    try:
        student = Student.query.get(student_id)
        db.session.delete(student)
        db.session.commit()
        payload = {"success": True}

    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_student_modules(obj, info, student_id=None):
    try:
        student_modules = StudentModule.query.all()
        if student_id:
            student_modules = StudentModule.query.filter_by(student_id=student_id)
            if student_modules:
                payload = {
                    "success": True,
                    "student_modules": student_modules
                }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_student_module(obj, info, student_id, module_id):
    try:
        student_module = StudentModule.query.get((student_id, module_id))
        print(student_module)
        if student_module:
            payload = {
                "success": True,
                "student_module": student_module
            }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_create_student_module(obj, info, student_id, module_id):
    try:
        student_module = StudentModule(
            student_id=student_id, module_id=module_id
        )
        db.session.add(student_module)
        db.session.commit()
        payload = {
            "success": True,
            "student_module": student_module.to_dict()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_update_student_module(obj, info, student_id, old_module_id, new_module_id):
    try:
        student_module = StudentModule.query.get((student_id, old_module_id))
        if student_module:
            student_module.module_id = new_module_id

            db.session.commit()
            payload = {
                "success": True,
                "student_module": student_module.to_dict()
            }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_delete_student_module(obj, info, student_id, module_id):
    try:
        module_id = StudentModule.query.get((student_id, module_id))
        db.session.delete(module_id)
        db.session.commit()
        payload = {"success": True}

    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload
