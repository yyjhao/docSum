f = open("fileList", "r")
ls = f.read().split("\n")
k = []

def sh(line):
    return "python read_without_co.py eval/contents/" + line + " | tee eval/output/pageRank/" + line 

for l in ls:
    k.append(sh(l))

print "\n".join(k)