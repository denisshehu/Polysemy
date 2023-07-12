from data_processing.data_storage import *
import matplotlib.pyplot as plt


def plot_1d(x):
    y = np.zeros(shape=len(x))
    plot_2d(x=x, y=y, x_label='x', y_label='y')


def plot_2d(x, y, x_label=None, y_label=None):
    fig, ax = plt.subplots()
    ax.scatter(x, y, c='black')
    if x_label is not None:
        ax.set_xlabel(x_label)
    if y_label is not None:
        ax.set_ylabel(y_label)
    plt.savefig(os.path.join(results_directory, 'a.jpg'))
    plt.show()


def plot_3d(x, y, z, c, cmap, label, elev, azim, name=None, max_value=None, equal=True, hide_z=False):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    if max_value is not None:
        sc = ax.scatter(x, y, z, c=c, cmap=cmap, vmin=0.0, vmax=max_value)
    else:
        sc = ax.scatter(x, y, z, c=c, cmap=cmap)

    cbar = plt.colorbar(sc)
    cbar.set_label(label)

    ax.view_init(elev=elev, azim=azim)

    if equal:
        plt.gca().set_aspect('equal')

    if hide_z:
        ax.set_zticklabels([])

    if name is not None:
        plt.savefig(name)

    plt.show()


def visualize_output(output_path):
    df = load_csv(output_path)

    n_columns = len(df.columns)
    point_column = list(df.iloc[:, :(n_columns - 2)].values)
    euclidicity_column = df.iloc[:, (n_columns - 2)]
    dimension_column = df.iloc[:, (n_columns - 1)]

    dimension = n_columns - 2
    if dimension == 1:
        plot_1d(x=df.iloc[:, 0])
    elif dimension == 2:
        plot_2d(x=df.iloc[:, 0], y=df.iloc[:, 1], x_label='x', y_label='y')
    elif dimension == 3:
        plot_3d(x=df.iloc[:, 0], y=df.iloc[:, 1], z=df.iloc[:, 2])

    plot_2d(euclidicity_column, dimension_column, 'Euclidicity', 'Dimension')

    return pd.DataFrame({'Point': point_column, 'Dimension': dimension_column, 'Euclidicity': euclidicity_column})