"""GUI related functions.

Author: Yuhuang Hu
Email : yuhuang.hu@uzh.ch
"""

import sys
import cv2
import numpy as np


def cv2pg(frame, wg_h, wg_w, bgr=True, color=[255, 0, 0]):
    """Convert a OpenCV frame to PyQtGraph frame.

    Parameters
    ----------
    frame : numpy.ndarray
        A OpenCV frame
    wg_h : int
        width of the frame widget
    wg_w : int
        height of the frame widget
    bgr : bool
        flag for indicating if the frame is in BGR panel.
        Default is True (is BGR), False (is not BGR)
    color : list
        The background color of appended border
    """
    if frame.ndim < 3:
        raise ValueError("Input is not a color image.")

    if bgr is True:
        frame = bgr2rgb(frame)

    frame = fit_frame(frame, wg_h, wg_w, color)
    frame = make_pg_frame(frame)

    return frame


def make_pg_frame(frame):
    """Transpose frame to PyQtGraph frame.

    Parameters
    ----------
    frame : numpy.ndarray
        frame in OpenCV space.

    Returns
    -------
    new_frame : numpy.ndarray
        new frame in PyQtGraph frame space.
    """
    return np.transpose(frame, axes=(1, 0, 2))


def fit_frame(frame, wg_h, wg_w, color=[255, 0, 0]):
    """Fit to size of frame widget.

    Parameters
    ---------
    frame : numpy.ndarray
        given image or frame
    wg_h : int
        width of the frame widget
    wg_w : int
        height of the frame widget
    color : list
        The background color of appended border

    Returns
    -------
    new_frame : numpy.ndarray
        fit frame
    """
    # new_frame = frame.copy()
    # try to save memory
    new_frame = frame
    frame_h = frame.shape[0]
    frame_w = frame.shape[1]
    # if the ratio is different, then append border
    if (float(wg_h)/float(wg_w)) != (float(frame_h)/float(frame_w)):
        # do something
        if (float(frame_h)/float(frame_w)) > (float(wg_h)/float(wg_w)):
            w_append = int((frame_h*wg_w-wg_h*frame_w)/wg_h)
            new_frame = cv2.copyMakeBorder(src=new_frame, top=0, bottom=0,
                                           left=w_append/2, right=w_append/2,
                                           borderType=cv2.BORDER_CONSTANT,
                                           value=color)

        elif (float(frame_h)/float(frame_w)) < (float(wg_h)/float(wg_w)):
            h_append = int((wg_h*frame_w-frame_h*wg_w)/wg_w)
            new_frame = cv2.copyMakeBorder(src=new_frame, top=h_append/2,
                                           bottom=h_append/2, left=0, right=0,
                                           borderType=cv2.BORDER_CONSTANT,
                                           value=color)

    new_frame = cv2.resize(new_frame, (wg_w, wg_h),
                           interpolation=cv2.INTER_AREA)

    return new_frame


def resize(frame, new_size):
    """Wrap OpenCV frame resize function.

    Parameters
    ----------
    frame : numpy.ndarray
        a given frame
    new_size : tuple
        new size in tuple: (width, height)

    Returns
    -------
    new_frame : numpy.ndarray
        resized frame
    """
    return cv2.resize(frame, new_size, interpolation=cv2.INTER_CUBIC)


def bgr2rgb(frame):
    """Convert color span from BGR to RGB.

    Parameters
    ----------
    frame : numpy.ndarray
        a given frame

    Returns
    -------
    new_frame : numpy.ndarray
        a converted frame
    """
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


def trans_bgr2rgb_seq(frames):
    """Transfer BGR sequence to RGB sequence.

    Parameters
    ----------
    frames : list
        a given BGR sequence

    Returns
    -------
    new_frames : list
        a converted RGB sequence
    """
    return [bgr2rgb(frame) for frame in frames]


def create_viewer_field(frames, inter_padding=20, border_padding=40,
                        color=[0, 0, 0]):
    """Create Viewer field by gluing multiple frames together.

    Parameters
    ----------
    frames : list
        list of frames in order, assumed order
        [original BGR frame, Parvo frame, Magno frame]
        P.S. make sure Magno frame is also a BGR image
    inter_padding : int
        spacing between each frame
    border_padding : int
        append border to fused frame
    color : list
        3 value that specify the color of the border

    Returns
    -------
    viewer_frame : numpy.ndarray
        A new frame that fit in viewer's size
    """
    viewer_frame = np.array([])

    for frame in frames:
        temp_frame = cv2.copyMakeBorder(frame, inter_padding, inter_padding,
                                        inter_padding, inter_padding,
                                        cv2.BORDER_CONSTANT, value=color)

        if not viewer_frame.size:
            viewer_frame = temp_frame
        else:
            viewer_frame = np.hstack((viewer_frame, temp_frame))

    viewer_frame = cv2.copyMakeBorder(viewer_frame, inter_padding,
                                      inter_padding, inter_padding,
                                      inter_padding, cv2.BORDER_CONSTANT,
                                      value=color)
    return viewer_frame


def get_viewer_frame(frame, viewer_size):
    """Get viewer frame.

    Parameters
    ----------
    frame : numpy.ndarray

    viewer_size : tuple

    Returns
    -------
    viewer_frame : numpy.ndarray
    """
    return cv2.resize(frame, (viewer_size[1], viewer_size[0]),
                      interpolation=cv2.INTER_CUBIC)


# GUI response functions
def p_no_state(button):
    """State response of IPL and OPL Parvo output normalization.

    Parameters
    ----------
    button : QtGui.QRadioButton
        the button state

    Returns
    -------
    response : bool
        True (if Yes selected), False (if No selected)
    """
    if button.text() == "Yes":
        if button.isChecked():
            return True
    elif button.text() == "No":
        if button.isChecked():
            return False


def m_no_state(button):
    """State response of IPL Magno output normalization.

    Parameters
    ----------
    button : QtGui.QRadioButton
        the button state

    Returns
    -------
    response : bool
        True (if Yes selected), False (if No selected)
    """
    if button.text() == "Yes":
        if button.isChecked():
            return True
    elif button.text() == "No":
        if button.isChecked():
            return False


def exit_wg_state(button, app):
    """Define exit button.

    Parameters
    ----------
    button : QtGui.QPushButton
        the exit button
    app : QtGui.QApplication
        the main QtGui application

    Returns
    -------
    exit the program
    """
    if button.isChecked():
        sys.exit(app.exec_())
