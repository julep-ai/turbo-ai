from lemminflect import getInflection

__all__ = [
    "inflect",
]


def inflect(word, tag):
    return getInflection(word, tag=tag)[0]
