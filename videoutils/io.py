#AUTOGENERATED! DO NOT EDIT! File to edit: dev/01_io.ipynb (unless otherwise specified).

__all__ = ['__all__', 'read_video', 'read_frames', 'capture', 'get_target_frames']

#Cell
from .utils import *

#Cell
__all__ = ['read_video', 'read_frames', 'capture', 'as_tensor', 'as_normalised_tensor', 'lapply']

#Cell
def read_video(fname         : Union[str, cv2.VideoCapture],
               start_idx     : Optional[int]=None,
               end_idx       : Optional[int]=None,
               frame_stride  : Optional[int]=None,
               target_frames : Union[tuple, list, int, np.array]=None,
               apply         : Optional[Callable]=None) -> Union[torch.Tensor, list]:
    """
    Flexible video reader where you can grab frames in different ways
    and return as different dtypes.

    **Args**

    * `fname`        : a `cv2.VideoCapture` object, or path to the video file
    * `start_idx`    : index of the frame where you'd like to start reading the file
    * `end_idx`      : index of the frame where you'd like to end reading the file
    * `frame_stride` : after reading the frame, every `frame_stride`th index will be read
    * `target_frames`: if this arg is used, `start_idx`, `end_idx`, and `frame_stride` are ignored. Can be an

            - `int`            : returns frame at this index
            - `list`/`np.array`: returns frame at index of each element
            - `tuple`          : a tuple like `(start_idx, end_idx, frame_stride)` where
                                 `frame_stride`is optional. If this is what you want, using the
                                 other args instead of `target_frames` is more flexible.
    * `apply`         : a function that transforms a single `np.array` of shape `(height, width, channels)`
    """
    cap    = capture(fname)
    if target_frames is None: target_frames = get_target_frames(fname, start_idx, end_idx, frame_stride)
    frames = read_frames(cap, target_frames)
    cap.release()

    if apply is not None:
        if apply == as_tensor or as_normalised_tensor: frames = torch.stack(lapply(frames, apply))
        else: frames = lapply(frames, apply)

    return frames

#Cell
def read_frames(cap: cv2.VideoCapture,
                target_frames: Union[tuple, list, int, np.array]) -> list:
    "Read specific frames from a `cv2.VideoCapture` object"
    if   isinstance(target_frames, tuple) : frame_idxs = np.arange(*target_frames)
    elif isinstance(target_frames, list)  : frame_idxs = target_frames
    elif isinstance(target_frames, int)   : frame_idxs = [target_frames]
    elif isinstance(target_frames, np.ndarray)   : frame_idxs = target_frames

    frames=[]
    for i in frame_idxs:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret==True: frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) # return np.array
        else: break
    return frames

#Cell
def capture(x: Union[str, cv2.VideoCapture]) -> cv2.VideoCapture:
    "Ensure `cv2.VideoCapture` works properly"
    assert isinstance(x, (str, cv2.VideoCapture)), \
    f"Expected `str` or `cv2.VideoCapture` but received {type(x)} "
    cap = cv2.VideoCapture(x) if isinstance(x, str) else x
    assert(cap.isOpened()), f'Failed to open video "{x}"'
    return cap

#Cell
def get_target_frames(file, start, end, stride):
    "flexibly get the indixes of the frames you want to grab"
    num_frames = capture(file).get(cv2.CAP_PROP_FRAME_COUNT)
    if start is not None:
        if end is None: return np.arange(0, num_frames, stride)
        else:           return np.arange(start, end, stride)
    if start is None:
        if end is None: return np.arange(0, num_frames, stride)
        else:           return np.arange(0, end, stride)