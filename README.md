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
#The list of polygons is used to blurr perticular areas of the image   
my_polygons=[
    [
        [100,100],[200,100],[200,200],[100,200]
    ]
]
img = fb.blur_path("<path to an image>") # Opens and runs inference on image stored in the disk
img2 = fb.blur_np(img_arr) # Runs inference on a numpy array
img3 = fb.blur_path("<path to an image>", max_object_size=50) # set max_object_size as an optional parameter to limit max. permissible blur size w.r.t image size
img4 = fb.blur_path("<path to an image>", polygons=my_polygons) # pass polygons as a parameter to blur perticular areas of an image other than object
```

## Support
- To gain access to the system, mail [sales](mailto:sales@detecttechnologies.com)
- For support on usage of the system, mail [support](mailto:support@detecttechnologies.com)
