# LING571 HW2

I followed the procedure described in the lecture slides.
The major difficulty that I had was handling unit productions.
At first, I misunderstood the procedure to eliminate unit
productions, and thought that I needed to resolve every unit
production down to the form "A -> terminal." I also attempted
to do this in a single pass. Later, I decided to only resolve
one level of unit production at a time, and run multiple passes
through the grammar until no unit productions are present in
the grammar. This turned out to be much easier to implement,
and seemed to be efficient enough to handle atis.cfg.

The parses produced by the CNF grammar contain a lot of inter-
mediate nonterminals (which were added to break down hybrid
and long rules), but the overall parses aren't much longer
than the original parses because we eliminated some unit
productions as well to balance for it.

Also, quite naturally, the parses produced by the CNF grammar
make much less sense linguistically compared to the original,
because the way we break down long rules isn't aware of the
syntactic structure of the phrase.

Overall, the CNF grammar seems to produce the same number of
parses as the original grammar, and the average number of parses
with both grammars are 16.208.
