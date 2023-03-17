from ariadne import convert_kwargs_to_snake_case
from module_models import Module, ModuleSkill


def resolve_module(obj, info):
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


def resolve_module_skill(obj, info):
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
