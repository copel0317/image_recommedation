import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import demo_torch

import pandas as pd
from pathlib import Path

#===================Test용 Dataframe==============================
img_0 = ["hash1", "The image shows a cactus plant standing in the middle of a frozen lake. The cactus is surrounded by large ice crystals that have formed on the surface of the water. In the background, there is a range of mountains with snow-capped peaks. The sky is clear and blue, with a few fluffy clouds floating in the distance. The overall mood of the image is peaceful and serene, with the cactus standing tall and proud in the center of the frozen lake."]
img_1 = ["hash2", "The logo design is simple and minimalistic, with a pink line drawing of a flamingo standing on one leg in the water. The design is clean and easy to recognize, making it suitable for use in various contexts such as a logo for a beach resort or a flamingo-themed event. The use of a flamingo as a symbol adds a touch of whimsy and fun to the design, making it memorable and eye-catching. Overall, it's a well-designed logo that effectively communicates the brand's message."]
imgs = [img_0,img_1]
Imgs = pd.DataFrame(imgs, columns=['Hash', 'Description'])
#=================================================================


#===============Model Initialize==========#
chat = demo_torch.initialize()

#===============Text generation==========#
def new_text(img_path,Imgs):
    llm_text = demo_torch.text_generate(img_path, chat)
    Hash=img_path.rsplit( ".", 1 )[0].rsplit("/",5)[5]

    #Hash와 사진을 Dataframe에 추가
    Imgs=pd.concat([Imgs, pd.DataFrame({'Hash': [Hash], 'Description': [llm_text]})])
    return Imgs

def generate(Imgs, photopath):
    for file in Path(photopath).iterdir():
        Imgs = new_text(str(file),Imgs)
        print(Imgs)
    return Imgs


photopath="/home/user/SaGol/MiniGPT-4/Images"
generate(Imgs,photopath)
    