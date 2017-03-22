import vk_api
import random
import time
import tqdm
import vk as vk1
import urllib

def get_photo(url, id):
    path = "vk_photos/" + str(id) + '.jpeg'
    file = open(path, "w+")
    urllib.request.urlretrieve(url, path)

def captcha_handler(captcha):
    key = input("Enter Captcha {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


def user_photos(id):
    session = vk1.Session(access_token='5514ece0b607363d71e6045e8db3bb672b92ded395897ea50c126e49bee803399b51c2f2dafdf4567df16')
    vk = vk1.API(session)
    values = {
        'owner_id': id,
        'count':100
    }
    photos = {'my_photos':[], 'friends_photos':[], 'ff_photos':[]}
    for el in vk.photos.getAll(owner_id=id, count=50)[1:]:
        photos['my_photos'].append(el['src'])
    friends_list = vk.friends.get(user_id=id)
    random.shuffle(friends_list)
    friends_list = friends_list[:100] #количество друзей
    for uid in tqdm.tqdm(friends_list):
        try:
            photo = vk.photos.getAll(owner_id=uid, count=10)[1:]
            for el in photo:
                photos['friends_photos'].append(el['src'])
        except:
            pass
    ff_list = []
    for uid in tqdm.tqdm(friends_list):
        try:
            ff_list.extend(vk.friends.get(user_id=uid))
        except:
            pass
    random.shuffle(ff_list)
    ff_list = ff_list[:100] #количество друзей друзей
    for uid in tqdm.tqdm(ff_list):
        try:
            photo = vk.photos.getAll(owner_id=uid, count=5)[1:]
        except:
            pass
        for el in photo:
            photos['ff_photos'].append(el['src'])
    return photos