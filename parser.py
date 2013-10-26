import re


def getSentences(input):
    article = " ".join(input.split("\n"))

    # short form
    article = re.sub(r"([A-Z])\.", r"\1\^", article)

    # decimal
    article = re.sub(r"([0-9]+)\.([0-9]*)", r"\1\^\2", article)

    # some words
    article = "e^g^".join(article.split("e.g."))
    article = "i^e^".join(article.split("i.e."))
    article = "al^".join(article.split("al."))

    # inverted commas
    article = "".join(re.compile("\"|\'").split(article))

    return filter(lambda x: re.match(r"^ *$", x) == None, re.compile("\. *|! *|\? *").split(article))

def revert(input):
    article = re.sub(r"([A-Z])\\\^", r"\1.", input)
    article = re.sub(r"([0-9]+)\\\^([0-9]*)", r"\1.\2", article)
    article = "e.g.".join(article.split("e^g^"))
    article = "i.e.".join(article.split("i^e^"))
    article = "al.".join(article.split("al^"))

    return article
