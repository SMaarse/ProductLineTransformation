
import logic
import testAddBeep, testRemoveBeep, testRemoveCancelWash

def applyRule(prod_line, rule, match):
    new_prod_line = prod_line

    # Phi_apply
    applyCondition = ""
    for preserved in match["C"]:
        applyCondition = logic.andG(applyCondition, preserved["object"].presence_condition)
    for deleted in match["D"]:
        applyCondition = logic.andG(applyCondition, deleted["object"].presence_condition)

    if logic.isSAT(logic.andG(prod_line.getPhi(), applyCondition)):
        # Add new features
        for feature_rhs in rule["RHS"].feature_model["features"]:
            if not feature_rhs in rule["LHS"].feature_model["features"]:
                print("Adding to feature model: FEATURE {}".format(feature_rhs))
                new_prod_line.addFeatureToFeatureModel(feature_rhs)
        # Add new constraints
        for constraint_rhs in rule["RHS"].feature_model["Phi"]:
            if not constraint_rhs in rule["LHS"].feature_model["Phi"]:
                new_constraint = logic.replaceVar(constraint_rhs, "Base", match["Base"])
                print("Adding to feature model: CONSTRAINT {}".format(logic.expressionToString(new_constraint)))
                new_prod_line.addConstraintToFeatureModel(new_constraint)

        # Remove features
        for feature_lhs in rule["LHS"].feature_model["features"]:
            if not feature_lhs in rule["RHS"].feature_model["features"]:
                print("Removing from feature model: FEATURE {}".format(feature_lhs))
                new_prod_line.removeFeatureFromFeatureModel(feature_lhs)
        # Remove constraints
        for constraint_lhs in rule["LHS"].feature_model["Phi"]:
            if not constraint_lhs in rule["RHS"].feature_model["Phi"]:
                print("Removing from feature model: CONSTRAINT {}".format(logic.expressionToString(constraint_lhs)))
                new_prod_line.removeConstraintFromFeatureModel(constraint_lhs)

        # Add new elements
        for a in rule["A"]:
            new_element = a
            # Check if the PC is not empty:
            if "presence_condition" in new_element and len(new_element["presence_condition"]) > 0:
                new_element["object"].presence_condition = logic.andG(applyCondition, new_element["presence_condition"])
            else: # If PC is empty, set the PC to applyCondition
                new_element["object"].presence_condition = applyCondition
            new_prod_line.addToDomainModel(new_element)
            print("Adding to domain model: {}".format(new_element["object"]))

        # Change PCs of preserved elements
        for c in match["C"]:
            # Check if the PC is not empty:
            if "presence_condition" in c and len(c["presence_condition"]) > 0:
                new_prod_line.setPCOnElement(c, logic.andG(c["object"].presence_condition, c["presence_condition"]))
                print("Updating PC in domain model: {}".format(c["object"]))

        # Remove elements
        for d in match["D"]:
            d["object"].presence_condition = logic.andG(d["object"].presence_condition, logic.notG(applyCondition))
            if not logic.isSAT(logic.andG(prod_line.getPhi(), d["object"].presence_condition)):
                new_prod_line.removeFromDomainModel(d)
                print("Removing from domain model: {}".format(deleted["object"]))
            else:
                print("Updating presence condition: {}".format(d["object"]))

    return new_prod_line

def performTest(test):
    print("Performing test: " + test.name)
    product_line = test.product_line
    print("\nProduct line:\n{}\n".format(product_line))

    for application in test.applications:
        print("Changes made by {}:".format(application["transformation_rule"]["name"]))
        product_line = applyRule(product_line, application["transformation_rule"], application["matching_site"])

        print("\nModified product line:\n{}\n".format(product_line))

if __name__ == "__main__":
    tests = [
        testAddBeep,
        testRemoveBeep,
        testRemoveCancelWash,
    ]

    print("Available tests:")
    for i in range(len(tests)):
        print("{} - {}".format(i+1, tests[i].name))
    print("\nSelect: ", end="")
    selection = int(input())-1

    performTest(tests[selection])
