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


def resolve_create_job(obj, info, job_id, job_name):
    try:
        job = Job(
            job_id=job_id, job_name=job_name
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


def resolve_update_job(obj, info, job_id, job_name):
    try:
        job = Job.query.get(job_id)
        if job:
            job.job_name = job_name
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


def resolve_job_skills(obj, info):
    try:
        job_skills = [job_skill.to_dict() for job_skill in JobSkill.query.all()]
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


def resolve_delete_job_skill(obj, info, job_id, job_skill):
    try:
        job_skill = JobSkill.query.get(job_id, job_skill)
        db.session.delete(job_skill)
        db.session.commit()
        payload = {"success": True}

    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload
