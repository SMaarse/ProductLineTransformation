
import productline as pl
import logic

name = "Removing Beep Feature"

feature_model = {
    "features": [
        "Wash",
        "Heat",
        "Delay",
        "Dry",
        "Beep",
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
        pl.Node(name="Beeping", presence_condition=logic.andG(logic.notG("Dry"), "Beep")),
        pl.Node(name="Logging", presence_condition=logic.andG(logic.notG("Dry"), logic.notG("Beep"))),
    ],
    "edges": [
        pl.Edge(source="Locking", target="Waiting",   presence_condition=logic.orG("Heat", "Delay")),
        pl.Edge(source="Waiting", target="Washing",   presence_condition=logic.orG("Heat", "Delay")),
        pl.Edge(source="Locking", target="Washing",   presence_condition=logic.notG("Heat")),
        pl.Edge(source="Washing", target="Drying",    presence_condition="Dry"),
        pl.Edge(source="Drying",  target="UnLocking", presence_condition="Dry"),
        pl.Edge(source="Washing", target="Beeping",   presence_condition=logic.andG(logic.notG("Dry"), "Beep")),
        pl.Edge(source="Beeping", target="UnLocking", presence_condition=logic.andG(logic.notG("Dry"), "Beep")),
        pl.Edge(source="Washing", target="Logging",   presence_condition=logic.andG(logic.notG("Dry"), logic.notG("Beep"))),
        pl.Edge(source="Logging", target="UnLocking", presence_condition=logic.andG(logic.notG("Dry"), logic.notG("Beep"))),
    ],
}

product_line = pl.ProductLine(feature_model, domain_model)

applications = [
    {
        "matching_site": {
            "C": [
                {
                    "kind": "node",
                    "object": domain_model["nodes"][2] # Washing node
                },
                {
                    "kind": "node",
                    "object": domain_model["nodes"][4] # UnLocking node
                },
            ],
            "D" : [
                {
                    "kind": "edge",
                    "object": domain_model["edges"][5], # Edge from Washing to Beeping
                },
                {
                    "kind": "edge",
                    "object": domain_model["edges"][6], # Edge from Beeping to Unlocking
                },
                {
                    "kind": "node",
                    "object": domain_model["nodes"][5], # Beeping
                },
            ],
        },
        "transformation_rule": {
            "name": "Rule 4: RemoveBeeping",
            "A": [],
            "LHS": pl.ProductLine({
                    "features": [],
                    "Phi": [],
                }, {"nodes": [], "edges": []}), # domain model is empty because it is irrelevent in this isolated execution of the algorithm
            "RHS": pl.ProductLine({
                    "features": [],
                    "Phi": [],
                }, {"nodes": [], "edges": []}), # domain model is empty because it is irrelevent in this isolated execution of the algorithm
        },
    },
    {
        "matching_site": {
            "C": [
                {
                    "kind": "node",
                    "object": domain_model["nodes"][2] # Washing node
                },
                {
                    "kind": "node",
                    "object": domain_model["nodes"][4] # UnLocking node
                },
            ],
            "D" : [
                {
                    "kind": "edge",
                    "object": domain_model["edges"][7], # Edge from Washing to Logging
                },
                {
                    "kind": "edge",
                    "object": domain_model["edges"][8], # Edge from Logging to Unlocking
                },
                {
                    "kind": "node",
                    "object": domain_model["nodes"][6], # Logging
                },
            ],
        },
        "transformation_rule": {
            "name": "Rule 5: RemoveLogging",
            "A": [],
            "LHS": pl.ProductLine({
                    "features": [],
                    "Phi": [],
                }, {"nodes": [], "edges": []}), # domain model is empty because it is irrelevent in this isolated execution of the algorithm
            "RHS": pl.ProductLine({
                    "features": [],
                    "Phi": [],
                }, {"nodes": [], "edges": []}), # domain model is empty because it is irrelevent in this isolated execution of the algorithm
        },
    },
    {
        "matching_site": {
            "C": [
                {
                    "kind": "node",
                    "object": domain_model["nodes"][2] # Washing node
                },
                {
                    "kind": "node",
                    "object": domain_model["nodes"][4] # UnLocking node
                },
            ],
            "D" : [],
        },
        "transformation_rule": {
            "name": "Rule 6: RestoreFinishWashing",
            "A": [
                {
                    "kind": "edge",
                    "object": pl.Edge(source="Washing", target="UnLocking"),
                },
            ],
            "LHS": pl.ProductLine({
                    "features": [
                        "Beep",
                    ],
                    "Phi": [],
                }, {"nodes": [], "edges": []}), # domain model is empty because it is irrelevent in this isolated execution of the algorithm
            "RHS": pl.ProductLine({
                    "features": [],
                    "Phi": [],
                }, {"nodes": [], "edges": []}), # domain model is empty because it is irrelevent in this isolated execution of the algorithm
        },
    },
]
