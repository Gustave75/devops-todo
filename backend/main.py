from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator

import models, schemas
from database import engine, get_db

# Crée les tables au démarrage
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API")

# CORS : autorise le frontend React à appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expose les métriques Prometheus sur /metrics
Instrumentator().instrument(app).expose(app)


@app.get("/tasks", response_model=list[schemas.TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()


@app.post("/tasks", response_model=schemas.TaskOut, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(title=task.title)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.patch("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, data: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    if data.title is not None:
        task.title = data.title
    if data.done is not None:
        task.done = data.done
    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    db.delete(task)
    db.commit()