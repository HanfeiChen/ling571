# LING571 HW3

This assignment is quite straightforward. Following
the pseudocode I was able to quickly implement
the CKY parsing forward algorithm.

Implementing the backward algorithm took a little
bit of effort. I ended up writing a recursive
algorithm. In the forward algorithm, I keep the "split"
index as the back pointer, and when reconstructing
I recursively parse the left side of the split
and the right side of the split.

I realize that my recursive algorithm is not optimal
as it could be doing repeated work. Using memoization
could improve the time complexity of the algorithm
at the cost of some space, which is definitely worth
implementing if the input size is large.
But for the input size required for this assignment,
the current recursive algorithm works well enough.
