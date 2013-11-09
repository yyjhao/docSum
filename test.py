import sys
import summarisation

if len(sys.argv) < 2:
    print "usage: python read.py filename"
    quit()

filename = sys.argv[1];

sentences = summarisation.summarise(filename, debug_output=True, co_ref=1)

print summarisation.outputspl(sentences)
# print sentences
