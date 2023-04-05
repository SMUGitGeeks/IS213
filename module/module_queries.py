from module_models import Module, ModuleSkill, db


# We need to have a resolver for each query and mutation we have defined in module.graphql

# get 1 specific module
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


# get all modules (get modules base on skills)
def resolve_modules(obj, info, skill_name=None):
    try:
        if skill_name:
            # get modules from Module table based on skill_name from ModuleSkill table
            modules = [module.to_dict() for module in
                       Module.query.join(ModuleSkill).filter(ModuleSkill.skill_name == skill_name).all()]
            payload = {
                "success": True,
                "modules": modules
            }
        else:
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


# create a module
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


# update a module
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


# delete a module
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


# get all module skills (get skills base on modules)
def resolve_module_skills(obj, info, module_id=None):
    try:
        if module_id:
            module_skills = [module_skill.to_dict() for module_skill in
                             ModuleSkill.query.filter_by(module_id=module_id).all()]
            payload = {
                "success": True,
                "module_skills": module_skills
            }
        else:
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


# create a module skill for a module
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


# update a module skill for a module
def resolve_update_module_skill(obj, info, module_id, old_skill, new_skill):
    try:
        # update old skill to new skill
        module_skill = ModuleSkill.query.filter_by(module_id=module_id, skill_name=old_skill).first()
        if module_skill and new_skill:
            module_skill.skill_name = new_skill

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


# delete a module skill for a module
def resolve_delete_module_skill(obj, info, module_id, skill_name):
    try:
        module_skill = ModuleSkill.query.filter_by(module_id=module_id, skill_name=skill_name).first()
        db.session.delete(module_skill)
        db.session.commit()
        payload = {"success": True}

    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload
