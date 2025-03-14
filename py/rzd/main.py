import datetime
from fastapi import FastAPI, Depends, Response, status, HTTPException
from . import schemas
from . import models
from rzd.database import engine, SessionLocal
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close

@app.post('/user/create')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
        new_user = models.Users(u_name = request.name)
        db.add(new_user)
        db.commit()
        return HTTPException(status_code=status.HTTP_200_OK)

@app.put('/user/rename')
def update_user(request: schemas.User, db: Session = Depends(get_db)):
    user = db.get(models.Users, request.id)
    user.u_name = request.name
    db.commit()
    return user

@app.get('/users')
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users

@app.get('/user/{name}')
def get_user_by_name(name: str, db: Session = Depends(get_db)):
      users = db.query(models.Users).where(models.Users.u_name == name).all()
      return users if len(users) != 0 else HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.get('/user/{id}')
def get_user_by_id(id: int, db: Session = Depends(get_db)):
      user = db.query(models.Users).filter(models.Users.user_id == id).first()
      return user

#Я хз, как нормально добавить данные из промежуточной таблицы.
@app.get('/user/{id}/sessions/')
def get_user_sessios(id: int, response: Response ,db: Session = Depends(get_db)):
        query = (
              select(models.Users)
              .options(joinedload(models.Users.work_hours).load_only(models.User_Work_sessions.work_hour))
              .options(selectinload(models.Users.user_wd))
              .where(models.Users.user_id == id)
        )
        res = db.execute(query)
        result = res.unique().scalar()
        return result

@app.post('/create_session/{date}/{id}/{hours}')
def create_session_by_uid(date: datetime.datetime, id: int, hours: int, db: Session = Depends(get_db)):
    work_day = db.query(models.Work_day).where(models.Work_day.day == date).first()
    if not work_day:
        db.add(models.Work_day(day = date))
        db.commit()
        work_day = db.query(models.Work_day).where(models.Work_day.day == date).first()
    user = db.query(models.Users).where(models.Users.user_id == id).first()
    #Добавить искл. для тёзок
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    uws = models.User_Work_sessions(date_id = work_day.wd_id, user_id = id, work_hour = hours)
    db.add(uws)
    db.commit()
    return uws

#это не работает(почти)
@app.get('/users/sessions/{month_start}/{month_end}')
def get_user_sessios_between(start: datetime.datetime, end: datetime.datetime ,db: Session = Depends(get_db)):
        query = (
              select(models.Work_day)
              .options(joinedload(models.Work_day.ses))
              .options(selectinload(models.Work_day.user_work_day))
              .filter(models.Work_day.day >= start, models.Work_day.day <= end)
        )
        res = db.execute(query)
        result = res.unique().scalar()
        return result
            