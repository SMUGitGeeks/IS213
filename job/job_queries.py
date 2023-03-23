from job_models import Job, JobSkill, db


# We need to have a resolver for each query and mutation we have defined in Job.graphql
def resolve_job(obj, info, job_id):
    try:
        job = Job.query.get(job_id)
        payload = {
            "success": True,
            "job": job.to_dict()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_jobs(obj, info):
    try:
        jobs = [job.to_dict() for job in Job.query.all()]
        payload = {
            "success": True,
            "jobs": jobs
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_create_job(obj, info, job_id, job_role, job_description, job_company):
    try:
        job = Job(
            job_id=job_id, job_role=job_role, job_description=job_description, job_company=job_company
        )
        db.session.add(job)
        db.session.commit()
        payload = {
            "success": True,
            "job": job.to_dict()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_update_job(obj, info, job_id, job_role, job_description, job_company):
    try:
        job = Job.query.get(job_id)
        if job:
            job.job_role = job_role
            job.job_description = job_description
            job.job_company = job_company
            db.session.commit()
            payload = {
                "success": True,
                "job": job.to_dict()
            }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_delete_job(obj, info, job_id):
    try:
        job_skills = JobSkill.query.filter_by(job_id = job_id)
        for job_skill in job_skills:
            db.session.delete(job_skill)
        job = Job.query.get(job_id)
        db.session.delete(job)
        db.session.commit()
        payload = {"success": True}

    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


# def resolve_job_skills(obj, info):
#     try:
#         job_skills = [job_skill.to_dict() for job_skill in JobSkill.query.all()]
#         payload = {
#             "success": True,
#             "job_skills": job_skills
#         }
#     except Exception as error:
#         payload = {
#             "success": False,
#             "errors": [str(error)]
#         }
#     return payload

##################

def resolve_job_skills(obj, info, job_id=None):
    try:
        job_skills = JobSkill.query.all()
        if job_id:
            job_skills = [job_skill.to_dict() for job_skill in JobSkill.query.filter_by(job_id = job_id).all]
        payload = {
            "success": True,
            "job_skills": job_skills
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

def resolve_job_skill(obj, info, job_id, skill_name):
    try:
        job_skill = JobSkill.query.get((job_id, skill_name))
        payload = {
            "success": True,
            "job_skill": job_skill
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

#########################################


def resolve_create_job_skill(obj, info, job_id, skill_name):
    try:
        job_skill = JobSkill(
            job_id=job_id, skill_name=skill_name
        )
        db.session.add(job_skill)
        db.session.commit()
        payload = {
            "success": True,
            "job_skill": job_skill.to_dict()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_update_job_skill(obj, info, job_id, skill_name):
    try:
        job_skill = JobSkill.query.get(job_id, skill_name)
        if job_skill:
            job_skill.job_skill = job_skill

            db.session.commit()
            payload = {
                "success": True,
                "job_skill": job_skill.to_dict()
            }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_delete_job_skill(obj, info, job_id, skill_name):
    try:
        job_skill = JobSkill.query.get(job_id, skill_name)
        db.session.delete(job_skill)
        db.session.commit()
        payload = {"success": True}

    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload
