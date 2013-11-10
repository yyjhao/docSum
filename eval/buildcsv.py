import sys

files = sys.argv[1:]
headers = [f.split(".")[0] for f in files]
r1 = [[] for h in headers]
r2 = [[] for h in headers]
r3 = [[] for h in headers]
r4 = [[] for h in headers]
l = [[] for h in headers]

data = [r1, r2, r3, r4, l]

for i in range(len(files)):
    cur_data = 0
    reading = False
    with open(files[i], "r") as f:
        for line in f:
            if line.find("Eval") == -1:
                if reading:
                    reading = False
                    cur_data += 1
            else:
                line = line.split("\n")[0]
                reading = True
                num = line.split("R:")[-1].split(" ")[0]
                data[cur_data][i].append(num)

out_files = ["rogue-1.csv", "rogue-2.csv", "rogue-3.csv", "rogue-4.csv", "rogue-l.csv"]
for i in range(5):
    with open(out_files[i], "w") as f:
        f.write(", ".join(headers) + "\n")
        for j in range(len(data[i][0])):
            f.write(", ".join([data[i][k][j] for k in range(len(data[i]))]) + "\n")


