# from make_embeddings_online import make_embeddings
from make_embeddings import make_embeddings, epochs_make_embeddings
from epochs_prediction_mlp import epochs_perform_predictions

def calc_distribution(tss):
    distribution = [0, 0]
    for ts in tss:
        for t in ts:
            if t == 0:
                distribution[0] += 1
            else:
                distribution[1] += 1
    return (distribution, distribution[1]/(distribution[0]+distribution[1]))


def walks_pipeline(epochs, graph_c, entities_c, target_value, entities_column, create_emb=True, show_all=True, walkLength=6, nWalks=6, reverse=True):
    # graph_c_name = graph_c.split('/')[-1]
    # entities_emb = "data/" + graph_c_name[:-4] + "_w_emb.csv"
    entities_emb = graph_c[:-4] + "_w_emb.csv"
    # entities_emb = graph_c[:-4] + "_w_emb_with_value.csv"
    # entities_emb = entities_file[:-4] + "_w_emb_with_value.csv"
    # entities_emb = entities_file


    if create_emb:
        # epochs_make_embeddings(epochs, entities_fn=entities_c, 
        make_embeddings(entities_fn=entities_c, 
                        kg_fn=graph_c, 
                        new_entities_fn=entities_emb,
                        entities_column_name=entities_column,reverse=reverse,
                        show_all=show_all)#, #need to show_all, only way to see time it takes to train representations
                        # walkLength=walkLength, nWalks=nWalks)

    final_results = epochs_perform_predictions(epochs, dataset_fn=entities_emb, show_all=show_all, target_value=target_value)
    # print(final_results["train_result"], final_results["test_result"])
    return final_results

def main(graph, entities_file, target_value, entities_column):
    epochs = 20
    walkLength = 2
    nWalks = 25
    reverse = True

    print(graph, '-', entities_file, "epochs=", epochs, "walkLength=", walkLength, "- nWalks=", nWalks)
    for i in range(0,1):
        results = walks_pipeline(epochs, graph, entities_file, target_value, entities_column, create_emb=False, show_all=False, walkLength=walkLength, nWalks=nWalks, reverse=reverse)
        for k in range(0,2):
            results = walks_pipeline(epochs, graph, entities_file, target_value, entities_column, create_emb=False, show_all=False, walkLength=walkLength, nWalks=nWalks, reverse=reverse)
        print("train_mae, test_mae, test_mape, base_mae, base_mape")

        print("--- finished ---")

if __name__ == '__main__':

    # # list_of_graphs = [ "samsung_try.ttl" ]
    # # list_of_graphs = [ "big_graph.ttl" ]
    # list_of_graphs = [ "res1dev1_graph_111.ttl" ]
    # list_of_graphs = [ "res1dev1CO2_graph_111.ttl" ]
    # list_of_graphs = [ "res1devA_graph_111.ttl" ]
    # list_of_graphs = [ "res1dev1TEMP_graph_111.ttl" ]
    # # list_of_graphs = [ "res1devA_graph_001.ttl" ]
    # # list_of_graphs = [ "big_graph_001.ttl" ]

    # # entities_file = "entityfile_small_with_value.csv"
    # # entities_file = "entities_2months.csv"
    # # entities_file = "entities_2months_2.csv"
    # # entities_file = "entities_2months_001_2.csv"
    # # entities_file = "entities_full_001.csv"
    # entities_file = "entities_full_111.csv"
    # entities_file = "res1dev1CO2_graph_001_w_emb_with_value.csv"
    # entities_file = "OfficeGraph_entities_w_valuew_weather.csv"

    # # entities_file = "res1dev1CO2_graph_111_w_emb_with_value.csv"
    # # entities_file = "opsd_data/Ares_Adev_111111111_uriTimeStamps_w_emb.csv"

    OfficeGraph = False
    opsd = False
    pecan = True
    if OfficeGraph:
        entities_column = "timestamp_uri"
        target_value = "outside_temp_Eindhoven"
        list_of_graphs = ["opsd/graphs/res1devA_enriched.nt"]
        entities_file = "opsd/opsd_entities.csv"
    elif opsd:
        list_of_graphs = ["opsd/graphs/res1devA_basic.nt"]
        entities_file = "opsd/opsd_entities.csv"
        target_value = "https://interconnectproject.eu/example/Konstanz_TempC"
        entities_column = "timestamp"
    elif pecan:
        list_of_graphs = ["pecan/graphs/res1devA_enriched.nt"]
        entities_file = "pecan/pecan_entities.csv"
        target_value = "outside_tempC"
        entities_column = "timestamp"

    for graph in list_of_graphs:
        main(graph, entities_file, target_value, entities_column)