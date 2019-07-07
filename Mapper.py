import re
import Metrics
import SQLite

class Mapper(object):
    degrees = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    durations = [0.0625, 0.125, 0.1875, 0.25, 0.375, 0.5, 0.75, 1]
    octave = {"min": 1, "max": 9}
    degree = {"min": 0, "max": len(degrees)}
    scale_range = {"min": 0, "max": 7}  # each octave has 8 notes
    duration_range = {"min": 0, "max": len(durations) - 1}

    def __init__(self):
        self.sqlite = SQLite.SQLite()
        self.connection = self.sqlite.create_connection(self.sqlite.database)

        self.degree = self.map_degree()
        self.octave = self.map_octave()
        self.type = self.map_type()

    @staticmethod
    def map_calculation(value, min_metric, max_metric, min_property, max_property):
        if max_metric == min_metric:
            return int(round(max_property/2))

        mapped_value = (value - min_metric) / (max_metric - min_metric)
        mapped_value = mapped_value * (max_property - min_property) + min_property
        return int(round(mapped_value))

    def map_degree(self):
        degree = "C"
        index_of_degree = self.degrees.index(degree)
        return index_of_degree

    @staticmethod
    def map_octave():
        return 5  # between 1 and 9

    @staticmethod
    def map_type():
        return 0  # 0 or 1

    def get_metrics_collection(self, key):
        graphs = self.sqlite.select_all_graphs(self.connection)
        metrics_collection = []

        for graph in graphs:
            metrics = self.sqlite.select_metrics_by_id(self.connection, graphs[graph]["metrics"])
            metrics_collection.append(metrics[key])

        return metrics_collection

    def get_complicated_metrics_collection(self, metrics, key):
        complicated_metrics_collection = []

        for metric in metrics:
            complicated_metrics = self.sqlite.select_complicated_metrics_by_id(self.connection, metric)
            complicated_metrics_collection.append(complicated_metrics[key])

        return complicated_metrics_collection

    def map(self, metric_id, metric_name, properties):
        # Retrieve the metrics for the current graph
        metrics = self.sqlite.select_metrics_by_id(self.connection, metric_id)

        # Get the current metric of the motive
        metric_keys = metric_name.split()
        metric = metrics[metric_keys[0]]

        # Retrieve metrics for all graphs
        metrics_collection = self.get_metrics_collection(metric_keys[0])

        if len(metric_keys) == 2:  # if the length is 2, then the metric consists of a complicated metric
            complicated_metrics = self.sqlite.select_complicated_metrics_by_id(self.connection, metric)
            metric = complicated_metrics[metric_keys[1]]
            metrics_collection = self.get_complicated_metrics_collection(metrics_collection, metric_keys[1])

        result = self.map_calculation(metric,
                                      min(metrics_collection),
                                      max(metrics_collection),
                                      properties["min"],
                                      properties["max"])

        return result
