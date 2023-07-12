from data_processing.data_storage import *


def plot_2d(x, y, x_label, y_label, file_path):
    plt.figure(figsize=(15, 5))
    plt.scatter(x, y, c='black')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(file_path, dpi=300)
    plt.close()


def plot_3d(x, y, z, c, color_map, color_bar_label, min_value, max_value,
            elevation, azimuth, aspect_ratio, show_ticks, file_path):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(x, y, z, c=c, cmap=color_map, vmin=min_value, vmax=max_value)
    fig.colorbar(scatter, label=color_bar_label)
    ax.view_init(elev=elevation, azim=azimuth)
    plt.gca().set_aspect(aspect_ratio)

    if not show_ticks:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])

    plt.savefig(file_path, dpi=300)
    plt.close()


def visualize_output(output_path, color_map='plasma', min_value=None, max_value=None,
                     elevation=30, azimuth=-60, aspect_ratio='equal', show_ticks=True):
    df = load_csv(output_path)

    n_columns = len(df.columns)
    points = list(df.iloc[:, :(n_columns - 2)].values)
    euclidicities = df.iloc[:, (n_columns - 2)]
    dimensions = df.iloc[:, (n_columns - 1)]

    prefix = output_path[:-10]
    plot_path = prefix + 'e_d.png'
    plot_2d(x=euclidicities, y=dimensions, x_label='Euclidicity', y_label='Dimension', file_path=plot_path)

    dimension = n_columns - 2
    if dimension <= 3:
        x = df.iloc[:, 0]
        y = np.zeros(shape=len(x)) if dimension < 2 else df.iloc[:, 1]
        z = np.zeros(shape=len(x)) if dimension < 3 else df.iloc[:, 2]

        plot_3d(x, y, z, dimensions, color_map, 'Dimension', min_value, max_value, elevation, azimuth,
                aspect_ratio, show_ticks, file_path=(prefix + 'd.png'))

        plot_3d(x, y, z, euclidicities, color_map, 'Euclidicity', min_value, max_value, elevation, azimuth,
                aspect_ratio, show_ticks, file_path=(prefix + 'e.png'))

    df = pd.DataFrame({'Point': points, 'Dimension': dimensions, 'Euclidicity': euclidicities})
    save_csv(df, prefix + 'df.csv')
