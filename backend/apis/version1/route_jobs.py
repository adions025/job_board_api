from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from db.session import get_db
from db.models.jobs import Job
from typing import List
from schemas.jobs import JobCreate, ShowJob
from db.repository.jobs import create_new_job, retreive_job, list_jobs, update_job_by_id
from db.repository.jobs import delete_job_by_id
from db.models.users import User
from apis.version1.route_login import get_current_user_from_token

router = APIRouter()


@router.post("/create-job/", response_model=ShowJob)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    current_user = 1
    job = create_new_job(job=job, db=db, owner_id=current_user)
    return job


@router.get("/get/{id}", response_model=ShowJob)  # if we keep just "{id}" . it would stat catching all routes
def read_job(id: int, db: Session = Depends(get_db)):
    job = retreive_job(id=id, db=db)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with this id {id} does not exist")
    return job


@router.get("/all", response_model=List[ShowJob])  # new
def read_jobs(db: Session = Depends(get_db)):
    jobs = list_jobs(db=db)
    return jobs


@router.put("/update/{id}")
def update_job(id: int, job: JobCreate, db: Session = Depends(get_db)):
    current_user = 1
    message = update_job_by_id(id=id, job=job, db=db, owner_id=current_user)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Job with id {id} not found")
    return {"msg": "Successfully updated data."}


"""
@router.delete("/delete/{id}")
def delete_job(id: int, db: Session = Depends(get_db)):
    current_user_id = 1
    message = delete_job_by_id(id=id, db=db, owner_id=current_user_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Job with id {id} not found")
    return {"msg": "Successfully deleted."}
"""


@router.delete("/delete/{id}")
def delete_job(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    job = retreive_job(id=id, db=db)
    if not job:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with {id} does not exist")
    print(job.owner_id, current_user.id, current_user.is_superuser)
    if job.owner_id == current_user.id or current_user.is_superuser:
        delete_job_by_id(id=id, db=db, owner_id=current_user.id)
        return {"msg": "Successfully deleted."}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"You are not permitted!!!!")
