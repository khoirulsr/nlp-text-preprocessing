"""Pembersihan teks Bahasa Indonesia: URL, normalisasi, stemming, dan pipeline lengkap."""
import re
from functools import lru_cache

from .stopword_removal import remove_stopwords_id

_URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", flags=re.IGNORECASE)


def remove_urls(text: str) -> str:
    """Hapus URL (https://..., http://..., www....) dari teks."""
    return _URL_PATTERN.sub(" ", text)


def normalize_text(text: str) -> str:
    """Ubah ke huruf kecil, buang angka/simbol/emoji, rapikan spasi.

    Karakter non-huruf diganti SPASI (bukan dihapus), supaya kata berhubung
    seperti "sehari-hari" menjadi "sehari hari", bukan "seharihari".
    """
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


@lru_cache(maxsize=1)
def _stemmer():
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

    return StemmerFactory().create_stemmer()


def stem_text(text: str) -> str:
    """Kembalikan tiap kata ke bentuk dasar (mis. memancing -> pancing)."""
    return _stemmer().stem(text)


def preprocess_id(text: str) -> str:
    """Pipeline lengkap Bahasa Indonesia:
    hapus URL -> hapus stopword -> normalisasi -> stemming.
    """
    text = remove_urls(text)
    text = remove_stopwords_id(text)
    text = normalize_text(text)
    return stem_text(text)
