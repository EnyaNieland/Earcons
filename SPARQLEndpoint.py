from SPARQLWrapper import SPARQLWrapper, JSON

class SPARQLEndpoint(object):
    # contains all prefixes that are used in any query
    id = "eb179d48fe507185aba44611dace610c"

    prefixes = """
        PREFIX ll:  <http://lodlaundromat.org/resource/>
        PREFIX llo: <http://lodlaundromat.org/ontology/>
        PREFIX llm: <http://lodlaundromat.org/metrics/ontology/>
    """

    # query is placeholder for queries that need to be placed in between the select
    selectQuery = """
        SELECT * WHERE {
            [query]
        } LIMIT 1000
    """

    exampleQuery = """
        SELECT * WHERE {
            ll:eb179d48fe507185aba44611dace610c llo:url ?item .
            ll:eb179d48fe507185aba44611dace610c llm:metrics llm:degree .
        } LIMIT 1000
    """

    # %s is the placeholder for the id of the requested item
    distinctItemQuery = "ll:%s llo:url ?item ."

    # example: ll:85d5a476b56fde200e770cefa0e5033c llm:metrics /llm:degree /llm:mean ?degree .
    metricsQuery = "%s llm:metrics %s ."

    def __init__(self):
        a = 0

    def runQuery(self, query):
        sparql = SPARQLWrapper("http://lodlaundromat.org/sparql")
        sparql.setQuery("""
            PREFIX ll:  <http://lodlaundromat.org/resource/>
            PREFIX llo: <http://lodlaundromat.org/ontology/>
            PREFIX llm: <http://lodlaundromat.org/metrics/ontology/>
            
            SELECT * WHERE {
                ll:eb179d48fe507185aba44611dace610c llo:url ?item .
                ll:eb179d48fe507185aba44611dace610c llm:metrics llm:degree .
            } LIMIT 1000
        """)

        # self.createQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()

    def createQuery(self, query):
        script = self.prefixes + self.selectQuery
        script = script.replace("[query]", query)
        return script

    def getCurrentValue(self, results, label):
        value = 0
        for result in results["results"]["bindings"]:
            value = int(result[label]["value"])
        print(label, ":", value)
        return value

    def analyzeData(self, results, label):
        min = 100000000
        max = 0

        for result in results["results"]["bindings"]:
            value = int(float(result[label]["value"]))
            if value < min:
                min = value
            if value > max:
                max = value

        print("min:", min, "max:", max)
        return [min, max]

    def staticData(self):
        return {"min": 1, "max": 77, "value": [1, 77, 50]}
