IMG_DIR = '/raid/ganesh/badri/RA/docker-basic-ocr/data/' 
MODEL_PATH = '/raid/ganesh/badri/RA/docker-basic-ocr/models/'
OUTPUT_DIR = '/raid/ganesh/badri/RA/docker-basic-ocr/data3/'
CUDA_DEVICE = '7'
BATCH_SIZE = 32


# LANGUAGES SUPPORTED BY ULCA
LANGUAGES = ['as', 'bn', 'brx', 'doi', 'en', 'grt', 'gu', 'hi', 'kha', 'kn', 'kok', 'ks', 'lus', 'mai', 'ml', 'mni', 'mr', 'ne', 'njz', 'or', 'pa', 'pnr', 'sa', 'sat', 'sd', 'si', 'ta', 'te', 'ur']
# LANGUAGES = ['as', 'bn', 'gu', 'hi', 'kn', 'ml', 'mni', 'mr', 'or', 'pa', 'ta', 'te', 'ur']

LANG_MAP={}
LANG_MAP['as']  = 'assamese'
LANG_MAP['bn']  = 'bengali'
LANG_MAP['gu']  = 'gujarati'
LANG_MAP['hi']  = 'hindi'
LANG_MAP['kn']  = 'kannada'
LANG_MAP['ml']  = 'malayalam'
LANG_MAP['mni'] = 'manipuri'
LANG_MAP['mr']  = 'marathi'
LANG_MAP['or']  = 'odia'
LANG_MAP['pa']  = 'punjabi'
LANG_MAP['ta']  = 'tamil'
LANG_MAP['te']  = 'telugu'
LANG_MAP['ur']  = 'urdu'


LANG_MAP['en']  = 'english'
LANG_MAP['brx'] = 'bodo'
LANG_MAP['doi'] = 'dogri'
LANG_MAP['grt'] = 'garo'
LANG_MAP['kha'] = 'khasi'
LANG_MAP['kok'] = 'konkani'
LANG_MAP['ks']  = 'kashmiri'
LANG_MAP['lus'] = 'lushei'
LANG_MAP['mai'] = 'maithili'
LANG_MAP['ne']  = 'nepali'
LANG_MAP['njz'] = 'nyishi'
LANG_MAP['pnr'] = 'panar'
LANG_MAP['sa']  = 'sanskrit'
LANG_MAP['sat'] = 'santali'
LANG_MAP['sd']  = 'sindhi'
LANG_MAP['si']  = 'sinhala'