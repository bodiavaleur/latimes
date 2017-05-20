import vk
import requests

SESH = vk.Session(access_token= 'TOKEN')
API = vk.API(SESH)

def wallPhoto(image):
    try:
        response = requests.get(image)
        if response.status_code == 200:
            f = open('img.jpg', 'wb')
            f.write(response.content)

        files = {'photo': ('img.jpg', open(r'img.jpg', 'rb'))}
        url = "https://pu.vk.com/c626326/upload.php"
        data={"act":"do_add",
              "gid":"145115285",
              "mid":"221643898",
              "aid":"-14",
              "hash":"97c801d5528617e03e808966f4d665dd",
              "rhash": "ab5ffa458d464d9e1e09df14ec203d51",
              "swfupload":"1",
              "wallphoto": "1",
              "api":"1"}
        req = requests.post(url, data, files = files)
        save = API.photos.saveWallPhoto(user_id  = '221643898',
                                        group_id = '145115285',
                                        photo    = req.json()['photo'],
                                        server   = req.json()['server'],
                                        hash     = req.json()['hash'])

        return(save[0]['id'])

    except Exception as err:
        print('[!] Error:', err)


def make_post(text, photo, link):
    try:
        API.wall.post(owner_id    = '-145115285',
                      from_group  = 1,
                      message     = text,
                      signed      = 0,
                      attachments = (photo, link)
                      )
        return True
        
    except Exception as err:
        print(err)
        return False
