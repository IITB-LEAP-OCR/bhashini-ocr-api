from pydantic import BaseModel

class OCRResponse(BaseModel):
    result_message: str
    result_html: str