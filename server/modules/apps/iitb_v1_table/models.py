from pydantic import BaseModel

class TSRResponse(BaseModel):
    result_message: str
    result_html: str