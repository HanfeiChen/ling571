# LING571 HW4

The hardest part of the homework is to choose an improvement over
the baseline induction model. My improvement uses parent annotation
to capture the structural dependence in the grammar, and annotates
each constituent with its parent node. This leads to more specific
rules and also sparsity. The result of my "improved" model has
a higher bracketing accuracy/precision/recall/F1 (95.44 vs 87.96),
but fails to parse many sentences that the baseline is able to
due to sparsity (the improved model only parsed 38 out of 55 test
sentences while the baseline parsed 50).

I considered using lexical information by annotating with lexical heads,
but the treebank doesn't contain head information, and I believed that
hardcoding lexical rules might not be ideal. So I stuck with parent
annotation which doesn't require extra information in the data.

The other parts of this assignment are quite standard.
