# image_recommedation
이미지에 대한 설명 생성, 사진 추천 기능 제공

구동 코드가 들어있는 파일은 image_recommendation/dev_runmodel.py입니다. (정리하다 꼬여 일단 이렇게 구동했습니다.)

## Setup
구동 조건 : SaGol/MiniGPT-4 에서 해당 repo clone  
가상 환경 : minigpt4  
현재 포트 : 8890 ("http://172.16.162.72:8890/getAltTexts")   
dev_runmodel.py에서 수정 가능합니다.

## route / result
|  route |       | result |
|----|----|--------------|
| /getAltTexts         | 사진 여러 장에 대한 pair를 여러 개 반환합니다. |[{"Hash":"penguin","Description":"The image shows three penguins sitting on top of a large snowdrift. One of the penguins is holding its wings out and pointing its beak up towards the sky. The other two penguins are standing next to each other with their wings folded down. The sky in the background is a light blue with clouds.","Id":"SaGol"},{"Hash":"plant","Description":"The image shows a group of cacti in a greenhouse with a white background and a large glass window. The cacti are in various shapes and sizes and are arranged in rows on the ground. The greenhouse is well lit and has several plants on shelves. The plants are healthy and well cared for.","Id":"SaGol"}]|
| /getAltText         | 해당하는 사진의 설명이 포함된 pair를 반환합니다.   |[{'Hash': '21123dasdasd12e','Description': 'This image shows a baby penguin standing on the snowy ground. It has black and white feathers and is wearing a black and white coat. The penguin is standing in the middle of the snow, looking towards the left side of the image. The image has a clear blue sky in the background.','Id': 'Sagol'}]|
| /getBestPictures    | 검색어와 함께 사진의 pair들을 제공하면 그 중 해당하는 사진의 이름을 반환합니다.   |'hedgehog.jpg' |
| /config             | 사진의 사이즈를 줄이는 비율을 설정합니다. 기본값은 0.5로, 1000x1000 사이즈의 경우 500x500을 처리합니다. min_size는 사진의 최소 가로/세로크기를 지정합니다.  ex)10x10 | {'halve_rate': 0.5, 'min_size': 10} |
| /getAltText_time    | getAltText의 결과값과 소요 시간, 추론에 사용된 사진의 사이즈를 반환합니다.(테스트용) |


## /getAltTexts
Id(text), Hash(text), files(images) 를 입력받아, 이미지들에 대한 설명들을 return합니다. 

files(images)는
files['key'] = (image_name, image_data(binary)) 형태의 딕셔너리 형태로 구성되며, key, image_name은 모델을 돌리는 데는 영향을 주지 않으나, 구현 중 필요해서 넣은 부분이라 임의로 설정하셔도 됩니다.

요청에 대한 응답은 한 번에 반환되며, 현재 모델에는 한 번에 5개의 사진을 넘겨주고 있습니다. 
(너무 많이 넣을 경우 Warning: The number of tokens in current conversation exceeds the max length. The model will not see the contexts outside the range. 가 발생)

실험할 때 사용한 코드
```
# images_subset = ['hedgehog.jpg', 'plants.jpg', .... ] 형태의 파일 이름들

def send_request(url, images_subset):
    data = {
        'Id': 'SaGol',
        'Hash': [os.path.splitext(image)[0] for image in images_subset]
    }
    files = {}
    for i, image in enumerate(images_subset, start=1):
        with open(image, 'rb') as img_file:
            files[f'Image{i}'] = (image, img_file.read())

    response = requests.post(url, data=data, files=files)

    # 응답 데이터 처리
    json_data = response.content.decode('UTF-8')
    data = json.loads(json_data)
    
    return data
```

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
