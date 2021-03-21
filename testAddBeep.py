
import productline as pl
import logic

name = "Adding Beep Feature"

feature_model = {
    "features": [
        "Wash",
        "Heat",
        "Delay",
        "Dry",
    ],
    "Phi": [
        "Wash",
        logic.implG("Delay", logic.notG("Heat")),
    ],
}

domain_model = {
    "nodes": [
        pl.Node(name="Locking"),
        pl.Node(name="Waiting", presence_condition=logic.orG("Heat", "Delay"), exit_actions=[
            {
                "action": "HeaterOff()",
                "presence_condition": "Heat",
            }
        ]),
        pl.Node(name="Washing", entry_actions=[
            {
                "action": "TempCheck()",
                "presence_condition": "Heat",
            }
        ]),
        pl.Node(name="Drying", presence_condition="Dry"),
        pl.Node(name="UnLocking"),
    ],
    "edges": [
        pl.Edge(source="Locking", target="Waiting",   presence_condition=logic.orG("Heat", "Delay")),
        pl.Edge(source="Waiting", target="Washing",   presence_condition=logic.orG("Heat", "Delay")),
        pl.Edge(source="Locking", target="Washing",   presence_condition=logic.notG("Heat")),
        pl.Edge(source="Washing", target="Drying",    presence_condition="Dry"),
        pl.Edge(source="Drying",  target="UnLocking", presence_condition="Dry"),
        pl.Edge(source="Washing", target="UnLocking", presence_condition=logic.notG("Dry")),
    ],
}

product_line = pl.ProductLine(feature_model, domain_model)

applications = [
    {
        "matching_site": {
            "C": [
                {
                    "kind": "node",
                    "object": domain_model["nodes"][2], # Washing node
                },
                {
                    "kind": "node",
                    "object": domain_model["nodes"][4] # UnLocking node
                },
            ],
            "D" : [
                {
                    "kind": "edge",
                    "object": domain_model["edges"][5], # Edge from Washing to Unlocking
                }
            ],
            "Base": "Wash",
        },
        "transformation_rule": {
            "name": "Rule 3: AddBeepFeature",
            "A": [
                {
                    "kind": "node",
                    "object": pl.Node(name="Beeping"),
                    "presence_condition": "Beep",
                },
                {
                    "kind": "edge",
                    "object": pl.Edge(source="Washing", target="Beeping"),
                    "presence_condition": "Beep",
                },
                {
                    "kind": "edge",
                    "object": pl.Edge(source="Beeping", target="Unlocking"),
                    "presence_condition": "Beep",
                },
                {
                    "kind": "node",
                    "object": pl.Node(name="Logging"),
                    "presence_condition": logic.notG("Beep"),
                },
                {
                    "kind": "edge",
                    "object": pl.Edge(source="Washing", target="Logging"),
                    "presence_condition": logic.notG("Beep"),
                },
                {
                    "kind": "edge",
                    "object": pl.Edge(source="Logging", target="Unlocking"),
                    "presence_condition": logic.notG("Beep"),
                },
            ],
            "LHS": pl.ProductLine({
                    "features": [
                        "Base",
                    ],
                    "Phi": [],
                }, {"nodes": [], "edges": []}), # domain model is empty because it is irrelevent in this isolated execution of the algorithm
            "RHS": pl.ProductLine({
                    "features": [
                        "Base",
                        "Beep",
                    ],
                    "Phi": [
                        logic.implG("Beep", "Base"),
                    ],
                }, {"nodes": [], "edges": []}), # domain model is empty because it is irrelevent in this isolated execution of the algorithm
        },
    },
]
