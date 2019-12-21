from src.im import IM

im = IM({"ip": "192.168.2.151", "user": "admin", "passwd": "lacapri001"})

img = im.get_image()

print(im)