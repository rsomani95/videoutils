#AUTOGENERATED! DO NOT EDIT! File to edit: dev/01_io.ipynb (unless otherwise specified).

__all__ = ['read_video', 'read_frames', 'capture', 'get_target_frames']

#Cell
from .utils import *

#Cell
def read_video(fname         : Union[str, cv2.VideoCapture],
               start_idx     : Optional[int]=None,
               end_idx       : Optional[int]=None,
               frame_stride  : Optional[int]=None,
               target_frames : Union[tuple, list, int, np.array]=None,
               apply         : Callable=None) -> Union[torch.Tensor, list]:
    """Flexible video reader where you can grab frames in different ways
    and return as different dtypes.
    """
    cap    = capture(fname)
    if target_frames is None: target_frames = get_target_frames(fname, start_idx, end_idx, frame_stride)
    frames = read_frames(cap, target_frames)
    cap.release()

    if apply is not None:
        if apply == as_tensor: frames = torch.stack(lapply(frames, apply))
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
    num_frames = capture(file).get(cv2.CAP_PROP_FRAME_COUNT)
    if start is not None:
        if end is None: return np.arange(0, num_frames, stride)
        else:           return np.arange(start, end, stride)
    if start is None:
        if end is None: return np.arange(0, num_frames, stride)
        else:           return np.arange(0, end, stride)