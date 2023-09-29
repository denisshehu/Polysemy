from data_processing.models.word_collection import *
from OLD.tardis.output_generation_t import *
from OLD.tardis.output_processing_t import *
from OLD.visualization_generation.results_visualization_t import *


def get_results(query, input=None, n_neighbors=50, max_dimension=2, n_steps=10, batch_size=None, seed=None,
                filename_prefix=None, keep_terminal_open=True, color_map='plasma', min_value_d=0, max_value_d=None,
                min_value_e=0, max_value_e=None, elevation=None, azimuth=None, aspect_ratio='equal',
                show_ticks_x=True, show_ticks_y=True, show_ticks_z=True):
    word_collection = query if isinstance(query, WordCollection) else None
    if word_collection is not None:
        query, input = extract_query_and_data(word_collection, n_neighbors)

    filename = generate_output(query, input, n_neighbors, max_dimension, n_steps, batch_size, seed, filename_prefix,
                               keep_terminal_open)
    process_output(filename, word_collection)
    # visualize_results(filename, color_map, min_value_d, max_value_d, min_value_e, max_value_e, elevation, azimuth,
    #                   aspect_ratio, show_ticks_x, show_ticks_y, show_ticks_z)
    visualize_results('summary_', color_map, min_value_d, max_value_d, min_value_e, max_value_e, elevation, azimuth,
                      aspect_ratio, show_ticks_x, show_ticks_y, show_ticks_z)
    # update_dataframe_e1(filename)
