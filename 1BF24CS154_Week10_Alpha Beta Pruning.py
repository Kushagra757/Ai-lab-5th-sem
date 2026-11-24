def count_leaves(node):
    if isinstance(node, (int, float)):
        return 1
    return sum(count_leaves(child) for child in node)


def alpha_beta(node, alpha, beta, is_max, path="Root"):
    
    global visited, pruned

    # Leaf node
    if isinstance(node, (int, float)):
        visited += 1
        print("Visited:", path, "=", node)
        return node

    if is_max:
        value = float('-inf')

        for i, child in enumerate(node):

            value = max(
                value,
                alpha_beta(child, alpha, beta, False,
                           path + "." + str(i+1))
            )

            alpha = max(alpha, value)

            # Alpha-Beta cutoff
            if alpha >= beta:

                remaining = node[i+1:]

                if remaining:
                    skipped = sum(count_leaves(x) for x in remaining)
                    pruned += skipped

                    print("Pruned at:", path)
                    print("Skipped leaf nodes:", skipped)

                break

        return value

    else:
        value = float('inf')

        for i, child in enumerate(node):

            value = min(
                value,
                alpha_beta(child, alpha, beta, True,
                           path + "." + str(i+1))
            )

            beta = min(beta, value)

            # Alpha-Beta cutoff
            if alpha >= beta:

                remaining = node[i+1:]

                if remaining:
                    skipped = sum(count_leaves(x) for x in remaining)
                    pruned += skipped

                    print("Pruned at:", path)
                    print("Skipped leaf nodes:", skipped)

                break

        return value


# MAIN PROGRAM

print("ALPHA-BETA PRUNING")

tree = eval(input("\nEnter game tree: "))

def validate(node):
    if isinstance(node, (int, float)) and not isinstance(node, bool):
        return

    if isinstance(node, list) and len(node) > 0:
        for child in node:
            validate(child)
        return

    raise ValueError("Invalid game tree")


validate(tree)

root = input("Enter root (MAX/MIN): ").upper()

if root not in ("MAX", "MIN"):
    raise ValueError("Enter MAX or MIN")

visited = 0
pruned = 0

print("\n--- SEARCH PROCESS ---")

result = alpha_beta(
    tree,
    float('-inf'),
    float('inf'),
    root == "MAX"
)

print("\n--- FINAL RESULT ---")
print("Optimal Value:", result)
print("Visited Leaf Nodes:", visited)
print("Pruned Leaf Nodes:", pruned)
print("Total Leaf Nodes:", visited + pruned)
