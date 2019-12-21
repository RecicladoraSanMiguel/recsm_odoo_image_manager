from src.im import IM

im = IM({"ip": "[camera ip]", "user": "[camera user]", "passwd": "[camera password]"}, {"ip": "[camera ip]", "user": "[camera user]", "passwd": "[camera password]"})

img = im.get_image()