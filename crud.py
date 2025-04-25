from sqlalchemy.orm import Session
from models import Libro
from schemas import LibroCreate

def obtener_libros(db: Session):
    return db.query(Libro).all()

def obtener_libro(db: Session, libro_id: int):
    return db.query(Libro).filter(Libro.id == libro_id).first()

def crear_libro(db: Session, libro: LibroCreate):
    nuevo_libro = Libro(**libro.dict())
    db.add(nuevo_libro)
    db.commit()
    db.refresh(nuevo_libro)
    return nuevo_libro

def actualizar_libro(db: Session, libro_id: int, libro_data: LibroCreate):
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if libro:
        for campo, valor in libro_data.dict().items():
            setattr(libro, campo, valor)
        db.commit()
        db.refresh(libro)
    return libro

def eliminar_libro(db: Session, libro_id: int):
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if libro:
        db.delete(libro)
        db.commit()
    return libro
