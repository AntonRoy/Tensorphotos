import vk_api
import random
import time
import tqdm

def captcha_handler(captcha):
    key = input("Enter Captcha {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


def user_photos(login, password, id):
    vk_app_id = -1
    try:
        vk = vk_api.VkApi(login, password, vk_app_id, captcha_handler=captcha_handler)
        vk.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
    values = {
        'owner_id': id,
        'count':50
    }
    photos = {'my_photos':[], 'friends_photos':[], 'ff_photos':[]}
    for el in vk.method('photos.getAll', values)['items']:
        photos['my_photos'].append(el['photo_130'])
    friends_list = vk.method('friends.get', {'user_id':id})['items']
    random.shuffle(friends_list)
    friends_list = friends_list[:20] #количество друзей
    for uid in tqdm.tqdm(friends_list):
        try:
            photo = vk.method('photos.getAll', {'owner_id': uid, 'count': 50})['items']
            for el in photo:
                photos['friends_photos'].append(el['photo_130'])
        except:
            pass
    ff_list = []
    for uid in tqdm.tqdm(friends_list):
        try:
            ff_list.extend(vk.method('friends.get', {'user_id': uid})['items'])
        except:
            pass
    random.shuffle(ff_list)
    ff_list = ff_list[:20] #количество друзей друзей
    for uid in tqdm.tqdm(ff_list):
        try:
            photo = vk.method('photos.getAll', {'owner_id': uid, 'count': 3})['items']
        except:
            pass
        for el in photo:
            photos['ff_photos'].append(el['photo_130'])
    return photos