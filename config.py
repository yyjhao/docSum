_ignored = [
    "for",
    "in",
    "is",
    "have",
    "has",
    "be",
    "been",
    "a",
    "the",
    "of",
    "this",
    "that",
    "these",
    "those",
    "since",
    "being",
    "because",
    "on",
    "under",
    "through",
    "and",
    "all",
    "to",
    "than",
    "then",
    "so",
    "many",
    "any",
    "some",
    "from",
    "much",
    "can",
    "could",
    "may",
    "maybe",
    "while",
    "when",
    "what",
    "who",
    "do",
    "don't",
    "not",
    "was",
    "were",
    "",
    " ",
    "or",
    "\"",
    "'",
    "it",
    "they",
    "are",
    "will",
    "-",
    "he",
    "no",
    "not",
    "but",
    "however",
    "moreover",
    "also",
    "there",
    "at",
    "us",
    "with",
    "as",
    "like",
    "say",
    "says",
    "such",
    "so",
    "over",
    "its",
    "theirs",
    "his",
    "her",
    "et",
    "al^",
    "i^e^",
    "e^g^",
    "would",
    "had",
    "by"
]

ignored = set(_ignored + [i.capitalize() for i in _ignored])

relates = set([
    "this",
    "that",
    "these",
    "those",
    "because",
    "but",
    "however",
    "moreover",
    "also",
    "there",
    "its",
    "theirs",
    "his",
    "her",
    "exmaple",
    "another"
])