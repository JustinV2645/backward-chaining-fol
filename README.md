# Backward Chaining for First Order Logic

A small rule based inference engine demonstrating forward chaining and backward chaining, built on the MIT 6.034 Lab 4 production system framework.

## Background

Forward chaining starts from known facts and repeatedly applies rules to derive new facts, until nothing new can be derived.

Backward chaining starts from a goal, a hypothesis you want to prove, and works backward, asking what would need to be true for this to hold. It breaks the goal into sub goals recursively until it reaches known facts. Backward chaining tends to be more efficient when there are many possible conclusions but only one goal you actually care about proving.

## Files

production.py and utils.py are the rule engine, unmodified, from the assignment. Not something you need to edit.

data.py contains the test datasets, unmodified, from the assignment.

backward_chaining.py is the implementation: transitive_rule, family_rules, and backchain_to_goal_tree.

## Part 1: Transitive Rule

A single rule that derives transitive relationships. If X beats Y and Y beats Z, it derives X beats Z.

IF(AND('(?x) beats (?y)', '(?y) beats (?z)'), THEN('(?x) beats (?z)'))

Run it with forward_chain([transitive_rule()], data).

## Part 2: Family Relations

A set of rules that derive child, sibling, grandparent, grandchild, and cousin from person(X) and parent(X, Y) facts. Uses forward chaining, repeatedly applying all rules until no new facts appear.

Run it with forward_chain(family_rules(), data).

## Part 3: Backward Chaining Goal Tree

backchain_to_goal_tree(rules, hypothesis) builds an AND/OR tree showing everything that would need to be true to prove a hypothesis.

Worked example. Hypothesis: opus is a penguin.

One rule in zookeeper_rules says:

IF(AND('(?x) is a bird', '(?x) does not fly', '(?x) swims', '(?x) has black and white color'), THEN('(?x) is a penguin'))

To prove opus is a penguin, we need opus is a bird, opus does not fly, opus swims, and opus has black and white color, all at once. opus is a bird is not a raw fact either. It is provable by other rules: has feathers, has hair, or flies and lays eggs. The tree recurses one more level for that piece.

OR('opus is a penguin', AND(OR('opus is a bird', 'opus has feathers', AND('opus flies', 'opus lays eggs')), 'opus does not fly', 'opus swims', 'opus has black and white color'))

Read this as: opus is a penguin is provable either directly, if it is already a known fact, or by proving the entire AND branch underneath it.

## Running the Code

python3 backward_chaining.py

This runs all three parts and prints results, including verification that the Black family dataset produces exactly 14 cousin relationships, and that the opus is a penguin goal tree matches the expected structure.

## Try It Yourself

Open backward_chaining.py.

Add your own rule to zookeeper_rules in data.py, or write a new small rule set.

Call backchain_to_goal_tree with your rules and a hypothesis string, and see what tree it builds.

Work through the tree by hand first, then check it against the code's output.
