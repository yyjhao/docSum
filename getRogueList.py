f = open("fileList", "r")
ls = f.read().split("\n")
k = []

def rogue(line):
    dots = line.split(".")
    dots[-1] = "abstract"
    dots.append("spl")
    abstract = ".".join(dots)
    return "output/pageRank/" + line + "\tabstracts/" + abstract

for l in ls:
    k.append(rogue(l))

print "\n".join(k)