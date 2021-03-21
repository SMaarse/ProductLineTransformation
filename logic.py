
from sympy.logic.boolalg import to_cnf
from sympy import symbols
from sympy.logic.inference import satisfiable
from sympy import true as sTrue

def trueG():
    return sTrue

def falseG():
    return ~sTrue

def andG(a, b):
    return {
        "gate": "and",
        "a": a,
        "b": b,
    }

def orG(a, b):
    return {
        "gate": "or",
        "a": a,
        "b": b,
    }

def notG(a):
    return {
        "gate": "not",
        "a": a,
    }

def implG(a, b):
    return {
        "gate": "imply",
        "a": a,
        "b": b,
    }

def replaceVar(expr, old, new):
    if isinstance(expr, str):
        if expr == old:
            return new
        return expr
    if expr["gate"] == "and":
        return andG(replaceVar(expr["a"], old, new), replaceVar(expr["b"], old, new))
    if expr["gate"] == "or":
        return orG(replaceVar(expr["a"], old, new), replaceVar(expr["b"], old, new))
    if expr["gate"] == "not":
        return notG(replaceVar(expr["a"], old, new))
    if expr["gate"] == "imply":
        return implG(replaceVar(expr["a"], old, new), replaceVar(expr["b"], old, new))

def getVars(expr):
    if isinstance(expr, str):
        if len(expr) == 0:
            return []
        return [expr]
    if expr["gate"] == "and":
        return list(dict.fromkeys(getVars(expr["a"]) + getVars(expr["b"])))
    if expr["gate"] == "or":
        return list(dict.fromkeys(getVars(expr["a"]) + getVars(expr["b"])))
    if expr["gate"] == "not":
        return getVars(expr["a"])
    if expr["gate"] == "imply":
        return list(dict.fromkeys(getVars(expr["a"]) + getVars(expr["b"])))

def buildExpr(expr, symbolOf):
    if isinstance(expr, str):
        if len(expr) == 0:
            return sTrue
        return symbolOf[expr]
    if expr["gate"] == "and":
        return buildExpr(expr["a"], symbolOf) & buildExpr(expr["b"], symbolOf)
    if expr["gate"] == "or":
        return buildExpr(expr["a"], symbolOf) | buildExpr(expr["b"], symbolOf)
    if expr["gate"] == "not":
        return ~buildExpr(expr["a"], symbolOf)
    if expr["gate"] == "imply":
        return buildExpr(expr["a"], symbolOf) >> buildExpr(expr["b"], symbolOf)

def expressionToString(expr):
    if isinstance(expr, str):
        return expr

    vars = getVars(expr) # a list of all variables used as strings
    if len(vars) == 0:
        return ""
    symbs = symbols(" ".join(vars)) # variables converted to sympy symbols
    if not isinstance(symbs, tuple): # if only one result is returned, make sure it is still in a list format
        symbs = [symbs]

    symbolOf = {}
    for varNr in range(len(vars)): # generate a mapping from string variables to sympy symbols
        symbolOf[vars[varNr]] = symbs[varNr]

    newexpr = buildExpr(expr, symbolOf) # build sympy expression using the expression and the symbol mapping
    return str(newexpr)

def isSAT(expr):
    vars = getVars(expr) # a list of all variables used as strings
    symbs = symbols(" ".join(vars)) # variables converted to sympy symbols
    if not isinstance(symbs, tuple): # if only one result is returned, make sure it is still in a list format
        symbs = [symbs]

    symbolOf = {}
    for varNr in range(len(vars)): # generate a mapping from string variables to sympy symbols
        symbolOf[vars[varNr]] = symbs[varNr]

    newexpr = buildExpr(expr, symbolOf) # build sympy expression using the expression and the symbol mapping
    cnf = to_cnf(newexpr) # convert the expression to cnf

    return satisfiable(cnf) != False # return whether or not the expression is satisfiable
