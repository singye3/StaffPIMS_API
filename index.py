from fastapi import FastAPI
from routes import address,staff,dependent,directory,training,institution,qualification

app = FastAPI()


app.include_router(address.router, prefix="/address", tags=["address"])
app.include_router(dependent.router, prefix="/dependent", tags=["dependent"])
app.include_router(staff.router, prefix="/staff", tags=["staff"])
app.include_router(directory.router, prefix="/directory", tags=["directory"])
app.include_router(training.router, prefix="/training", tags=["training"])
app.include_router(institution.router, prefix="/institution", tags=["institution"])
app.include_router(qualification.router, prefix="/qualification", tags=["qualification"])