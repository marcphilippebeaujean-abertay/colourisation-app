import matplotlib.pyplot as plt
import numpy as np


def display_img_sample(imgs, title):
    assert len(imgs) == 100
    img_rows, img_cols = imgs.shape[1], imgs.shape[2]
    imgs = imgs.reshape((10, 10, img_rows, img_cols, 3))
    imgs = np.vstack([np.hstack(i) for i in imgs])
    plt.figure()
    plt.axis('off')
    plt.title(title)
    plt.imshow(imgs, interpolation='none', cmap='gray')
    plt.show()
    

def plot_loss_history(train_hist, model_name):
    epochs = range(1, len(train_hist["loss"])+1)
    # Retrieve loss values
    loss_values = train_hist["loss"]
    val_loss_values = train_hist["val_loss"]

    plt.plot(epochs, loss_values, "bo", label="Training Set Loss")
    plt.plot(epochs, val_loss_values, "b", label="Validation Set Loss")
    plt.title("Training and Validation Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.title(model_name)
    plt.show()


def plot_predictions_data(predictions, model_name):
    _, axs = plt.subplots(1, 2, figsize=(3, 4))
    for i, ax in enumerate(axs):
        ax.boxplot(predictions[..., 0+i:1+i].flatten())
        if i is 0:
            ax.set_xlabel('a channel')
        else:
            ax.set_xlabel('b channel')
        ax.set_ylim((0, 1))
        ax.set_yticklabels([])
        ax.set_xticklabels([])
    plt.title(model_name)
    plt.show()
