from utils.main import *


def plot_2d(data, color=False):
    c = data[:, 0] if color else 'black'
    plt.scatter(data[:, 0], data[:, 1], c=c)
    plt.gca().set_aspect('equal')
    plt.show()


def plot_3d(data, color=False, elev=None, azim=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    c = data[:, 0] if color else 'black'
    ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=c)
    plt.gca().set_aspect('equal')
    ax.view_init(elev=elev, azim=azim)
    plt.show()
