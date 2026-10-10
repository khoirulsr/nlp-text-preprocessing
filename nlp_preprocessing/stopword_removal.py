"""Penghapusan stopword untuk Bahasa Inggris (NLTK) dan Indonesia (Sastrawi)."""
from functools import lru_cache


@lru_cache(maxsize=1)
def _english_stopwords() -> frozenset:
    # Import di dalam fungsi: modul ini tetap bisa di-import tanpa memuat NLTK
    # sampai fungsinya benar-benar dipakai.
    import nltk
    from nltk.corpus import stopwords

    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords", quiet=True)
    return frozenset(stopwords.words("english"))


@lru_cache(maxsize=1)
def _indonesian_remover():
    from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

    return StopWordRemoverFactory().create_stop_word_remover()


def remove_stopwords_en(text: str) -> str:
    """Hapus stopword Inggris. Teks dipecah per spasi (split), jadi tanda baca
    yang menempel pada kata (mis. "rest:") ikut terbawa."""
    stop_words = _english_stopwords()
    return " ".join(word for word in text.split() if word.lower() not in stop_words)


def remove_stopwords_id(text: str) -> str:
    """Hapus stopword Indonesia memakai daftar bawaan Sastrawi."""
    return _indonesian_remover().remove(text)
