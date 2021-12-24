# dt-face-blur-api

This is a client-side python library to talk to the DT Face Blur API

## Installation
dt-face-blur-api requires Python 3.5.6+ to run.

```sh
pip install git+https://github.com/detecttechnologies/dt-face-blur-api.git
```

## Usage
```python
from dt_face_blur_api import FaceBlurAPI

fb = FaceBlurAPI(
    api_url="<URL of the API>",
    username="<Username>",
    password="<Password>"
)
img = fb.blur_path("<path to an image>") # Opens and runs inference on image stored in the disk
img2 = fb.blur_np(img_arr) # Runs inference on a numpy array
```
