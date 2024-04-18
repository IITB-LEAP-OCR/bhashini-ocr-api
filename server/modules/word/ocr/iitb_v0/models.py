from enum import Enum
from typing import List, Optional
from fastapi import UploadFile, File, Form
from pydantic import BaseModel, Field


class ModalityEnum(str, Enum):
	printed = 'printed'
	handwritten = 'handwritten'

class LanguageEnum(str, Enum):
	en = 'en'	# english
	hi = 'hi'	# hindi
	mr = 'mr'	# marathi
	ta = 'ta'	# tamil
	te = 'te'	# telugu
	kn = 'kn'	# kannada
	gu = 'gu'	# gujarati
	pa = 'pa'	# punjabi
	bn = 'bn'	# bengali
	ml = 'ml'	# malayalam
	asa = 'as'	# assamese
	ori = 'or'	# oriya
	mni = 'mni'	# manipuri
	ur = 'ur'	# urdu

class OCRRequest(BaseModel):
    image_content: List[UploadFile]
    modality: Optional[ModalityEnum] = Field(
        ModalityEnum.printed,
        description='Specify the modality of the word image.'
    )
    language: Optional[str] = Field(
        None,
        description='Specify the language of the word image as an ISO 639-1 code.'
    )
    script: Optional[str] = Field(
        None,
        description='Specify the script of the word image as an ISO 15924 code.'
    )

class OCRResponse(BaseModel):
    """
    Response format for OCR translation.
    """
    output: List[str]
    status: int