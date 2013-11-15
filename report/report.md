---
title: CS2309 Report
author: ['Yao Yujian', 'Wang Chao']
abstract: |
  Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
  tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
  quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
  consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
  cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
  proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
---

# Introduction

With the scaling of Internet, people are overwhelmed by a large number
of documents on-line. To filter out useful information becomes harder
and harder. As a result, it is necessary to develop a fast way which can be used 
to generate a short piece of text covering all the main topics of a document and 
catching all relevant points. Automatic document summarization can help users in 
such process.

In this paper, we propose a novel automatic document summarization algorithm which
is named as SenRank. We model an article as a graph of continuous floating ideas as
well as sentences. Consequently, the overlap of words between sentences is able to 
signify their relations. With the aid of co-reference, we run PageRank on such graph 
and aggregate top few sentences as a summary. To make this summary succinct, we remove
some sentences which have overlap with others.

Then we use the ROUGE(Recall-Oriented Understudy for Gisting Evalution) toolkit to test
SenRank. The results show that SenRank has a good performance as what we expect.



# Formulation

## Assumptions

We start the formulation with the following assumptions:

1. Articles consist of ideas
1. Ideas flow
1. Each sentence presents some ideas
1. Ideas are expressed through words
1. Overlap of words signifies relation of ideas

We can then assume that a sentence is significant, thus _summarizing_, if
ideas from many other sentences flow to it.

We further assume that by assembling a set of _summarizing_ sentences, we
can produce a good summary. Further, to shorten the length of the summary,
we should try to minimize overlaps among sentences in this set.

## Construction of article graph

To make use of the assumptions, we formulate the article as a graph of
sentences.

Formally, we can build a complete graph $\mathcal{G} = (V, E)$, where $V$ is the
set of sentences, and $\forall (u, v) \in E, weight(e) = relation(u, v)$.

Further, we define $relation(u, v)$ to be the number of word overlaps
(where only a subset of all words are considered) plus the number of shared
references (by making use of co-reference _(citation)_). Moreover, we assume
that $relation(u, v) = relation(v, u)$, as both word-overlap and co-reference
has no direction.

With the graph, we can then find out the probability of ideas flowing to a
sentence with the PageRank _(citation)_ algorithm. Then we can rank the
sentences with their PageRank score and pick the top few sentences that
do not overlap too much as the summary.

# Algorithm

With the graph formulation, SenRank works by following the steps detailed in
this section.

## Tokenization and derivation of co-references

We use Stanford Corenlp _(citation)_ to tokenize the article and then generate
the co-reference data.

## Parsing co-references

The co-reference data obtained from Stanford Corenlp is a list of tuples:
$(c_1, c_2,...,c_n), (d_1, d_2,...,d_n)...$, where $c_i, d_i$ refers to a
sentence in the article. Each tuple represents the occurrence of one entity
in sentences. So $(c_1, c_2,...,c_n)$ means that a particular entity appears
in Sentence $c_1, c_2,...c_n$. Moreover, there can be some $i, j$ such that
$i /neq j$ and $c_i = c_j$ in some tuples, i.e., if an entity appears for
multiple times in a sentence, that sentence will be recorded for multiple
times in the tuple.

SenRank then use this co-reference data to build an adjacency matrix

$$ A_{ij} = a_{ij} + a_{ji}$$

where $a_{ij}$ is the number of times Sentence $i$ appearing in tuples that
also contains Sentence $j$.

For example, we may have obtained the co-reference data $(1,1,2,3), (1,3)$.
Then $a_{12} = 2$, $a_{21} = 1$, thus $A_{12} = A_{21} = 3$

## Counting word overlap

SenRank then process all sentences and form another adjacency matrix

$$ B_{ij} = \sum\limits_{w \in W} w_iw_j$$

where $W$ is the set of words that are considered for word overlap and $w_i$
refers to the number of time Word $w$ appears in Sentence $i$.

## Building article graph

With $A$ and $B$, SenRank builds the final adjacency matrix

$$ C = k_aA + k_bB $$

where $k_a$ and $k_b$ are some constants that can be tweaked for optimal
performance.

## Running PageRank

