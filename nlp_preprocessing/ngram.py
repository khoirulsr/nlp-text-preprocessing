"""Pembuatan n-gram (unigram, bigram, trigram, dst.)."""


def make_ngrams(text: str, n: int) -> list:
    """Kembalikan daftar n-gram dari teks (dipecah per spasi).

    n=1 -> unigram, n=2 -> bigram, n=3 -> trigram.
    """
    if n < 1:
        raise ValueError("n harus >= 1")
    from nltk.util import ngrams

    return [" ".join(gram) for gram in ngrams(text.split(), n)]
