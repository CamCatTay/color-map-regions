COLORS = {
    1: "Red",
    2: "Blue",
    3: "Green",
    4: "Yellow",
}

ADJACENCY = {
    "AL": ["MS", "TN", "GA", "FL"],
    "AR": ["MO", "TN", "MS", "LA", "TX", "OK"],
    "AZ": ["CA", "NV", "UT", "CO", "NM"],
    "CA": ["OR", "NV", "AZ"],
    "CO": ["WY", "NE", "KS", "OK", "NM", "AZ", "UT"],
    "CT": ["NY", "MA", "RI"],
    "DE": ["MD", "PA", "NJ"],
    "FL": ["GA", "AL"],
    "GA": ["FL", "AL", "TN", "NC", "SC"],
    "IA": ["MN", "WI", "IL", "MO", "NE", "SD"],
    "ID": ["MT", "WY", "UT", "NV", "OR", "WA"],
    "IL": ["WI", "IN", "KY", "MO", "IA"],
    "IN": ["MI", "OH", "KY", "IL"],
    "KS": ["NE", "MO", "OK", "CO"],
    "KY": ["OH", "WV", "VA", "TN", "MO", "IL", "IN"],
    "LA": ["TX", "AR", "MS"],
    "MA": ["NY", "CT", "RI", "NH", "VT"],
    "MD": ["VA", "WV", "PA", "DE"],
    "ME": ["NH"],
    "MI": ["OH", "IN", "WI"],
    "MN": ["WI", "IA", "SD", "ND"],
    "MO": ["IA", "IL", "KY", "TN", "AR", "OK", "KS", "NE"],
    "MS": ["LA", "AR", "TN", "AL"],
    "MT": ["ID", "WY", "SD", "ND"],
    "NC": ["VA", "TN", "GA", "SC"],
    "ND": ["MN", "SD", "MT"],
    "NE": ["SD", "IA", "MO", "KS", "CO", "WY"],
    "NH": ["ME", "MA", "VT"],
    "NJ": ["NY", "PA", "DE"],
    "NM": ["CO", "OK", "TX", "AZ", "UT"],
    "NV": ["CA", "OR", "ID", "UT", "AZ"],
    "NY": ["PA", "NJ", "CT", "MA", "VT"],
    "OH": ["PA", "WV", "KY", "IN", "MI"],
    "OK": ["KS", "MO", "AR", "TX", "NM", "CO"],
    "OR": ["WA", "ID", "NV", "CA"],
    "PA": ["NY", "NJ", "DE", "MD", "WV", "OH"],
    "RI": ["CT", "MA"],
    "SC": ["NC", "GA"],
    "SD": ["ND", "MN", "IA", "NE", "WY", "MT"],
    "TN": ["KY", "VA", "NC", "GA", "AL", "MS", "AR", "MO"],
    "TX": ["NM", "OK", "AR", "LA"],
    "UT": ["ID", "WY", "CO", "NM", "AZ", "NV"],
    "VA": ["MD", "WV", "KY", "TN", "NC"],
    "VT": ["NY", "MA", "NH"],
    "WA": ["OR", "ID"],
    "WI": ["MN", "MI", "IL", "IA"],
    "WV": ["OH", "PA", "MD", "VA", "KY"],
    "WY": ["MT", "SD", "NE", "CO", "UT", "ID"],
}

STATE_NAMES = {
    "AL": "Alabama",       "AR": "Arkansas",      "AZ": "Arizona",
    "CA": "California",    "CO": "Colorado",      "CT": "Connecticut",
    "DE": "Delaware",      "FL": "Florida",       "GA": "Georgia",
    "IA": "Iowa",          "ID": "Idaho",         "IL": "Illinois",
    "IN": "Indiana",       "KS": "Kansas",        "KY": "Kentucky",
    "LA": "Louisiana",     "MA": "Massachusetts", "MD": "Maryland",
    "ME": "Maine",         "MI": "Michigan",      "MN": "Minnesota",
    "MO": "Missouri",      "MS": "Mississippi",   "MT": "Montana",
    "NC": "North Carolina","ND": "North Dakota",  "NE": "Nebraska",
    "NH": "New Hampshire", "NJ": "New Jersey",    "NM": "New Mexico",
    "NV": "Nevada",        "NY": "New York",      "OH": "Ohio",
    "OK": "Oklahoma",      "OR": "Oregon",        "PA": "Pennsylvania",
    "RI": "Rhode Island",  "SC": "South Carolina","SD": "South Dakota",
    "TN": "Tennessee",     "TX": "Texas",         "UT": "Utah",
    "VA": "Virginia",      "VT": "Vermont",       "WA": "Washington",
    "WI": "Wisconsin",     "WV": "West Virginia", "WY": "Wyoming",
}

# Smallest-Last Greedy graph coloring algorithm.
def greedy_color(adjacency: dict):

    # Order
    # Give states degree counts so when a vertex is removed it's neighbors lose a connection
    degrees = {s: len(neighbors) for s, neighbors in adjacency.items()}
    remaining = set(adjacency.keys())
    removal_stack = []

    while remaining:
        # Pick the remaining vertex with the smallest current degree
        vertex = min(remaining, key=lambda s: (degrees[s], s))
        removal_stack.append(vertex)
        remaining.remove(vertex)
        # Decrement the degree of its still seen in neighbors
        for neighbor in adjacency[vertex]:
            if neighbor in remaining:
                degrees[neighbor] -= 1

    # Color in reverse removal order
    ordered_states = reversed(removal_stack)

    # Color
    color_assignment = {}

    for state in ordered_states:
        neighbor_colors = {
            color_assignment[neighbor]
            for neighbor in adjacency[state]
            if neighbor in color_assignment
        }

        for color in range(1, len(COLORS) + 1):
            if color not in neighbor_colors:
                color_assignment[state] = color
                break
        else:
            raise RuntimeError(f"Could not assign a color to {state}")

    return color_assignment

# Brute force check all states to see if any of it's neighbors have the same color as it
def validate_coloring(adjacency: dict, color_assignment: dict):
    for state, neighbors in adjacency.items():
        for neighbor in neighbors:
            if color_assignment.get(state) == color_assignment.get(neighbor):
                return False
    return True

# Print a table containing information about the graph
def print_results(color_assignment: dict):
    col_w = [5, 22, 8, 10]
    separator = "+" + "+".join("-" * w for w in col_w) + "+"
    header = (
        f"| {'Abbr':^{col_w[0]-2}} "
        f"| {'State Name':^{col_w[1]-2}} "
        f"| {'Color #':^{col_w[2]-2}} "
        f"| {'Color':^{col_w[3]-2}} |"
    )

    print("\n  GRAPH COLORING WITH GREEDY ALGORITHM / SMALLEST-LAST ORDERING")
    print(separator)
    print(header)
    print(separator)

    for abbr, color_num in sorted(color_assignment.items()):
        name  = STATE_NAMES.get(abbr, abbr)
        color = COLORS[color_num]
        print(
            f"| {abbr:^{col_w[0]-2}} "
            f"| {name:<{col_w[1]-2}} "
            f"| {color_num:^{col_w[2]-2}} "
            f"| {color:<{col_w[3]-2}} |"
        )

    print(separator)


def main():
    color_assignment = greedy_color(ADJACENCY)

    print_results(color_assignment)

    # Validation
    valid = validate_coloring(ADJACENCY, color_assignment)

    print(f"\n  Total states colored : {len(color_assignment)}")
    print(f"  Coloring valid       : {'YES' if valid else 'NO'}")

if __name__ == "__main__":
    main()
