import winsound

from to_be_deleted.OLD.tardis.main_t import *

word_collection = load_yaml(normalized_sc_word_collection_path)
query = word_collection.get_monosemes_and_polysemes(n=100, use_n_total_senses=True)

words = list(query.words.values())

for i in range(int(len(words)/2)):
    for j in [i, i + 100]:
        value = words[j].value
        new_query = query.filter_by_membership('value', value)

        dataframe = load_csv(os.path.join(intrinsic_dimension_directory, 'intrinsic_dimension_200t.csv'))
        dimension = round(list(dataframe[dataframe['Word'] == value]['Intrinsic dimension estimate'])[0])

        get_results(query=new_query, max_dimension=dimension, seed=1, filename_prefix='final', keep_terminal_open=False)

winsound.Beep(500, 3000)
