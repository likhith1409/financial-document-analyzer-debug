from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import os
import uuid
import asyncio
from contextlib import asynccontextmanager
from datetime import timedelta, datetime
from typing import List

from crew import CustomCrew
from agents import financial_analyst, investment_advisor, risk_assessor
from task import analyze_financial_document, investment_analysis, risk_assessment
from database import db
from auth import (
    User,
    UserInDB,
    get_current_active_user,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    pwd_context,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create a test user on application startup if it doesn't exist."""
    if not db.db["users"].find_one({"username": "testuser"}):
        hashed_password = pwd_context.hash("testpassword")
        db.db["users"].insert_one({
            "username": "testuser",
            "hashed_password": hashed_password,
            "email": "test@example.com",
            "full_name": "Test User",
            "disabled": False
        })
        print("---")
        print("Default user 'testuser' with password 'testpassword' created.")
        print("---")
    yield

app = FastAPI(title="Financial Document Analyzer", lifespan=lifespan)

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory to serve files
app.mount("/static", StaticFiles(directory="static"), name="static")

async def run_crew(query: str, file_path: str):
    """Runs the financial analysis crew asynchronously."""
    financial_crew = CustomCrew(
        agents=[financial_analyst, investment_advisor, risk_assessor],
        tasks=[analyze_financial_document, investment_analysis, risk_assessment],
    )
    
    input_payload = {'query': query, 'file_path': file_path}
    result = await financial_crew.kickoff(input_payload)
    
    return result

@app.get("/", response_class=FileResponse)
async def root():
    """Serve the main HTML page"""
    return FileResponse('static/index.html')

@app.post("/register", response_model=User)
async def register_user(user: UserInDB):
    # In a real app, you'd want to handle potential duplicate usernames
    hashed_password = pwd_context.hash(user.hashed_password)
    user_in_db = user.dict()
    user_in_db["hashed_password"] = hashed_password
    db.db["users"].insert_one(user_in_db)
    return user


@app.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.db["users"].find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/analyze")
async def analyze_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights"),
    current_user: User = Depends(get_current_active_user),
):
    """Analyze financial document and provide comprehensive investment recommendations"""
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate query
        if not query:
            query = "Analyze this financial document for investment insights"
            
        # Process the financial document with all analysts
        response = await run_crew(query=query.strip(), file_path=file_path)
        
        # Default values for analysis parts
        financial_analysis_result = "No financial analysis available."
        investment_advising_result = "No investment advising available."
        risk_assessment_result = "No risk assessment available."

        # Find the correct results from the response dictionary
        for task_desc, result in response.items():
            if "Analyze the financial document" in task_desc:
                financial_analysis_result = result
            elif "develop a strategic investment plan" in task_desc:
                investment_advising_result = result
            elif "Conduct a thorough risk assessment" in task_desc:
                risk_assessment_result = result
        
        analysis_payload = {
            "financial_analysis": financial_analysis_result,
            "investment_advising": investment_advising_result,
            "risk_assessment": risk_assessment_result,
        }

        # Store the result in the database, associated with the user
        db.collection.insert_one({
            "username": current_user.username,
            "query": query,
            "file_path": file_path,
            "analysis": analysis_payload,
            "created_at": datetime.utcnow(),
        })

        return {
            "status": "success",
            "query": query,
            "analysis": analysis_payload,
            "file_processed": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    
    finally:
        # The file is intentionally not deleted to be available for history
        pass

@app.get("/history", response_model=List[dict])
async def get_user_history(current_user: User = Depends(get_current_active_user)):
    """Fetch analysis history for the current user."""
    history = db.get_results_by_username(current_user.username)
    
    # Manually convert ObjectId to string for each item in the history
    for item in history:
        item["_id"] = str(item["_id"])
        
    return JSONResponse(content=jsonable_encoder(history))

if __name__ == "__main__":
    import uvicorn
    print("---")
    print("FastAPI app running on http://localhost:9000")
    print("---")
    uvicorn.run(app, host="0.0.0.0", port=9000)
