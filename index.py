from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import address,staff,dependent,directory,training,institution,qualification,user,staff_training

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(staff_training.router, prefix="/stafftraining", tags=["stafftraining"])
app.include_router(address.router, prefix="/address", tags=["address"])
app.include_router(dependent.router, prefix="/dependent", tags=["dependent"])
app.include_router(staff.router, prefix="/staff", tags=["staff"])
app.include_router(directory.router, prefix="/directory", tags=["directory"])
app.include_router(training.router, prefix="/training", tags=["training"])
app.include_router(institution.router, prefix="/institution", tags=["institution"])
app.include_router(qualification.router, prefix="/qualification", tags=["qualification"])