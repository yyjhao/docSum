import re
import numpy as np
from scipy.sparse import csc_matrix
 
def pageRank(G, s = .85, maxerr = .001):
    """
    Computes the pagerank for each of the n states.
 
    Used in webpage ranking and text summarization using unweighted
    or weighted transitions respectively.
 
 
    Args
    ----------
    G: matrix representing state transitions
       Gij can be a boolean or non negative real number representing the
       transition weight from state i to j.
 
    Kwargs
    ----------
    s: probability of following a transition. 1-s probability of teleporting
       to another state. Defaults to 0.85
 
    maxerr: if the sum of pageranks between iterations is bellow this we will
            have converged. Defaults to 0.001
    """
    n = G.shape[0]
 
    # transform G into markov matrix M
    M = csc_matrix(G,dtype=np.float)
    rsums = np.array(M.sum(1))[:,0]
    ri, ci = M.nonzero()
    M.data /= rsums[ri]
 
    # bool array of sink states
    sink = rsums==0
 
    # Compute pagerank r until we converge
    ro, r = np.zeros(n), np.ones(n)
    while np.sum(np.abs(r-ro)) > maxerr:
        ro = r.copy()
        # calculate each pagerank at a time
        for i in xrange(0,n):
            # inlinks of state i
            Ii = np.array(M[:,i].todense())[:,0]
            # account for sink states
            Si = sink / float(n)
            # account for teleportation to state i
            Ti = np.ones(n) / float(n)
 
            r[i] = ro.dot( Ii*s + Si*s + Ti*(1-s) )
 
    # return normalized pagerank
    return r/sum(r)


f = open("long.txt.sub", "r")
article = " ".join(f.read().split("\n"))

article = re.sub(r"([A-Z])\.", r"\1\^", article).lower()
article = re.sub(r"([0-9]+)\.([0-9]*)", r"\1\^\2", article)
article = re.sub(r"<|>", "", article);
article = "e^g^".join(article.split("e.g."))
article = "i^e^".join(article.split("i.e."))
article = "al^".join(article.split("al."))
article = "".join(article.split("'s"))
article = "".join(re.compile("\"|\'").split(article))

sentences = re.compile("\. |! |\? ").split(article)

adjMax = [[0 for s in sentences] for s in sentences]

ignored = set([
    "for",
    "in",
    "is",
    "have",
    "has",
    "be",
    "been",
    "a",
    "the",
    "of",
    "this",
    "that",
    "these",
    "those",
    "since",
    "being",
    "because",
    "on",
    "under",
    "through",
    "and",
    "all",
    "to",
    "than",
    "then",
    "so",
    "many",
    "any",
    "some",
    "from",
    "much",
    "can",
    "could",
    "may",
    "maybe",
    "while",
    "when",
    "what",
    "who",
    "do",
    "don't",
    "not",
    "was",
    "were",
    "",
    " ",
    "or",
    "\"",
    "'",
    "it",
    "they",
    "are",
    "will",
    "-",
    "he",
    "no",
    "not",
    "but",
    "however",
    "moreover",
    "also",
    "there",
    "at",
    "us",
    "with",
    "as",
    "like",
    "say",
    "says",
    "such",
    "so",
    "over",
    "its",
    "theirs",
    "his",
    "her",
    "et",
    "al^",
    "i^e^",
    "e^g^",
    "would",
    "had",
    "by"
])

relates = set([
    "this",
    "that",
    "these",
    "those",
    "because",
    "but",
    "however",
    "moreover",
    "also",
    "there",
    "its",
    "theirs",
    "his",
    "her",
    "exmaple",
    "another"
])

def findRelation(csen):
    csen = "".join(re.compile(",|\"|\'|;|:|\]|\[|\(|\)").split(csen))
    count = 0
    for w in csen.split(" "):
        if w in relates:
            count += 1

    return count

def findOverlap(sen1, sen2):
    sen1 = "".join(re.compile(",|\"|\'|;|:|\]|\[|\(|\)").split(sen1))
    sen2 = "".join(re.compile(",|\"|\'|;|:|\]|\[|\(|\)").split(sen2))
    words1 = sen1.split(" ")
    words2 = sen2.split(" ")
    count = 0
    for w in words1:
        if w not in ignored:
            for ww in words2:
                if w == ww:
                    print w
                    count += 1
    return count + 0.0

def words(sentence):
    sentence = "".join(re.compile(",|\"|\'|;|:|\]|\[|\(|\)").split(sentence))
    count = 0
    for w in sentence.split(" "):
        if w not in ignored:
            count += 1
    if count == 0:
        return 1
    return count

for s in range(len(sentences)):
    if s > 0:
        adjMax[s][s - 1] += findRelation(sentences[s])
    for ss in range(len(sentences)):
        if s != ss:
            adjMax[s][ss] += findOverlap(sentences[s], sentences[ss])

for m in adjMax:
    print " ".join([str(i) for i in m])

# for s in range(len(adjMax)):
#     for ss in range(len(adjMax)):
#         if adjMax[s][ss] > 2:
#             print sentences[s], "+", sentences[ss]

G = np.array(adjMax)
rank = pageRank(G,s=0.1)

l = []
ind = 0
for r in rank:
    l.append((r, ind))
    ind += 1

l.sort()
l.reverse()

for k in l:
    print sentences[k[1]]
    print k[0]
    print "==============="