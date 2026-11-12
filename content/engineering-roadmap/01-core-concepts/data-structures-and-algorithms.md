# Data Structures and Algorithms (DSA)

**Level: Intermediate** · Start with the Year 1 roadmap if these ideas are unfamiliar.

Audience: students learning programming, especially computing and software-oriented pathways
Year/level: begin in Year 1 after programming basics; develop depth in Years 2–3
Status: Draft | Independent review pending
Last updated: 10 November 2026
Reviewed by: Pending

A **data structure** organises information so a program can use it. An **algorithm** is a sequence of steps to solve a problem. DSA connects the two: choose how to store data, choose how to process it, and explain whether the solution is correct and efficient.

For a library system, book records might sit in an array, titles are strings, a waiting list needs queue behaviour, a catalogue can have a hierarchy, and connections between branches can form a graph. Different operations call for different choices.

## Before you start

Learn variables, conditions, loops, functions and basic input/output in one language. Then practise collections, references where relevant, and recursion: solving a problem through smaller instances of the same problem. Every recursive solution needs a stopping condition.

Use one language consistently at first. Understand both the operations your language provides and the underlying idea. A Python list, for example, should not be assumed to have the same representation as a linked list simply because both are called lists.

## Core topics and first exercises

| Topic | What it means | Where it helps | First practice |
| --- | --- | --- | --- |
| **Arrays** | An indexed sequence; representation and resizing rules depend on the language/container | Storing readings, marks or other ordered records | Find the minimum, maximum and second-largest distinct value; handle empty and duplicate inputs |
| **Strings** | Sequences representing text | Names, search terms and input processing | Count characters, compare strings and check a palindrome; state case/space rules |
| **Linked Lists** | Nodes connected by references rather than indexed contiguous storage | Learning reference updates and insertion/removal trade-offs | Traverse, insert, delete and reverse a singly linked list |
| **Stacks** | Last in, first out | Nested expressions and undo-like processing | Check balanced brackets; handle an unmatched closing bracket |
| **Queues** | First in, first out | Waiting tasks and breadth-first traversal | Simulate a service queue and explain what happens when it is empty |
| **Hash Maps and Sets** | Key-based storage or unique-value membership | Frequency counts, lookup and duplicate detection | Count word frequencies and find repeated values |
| **Trees** | Hierarchical nodes connected without cycles; a rooted tree has parent/child relationships | Hierarchies and ordered-search structures | Traverse a binary tree and find its height; define your height convention |
| **Graphs** | Vertices connected by edges; edges may have directions or weights | Routes, dependencies and networks | Represent a graph with adjacency lists and visit reachable vertices using BFS and DFS |
| **Sorting** | Reordering items according to a comparison rule | Ranking records and preparing data for other operations | Trace insertion sort, then implement merge sort and compare the approaches |
| **Searching** | Finding an item or determining that it is absent | Record lookup and finding positions | Compare linear search with binary search on sorted data |
| **Dynamic Programming** | Reusing solutions to overlapping subproblems through stored states | Counting, optimisation and sequence problems with suitable structure | Count ways to climb steps, then solve a small minimum-coin problem with an unreachable case |

Stacks, queues, hashing and recursion support the requested tree, graph and dynamic-programming topics, so learn them along the way.

## Reason about time and space

Let `n` describe input size. **Time complexity** describes how work grows with that size; **space complexity** describes memory growth. Say whether you mean total or extra space, and distinguish worst-case from expected or amortised bounds.

