# LING571 HW6

This assignment is like the previous one, but with more emphasis on semantics.
Therefore, I initially thought I could just forget about the syntactic restrictions,
because we don't need to rule out any ungrammatical sentences. But I later realized
that syntactic information does disambiguate sentences. For example, the sentence
"Jack does not eat or drink" could be parsed as ((NP Jack) (VP (VP does not eat)
(CONJ or) (VP drink)) if syntax doesn't require that the NUM of "drink" agrees
with the NUM of "Jack". Therefore, I found it necessary to add the NUM feature,
which is not really semantic, but does help with disambiguation.

Another thing that I'm not entirely sure about is the NUM for the NP -> NP or NP.
I'm not sure which NUM the parent NP should be even if I know the NUM for the children.
In my grammar I'm not adding any constraints for this rule, but I guess that this
might cause ambiguity in some weird cases.
