class Var:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "?" + self.name


# Parse FOL expressions
def parse(expr):
    import re

    tokens = re.findall(r'\?[a-zA-Z_]\w*|[a-zA-Z_]\w*|[(),]', expr)
    pos = [0]

    def read():
        token = tokens[pos[0]]
        pos[0] += 1

        if token.startswith("?"):
            return Var(token[1:])

        if pos[0] < len(tokens) and tokens[pos[0]] == "(":
            pos[0] += 1
            args = []

            while tokens[pos[0]] != ")":
                args.append(read())

                if tokens[pos[0]] == ",":
                    pos[0] += 1

            pos[0] += 1
            return (token, args)

        return token

    return read()


# Apply substitutions
def apply(term, subst):
    if isinstance(term, Var):
        if term in subst:
            return apply(subst[term], subst)
        return term

    if isinstance(term, tuple):
        return (term[0], [apply(x, subst) for x in term[1]])

    return term


# Occurs check
def occurs(var, term, subst):
    term = apply(term, subst)

    if var == term:
        return True

    if isinstance(term, tuple):
        return any(occurs(var, x, subst) for x in term[1])

    return False


# Unification algorithm
def unify(x, y, subst=None):

    if subst is None:
        subst = {}

    x = apply(x, subst)
    y = apply(y, subst)

    if x == y:
        return subst

    if isinstance(x, Var):
        if occurs(x, y, subst):
            return None
        subst[x] = y
        return subst

    if isinstance(y, Var):
        if occurs(y, x, subst):
            return None
        subst[y] = x
        return subst

    if isinstance(x, tuple) and isinstance(y, tuple):

        if x[0] != y[0] or len(x[1]) != len(y[1]):
            return None

        for a, b in zip(x[1], y[1]):
            subst = unify(a, b, subst)

            if subst is None:
                return None

        return subst

    return None


# Display the MGU
def solve(expr1, expr2):

    x = parse(expr1)
    y = parse(expr2)

    result = unify(x, y)

    print("\nExpression 1:", expr1)
    print("Expression 2:", expr2)

    if result is None:
        print("No Unifier Exists!")
    else:
        print("Unification Successful!")
        print("MGU:")

        for var in result:
            print(var, "=", apply(result[var], result))


# Test expressions
solve("P(f(a), g(?y))", "P(?X, ?X)")

solve("Q(a, g(?x,a), f(?y))",
      "Q(a, g(f(b),a), ?x)")

solve("P(b, ?x, f(g(?z)))",
      "P(?z, f(?y), f(?y))")

solve("Knows(Father(?y), ?y)",
      "Knows(?x, ?x)")
