
import logic

class Node:
    def __init__(self, name="unnamed", presence_condition="", entry_actions=[], exit_actions=[]):
        self.name = name
        self.presence_condition = presence_condition
        self.entry_actions = entry_actions
        self.exit_actions = exit_actions
    def __str__(self):
        return "NODE {}: {}".format(self.name, logic.expressionToString(self.presence_condition))

class Edge:
    def __init__(self, source="", target="", presence_condition=""):
        if len(source) <= 0 or len(target) <= 0:
            raise Exception("Edge source and target nodes must be strings of length > 0")
        self.source = source
        self.target = target
        self.presence_condition = presence_condition
    def __str__(self):
        return "EDGE {} -> {}: {}".format(self.source, self.target, logic.expressionToString(self.presence_condition))

class ProductLine:

    def __init__(self, feature_model, domain_model):
        self.feature_model = feature_model
        self.domain_model = domain_model

    def __str__(self):
        str = "Features: " + ", ".join(self.feature_model["features"])
        str += "\nPhi: " + logic.expressionToString(self.getPhi())

        str += "\nNodes: ({})".format(len(self.domain_model["nodes"]))
        for node in self.domain_model["nodes"]:
            str += "\n\t{}".format(node)
        str += "\nEdges: ({})".format(len(self.domain_model["edges"]))
        for edge in self.domain_model["edges"]:
            str += "\n\t{}".format(edge)

        return str

    def getPhi(self):
        expr = ""
        for condition in self.feature_model["Phi"]:
            expr = logic.andG(expr, condition)
        return expr

    def addToDomainModel(self, new):
        if new["kind"] == "node":
            self.domain_model["nodes"].append(new["object"])
        elif new["kind"] == "edge":
            self.domain_model["edges"].append(new["object"])

    def removeFromDomainModel(self, deleted):
        if deleted["kind"] == "node":
            self.domain_model["nodes"].remove(deleted["object"])
        elif deleted["kind"] == "edge":
            self.domain_model["edges"].remove(deleted["object"])

    def addFeatureToFeatureModel(self, new):
        self.feature_model["features"].append(new)

    def removeFeatureFromFeatureModel(self, deleted):
        self.feature_model["features"].remove(deleted)

    def setPCOnElement(self, element, pc):
        if element["kind"] == "node":
            for node in self.domain_model["nodes"]:
                if node == element["object"]:
                    element["object"].presence_condition = pc
                    node = element["object"]
                    break
        elif element["kind"] == "edge":
            for edge in self.domain_model["edges"]:
                if edge == element["object"]:
                    element["object"]["presence_condition"] = pc
                    edge = element["object"]
                    break

    def addConstraintToFeatureModel(self, new):
        self.feature_model["Phi"].append(new)

    def removeConstraintFromFeatureModel(self, deleted):
        self.feature_model["Phi"].remove(deleted)
