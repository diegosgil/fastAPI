from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <- Nuevo import
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

# Crear las tablas en la BD
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency para obtener sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index():
    return {"mensaje": "Hola, Pythonianos!"}

@app.post("/libros", response_model=schemas.LibroOut)
def crear_libro(libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    return crud.crear_libro(db, libro)

@app.get("/libros", response_model=list[schemas.LibroOut])
def listar_libros(db: Session = Depends(get_db)):
    return crud.obtener_libros(db)

@app.get("/libros/{id}", response_model=schemas.LibroOut)
def obtener_libro(id: int, db: Session = Depends(get_db)):
    libro = crud.obtener_libro(db, id)
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@app.put("/libros/{id}", response_model=schemas.LibroOut)
def actualizar_libro(id: int, libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    libro_actualizado = crud.actualizar_libro(db, id, libro)
    if libro_actualizado is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro_actualizado

@app.delete("/libros/{id}")
def eliminar_libro(id: int, db: Session = Depends(get_db)):
    libro_eliminado = crud.eliminar_libro(db, id)
    if libro_eliminado is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return {"mensaje": f"Libro con ID {id} eliminado"}
