import sys
import summarisation

if len(sys.argv) < 2:
    print "usage: python read.py filename"
    quit()

filename = sys.argv[1];

sentences = summarisation.summarise(filename, debug_output=False, co_ref=3, overlap=False)

print summarisation.outputspl(sentences)
# print sentences
