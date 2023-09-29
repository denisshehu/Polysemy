def plot_2d(x, y, x_label, y_label, figure_path, y_min=None, y_max=None):
    plt.figure(figsize=(15, 5))
    plt.plot(x, y, marker='o', color='black')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.ylim(y_min, y_max)
    plt.savefig(figure_path, dpi=300)
    plt.close()
