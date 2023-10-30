import sys
sys.path.append('/home/user/SaGol/MiniGPT-4')
import demo_torch
import pandas as pd
from pathlib import Path


#Generator 객체는 실행될 때 initialize 되어 chat을 상태로 저장하고, generate라는 메소드 하나를 가진다.
class Generator:
    def __init__(self, gpu_id):
        self.chat = demo_torch.initialize(gpu_id)
        self.data = None
        
#===============Text generation============#

    def generate(self, img, str, Id):
        self.data = None
        llm_text = demo_torch.text_generate(img, self.chat)
        self.data= pd.DataFrame({'Hash': [str], 'Description': [llm_text], 'Id': [Id]})
        return self.data
