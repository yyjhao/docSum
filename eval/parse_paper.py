import re
import sys

extractor = re.compile(r".*abstract \.\n(.*)introduction \.\n(.*)", re.DOTALL | re.M)

for filename in sys.argv[1:]:
    f = open(filename, "r")

    article = f.read()
    f.close()
    m = extractor.match(article)
    if not m:
        print filename
    else:
        out = open(filename + ".abstract.spl", "w")
        out.write(m.group(1))
        out.close()

        out = open(filename + ".spl", "w")
        out.write(m.group(2))
        out.close()
