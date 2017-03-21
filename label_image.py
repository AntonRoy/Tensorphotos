import tensorflow as tf, sys
import urllib.request
import vkpars
import tqdm

def photos_class(id):
    vup = vkpars.user_photos(id)
    data = vup['my_photos'] + vup['friends_photos'] + vup['ff_photos']
    count = 10 #количество фотографий
    data = data[:count]
    return class_of_photos(data)


def get_class(url):
    image_data = urllib.request.urlopen(url).read()
    label_lines = [line.rstrip() for line in tf.gfile.GFile("tf_files/retrained_labels.txt")]

    with tf.gfile.FastGFile("tf_files/retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        max_score = 0.0
        photo_class = None
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            if score > max_score:
                max_score = score
                photo_class = human_string
        return photo_class


def class_of_photos(url_list):
    for i in tqdm.tqdm(range(len(url_list))):
        url_list[i] = (url_list[i], get_class(url_list[i]))
    return url_list