import re

# Tokenize the expression
def tokenize(expression):
    return re.findall(r'<->|->|[A-Za-z][A-Za-z0-9_]*|[~&|()]', expression)


# Parser for propositional logic
class Parser:
    def __init__(self, expression):
        self.tokens = tokenize(expression)
        self.pos = 0

    def match(self, token):
        if self.pos < len(self.tokens) and self.tokens[self.pos] == token:
            self.pos += 1
            return True
        return False

    def parse(self):
        result = self.iff()

        if self.pos != len(self.tokens):
            raise ValueError("Invalid expression")

        return result

    def iff(self):
        left = self.implies()
        while self.match('<->'):
            right = self.implies()
            left = ('<->', left, right)
        return left

    def implies(self):
        left = self.or_expr()
        if self.match('->'):
            right = self.implies()
            return ('->', left, right)
        return left

    def or_expr(self):
        left = self.and_expr()
        while self.match('|'):
            right = self.and_expr()
            left = ('|', left, right)
        return left

    def and_expr(self):
        left = self.not_expr()
        while self.match('&'):
            right = self.not_expr()
            left = ('&', left, right)
        return left

    def not_expr(self):
        if self.match('~'):
            return ('~', self.not_expr())

        if self.match('('):
            result = self.iff()
            if not self.match(')'):
                raise ValueError("Missing closing parenthesis")
            return result

        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            self.pos += 1
            return token

        raise ValueError("Invalid expression")


# Find proposition symbols
def get_symbols(expr):
    if isinstance(expr, str):
        return {expr}

    if expr[0] == '~':
        return get_symbols(expr[1])

    return get_symbols(expr[1]) | get_symbols(expr[2])


# Evaluate logical expression
def PL_TRUE(expr, model):

    if isinstance(expr, str):
        return model[expr]

    op = expr[0]

    if op == '~':
        return not PL_TRUE(expr[1], model)

    left = PL_TRUE(expr[1], model)
    right = PL_TRUE(expr[2], model)

    if op == '&':
        return left and right

    if op == '|':
        return left or right

    if op == '->':
        return (not left) or right

    if op == '<->':
        return left == right


# TT-CHECK-ALL algorithm
def TT_CHECK_ALL(KB, alpha, symbols, model):

    if not symbols:
        if PL_TRUE(KB, model):
            return PL_TRUE(alpha, model)
        else:
            return True

    P = symbols[0]
    rest = symbols[1:]

    return (
        TT_CHECK_ALL(KB, alpha, rest,
                     {**model, P: True})
        and
        TT_CHECK_ALL(KB, alpha, rest,
                     {**model, P: False})
    )


# TT-ENTAILS algorithm
def TT_ENTAILS(KB, alpha):

    kb = Parser(KB).parse()
    query = Parser(alpha).parse()

    symbols = list(get_symbols(kb) | get_symbols(query))

    return TT_CHECK_ALL(kb, query, symbols, {})


# Main program
print("PROPOSITIONAL LOGIC - TRUTH TABLE ENUMERATION")

KB = input("Enter Knowledge Base (KB): ")
alpha = input("Enter Query (alpha): ")

try:
    result = TT_ENTAILS(KB, alpha)

    if result:
        print("\nKB entails the Query (TRUE)")
    else:
        print("\nKB does not entail the Query (FALSE)")

except (ValueError, IndexError) as e:
    print("Invalid logical expression:", e)
