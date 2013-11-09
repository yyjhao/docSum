import os
import sys
import shutil
import splitAndParse
import summarisation
import random

filepath = sys.argv[1]

if not os.path.isdir("stanford-corenlp"):
    print >> sys.stderr, "Please put the Stanford CoreNLP package into the stanford-corenlp directory."
    quit()

filename = filepath.split("/")[-1]
if not os.path.isfile("stanford-corenlp/" + filename + ".xml"):
    shutil.copyfile(filepath, "stanford-corenlp/" + filename)
    if os.name == "nt":
        os.system("cd stanford-corenlp && java -cp stanford-corenlp-3.2.0.jar;stanford-corenlp-3.2.0-models.jar;xom.jar;joda-time.jar;jollyday.jar -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -file " + filename)
    else:
        os.system("cd stanford-corenlp && java -cp stanford-corenlp-3.2.0.jar:stanford-corenlp-3.2.0-models.jar:xom.jar:joda-time.jar:jollyday.jar -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -file " + filename)

sentences, coref = splitAndParse.splitSentencesAndParse("stanford-corenlp/" + filename + ".xml")

order = range(len(sentences))

random.shuffle(order)

def cutoff_words(order, sentences, wc):
    r = []
    w = 0
    for k in order:
        sentence = sentences[k]
        swc = summarisation.words(sentence)
        if swc + w > wc:
            r.append((k, summarisation.cut_words(sentence, wc - w)))
            w = wc
        else:
            r.append((k, sentence))
            w += swc
        if w == wc:
            break
    r.sort()
    return [rr[1] for rr in r]

print summarisation.outputspl(cutoff_words(order, sentences, 200))