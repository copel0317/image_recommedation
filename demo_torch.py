import argparse
import os
import random

import numpy as np
import torch
import torch.backends.cudnn as cudnn
import gradio as gr

from minigpt4.common.config import Config
from minigpt4.common.dist_utils import get_rank
from minigpt4.common.registry import registry
from minigpt4.conversation.conversation import Chat, CONV_VISION

# imports modules for registration
from minigpt4.datasets.builders import *
from minigpt4.models import *
from minigpt4.processors import *
from minigpt4.runners import *
from minigpt4.tasks import *


def parse_args():
    parser = argparse.ArgumentParser(description="Demo")
    parser.add_argument("--cfg-path", required=True, help="path to configuration file.")
    parser.add_argument("--gpu-id", type=int, default=0, help="specify the gpu to load the model.")
    parser.add_argument(
        "--options",
        nargs="+",
        help="override some settings in the used config, the key-value pair "
        "in xxx=yyy format will be merged into config file (deprecate), "
        "change to --cfg-options instead.",
    )
    args = parser.parse_args()
    return args


def setup_seeds(config):
    seed = config.run_cfg.seed + get_rank()

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    cudnn.benchmark = False
    cudnn.deterministic = True


def initialize() :   
    print('Initializing Chat')
    args = parse_args()
    cfg = Config(args)

    model_config = cfg.model_cfg
    model_config.device_8bit = args.gpu_id
    model_cls = registry.get_model_class(model_config.arch)
    model = model_cls.from_config(model_config).to('cuda:{}'.format(args.gpu_id))

    vis_processor_cfg = cfg.datasets_cfg.cc_sbu_align.vis_processor.train
    vis_processor = registry.get_processor_class(vis_processor_cfg.name).from_config(vis_processor_cfg)
    chat = Chat(model, vis_processor, device='cuda:{}'.format(args.gpu_id))
    print('Initialization Finished')

def model_processing(img_path,prompt, num_beams, temperature):
    img_list = []
    chat_state = CONV_VISION.copy()
    llm_message = chat.upload_img(img_path, chat_state, img_list)
    chat.ask(prompt, chat_state)
    llm_message = chat.answer(conv=chat_state,
                         img_list=img_list,
                         num_beams=num_beams,
                         temperature=temperature,
                         max_new_tokens=300,
                         max_length=2000)[0]
    return llm_message    


def text_generate(img_path):
    with torch.no_grad() as demo:
        llm_message = model_processing(img_path,prompt,num_beams, temperature)
    return llm_message

# ========================================
#             #Variables
# ========================================
num_beams=1
temperature=1.0
prompt="Describe the image."
img_path="/home/user/SaGol/MiniGPT-4/Images/penguins.jpg"


# ========================================
#              Main function
# ========================================
initialize()
llm_message = text_generate(img_path)
print(llm_message)



