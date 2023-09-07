from data_processing.data_storage import *


def plot_2d(x, y, x_label, y_label, figure_path, n_senses=None):
    plt.figure(figsize=(15, 5))

    if n_senses is None:
        plt.scatter(x, y, c='black')
    else:
        monosemes = [i for i in range(len(n_senses)) if n_senses[i] == 1]
        polysemes = [i for i in range(len(n_senses)) if i not in monosemes]
        plt.scatter(x[monosemes], y[monosemes], c='black', label='Monoseme')
        plt.scatter(x[polysemes], y[polysemes], c='red', label='Polyseme')
        plt.legend()

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(figure_path, dpi=300)
    plt.close()


def plot_3d(x, y, z, c, color_map, color_bar_label, min_value, max_value, elevation, azimuth, aspect_ratio,
            show_ticks_x, show_ticks_y, show_ticks_z, figure_path):
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

    plt.savefig(figure_path, dpi=300)
    plt.close()


def string2array(string):
    string = string[1:-1].strip()
    string = string.replace('\n', '')
    string = re.sub(r'\s+', ' ', string)
    return np.array(string.split(sep=' '), dtype=np.float32)


def visualize_results(filename, color_map, min_value_d, max_value_d, min_value_e, max_value_e, elevation, azimuth,
                      aspect_ratio, show_ticks_x, show_ticks_y, show_ticks_z):
    results_path = os.path.join(results_subdirectory, f'{filename}results.csv')
    results = load_csv(results_path)

    dimension_label = 'Dimension'
    euclidicity_label = 'Euclidicity'

    points = results['Point']
    dimensions = results[dimension_label]
    euclidicities = results[euclidicity_label]

    if 'Word' in results.columns:
        n_senses_label = 'Number of senses'
        n_senses = results[n_senses_label]

        plot_2d(x=euclidicities, y=dimensions, x_label=euclidicity_label, y_label=dimension_label,
                figure_path=os.path.join(euclidicity_dimension_directory, f'{filename}e_d.png'), n_senses=n_senses)
        plot_2d(x=euclidicities, y=n_senses, x_label=euclidicity_label, y_label=n_senses_label,
                figure_path=os.path.join(euclidicity_senses_directory, f'{filename}e_s.png'), n_senses=n_senses)
        plot_2d(x=n_senses, y=dimensions, x_label=n_senses_label, y_label=dimension_label,
                figure_path=os.path.join(senses_dimension_directory, f'{filename}s_d.png'), n_senses=n_senses)
    else:
        plot_2d(x=euclidicities, y=dimensions, x_label=euclidicity_label, y_label=dimension_label,
                figure_path=os.path.join(euclidicity_dimension_directory, f'{filename}e_d.png'))

    dimension = len(string2array(points[0]))
    if dimension <= 3:
        points = np.array([string2array(point) for point in points])
        x = np.array([point[0] for point in points])
        y = np.zeros(shape=len(x)) if dimension < 2 else np.array([point[1] for point in points])
        z = np.zeros(shape=len(x)) if dimension < 3 else np.array([point[2] for point in points])

        if dimension < 3:
            elevation, azimuth, show_ticks_z = 90, -90, False

        plot_3d(x, y, z, dimensions, color_map, dimension_label, min_value_d, max_value_d,
                elevation, azimuth, aspect_ratio, show_ticks_x, show_ticks_y, show_ticks_z,
                figure_path=os.path.join(dimension_directory, f'{filename}d.png'))

        plot_3d(x, y, z, euclidicities, color_map, euclidicity_label, min_value_e, max_value_e,
                elevation, azimuth, aspect_ratio, show_ticks_x, show_ticks_y, show_ticks_z,
                figure_path=os.path.join(euclidicity_directory, f'{filename}e.png'))
