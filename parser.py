import re


def getSentences(input):
    article = " ".join(input.split("\n"))

    # short form
    article = re.sub(r"([A-Z])\.", r"\1\^", article).lower()

    # decimal
    article = re.sub(r"([0-9]+)\.([0-9]*)", r"\1\^\2", article)

    # ?
    article = re.sub(r"<|>", "", article);

    # some words
    article = "e^g^".join(article.split("e.g."))
    article = "i^e^".join(article.split("i.e."))
    article = "al^".join(article.split("al."))

    # someone's
    article = "".join(article.split("'s"))

    # inverted commas
    article = "".join(re.compile("\"|\'").split(article))

    return re.compile("\. |! |\? ").split(article)
