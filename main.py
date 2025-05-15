import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src_poc1.app import todo_app
from src_poc1.database import (
    Base as BasePOC1, 
    engine as engine_poc1
)
from src_poc2.app import auth_app
from src_poc2.configurations.database import (
    Base as BasePOC2,
    engine as engine_poc2
)
from src_poc2.middleware import register_middlewares


app = FastAPI(
    title="Combined FastAPI Application",
    version="1.0.0",
    description="""
This project includes two separate services:

- Visit `/poc1/docs` for the Todo API Docs
- Visit `/poc2/docs` for the Auth API Docs
"""
)


register_middlewares(app)

app.mount("/poc1", todo_app)
app.mount("/poc2", auth_app)


templates = Jinja2Templates(directory="doc_templates")

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def custom_docs(request: Request):
    return templates.TemplateResponse("custom_docs.html", {"request": request})


@app.on_event("startup")    
def on_startup() -> None:
    BasePOC1.metadata.create_all(bind=engine_poc1)
    BasePOC2.metadata.create_all(bind=engine_poc2)


def main():
    uvicorn.run(app, port=8000)

if __name__ == "__main__":
    main()