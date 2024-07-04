import os
import json
import argparse
import torch

from doctr.io import DocumentFile
from doctr.models.recognition.predictor import RecognitionPredictor
from doctr.models.preprocessor import PreProcessor


from config import *



device = torch.device("cuda:"+str(CUDA_DEVICE) if torch.cuda.is_available() else "cpu")

# Load the model

def initialize_model(args):
    
    language = args.language
    model = args.model
    modality = args.modality
    vocab_type = args.vocab_type
    
    rec_model = torch.load(os.path.join(MODEL_PATH, f'{vocab_type}_{modality}_{model}_{LANG_MAP[language]}.pt'), map_location=device)
    rec_model.to(device)
    rec_model.eval() 

    reco_predictor = RecognitionPredictor(PreProcessor((32, 128), preserve_aspect_ratio=True, batch_size=BATCH_SIZE, mean=(0.694, 0.695, 0.693), std=(0.299, 0.296, 0.301)), rec_model)
    return reco_predictor


# BASE FUNCTION TO PERFORM DOCTR PREDICTIONS
def predict(args):
    img_files=os.listdir(IMG_DIR)
    # print('data ls :',img_files)
    model=initialize_model(args)
    results = {}
    for img in img_files:
        if img[-4:]!='json' and img[-3:]!='txt':
            doc = DocumentFile.from_images(os.path.join(IMG_DIR,img))
            result = model(doc)
            results[img] = result[0][0]

    results = {k: results[k] for k in sorted(results.keys(), key=lambda x: (int(x.split('.')[0]), x))}
    return results

def main(args):
    print(args)
    try:
        output = predict(args)
        
        print(output)
        print('--------------------------------------------DONE-------------------------------------------')
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            
        with open(os.path.join(OUTPUT_DIR,"out.json"),"w") as f:
            json.dump(output,f, indent=4, ensure_ascii=False)
            
    except Exception as e:
        print(e)


def parse_args():
    parser = argparse.ArgumentParser(description="Text Recognition for Indian Languages", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-l", "--language", type=str, default="hi", help="language for OCR in coded: as|bn|gu|hi|kn|ml|mni|mr|or|pa|ta|te|ur")
    parser.add_argument("-t", "--modality", type=str, default="printed", help="Type of Modality: handwritten|printed")
    parser.add_argument("-m", "--model", type=str, default="crnn_vgg16_bn", help="type of model : crnn_vgg16_bn|master|parseq")
    parser.add_argument("-v", "--vocab_type", type=str, default="all", help="type of Vocab (all|akshara|handwritten)")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    main(args)