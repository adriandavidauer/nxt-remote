from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np


class ImageModel():
    def __init__(self, model_path, labels_path=None) -> None:
        # Load the model
        self.model = load_model(model_path)
        self.labels = None
        if labels_path:
            self.labels = self.txt_to_labels(labels_path)

    def txt_to_labels(self, label_path):
        labels = {}
        with open(label_path, 'r') as txt_file:
            for line in txt_file.readlines():
                splitted_line = line.split(' ')
                class_num = int(splitted_line[0].strip())
                label = " ".join(splitted_line[1:]).strip()
                labels[class_num] = label
        return labels

    def predict(self, image_path, image=None):
        """
        predicts from a given path or image if image is given path will be ignored.
        """
        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        # init image
        if image is None:
            image = Image.open(image_path).convert('RGB')
        else:
            image = Image.fromarray(image, 'RGB')
        # resize the image to a 224x224 with the same strategy as in TM2:
        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        # turn the image into a numpy array
        image_array = np.asarray(image)
        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = self.model.predict(data)
        if self.labels:
            labeld_prediction = {}
            for class_num, label in self.labels.items():
                labeld_prediction[label] = prediction[0][class_num]
            return labeld_prediction
        else:
            return prediction


if __name__ == "__main__":
    import cv2 as cv
    import argparse
    parser = argparse.ArgumentParser(
        description='keras model prediction from teachable machine')
    parser.add_argument('model_path', help="Path to the model file")
    parser.add_argument('--labels', help="Path to the labels file")
    parser.add_argument('--image', help='Path to a single image to predict')
    parser.add_argument(
        '--cam', help='if this option is set the webcam will be used - therefore image path will be ignored', action='store_true')
    parser.add_argument(
        '--cam_port', help='cam_port decides which cam to use')
    args = parser.parse_args()

    model = ImageModel(model_path=args.model_path, labels_path=args.labels)
    if not args.cam:
        print(f"Prediction of {args.image} is {model.predict(args.image)}")
    else:
        if not args.cam_port:
            args.cam_port = 0
        cam = cv.VideoCapture(args.cam_port)
        result, image = cam.read()
        while result:
            print(
                f"Prediction is {model.predict(image_path=None, image=image)}")
            result, image = cam.read()
