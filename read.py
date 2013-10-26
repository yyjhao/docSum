import re
import numpy as np
import PageRank
import sys
import config
import parser

if len(sys.argv) < 2:
    print "usage: python read.py filename"
    quit()

filename = sys.argv[1];

f = open(filename, "r")

article = f.read()

sentences = parser.getSentences(article)

adjMax = [[0 for s in sentences] for s in sentences]

def findRelation(csen):
    csen = "".join(re.compile(",|\"|\'|;|:|\]|\[|\(|\)").split(csen))
    count = 0
    for w in csen.split(" "):
        if w in config.relates:
            count += 1

    return count

def findOverlap(sen1, sen2):
    sen1 = "".join(re.compile(",|\"|\'|;|:|\]|\[|\(|\)").split(sen1))
    sen2 = "".join(re.compile(",|\"|\'|;|:|\]|\[|\(|\)").split(sen2))
    words1 = sen1.split(" ")
    words2 = sen2.split(" ")
    count = 0
    for w in words1:
        if w not in config.ignored:
            for ww in words2:
                if w == ww or w.capitalize() == ww or ww.capitalize() == w:
                    count += 1
    return count + 0.0

def words(sentence):
    sentence = "".join(re.compile(",|\"|\'|;|:|\]|\[|\(|\)").split(sentence))
    count = 0
    for w in sentence.split(" "):
        if w not in config.ignored:
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

# for m in adjMax:
#     print " ".join([str(i) for i in m])

G = np.array(adjMax)
rank = PageRank.zeroToOne(G,s=0.1)

l = []
ind = 0
for r in rank:
    l.append((r, ind))
    ind += 1

l.sort()
l.reverse()
# print all inportant sentences
# for k in l:
#     print sentences[k[1]]
#     print k[0]
#     print "==============="

def topPercentage(sentences, l):
    percentage = 0.15
    s = [k[1] for k in l[:int(len(l) * percentage + 0.5)]]
    s.sort()
    return [sentences[ss] for ss in s]

def cutoffScore(sentences, l):
    cutoff = 0.5
    r = []
    for k in l:
        if k[0] > cutoff:
            r.append(k[1])
    r.sort()
    return [sentences[ss] for ss in r]

def output(sentences):
    print parser.revert(".\n".join(sentences)) + "."

# output(cutoffScore(sentences, l))
output(topPercentage(sentences, l))