SenRank then runs the PageRank algorithm on $C$ to obtain PageRank scores
for all sentences

## Generating a summary

Finally SenRank generates a summary with the following algorithm:

Firstly we define $m$ as the threshold such that
$weight(u, v) > m $ means that u and v are similar enough that they cannot
both appear in the summary.

1. $S$ is the set of all sentences
1. $R$ is the set of sentences in the summary, initially $R = \emptyset$
1. Loop while $S \neq \emptyset$
    1. Pick $s \in S$ such that $s$ has a highest score
    1. $R = R \cup \{s\}$
    1. Let $T = \{i \mid C_{si} > m\}$
    1. $S = S - T$
    1. If $R$ exceeds the word limit, trancate the last sentence added to R to match the word limit
    1. If $R$ matches the word limit, terminate the loop
1. Output sentences in $R$ according to their original order in the article

# Experiment Setup

We test our algorithm on 178 papers in Scholarly Paper Recommendation Dataset
_(citation)_. The abstracts are used as model summaries and the contents are
used as input articles. We then use ROUGE _(citation)_ to evaluate the quality
of the generated summaries. We use the R-score of ROGUE since the model
summaries do not have a word limit.

We setup our algorithm such that the word limit is 200 and $m = 20$.

Moreover, we run the experiments on the following algorithms:

1. Random: randomly pick sentences from the article until word limit is matched
1. Degree: Set $k_a = 0$, so we do not consider co-reference. Further, we do not run PageRank and instead rank sentences by their degrees in the graph (sum of the row in $C$)
1. PageRank: Set $k_a = 0$. Again we do not consider co-reference.
1. Coref_equal: Set $k_a = 1$ and $k_b = 1$
1. Coref_twice: Set $k_a = 2$ and $k_b = 1$
1. Coref_large: Set $k_a = 5$ and $k_b = 1$
1. Coref_only: Set $k_a = 1$ and $k_b = 0$, so we only consider co-reference but not word overlap.

# Results

: Mean values of ROUGE-R Scores \label{1}

+-------------+----------+----------+----------+----------+
| Algorithm   | ROUGE-1  | ROUGE-2  | ROUGE-3  | ROUGE-L  |
+=============+==========+==========+==========+==========+
| Random      | 0.266158 | 0.056647 | 0.015765 | 0.251459 |
+-------------+----------+----------+----------+----------+
| Degree      | 0.302039 | 0.079483 | 0.023131 | 0.279868 |
+-------------+----------+----------+----------+----------+
| PageRank    | 0.308187 | 0.080359 | 0.024296 | 0.285539 |
+-------------+----------+----------+----------+----------+
| Coref_equal | 0.312450 | 0.078048 | 0.022415 | 0.287519 |
+-------------+----------+----------+----------+----------+
| Coref_twice | 0.321284 | 0.083117 | 0.025682 | 0.294462 |
+-------------+----------+----------+----------+----------+
| Coref_large | 0.312604 | 0.080656 | 0.025286 | 0.288393 |
+-------------+----------+----------+----------+----------+
| Coref_only  | 0.287429 | 0.072876 | 0.022825 | 0.268019 |
+-------------+----------+----------+----------+----------+

: 1-tailed paired t-tests on ROUGE-L scores on various algorithms \label{2}

+---------+-----------------+-------------------+------------------------+------------------------+------------------------+-----------------------+
| Test    | Random < Degree | Degree < PageRank | PageRank < Coref_equal | PageRank < Coref_twice | PageRank < Coref_large | Coref_only < PageRank |
+=========+=================+===================+========================+========================+========================+=======================+
| p-value | 0.000           | 0.055             | 0.307                  | 0.032                  | 0.307                  | 0.008                 |
+---------+-----------------+-------------------+------------------------+------------------------+------------------------+-----------------------+

This shows that the SenRank algorithm (even the stripped down version)
can produce summaries of reasonable quality. Moreover, by t-test results,
we can see that PageRank seems to perform better than Degree, although the
difference is not very significant.

Furthermore, the coefficients $k_a$ and $k_b$ affect the performance
of SenRank, and co-reference alone is even worse than using word overlaps.

# Conclusion

# References