| Operation or approach | Useful bound and condition |
| --- | --- |
| Access an array element by index | O(1) in the usual array model |
| Linear search | O(n) worst-case comparisons |
| Binary search | O(log n) comparisons; O(log n) time with constant-time indexed access to sorted data |
| Insert/delete in a linked list | O(1) pointer updates once the necessary node/predecessor is available; finding it may take O(n) |
| Hash-map lookup | Commonly expected O(1) under suitable hashing assumptions; not a universal worst-case guarantee |
| Binary-search-tree lookup | O(h), where h is height; balanced trees keep h logarithmic, while a skewed tree can have h proportional to n |
| Merge sort on an array | O(n log n) time and typically O(n) extra storage |
| BFS/DFS with adjacency lists | O(V + E) for a complete traversal, where V counts vertices and E edges |
| Dynamic programming | Derive the bound from the number of states and work per state; there is no single complexity for all DP problems |

A theoretical bound does not replace checking correctness or measuring your actual program. Small inputs, memory limits and implementation details also influence a choice.

## A staged learning path

1. **Arrays and strings:** traversal, frequency counting, two-pointer exercises and boundary conditions. Explain why each pointer moves.
2. **Searching and sorting:** establish preconditions, trace algorithms by hand and compare complexity. Binary search requires an appropriate sorted or monotonic structure.
3. **References and recursion:** linked lists, stacks, queues and the call stack. Draw how references change before coding a deletion.
4. **Trees and graphs:** depth-first and breadth-first traversal, visited tracking and disconnected components. BFS gives shortest paths by number of edges in unweighted graphs; weighted shortest paths need an appropriate algorithm.
5. **Dynamic programming:** start with a recursive definition, identify repeated subproblems, then use memoisation or tabulation. Explain the state before writing a table.

Begin basic arrays, strings and search in Year 1. Use Year 2 for the full sequence. Revisit trees, graphs and DP in Year 3 when your projects or intended role call for deeper practice. Move at a pace supported by your course and understanding.

## Work through dynamic programming

Suppose you can climb one or two steps at a time. Let `ways(n)` count the distinct sequences that reach step n. The final move comes from n−1 or n−2, so `ways(n) = ways(n−1) + ways(n−2)` for n ≥ 2. Choose `ways(0) = 1` and `ways(1) = 1`.

Draw the repeated calls for a small n. Memoisation stores results during recursion; tabulation builds them in order. With constant-time arithmetic, computing each state once takes O(n) time. A full table uses O(n) space; keeping only the previous two results uses O(1) extra space. Very large integer results require considering the cost of arithmetic as well.

For every DP exercise, state:

- What one state represents.
- The base cases and recurrence.
- Why the recurrence covers the valid choices.
- The evaluation order and handling of impossible states.
- Time and memory bounds.

## Practise for understanding

For each problem:

1. Restate the input, output and constraints, including units where relevant.
2. Work through a small example by hand.
3. Write a simple correct approach before optimising it.
4. Explain the data structure and why it fits the operations.
5. Implement and check normal inputs plus relevant boundary cases: empty, single item, duplicates, sorted/reversed order, missing target or disconnected vertices.
6. Compare your output with a simple reference method on small cases.
7. Record the complexity, one mistake and how you fixed it.

Avoid measuring progress only by question counts or memorised patterns. Revisit a problem later and explain the solution without looking at it.

## Connect DSA to a project

Extend a library or task-management project: use a map for identifier lookup, sorting for a report, a queue for pending requests and a graph for dependencies. Explain which structures you actually need rather than adding every structure to one project. Use tested language-library collections in application code while implementing smaller versions separately to learn their behaviour.

## Checklist

- [ ] I can explain each core topic using an example.
- [ ] I can state the preconditions of an algorithm.
- [ ] I can trace references, recursion and visited state on paper.
- [ ] I can justify a time/space bound with its assumptions.
- [ ] I can test boundary cases and explain one failure.
- [ ] I can define a DP state and recurrence before implementing it.

## Further study

[MIT OpenCourseWare: Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) provides a course starting point. Select topics based on your prerequisites; use your college’s syllabus to coordinate practice.

This chapter was added following the project owner’s request; it extends the original blueprint. Independent technical review is pending.

[Back to the roadmap](../index.md) | [Year 2 learning path](../year-2/README.md)
