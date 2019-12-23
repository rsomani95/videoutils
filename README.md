<!--

#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: nbs/index.ipynb
# command to build the docs after a change: nbdev_build_docs

-->

# Video Utilities for OpenCV

> `videoutils` lets you get rid of writing boilerplate code for reading video and adds some convenience on top of that.


## Install

`pip install videoutils`

## How to use
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
from videoutils.io import read_video, as_tensor, bgr2rgb, resize
fname = 'files/interstellar-waves-edit.mp4'
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
x = read_video(fname)
len(x)
x[0].shape
```

</div>
<div class="output_area" markdown="1">




    1578






    (480, 720, 3)



</div>

</div>

By default, `read_video` returns a list of `np.array`s of shape `(height, width, channels)`. <br>
However, you can define precisely which frames you'd like to grab in a number of ways. This is done by using either the {`start_idx`, `end_idx`, `frame_stride`} or `target_frames` arguments. 

### Grab the first `n` frames
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
n = 50
x  = read_video(fname, end_idx=n)
x2 = read_video(fname, target_frames=(0,n))

len(x)
len(x) == len(x2)
```

</div>
<div class="output_area" markdown="1">




    50






    True



</div>

</div>

### Grab every `n`th frame
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
n=5
x = read_video(fname, frame_stride=n, end_idx=50)
len(x)
```

</div>
<div class="output_area" markdown="1">




    10



</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
x = read_video(fname, frame_stride=50) # total frames = 1578
len(x)
```

</div>
<div class="output_area" markdown="1">




    32



</div>

</div>

### Grab frames at specific indices
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
x = read_video(fname, target_frames=[10, 50, 76, 420])
len(x)
```

</div>
<div class="output_area" markdown="1">




    4



</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
x  = read_video(fname, start_idx=10, end_idx=15)
x2 = read_video(fname, target_frames=(10, 15))

len(x)
len(x) == len(x2)
```

</div>
<div class="output_area" markdown="1">




    5






    True



</div>

</div>

### Return as `torch.Tensor`

You can pass any function that transforms a `np.array` of shape `(height, width, channels)` to the `apply` argument. `Videoutils` provides `as_tensor` for convenience -- if you use this function, `read_video` will automatically call `torch.stack` and return the collection of frames as a 4D tensor, else it will return a `list` of 3D arrays/tensors.
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
xx = partial(as_tensor)
```

</div>
<div class="output_area" markdown="1">




    functools.partial



</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
import torch
from functools import partial

x  = read_video(fname, end_idx=10, apply=as_tensor)
x2 = read_video(fname, end_idx=10, apply=partial(as_tensor, normalise=True))
x2 = torch.stack(x2) # since we aren't using `as_tensor`, but a partial (thus different) function

x.shape
x.shape == x2.shape
x.mean(), x2.mean()
```

</div>
<div class="output_area" markdown="1">




    torch.Size([10, 480, 720, 3])






    True






    (tensor(36.8276), tensor(0.1443))



</div>

</div>

### Resize Video

`read_video` has an optional argument `resize_func` which is meant to be a function that resizes a `np.array` of shape `(height, width, channels)`. <br>
You can use the predefined `resize` function or pass in a custom function here.
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
help(resize)
```

</div>
<div class="output_area" markdown="1">

    Help on function resize in module videoutils.utils:
    
    resize(image, height=None, width=None, keep_aspect_ratio=True, scale_factor=1.0)
        Resize by `scale_factor` if preserving aspect ratio else
        resize by custom `height` and `width`
    


</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
x = read_video(fname, target_frames=[0,1,2], apply=as_tensor,
               resize_func=partial(resize, scale_factor=2.))
x.shape
```

</div>
<div class="output_area" markdown="1">




    torch.Size([3, 960, 1440, 3])



</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
x = read_video(fname, target_frames=[0,1,2], apply=as_tensor,
               resize_func=partial(resize, width=200, height=100, keep_aspect_ratio=False))
x.shape
```

</div>
<div class="output_area" markdown="1">




    torch.Size([3, 100, 200, 3])



</div>

</div>
