from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from database.db import get_db
from psycopg2.extensions import connection
from psycopg2.errors import UniqueViolation
import bcrypt


class User(BaseModel):
    username: str
    password: str


router = APIRouter()

@router.post("/login")
async def login(user: User, conn: connection = Depends(get_db)):
    """
    Login endpoint to authenticate user.
    """
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, password, username FROM users WHERE username = %s;", (user.username,))
        result = cursor.fetchone()

        if result is None:
            raise HTTPException(status_code=401, detail="No user found")

        user_id, db_password, username = result
        if not bcrypt.checkpw(user.password.encode("utf-8"), db_password.encode("utf-8")):
            raise HTTPException(status_code=401, detail="Incorrect password")

        return {"id": user_id, "username": username}


@router.post("/register")
async def register(user: User, conn: connection = Depends(get_db)):
    """
    Registration endpoint to create a new user.
    """
    print(f"user :{user}")
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s;", (user.username,))
        user_count = cursor.fetchone()[0]

        if user_count > 0:
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s);",
                (user.username, hashed_password)
            )
            conn.commit()
            return {"message": "User created successfully!"}
        except UniqueViolation:
            conn.rollback()
            raise HTTPException(status_code=400, detail="Username already exists")
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
