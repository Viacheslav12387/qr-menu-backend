from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import SessionLocal, engine, Base
import crud, models, schemas
from security import create_access_token, get_current_user
from security import get_current_user


Base.metadata.create_all(bind=engine)

app = FastAPI()  # ✅ DEFINIUJESZ app TU

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# endpointy muszą być poniżej app = FastAPI()
@app.get("/moje-konto")
def moje_konto(current_user: models.User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "rola": current_user.role
    }


Base.metadata.create_all(bind=engine)

app = FastAPI()

# zależność do bazy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/produkty/")
def dodaj_produkt(prod: schemas.ProductCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_product(db, prod)

@app.get("/produkty/")
def lista_produktow(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_products(db)

@app.delete("/produkty/{produkt_id}")
def usun_produkt(produkt_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    usuniety = crud.delete_product(db, produkt_id)
    if not usuniety:
        raise HTTPException(status_code=404, detail="Produkt nie znaleziony")
    return {"message": "Usunięto produkt"}

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    istnieje = db.query(models.User).filter(models.User.email == user.email).first()
    if istnieje:
        raise HTTPException(status_code=400, detail="Użytkownik już istnieje")
    return crud.create_user(db, user.email, user.password)

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    auth_user = crud.authenticate_user(db, user.email, user.password)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Nieprawidłowe dane logowania")

    token = create_access_token(
        data={"sub": auth_user.email},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": token, "token_type": "bearer"}
