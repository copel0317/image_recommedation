# image_recommedation
이미지에 대한 설명 생성, 사진 추천 기능 제공

구동 코드가 들어있는 파일은 image_recommendation/runmodel.py입니다. (정리하다 꼬여 일단 이렇게 구동했습니다.)

## Setup
구동 조건 : SaGol/MiniGPT-4 에서 해당 repo clone  
가상 환경 : minigpt4
현재 포트 : 8890 ("http://172.16.162.72:8890/getAltText") / runmodel.py에서 수정 가능합니다.

## route / result
|  route |       | result |
|----|----|--------------|
| /getAltText         | 해당하는 사진의 설명이 포함된 pair를 반환합니다.   |[{'Hash': '21123dasdasd12e','Description': 'This image shows a baby penguin standing on the snowy ground. It has black and white feathers and is wearing a black and white coat. The penguin is standing in the middle of the snow, looking towards the left side of the image. The image has a clear blue sky in the background.','Id': 'Sagol'}]|
| /getBestPictures    | 검색어와 함께 사진의 pair들을 제공하면 그 중 해당하는 사진의 이름을 반환합니다.   |'hedgehog.jpg' |
| /config             | 사진의 사이즈를 줄이는 비율을 설정합니다. 기본값은 0.5로, 1000x1000 사이즈의 경우 500x500을 처리합니다. min_size는 사진의 최소 가로/세로크기를 지정합니다.  ex)10x10 | {'halve_rate': 0.5, 'min_size': 10} |
| /getAltText_time    | getAltText의 결과값과 소요 시간, 추론에 사용된 사진의 사이즈를 반환합니다.(테스트용) |


## /getAltText
Id(text), Hash(text), Image(image) 를 입력받아, image의 설명을 return합니다.  
실험할 때 사용한 코드
```
def makeDescription (Img, Hash, Id) :
    url = "http://172.16.162.72:8890/getAltText"
    with open(Img, 'rb') as img_file:
        data = {'Id' : Id, 'Hash': Hash}
        files = {'Image': img_file}
        res = requests.post(url, data=data, files=files)
        result = json.loads(res.content)
        return result

#=====================================================             #사진의 기본 프롬프트는 Describe the image.
Img = "C:/Users/Administrator/Desktop/apple.jpg"
Hash = "21123dasdasd12e"
Id = "Sagol"
#=====================================================
makeDescription(Img, Hash, Id)
```



## /getBestPictures
userText(Text), data(pairs)를 입력받아 data에서 userText에 맞는 사진의 이름을 반환합니다.  
실험할 때 사용한 코드
```
def makeDescription_directory (img_path, Id) :
    combined_data = []
    for file in Path(img_path).iterdir():
        if file.is_file():
            Hash = file.name
            combined_data.extend(makeDescription (file, Hash, Id))
        else :
            pass
    return combined_data

def recommendImages (userText, pairs) :
    url = "http://172.16.162.72:8890/getBestPictures"
    data = {'userText' : userText, 'data': json.dumps(pairs)} 
    result = requests.post(url, data = data)
    return result.content.decode("UTF-8")[1:-1]

img_path = "C:/Users/Administrator/Desktop/Images"
Id = "Hcail"
result = makeDescription_directory(img_path, Id)

#사진 추천
userText = " 고슴도치 사진을 찾아 줘."
pairs = result
recommended = recommendImages (userText, pairs)
```

## /config
halve(float), min_size(int)를 입력받습니다.
```
def config(halve, min_size) :
    url = "http://172.16.162.72:8890/config"
    data = {'halve' : halve, 'min_size': min_size}
    res = requests.post(url, data=data)
    result = json.loads(res.content)
    return result
config(0.1, 100)
```

TODO 
1. 병렬처리가 현재 되지 않고 있습니다.  
2. 현재 Generator는 tools의 generator.py에 구현되어 있으며, runmodel.py에서는 0번 그래픽카드를 사용하도록 되어 있습니다.  
3. 현재 프롬프트가 "Describe the image"로 설정되어있습니다. 한 번씩 이상한 답변을 할 때가 있는데 이 부분을 수정해야 할 것 같습니다.
