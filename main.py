"""
OCR API

Author: Krishna Tulsyan (kt.krishna.tulsyan@gmail.com)
"""

import uvicorn

PORT = 8058

if __name__ == '__main__':
	uvicorn.run('server.app:app', host='0.0.0.0', port=PORT, reload=True)