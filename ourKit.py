import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_categories(base_path):
    categories = os.listdir(base_path)
    return categories


def load_images_from_folder(folder, num_images=None):
    images = []  # list to store images
    if (
        num_images is not None
    ):  # if num_images is not None, randomly select num_images images.
        indices = np.random.permutation(len(os.listdir(folder)))[:num_images]
    else:  # if num_images is None, load all images randomly.
        indices = np.random.permutation(len(os.listdir(folder)))
    filenames = np.array(os.listdir(folder))[indices]  # get all files in the folder
    for filename in filenames:
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            images.append(img)
    return images


def show_images(images, titles=None):
    fig, axes = plt.subplots(1, len(images), figsize=(15, 5))
    for i, img in enumerate(images):
        axes[i].imshow(img, cmap="gray")
        axes[i].axis("off")
        if titles:
            axes[i].set_title(titles[i])
    plt.show()


def get_class_distribution(images, categories):
    # Count number of images in each category
    class_distribution = {}
    for category in categories:
        class_distribution[category] = len(images[category])

    # Create a DataFrame from the class distribution
    return pd.DataFrame(
        class_distribution.values(), index=class_distribution.keys(), columns=["count"]
    )


def get_shape_distribution(images, categories):
    shape_distribution = {}
    for category in categories:
        for img in images[category]:
            shape = img.shape
            if shape in shape_distribution:
                shape_distribution[shape] += 1
            else:
                shape_distribution[shape] = 1
    return shape_distribution


def resize_images(images, categories, target_shape):
    # Resize all images to the target shape
    for category in categories:
        for i, img in enumerate(images[category]):
            images[category][i] = cv2.resize(img, target_shape, cv2.INTER_AREA)


# Histograms of pixel values for each category
def plot_histogram(images, title):
    plt.hist(images.ravel(), bins=256, range=(0, 256))
    plt.title(title)
    plt.xlabel("Pixel Values")
    plt.ylabel("Frequency")
    plt.show()
