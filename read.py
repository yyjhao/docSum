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

words_used = set()

def findOverlap(sen1, sen2):
    sen1 = "".join(re.compile(",|\"|\'|;|:|\]|\[|\(|\)").split(sen1.lower()))
    sen2 = "".join(re.compile(",|\"|\'|;|:|\]|\[|\(|\)").split(sen2.lower()))
    words1 = filter(lambda x: x not in config.ignored and not x.isdigit(), sen1.split(" "))
    words2 = filter(lambda x: x not in config.ignored and not x.isdigit(), sen2.split(" "))
    count = 0
    for w in words1:
        for ww in words2:
            if isOverlap(w, ww):
                if w != ww:
                    words_used.add((w, ww))
                else:
                    words_used.add(w)
                count += 1
    return count + 0.0

def isOverlap(w1, w2):
    return (w1 == w2 or 
            isVerySimilar(w1, w2) or
            isVerySimilar(w2, w1))

def isVerySimilar(w1, w2):
    ws = w1.split(w2)
    if len(ws) == 1:
        return False
    if len(ws) < 3:
        if len(ws[0]) < 2 and len(ws[1]) < 4 and not re.match("^[A-Za-z]*$", ws[0]):
            return True

    return False

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
        adjMax[s][s - 1] += findRelation(sentences[s]) * 0
    for ss in range(len(sentences)):
        if s != ss:
            adjMax[s][ss] += findOverlap(sentences[s], sentences[ss])

# for m in adjMax:
#     print " ".join([str(i) for i in m])

G = np.array(adjMax)
rank = PageRank.pageRank(G,s=0.9)

l = []
ind = 0
for r in rank:
    l.append((r, ind))
    ind += 1

l.sort()
l.reverse()
print words_used
# print all inportant sentences
for k in l:
    print sentences[k[1]]
    print k[0]
    print "==============="

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
