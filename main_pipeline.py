from prediction_pipeline import main as pred_main
from classification_pipeline import main as clas_main

import time

if __name__ == '__main__':
	OfficeGraph = False
	OfficeGraph_reverse = True
	opsd = False
	PecanStreet = False

	if OfficeGraph:
		# graph_name = "res1dev1TEMP_graph_111.ttl"
		target_class = "hot_cold_binary"
		target_value = "outside_temp_Eindhoven"
		entities_file = "OfficeGraph_entities_w_valuew_weather.csv"
		entities_column = "timestamp_uri"
		list_of_graph_names = ["res1devA_basic", "res1devA_enriched", "res2devA_basic", "res2devA_enriched", "res3devA_basic", "res3devA_enriched", "res4devA_basic", "res4devA_enriched", "res5devA_basic", "res5devA_enriched", "res6devA_basic", "res6devA_enriched", "res7devA_basic", "res7devA_enriched", "res8devA_basic", "res8devA_enriched", "res9devA_basic", "res9devA_enriched", "res10devA_basic", "res10devA_enriched"]
		list_of_graph_names = ["res1devA_basic", "res1devA_enriched"]
	elif OfficeGraph_reverse:
		target_class = "hot_cold_binary"
		target_value = "outside_temp_Eindhoven"
		entities_file = "OfficeGraph_entities_w_valuew_weather.csv"
		entities_column = "timestamp_uri"
		# list_of_graph_names = ["reverse3_graph_001.ttl", "reverse3_graph_111.ttl", "reverse4_graph_001.ttl", "reverse4_graph_111.ttl", "reverse5_graph_001.ttl", "reverse5_graph_111.ttl", "reverse6_graph_001.ttl", "reverse6_graph_111.ttl", "reverse7_graph_001.ttl", "reverse7_graph_111.ttl"]
		list_of_graph_names = ["reverse7_graph_111.ttl"]
	elif opsd:
		# graph_name = "opsd/graphs/res1devA_enriched.nt"
		entities_file = "opsd/opsd_entities.csv"
		target_class = "https://interconnectproject.eu/example/Konstanz_HotCold"
		target_value = "https://interconnectproject.eu/example/Konstanz_TempC"
		entities_column = "timestamp"
		# list_of_graph_names = ["res1devA_basic", "res1devA_enriched", "res6devA_basic", "res6devA_enriched", "res3devA_basic", "res3devA_enriched", "res2devA_basic", "res2devA_enriched", "res4devA_basic", "res4devA_enriched", "res5devA_basic", "res5devA_enriched"]
		# list_of_graph_names = ["res4devA_enriched", "res5devA_basic", "res5devA_enriched"]
		list_of_graph_names = ["res1devA_basic", "res1devA_basic", "res4devA_basic", "res6devA_basic"] #todo!
	elif PecanStreet:
		# list_of_graph_names = ["res1devA_basic", "res1devA_enriched", "res2devA_basic", "res2devA_enriched", "res3devA_basic", "res3devA_enriched", "res4devA_basic", "res4devA_enriched", "res5devA_basic", "res5devA_enriched", "res6devA_basic", "res6devA_enriched", "res7devA_basic", "res7devA_enriched", "res8devA_basic", "res8devA_enriched", "res9devA_basic", "res9devA_enriched", "res10devA_basic", "res10devA_enriched"]
		list_of_graph_names = ["res10devA_enriched"]
		# list_of_graph_names = ["res8devA_enriched", "res10devA_basic"] #1 MORE!
		entities_file = "pecan/pecan_entities.csv"
		target_class = "https://interconnectproject.eu/example/Konstanz_HotCold"
		entities_column = "timestamp"
		target_value = "outside_tempC"


	# list_of_graph_names = ["big_graph_001.ttl", "big_graph.ttl"]
	# list_of_graph_names = ["res3devA_graph_001.ttl"]
	# list_of_graph_names = ["res9devA_graph_111.ttl","res9devA_graph_001.ttl"]
	# list_of_graph_names = ["res2devA_graph_111.ttl","res2devA_graph_001.ttl", "res3devA_graph_001.ttl"]
	# list_of_graph_names = ["res2devA_graph_111.ttl","res2devA_graph_001.ttl"]
	# list_of_graph_names = ["res4devA_graph_111.ttl","res4devA_graph_001.ttl"]

	for graph_name in list_of_graph_names:
		if opsd: graph_name = "opsd/graphs/" + graph_name + ".nt"
		if PecanStreet: graph_name = "pecan/graphs/" + graph_name + ".nt"
		if OfficeGraph: graph_name = "office/graphs/" + graph_name + ".nt"
		if OfficeGraph_reverse: graph_name = "office_reverse/graphs/" + graph_name
		for i in range(0,3):
			start_clas_time = time.time()
			clas_main(graph_name, entities_file, target_class, entities_column)
			end_clas_time = time.time()
			print("Classification executed in", end_clas_time - start_clas_time, "seconds")

			start_pred_time = time.time()
			pred_main(graph_name, entities_file, target_value, entities_column)
			end_pred_time = time.time()
			print("Prediction executed in", end_pred_time - start_pred_time, "seconds")