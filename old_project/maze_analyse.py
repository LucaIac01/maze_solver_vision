import cv2  # Library for image processing
from PIL import Image
import numpy as np  # Library for working with arrays and matrices



def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load image from '{}'".format(image_path))
        exit()
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyWindow('image')
    return image

def reshape_func(img_name):
    # Percorsi delle immagini
    image_to_resize_path = img_name  # Immagine da ridimensionare
    reference_image_path = './maze_image/maze2.png'  # Immagine di riferimento

    # Carica le immagini
    image_to_resize = Image.open(image_to_resize_path)
    reference_image = Image.open(reference_image_path)

    # Ottieni le dimensioni dell'immagine di riferimento
    new_size = reference_image.size  # Restituisce una tupla (larghezza, altezza)
    print(new_size)

    # Ridimensiona l'immagine
    resized_image = image_to_resize.resize(new_size, Image.Resampling.LANCZOS)

    # Salva o visualizza il risultato
    resized_image.save('./cropped_maze_reshape.png')  # Salva l'immagine ridimensionata
    resized_image.show()  # Visualizza l'immagine ridimensionata

    return './cropped_maze_reshape.png'


def main():
    path = reshape_func('./cropped_maze.png')

    img = load_image(path)
    height, width, channels = img.shape

    print(height, width, channels)





    cv2.destroyAllWindows()









if __name__ == '__main__':
    main()