from datetime import datetime

from dateutil.tz import gettz
from fastapi import Depends, FastAPI, Form, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .modules.word.ocr.routes import router as iitb_v2_router
from .modules.page.textron.routes import router as text_detection_routes
from .modules.page import router as page_level_router
from .modules.word import router as word_level_router

app = FastAPI(
	title='BHASHINI OCR API',
	docs_url='/api/0.0.1/docs',
	openapi_url='/api/0.0.1/openapi.json'
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
app.include_router(text_detection_routes)
app.include_router(iitb_v2_router)

@app.middleware('http')
async def log_request_timestamp(request: Request, call_next):
	local_tz = gettz('Asia/Kolkata')
	print(f'Received request at: {datetime.now(tz=local_tz).isoformat()}')
	return await call_next(request)

@app.get('/ocr/ping', tags=['Testing'])
def test_server_online():
	return 'pong'