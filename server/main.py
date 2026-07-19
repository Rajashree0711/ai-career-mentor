from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import engine, get_db
from models import User
from schemas import UserCreate, UserResponse, UserLogin, Token
from security import hash_password, verify_password, create_access_token, get_current_user
from fastapi import UploadFile, File
import cloudinary.uploader
from models import Resume
from schemas import ResumeResponse
import cloudinary_config

app = FastAPI(title="AI Career Mentor API")

@app.get("/")
def read_root():
    return {"message": "AI Career Mentor API is running"}

@app.get("/db-check")
def db_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"database": "connected successfully"}
    except Exception as e:
        return {"database": "connection failed", "error": str(e)}

@app.post("/auth/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/auth/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
@app.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/resume/upload", response_model=ResumeResponse)
def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    upload_result = cloudinary.uploader.upload(
    file.file,
    resource_type="raw",
    folder="resumes",
    use_filename=True,
    unique_filename=True,
    format="pdf"
)

    new_resume = Resume(
        user_id=current_user.id,
        file_url=upload_result["secure_url"],
        file_name=file.filename
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    return new_resume