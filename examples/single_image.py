from src.im import IM

im = IM({"ip": "[CAM_IP]", "user": "[CAM_USER]", "passwd": "[CAM_PASSWD]"})

img = im.get_image()

print(img)
