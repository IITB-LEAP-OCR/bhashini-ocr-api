from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .modules.page import router as page_level_router
from .modules.word import router as word_level_router

app = FastAPI(
	title='Bhashini OCR API',
	description='',
    root_path="/api/0.0.1"
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=['*'],
	allow_methods=['*'],
	allow_headers=['*'],
	allow_credentials=True,
)

app.include_router(page_level_router)
app.include_router(word_level_router)