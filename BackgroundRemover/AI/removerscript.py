import os
import sys
import argparse
import numpy as np
from PIL import Image
import os.path
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms

from .src.models.modnet import MODNet
from remover.models import TheImages

def remove_background(image, matte):
    # obtain predicted foreground
    image = np.asarray(image)
    if len(image.shape) == 2:
        image = image[:, :, None]
    if image.shape[2] == 1:
        image = np.repeat(image, 3, axis=2)
    elif image.shape[2] == 4:
        image = image[: :, 0:3]
    matte = np.repeat(np.asarray(matte)[:, :, None], 3, axis=2) / 255
    foreground = image * matte + np.full(image.shape, 255) * (1 - matte)

    return Image.fromarray(np.uint8(foreground))


def image(image):
    ref_size = 512
    BASE_DIR = Path(__file__).resolve().parent.parent
    ckpt_path = os.path.join(BASE_DIR,'AI/pretrained/modnet_photographic_portrait_matting.ckpt')

    # define image to tensor transform
    im_transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ]
    )

    # create MODNet and load the pre-trained ckpt
    modnet = MODNet(backbone_pretrained=False)
    modnet = nn.DataParallel(modnet)
    if torch.cuda.is_available():
        modnet = modnet.cuda()
        weights = torch.load(ckpt_path)
    else:
        weights = torch.load(ckpt_path, map_location=torch.device('cpu'))
    modnet.load_state_dict(weights)
    modnet.eval()

    # read image
    im = Image.open(image)

    # unify image channels to 3
    im = np.asarray(im)
    if len(im.shape) == 2:
        im = im[:, :, None]
    if im.shape[2] == 1:
        im = np.repeat(im, 3, axis=2)
    elif im.shape[2] == 4:
        im = im[:, :, 0:3]

    # convert image to PyTorch tensor
    im = Image.fromarray(im)
    im = im_transform(im)

    # add mini-batch dim
    im = im[None, :, :, :]

    # resize image for input
    im_b, im_c, im_h, im_w = im.shape
    if max(im_h, im_w) < ref_size or min(im_h, im_w) > ref_size:
        if im_w >= im_h:
            im_rh = ref_size
            im_rw = int(im_w / im_h * ref_size)
        elif im_w < im_h:
            im_rw = ref_size
            im_rh = int(im_h / im_w * ref_size)
    else:
        im_rh = im_h
        im_rw = im_w

    im_rw = im_rw - im_rw % 32
    im_rh = im_rh - im_rh % 32
    im = F.interpolate(im, size=(im_rh, im_rw), mode='area')

    # inference
    _, _, matte = modnet(im.cuda() if torch.cuda.is_available() else im, True)

    # resize and save matte
    matte = F.interpolate(matte, size=(im_h, im_w), mode='area')
    matte = matte[0][0].data.cpu().numpy()
    matte_name = image.split('.')[0] + 'matte.png'
    foreground_name = image.split('.')[0] + 'foreground.png'
    matte = Image.fromarray(((matte * 255).astype('uint8')), mode='L')
    matte.save(os.path.join(image, matte_name))

    foreground = remove_background(Image.open(image), Image.open(os.path.join(image, matte_name)))
    matte_path = os.path.join(image, matte_name)
    os.remove(matte_path)
    foreground.save(os.path.join(image, foreground_name))
    return os.path.join(image, foreground_name)