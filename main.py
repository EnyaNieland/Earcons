import MidiPlayer
import GUI
import Mapper
import Metrics
# import SPARQLEndpoint
import Earcon
import SQLite
import time
import re

# sparql = SPARQLEndpoint.SPARQLEndpoint()
midi_player = MidiPlayer.MidiPlayer()
mapper = Mapper.Mapper()
gui = GUI.GUI()
sqlite = SQLite.SQLite()


def create_tables(connection):
    if connection is not None:
        sqlite.create_table(connection, sqlite.complicated_metrics)
        sqlite.create_table(connection, sqlite.metrics)
        sqlite.create_table(connection, sqlite.graph)
    else:
        print("Error! cannot create the database connection.")


def retrieve_data(uri):
    # itemQuery = sparql.distinctItemQuery %sparql.id
    # degreeQuery = sparql.metricsQuery %("ll:" + sparql.id, "/ llm:degree / llm:degree ?min ?max ?mean")
    # results = sparql.runQuery(itemQuery + degreeQuery)
    # result = sparql.getCurrentValue(results, "degree")
    # uri = "http://dbpedia.org/resource/Semantic_Web"


    metrics = Metrics.Metrics(uri)
    metrics_id = metrics.get_metrics_id()
    print(metrics_id)
    graph_id = metrics.get_graph_id()

    # TODO: replace retrieve metrics with sql query
    results = metrics.retrieve_metrics()
    return metrics_id


if __name__ == "__main__":
    connection = sqlite.create_connection(sqlite.database)
    create_tables(connection)

    uri = gui.retrieveInput()
    earconType = gui.retrieveEarconType()
    motive_order = gui.retrieveMotiveOrder()

    metric_id = retrieve_data(uri)

    # degree = sparql.runSelectQuery(sparql.degreeQuery %("degree", "degree"))
    # indegree = sparql.runSelectQuery(sparql.degreeQuery %("inDegree", "inDegree"))
    # outdegree = sparql.runSelectQuery(sparql.degreeQuery %("outDegree", "outDegree"))

    mapped_values = []
    for metric_name in motive_order:
        mapped_value = {}
        if re.match(r'^1', earconType):
            # 1. Frequency
            mapped_value["frequency"] = mapper.map(metric_id, metric_name, mapper.scale_range)
            mapped_value["duration"] = None
        elif re.match(r'^2', earconType):
            # 2. Length
            # TODO: change frequencies to durations
            mapped_value["duration"] = mapper.map(metric_id, metric_name, mapper.duration_range)
            mapped_value["frequency"] = None
        elif re.match(r'^3', earconType):
            # 3. Frequency + Length
            mapped_value["frequency"] = mapper.map(metric_id, metric_name, mapper.scale_range)
            mapped_value["duration"] = mapper.map(metric_id, metric_name, mapper.duration_range)
        mapped_values.append(mapped_value)

    print("Mapped values:", mapped_values)

    earcon = Earcon.Earcon(mapped_values).earcon
    print("Earcon:", earcon)
    finished_playing_motive = False

    while not finished_playing_motive:
        time.sleep(1)
        midi_player.play_motive(earcon)
        finished_playing_motive = midi_player.finished_playing_motive
