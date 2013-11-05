import re
import numpy as np
import PageRank
import sys
import config
import splitAndParse
import os
import shutil

if len(sys.argv) < 2:
    print "usage: python read.py filename"
    quit()

filename = sys.argv[1];

if not os.path.isdir("stanford-corenlp"):
    print "Please put the Stanford CoreNLP package into the stanford-corenlp directory."
    quit()

shutil.copyfile(filename, "stanford-corenlp/" + filename)
if os.name == "nt":
    os.system("cd stanford-corenlp && java -cp stanford-corenlp-3.2.0.jar;stanford-corenlp-3.2.0-models.jar;xom.jar;joda-time.jar;jollyday.jar -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -file " + filename)
else:
    os.system("cd stanford-corenlp && java -cp stanford-corenlp-3.2.0.jar:stanford-corenlp-3.2.0-models.jar:xom.jar:joda-time.jar:jollyday.jar -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -file " + filename)


sentences, coref = splitAndParse.splitSentencesAndParse("stanford-corenlp/" + filename + ".xml")

# print coref

adjMax = [[0 for s in sentences] for s in sentences]

for co in coref:
    dic = {}
    for s in co:
        if s in dic:
            dic[s] += 1
        else:
            dic[s] = 1
    for s in dic:
        for ss in dic:
            if s != ss:
                adjMax[s][ss] += (dic[s] + 0.0) / dic[ss]

words_used = set()

def findOverlap(sen1, sen2):
    words1 = filter(lambda x: x not in config.ignored and not x.isdigit(), sen1)
    words2 = filter(lambda x: x not in config.ignored and not x.isdigit(), sen2)
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

print "before overlap"
for m in adjMax:
    print " ".join([str(i) for i in m])

for s in range(len(sentences)):
    for ss in range(len(sentences)):
        if s != ss:
            adjMax[s][ss] += findOverlap(sentences[s], sentences[ss])

print "after overlap"
for m in adjMax:
    print " ".join([str(i) for i in m])

G = np.array(adjMax)
# rank = PageRank.pageRank(G,s=0.9)
rank = PageRank.zeroToOne(G, s=0.5)

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
    print de_nlp("\n".join([" ".join(s) for s in sentences]))

def de_nlp(article):
    article = "(".join(article.split("-LRB- "))
    article = "[".join(article.split("-LSB- "))
    article = ")".join(article.split(" -RRB-"))
    article = "]".join(article.split(" -RSB-"))
    article = "-".join(article.split(" -- "))
    article = re.sub(r" ([^a-zA-Z]) ", r"\1 ", article)
    article = re.sub(r" \.", ".", article)
    article = re.sub(r" 's ", "'s ", article)
    article = re.sub(r" n't ", "n't ", article)
    article = re.sub(r"`` ", "\"", article)
    article = re.sub(r" ''", "\"", article)
    return article

# output(cutoffScore(sentences, l))
output(topPercentage(sentences, l))
