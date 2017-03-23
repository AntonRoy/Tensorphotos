import urllib.request
import vkpars
import tqdm
from label_image import class_of_photos
'''
эта функция изпользуя мною написанный файл vkpars выкачивает все фотографии пользователя по id,
разбивает на блоки,
далее вызывает функцию class_of_photos для каждого блока и вконце возвращает словарь, ключи которого это классы, а значения это списки фотографий принадлежащие данному классу
'''
def photos_class(id):
    vup = vkpars.user_photos(id)
    vk_data = vup['ff_photos'] + vup['my_photos'] + vup['friends_photos'] #все фотографии пользователя, его друзей и друзей друзей
    batch_size = 15 #количество фотографий в одном блоке
    data = []
    i = 1
    vk_data = vk_data[:10]#количество фотографий всего(берем нужное число фотографий от vk_data)
    PhotoSet = {'all':[], 'ladies naked': [], 'ladies swimsuit': [], 'men naked': [], 'men swimsuit': []}
    while i * batch_size <= len(vk_data):
        PhotoSet = class_of_photos(vk_data[(i-1)*batch_size:i*batch_size], PhotoSet)
        i += 1
    if (i - 1) * batch_size != len(vk_data):
        PhotoSet = class_of_photos(vk_data[(i - 1) * batch_size:], PhotoSet)
    print('все фотографии:', PhotoSet['all'])
    print('ladies naked:', PhotoSet['ladies naked'])
    print('ladies swimsuit:', PhotoSet['ladies swimsuit'])
    print('men naked:', PhotoSet['men naked'])
    print('men swimsuit:', PhotoSet['men swimsuit'])
    return PhotoSet
