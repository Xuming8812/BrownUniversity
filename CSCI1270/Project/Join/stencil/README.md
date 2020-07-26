BannerID:B01532164

#Question1:

For Nested loop join:
Business joining review requires 57285 block accesses, while review joining user requires 83750 block accesses.
For Block Nested Loop join:
Business joining review requires 28724 block accesses, while review joining user requires 41917 block accesses.

Let r be the outer relation and s be inner relation. The cost of Block Nested Loop join is br*bs+br, while the cost of Nested Loop join is nr*bs+br. We can assume that one block can store multiple tuples. This is the reason why Block Nested Loop Join requires less block accesses.

#Question2:
Using the following sql query to test the difference between HeuristicQueryPlanner and SelectQueryPlanner

select id, name, stars from business join review on bid = id where stars = 3

By using HeuristicQueryPlanner, the planer chooses Nested Loop Join algorithm and the number of block accesses is 509.

By using SelectQueryPlanner, the planner also chooses Nested Loop Join algorithm and the number of block accesses is 57285.

Therefore, it's obvious that HeuristicQueryPlanner, which places the selection operation close to the bottom, has a much less cost. That is because after applying the selection first, there won't that many tuples to join with the other table.

#Question3:

By using B+tree, we can implement index nested loop join.
The algorithm for this index nested loop join:
Step1: Use B+tree to store clustered/non-clustered index of the inner relation s.
Step2: For each tuple in the outer relation r, use the attribute that we do the join as the index to search in the B+tree to find the tuple in s that satisfies ths join condition

The cost of the index nested loop join is br+nr*c, where c is the cost to look up the index in B+tree;

B tree seems better than B+tree. B tree also contains data in internal nodes which is more close to the node, while B+tree only store data in leaf nodes. Therefore, accessing data from a B tree is faster than a B+tree. In the index nested loop join, the cost to look up the index in a B tree is less than the B+tree.


