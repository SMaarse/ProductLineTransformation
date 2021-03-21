
import productline as pl
import logic

name = "Removing Cancel Feature"

feature_model = {
    "features": [
        "Wash",
        "Heat",
        "Delay",
        "Dry",
        "Cancel",
    ],
    "Phi": [
        "Wash",
        logic.implG("Delay", logic.notG("Heat")),
        logic.implG("Cancel", "Delay"),
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
        pl.Edge(source="Waiting", target="UnLocking", presence_condition=logic.andG("Cancel", logic.orG("Heat", "Delay"))),
    ],
}

product_line = pl.ProductLine(feature_model, domain_model)

applications = [
    {
        "matching_site": {
            "C": [
                {
                    "kind": "node",
                    "object": domain_model["nodes"][1], # Waiting node
                },
                {
                    "kind": "node",
                    "object": domain_model["nodes"][4] # UnLocking node
                },
            ],
            "D" : [
                {
                    "kind": "edge",
                    "object": domain_model["edges"][6], # Edge from Waiting to Unlocking
                }
            ],
            "Base": "",
        },
        "transformation_rule": {
            "name": "Rule 7: RemoveCancelWash",
            "A": [],
            "LHS": pl.ProductLine({
                    "features": [
                        "Cancel",
                    ],
                    "Phi": [
                        logic.implG("Cancel", "Delay"),
                    ],
                }, {"nodes": [], "edges": []}), # domain model is empty because it is irrelevent in this isolated execution of the algorithm
            "RHS": pl.ProductLine({
                    "features": [],
                    "Phi": [],
                }, {"nodes": [], "edges": []}), # domain model is empty because it is irrelevent in this isolated execution of the algorithm
        },
    },
]
