import tensorflow as tf, sys
import urllib.request
import vkpars
import tqdm

#эта функция принимает на фход одну фотографию и возвращает ее класс
def get_class(url):
    image_data = urllib.request.urlopen(url).read()
    label_lines = [line.rstrip() for line in tf.gfile.GFile("tf_files/retrained_labels.txt")]
    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        max_score = 0.0#максимальная вероятность з всех классов
        for node_id in top_k:
            human_string = label_lines[node_id]#текущий класс
            score = predictions[0][node_id]#вероятность принадлежности текущему классу
            #здесь я проверяю если скор максимальный, то photo_class = типу с максимальным скором
            if score > max_score:
                max_score = score
                photo_class = human_string
        return photo_class

#эта функция обрабатывает блок фотографий, для каждого блока создается граф
def class_of_photos(url_list, PhotoSet):
    #делаю граф
    with tf.gfile.FastGFile("tf_files/retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')
    PhotoSet['all'].extend(url_list)
    #для каждой фотографии из списка получаю ее класс при помощи функции get_class() и добавляю ее в нужноый раздел словоря
    for url in tqdm.tqdm(url_list):
        PhotoSet[get_class(url)].append(url)
    return PhotoSet