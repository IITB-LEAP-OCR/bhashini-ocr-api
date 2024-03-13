from pydantic import BaseModel, Field
from typing import Optional

class SIResponse(BaseModel):
	text: Optional[str] = Field(description="This field contains the identified language/script for the image.\
							 This can take one of the 11 values.\
							 devanagari,\
							 bengali,\
							 gujarati,\
							 gurumukhi,\
							 kannada,\
							 malayalam,\
							 odia,\
							 tamil,\
							 urdu,\
							 latin,\
							 odia\
							 ")

class ClassifyResponse(BaseModel):
	text: str