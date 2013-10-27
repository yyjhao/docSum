def splitSentencesAndParse(fileName):
	sentences = []
	coreference = []
	coNum = -1
	num = -1
	with open(fileName) as f:
		for line in f:
			#split sentences
			if (line.find("<sentence id=") != -1):
				if (num != -1):
					sentences.append(word)
				num += 1
				word = []
			if (line.find("<word>") != -1):
				start = line.find("<word>") + 6
				end = line.find("</word>")
				word.append(line[start:end])
			#find coreference
			if (line.find("mention representative=\"true\"") !=-1):
				if (coNum != -1):
					coreference.append(sen)
				coNum += 1
				sen = []
			if (line.find("<sentence>") != -1):
				start = line.find("<sentence>") + 10
				end = line.find("</sentence>")
				sen.append(int(line[start:end]))
	sentences.append(word)
	coreference.append(sen)
	print sentences
	return [sentences, coreference]
splitSentencesAndParse("tech2.ascii.txt.xml")