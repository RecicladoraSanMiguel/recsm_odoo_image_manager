from ..models import ImageModel
from ..modules.http import HTTP


class ImageController:

    def __init__(self, cam1, cam2):
        self._cam1 = self.set_camera(cam1)
        self._cam2 = self.set_camera(cam2) if cam2 else False
        self._http = HTTP()
        self.imageM = ImageModel()

    def get_image(self):
        image = False
        img1 = self.get_web_image(self._cam1)

        if self._cam2:
            img2 = self.get_web_image(self._cam2)

            if img1["request"].is_valid() and img2["request"].is_valid():
                image = self.imageM.process_image(img1["image"], img2["image"])

            return {"cam1": img1["request"], "cam2": img2["request"], "image": image}

        else:
            img1 = self.get_web_image(self._cam1)

            if img1["request"].is_valid():
                image = self.imageM.process_image(img1["image"])

            return {"cam1": img1["request"], "image": image}

    def get_web_image(self, cam):
        image = False
        image_request = self._http.get(cam)

        if image_request.is_valid():
            request_bytes = image_request.get_response_body_binary()
            image = self.imageM.convert_bytes_to_image(request_bytes)

        return {"request": image_request, "image": image}

    def set_camera(self, cam):
        cam_conn_string = self.get_camera_url(cam["ip"], cam["user"], cam["passwd"])
        return cam_conn_string

    @staticmethod
    def get_camera_url(ip, user, passwd, secure=False):
        protocol = ("http", "https")[secure]
        return protocol + "://" + ip + "/cgi-bin/api.cgi?cmd=Snap&channel=0&rs=wuuPhkmUCeI9WG7C&user=" + user + "&password=" + passwd
        # http://192.168.2.32/cgi-bin/api.cgi?cmd=Snap&channel=0&rs=wuuPhkmUCeI9WG7C&user=admin&password=lacapri001
