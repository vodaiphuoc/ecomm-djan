from huggingface_hub import hf_hub_download
from underthesea import word_tokenize, text_normalize
import emoji
import fasttext
import re
import os

class PreProcessing(object):

    _replacements = {
        "laems": "lắm",
        "k dk": "không được",
        "ko": "không",
        "ko tl": "không trả lời",
        "hok": "không",
        "hàg": "hàng",
        "kp": "không phải",
        "khong xl": "không xin lỗi",
        "khong": "không",
        "k": "không",
        "thik": "thích",
        "xog": "xong",
        "e bé": "em bé",
        "tks": "cảm ơn",
        "thanks": "cảm ơn",
        "sp": "sản phẩm",
        "sx": "sản xuất",
        "meosddc": "méo được",
        "cg": "cũng",
        "cgiac": "cảm giác",
        "siu": "siêu",
        "dt": "điện thoại",
        "đc": "được",
        "trc": "trước",
        "lhe": "liên hệ",
        "nt": "nhắn tin",
        "ntn": "như thế nào",
        "thấy ntn": "thấy như thế này",
        "k bt ntn": "không biết như thế nào",
        "shopkhá": "cửa hàng khá",
        "phẩmkémvề ": "phẩm kém về ",
        "tl": "trả lời",
        "lắmmàu": "lắm màu",
        "êmda": "êm da",
        "thj": "thì"
    }

    
    _remove_str = ["♡ ♡ ♡","❤","\=\)\)\)", "\=\)\)", "\=\)","\:\)\)\)", "\:\)\)", "\:\)"]

    def _get_replacements_pattern(self):
        replacements = {}

        for k,v in PreProcessing._replacements.items():
            if k != "k bt ntn":
                replacements[f" {k} "] = f" {v} " 
            else:
                replacements[f"{k} "] = f"{v} " 


        return re.compile("|".join(replacements.keys())), replacements, re.compile("|".join(PreProcessing._remove_str))
        
    def __init__(self):
        self._replacements_pattern, self.replacements, self._remove_pattern = self._get_replacements_pattern()


    def forward(self, text:str):
        # 1. lower all string
        text = text.lower()

        # 2. normalize
        text = text_normalize(text)

        # 3. remove emojies
        text = emoji.replace_emoji(text, replace='')

        # 4. remove words
        text = self._remove_pattern.sub('', text)

        # 5. replace words
        text = self._replacements_pattern.sub(lambda match: self.replacements[match.group()], text)

        # 6. remove any ',' left after cleaning words
        text = re.sub(r"\,\s",'',text)

        # 7. tokenize via underthesea
        text = word_tokenize(text, format="text")

        return text


class ModelServing(object):
    def __init__(self):
        try:
            _model_path = hf_hub_download(
                repo_id=os.environ['HF_REPO'], 
                filename="fasttext_sentiment.bin"
            )
            
            self._pre_processing = PreProcessing()
            self._model = fasttext.load_model(_model_path)
        except Exception as e:
            print(e)

    def forward(self, text:str | list[str])->bool | list[bool]:
        output_single = False
        if isinstance(text, str):
            text = [text]
            output_single = True
        processed_text = [self._pre_processing.forward(_text) for _text in text]
        labels, probs = self._model.predict(processed_text)
        
        outputs = [int(ele[0][-1]) == 1  for ele in labels]
        return outputs[0] if output_single else outputs