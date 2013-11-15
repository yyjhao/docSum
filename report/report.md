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



# Algorithm

$$ C_{ij} = \sum a_{ij} $$


# Experiment Setup


# Results



# Conclusion

# References