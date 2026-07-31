from production import IF, AND, OR, NOT, THEN, DELETE, forward_chain
from production import match, populate, simplify, variables, PASS, FAIL
from data import (poker_data, abc_data, minecraft_data,
                   simpsons_data, black_data,
                   sibling_test_data, grandparent_test_data,
                   zookeeper_rules, zoo_data)

# Problem 4: Transitive Rule


def transitive_rule():
    """
    A one-rule system that finds all transitive combinations of
    'beats' relationships. If X beats Y, and Y beats Z, then X beats Z.
    """
    rule = IF(
        AND('(?x) beats (?y)', '(?y) beats (?z)'),
        THEN('(?x) beats (?z)')
    )
    return rule


def family_rules():
    """
    A set of forward-chaining rules that derive sibling, child,
    cousin, grandparent, and grandchild relations from 'person (?x)'
    and 'parent (?x) (?y)' facts.
    """
    rules = [
        # Every person is their own 'self' marker, used to exclude
        # matching someone against themselves.
        IF('person (?x)',
           THEN('self (?x) (?x)')),

        # child: the reverse of parent
        IF('parent (?p) (?c)',
           THEN('child (?c) (?p)')),

        # sibling: share a parent, but aren't the same person
        IF(AND('parent (?p) (?x)',
               'parent (?p) (?y)',
               NOT('self (?x) (?y)')),
           THEN('sibling (?x) (?y)')),
 
        # grandparent: parent of a parent
        IF(AND('parent (?p) (?x)',
               'parent (?x) (?y)'),
           THEN('grandparent (?p) (?y)')),

        # grandchild: the reverse of grandparent
        IF('grandparent (?g) (?c)',
           THEN('grandchild (?c) (?g)')),
    # cousin: parents are siblings, but X and Y aren't siblings
        IF(AND('parent (?px) (?x)',
               'parent (?py) (?y)',
               'sibling (?px) (?py)',
               NOT('sibling (?x) (?y)')),
           THEN('cousin (?x) (?y)')),
    ]
    return rules


# Part 6
def _backchain_leaf(rules, expr):
    """
    Helper: recursively backchain over every leaf string in an
    already-instantiated (variable-substituted) AND/OR expression.
    """
    if isinstance(expr, str):
        return backchain_to_goal_tree(rules, expr)
    elif isinstance(expr, (AND, OR)):
        return expr.__class__(*[_backchain_leaf(rules, x) for x in expr])
    else:
        return expr


def backchain_to_goal_tree(rules, hypothesis):
    """
    Given a hypothesis (string) and a list of rules, return an
    AND/OR tree representing everything that would need to be true
    to prove the hypothesis.
    """
    goal_tree = OR(hypothesis)

    for rule in rules:
        consequent = rule.consequent()
        bindings = match(consequent, hypothesis)
        if bindings is not None:
            antecedent = rule.antecedent()
            instantiated = populate(antecedent, bindings)
            subtree = _backchain_leaf(rules, instantiated)
            goal_tree.append(subtree)

    return simplify(goal_tree)


if __name__ == "__main__":
    print("=== Problem 4: Transitive Rule ===")
    print("\nabc_data result:")
    print(forward_chain([transitive_rule()], abc_data))

    print("\npoker_data result:")
    print(forward_chain([transitive_rule()], poker_data))

    print("\nminecraft_data result:")
    print(forward_chain([transitive_rule()], minecraft_data))

    print("\n=== Part 5: Family Relations (child, sibling so far) ===")
    print("\nsibling_test_data result:")
    print(forward_chain(family_rules(), sibling_test_data, verbose=False))

    print("\ngrandparent_test_data result:")
    print(forward_chain(family_rules(), grandparent_test_data, verbose=False))
    
    print("\nsimpsons_data result:")
    print(forward_chain(family_rules(), simpsons_data, verbose=False))

    black_family_result = forward_chain(family_rules(), black_data, verbose=False)
    black_family_cousins = [r for r in black_family_result if r.startswith('cousin')]
    print(f"\nblack_data cousin relations found ({len(black_family_cousins)}, expected 14):")
    for c in black_family_cousins:
        print(f"  {c}")
    print("\n=== Part 6: Backward Chaining Goal Tree ===")
    tree = backchain_to_goal_tree(zookeeper_rules, 'opus is a penguin')
    print(tree)
