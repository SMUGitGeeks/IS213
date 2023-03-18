from module_models import Module, ModuleSkill, db


# We need to have a resolver for each query and mutation we have defined in module.graphql
def resolve_module(obj, info, module_id):
    try:
        module = Module.query.get(module_id)
        payload = {
            "success": True,
            "module": module.to_dict()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_modules(obj, info):
    try:
        modules = [module.to_dict() for module in Module.query.all()]
        payload = {
            "success": True,
            "modules": modules
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_create_module(obj, info, module_id, module_name):
    try:
        module = Module(
            module_id=module_id, module_name=module_name
        )
        db.session.add(module)
        db.session.commit()
        payload = {
            "success": True,
            "module": module.to_dict()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_update_module(obj, info, module_id, module_name):
    try:
        module = Module.query.get(module_id)
        if module:
            module.module_name = module_name
            db.session.commit()
            payload = {
                "success": True,
                "module": module.to_dict()
            }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_delete_module(obj, info, module_id):
    try:
        module = Module.query.get(module_id)
        db.session.delete(module)
        db.session.commit()
        payload = {"success": True}

    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_module_skills(obj, info):
    try:
        module_skills = [module_skill.to_dict() for module_skill in ModuleSkill.query.all()]
        payload = {
            "success": True,
            "module_skills": module_skills
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_create_module_skill(obj, info, module_id, skill_name):
    try:
        module_skill = ModuleSkill(
            module_id=module_id, skill_name=skill_name
        )
        db.session.add(module_skill)
        db.session.commit()
        payload = {
            "success": True,
            "module_skill": module_skill.to_dict()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_update_module_skill(obj, info, module_id, skill_name):
    try:
        module_skill = ModuleSkill.query.get(module_id, skill_name)
        if module_skill:
            module_skill.module_skill = module_skill

            db.session.commit()
            payload = {
                "success": True,
                "module_skill": module_skill.to_dict()
            }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_delete_module_skill(obj, info, module_id, module_skill):
    try:
        module_skill = ModuleSkill.query.get(module_id, module_skill)
        db.session.delete(module_skill)
        db.session.commit()
        payload = {"success": True}

    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload
