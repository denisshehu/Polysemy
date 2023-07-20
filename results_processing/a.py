from data_processing.data_storage import *


def plot_2d(x, y, x_label, y_label, file_path):
    plt.figure(figsize=(15, 5))
    plt.scatter(x, y, c='black')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(file_path, dpi=300)
    plt.close()


def plot_3d(x, y, z, c, color_map, color_bar_label, min_value, max_value,
            elevation, azimuth, aspect_ratio, show_ticks_x, show_ticks_y, show_ticks_z, file_path):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(x, y, z, c=c, cmap=color_map, vmin=min_value, vmax=max_value)
    fig.colorbar(scatter, label=color_bar_label)
    ax.view_init(elev=elevation, azim=azimuth)
    plt.gca().set_aspect(aspect_ratio)

    if not show_ticks_x:
        ax.set_xticks([])
    if not show_ticks_y:
        ax.set_yticks([])
    if not show_ticks_z:
        ax.set_zticks([])

    plt.savefig(file_path, dpi=300)
    plt.close()


def visualize_output(output_path, words=None, color_map='plasma', min_value_d=None, max_value_d=None,
                     min_value_e=None, max_value_e=None, elevation=30, azimuth=-60, aspect_ratio='equal',
                     show_ticks_x=True, show_ticks_y=True, show_ticks_z=True):
    df = load_csv(output_path)

    n_columns = len(df.columns)
    points = list(df.iloc[:, :(n_columns - 2)].values)
    euclidicities = df.iloc[:, (n_columns - 2)]
    dimensions = df.iloc[:, (n_columns - 1)]

    prefix = output_path[:-10]
    plot_path = prefix + 'e_d.png'
    plot_2d(x=euclidicities, y=dimensions, x_label='Euclidicity', y_label='Dimension', file_path=plot_path)

    if words is not None:
        value = []
        n_senses = []
        for point in points:
            for word in words:
                if np.array_equal(point, word.embedding):
                    value.append(word.value)
                    n_senses.append(word.n_senses)
                    break

        plot_path = prefix + 'e_s.png'
        plot_2d(x=euclidicities, y=n_senses, x_label='Euclidicity', y_label='Number of senses', file_path=plot_path)

        plot_path = prefix + 's_d.png'
        plot_2d(x=n_senses, y=dimensions, x_label='Number of senses', y_label='Dimension', file_path=plot_path)

        df = pd.DataFrame({'Word': value, 'Point': points, 'Dimension': dimensions, 'Euclidicity': euclidicities,
                           'Number of senses': n_senses})
        save_csv(df, prefix + 'dataframe.csv')
    else:
        dimension = n_columns - 2
        if dimension <= 3:
            x = df.iloc[:, 0]
            y = np.zeros(shape=len(x)) if dimension < 2 else df.iloc[:, 1]
            z = np.zeros(shape=len(x)) if dimension < 3 else df.iloc[:, 2]

            plot_3d(x, y, z, dimensions, color_map, 'Dimension', min_value_d, max_value_d, elevation, azimuth,
                    aspect_ratio, show_ticks_x, show_ticks_y, show_ticks_z, file_path=(prefix + 'd.png'))

            plot_3d(x, y, z, euclidicities, color_map, 'Euclidicity', min_value_e, max_value_e, elevation, azimuth,
                    aspect_ratio, show_ticks_x, show_ticks_y, show_ticks_z, file_path=(prefix + 'e.png'))

        df = pd.DataFrame({'Point': points, 'Dimension': dimensions, 'Euclidicity': euclidicities})
        save_csv(df, prefix + 'dataframe.csv')
