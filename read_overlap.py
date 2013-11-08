import sys
import summarisation

if len(sys.argv) < 2:
    print "usage: python read.py filename"
    quit()

filename = sys.argv[1];

sentences = summarisation.summarise(filename, debug_output=False, page_rank=False, co_ref=False)

print summarisation.outputspl(sentences)
# print sentences
