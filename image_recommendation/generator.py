import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import demo_torch

import pandas as pd
from pathlib import Path


#Generator 객체는 실행될 때 initialize 되어 chat을 상태로 저장하고, generate라는 메소드 하나를 가진다.
class Generator:
    def __init__(self):
        self.chat = demo_torch.initialize()
        self.data = None
        
#===============Text generation============#

    def generate(self, img, str, Id):
        self.data = None
        llm_text = demo_torch.text_generate(img, self.chat)
        self.data= pd.DataFrame({'Hash': [str], 'Description': [llm_text], 'Id': [Id]})
        return self.data
    
AltTextGenerator = Generator()