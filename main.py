import uvicorn

from server.modules.config import PORT

if __name__ == '__main__':
	uvicorn.run('server.app:app', host='0.0.0.0', port=PORT, reload=True)