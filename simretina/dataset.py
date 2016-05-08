"""Utility functions and pre-load examples.

Author: Yuhuang Hu
Email : yuhuang.hu@uzh.ch
"""

import os
from os.path import join
import numpy as np
import cv2
import av

from simretina import package_data_path


def get_image(image_path, color=True, size=True):
    """Get image by given image path.

    Parameters
    ----------
    image_path : string
        target image absolute path
    color : bool
        if color is True then return a color frame with BGR encoding.
        if color is False then return a grey scale frame.
    size : bool
        if size is True then return the size of the frame.
        if size is False then just return the frame.

    Returns
    -------
    frame : numpy.ndarray
        a frame that contains target image.
    size : tuple
        size of the frame (optional).
    """
    frame = cv2.imread(image_path)

    if color is False:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if size is True:
        return frame, frame.shape
    else:
        return frame


def get_video(vid_path, color=True, size=True):
    """Get video by given video path.

    Parameters
    ----------
    image_path : string
        target image absolute path
    color : bool
        if color is True then return color frames with BGR encoding.
        if color is False then return grey scale frames.
    size : bool
        if size is True then return the size of the frame.
        if size is False then just return the frame.

    Returns
    -------
    frames : list
        a list of frames that contains the video
    size : tuple
        size of the frame (optional).
    """
    container = av.open(vid_path)
    video = next(s for s in container.streams if s.type == b'video')

    frames = []
    for packet in container.demux(video):
        for frame in packet.decode():
            frame_t = np.array(frame.to_image())
            frame_t = cv2.cvtColor(frame_t, cv2.COLOR_RGB2BGR)
            if color is False:
                frame_t = cv2.cvtColor(frame_t, cv2.COLOR_BGR2GRAY)
            frames.append(frame_t)

    if size is True:
        return frames, frames[0].shape
    else:
        return frames


def get_lenna(color=True, size=True):
    """Get Lenna image.

    Parameters
    ----------
    color : bool
        if color is True then return a color frame with BGR encoding.
        if color is False then return a grey scale frame.
    size : bool
        if size is True then return the size of the frame.
        if size is False then just return the frame.

    Returns
    -------
    frame : numpy.ndarray
        a frame that contains Lenna image.
    size : tuple
        size of the frame (optional).
    """
    lenna_path = join(package_data_path, "lenna.png")
    if not os.path.isfile(lenna_path):
        raise ValueError("The Lenna image is not existed!")

    return get_image(lenna_path, color=color, size=size)


def get_dog(color=True, size=True):
    """Get dog image.

    The picture of dog is retrieved from Caltech-256 datasets which
    you can find from [here](www.vision.caltech.edu/Image_Datasets/Caltech256/)

    Parameters
    ----------
    color : bool
        if color is True then return a color frame with BGR encoding.
        if color is False then return a grey scale frame.
    size : bool
        if size is True then return the size of the frame.
        if size is False then just return the frame.

    Returns
    -------
    frame : numpy.ndarray
        a frame that contains dog image.
    size : tuple
        size of the frame (optional).
    """
    dog_path = join(package_data_path, "dog.jpg")
    if not os.path.isfile(dog_path):
        raise ValueError("The Dog image is not existed!")

    return get_image(dog_path, color=color, size=size)


def get_yuhuang(color=True, size=True):
    """Get Yuhuang Hu's photo.

    Parameters
    ----------
    color : bool
        if color is True then return a color frame with BGR encoding.
        if color is False then return a grey scale frame.
    size : bool
        if size is True then return the size of the frame.
        if size is False then just return the frame.

    Returns
    -------
    frame : numpy.ndarray
        a frame that contains Yuhuang Hu's photo.
    size : tuple
        size of the frame (optional).
    """
    yh_path = join(package_data_path, "yuhuang-hu-photo.png")
    if not os.path.isfile(yh_path):
        raise ValueError("The Yuhuang Hu's photo is not existed!")

    return get_image(yh_path, color=color, size=size)


def get_horse_riding(color=True, size=True):
    """Get Horse Riding video sequence.

    The video is retrieved from UCF-101 dataet which is
    available from [here](crcv.ucf.edu/data/UCF101.php)

    Parameters
    ----------
    color : bool
        if color is True then return color frames with BGR encoding.
        if color is False then return grey scale frames.
    size : bool
        if size is True then return the size of the frame.
        if size is False then just return the frame.

    Returns
    -------
    frame : list
        list of frames that contains Horse Riding video.
    size : tuple
        size of the frame (optional).
    """
    hr_path = join(package_data_path, "HorseRiding.avi")
    if not os.path.isfile(hr_path):
        raise ValueError("The Horse Riding video is not existed!")
    return get_video(hr_path, color=color, size=size)


def get_taichi(color=True, size=True):
    """Get Tai Chi video sequence.

    The video is retrieved from UCF-101 dataet which is
    available from [here](crcv.ucf.edu/data/UCF101.php)

    Parameters
    ----------
    color : bool
        if color is True then return color frames with BGR encoding.
        if color is False then return grey scale frames.
    size : bool
        if size is True then return the size of the frame.
        if size is False then just return the frame.

    Returns
    -------
    frame : list
        list of frames that contains Tai Chi video.
    size : tuple
        size of the frame (optional).
    """
    tc_path = join(package_data_path, "TaiChi.avi")
    if not os.path.isfile(tc_path):
        raise ValueError("The Tai Chi video is not existed!")
    return get_video(tc_path, color=color, size=size)
