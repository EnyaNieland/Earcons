import rdflib
import SQLite


class Metrics(object):

    def __init__(self, link):
        self.sqlite = SQLite.SQLite()
        self.connection = self.sqlite.create_connection(self.sqlite.database)

        graph = self.retrieve_dataset(link)
        nodes = self.get_number_of_nodes(graph)
        in_degree_id = self.get_in_degree(graph)
        out_degree_id = self.get_out_degree(graph)

        metrics = (nodes, in_degree_id, out_degree_id)
        self.metrics_id = self.sqlite.create_metrics(self.connection, metrics)

        cursor = self.connection.cursor()
        cursor.execute("SELECT rowid FROM graph WHERE uri = ?", (link,))
        data = cursor.fetchone()

        if data is None:
            graph_data = (link, self.metrics_id)
            self.graph_id = self.sqlite.create_graph(self.connection, graph_data)
        else:
            graph_data = (link, self.metrics_id, data[0])
            self.sqlite.update_graph(self.connection, graph_data)
            self.graph_id = data[0]

        self.connection.commit()

    def retrieve_dataset(self, link):
        graph = rdflib.Graph()
        graph.load(link)

        return graph

    def get_number_of_nodes(self, data):
        return len(data.all_nodes())

    def get_in_degree(self, data):
        amount = len(list(data.objects()))
        total = 0
        min = 1000000
        max = 0

        for object in data.objects():
            connection = data.subject_predicates(object)
            in_degree = len(list(connection))
            total += in_degree

            if in_degree < min:
                min = in_degree

            if in_degree > max:
                max = in_degree

        mean = total / amount

        in_degree_metrics = (min, max, mean)
        return self.sqlite.create_complicated_metrics(self.connection, in_degree_metrics)

    def get_out_degree(self, data):
        amount = len(list(data.subjects()))
        total = 0
        min = 1000000
        max = 0

        for subject in data.subjects():
            connection = data.predicate_objects(subject)
            out_degree = len(list(connection))
            total += out_degree

            if out_degree < min:
                min = out_degree

            if out_degree > max:
                max = out_degree

        mean = total / amount

        out_degree_metrics = (min, max, mean)
        return self.sqlite.create_complicated_metrics(self.connection, out_degree_metrics)

    def get_graph_id(self):
        return self.graph_id

    def get_metrics_id(self):
        return self.metrics_id

    @staticmethod
    def retrieve_metrics():
        # return {"nodes": nodes, "indegree": inDegree, "outdegree": outDegree}
        return {"min": 1, "max": 77, "value": [1, 77, 50]}

