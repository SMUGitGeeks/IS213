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


def resolve_create_student(obj, info, student_id, module_id):
    try:
        student = Student(
            student_id=student_id, module_id=module_id
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


def resolve_update_student(obj, info, student_id, module_id):
    try:
        student = Student.query.get(student_id)
        if student:
            student.module_id = module_id
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


def resolve_student_modules(obj, info, student_id):
    try:
        student_modules = StudentModule.query.all()
        if student_id:
            student_modules = StudentModule.query.filter_by(student_id = student_id)
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
        module_id = StudentModule(
            student_id=student_id, module_id=module_id
        )
        db.session.add(module_id)
        db.session.commit()
        payload = {
            "success": True,
            "module_id": module_id.to_dict()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_update_student_module(obj, info, student_id, module_id):
    try:
        module_id = StudentModule.query.get(student_id, module_id)
        if module_id:
            module_id.module_id = module_id

            db.session.commit()
            payload = {
                "success": True,
                "module_id": module_id.to_dict()
            }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_delete_student_module(obj, info, student_id, module_id):
    try:
        module_id = StudentModule.query.get(student_id, module_id)
        db.session.delete(module_id)
        db.session.commit()
        payload = {"success": True}

    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload
