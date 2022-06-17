import base64
import json
import time

import cv2
import numpy as np
import requests
from logzero import logger
from requests import RequestException


class FaceBlurAPI:
    def __init__(self, api_url, username, password):
        """FaceBlurAPI constructor

        Args:
            api_url (str): API URL
            username (str): Login username
            password (str): Login Password
        """
        self.api_url = api_url
        self.username = username
        self.password = password
        self.auth_token = ""
        self.login()

    def login(self):
        """Login Method"""
        payload = json.dumps({"username": self.username, "password": self.password})
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(f"{self.api_url}/api/token/", headers=headers, data=payload)
            self.auth_token = json.loads(response.content).get("access")
            logger.info("Succesfully obtained token for DT API!")
        except Exception as e:
            logger.exception(e)

    def return_sub6m_json(self, img, max_object_size):
        """Progressively increases compression of image to generate JSON of size <6MB

        Args:
            img (np.array): Input image
            max_object_size (int): Max permissible blur size w.r.t image size in percentage

        Returns:
            json_str (str): Returns sub 6Mb json payload
        """
        jpeg_quality = 100
        target_size = 6000
        while jpeg_quality > 50:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
            img_bytes = cv2.imencode(".jpg", img, encode_param)[1].tobytes()
            img_str = base64.b64encode(img_bytes).decode("utf-8")
            data = {"img": img_str, "jpeg_quality": jpeg_quality, "max_object_size": max_object_size}
            data_json = json.dumps(data)
            logger.info(f"data_json size in KB: {len(data_json)/1024}")

            if len(data_json) / 1024 < target_size:
                return data_json
            jpeg_quality -= 5
        return None

    def blur_np(self, img, max_object_size=-1):
        """Blurs image given as np.array/cv2 image

        Args:
            img (np.array): Input image
            max_object_size (int): Max permissible blur size w.r.t image size in percentage

        Returns:
            img (np.array): Face blurred image
        """
        data_json = self.return_sub6m_json(img, max_object_size)

        if not data_json:
            logger.error("Image too large to compress")
            return None

        headers = {"Authorization": f"Bearer {self.auth_token}", "Content-Type": "application/json"}
        MAX_RETRY = 3
        retries = 0
        while retries <= MAX_RETRY:
            try:
                response = requests.post(url=f"{self.api_url}/blur/", headers=headers, data=data_json)
                response.raise_for_status()
                break
            except RequestException as e:
                retries += 1
                if retries <= MAX_RETRY:
                    logger.error(f"API Request failed, trying again!")
                    time.sleep(2)
                    if e.response.status_code == 403:
                        # Auth token expired, login again
                        self.login()
                else:
                    raise RequestException(e)
        d = json.loads(response.content)
        im_bytes = base64.b64decode(d["img"])
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        return img

    def blur_path(self, path, max_object_size=100):
        """Blurs image given as a path

        Args:
            path (str): Input image path
            max_object_size (int): Max permissible blur size w.r.t image size in percentage

        Returns:
            img (np.array): Face blurred image
        """
        img = cv2.imread(str(path))
        return self.blur_np(img, max_object_size)
