"""Test preprocessing.

Nilai yang diharapkan pada test stopword dan n-gram diambil dari hasil run
asli di notebook/VS Code (NLTK dan Sastrawi).

Jalankan: pytest
"""
from nlp_preprocessing import (
    make_ngrams,
    normalize_text,
    preprocess_id,
    remove_stopwords_en,
    remove_stopwords_id,
    remove_urls,
)


# ---------- Test yang butuh NLTK / Sastrawi (dengan output asli) ----------
def test_remove_stopwords_en():
    text = "Sip and rest: Enjoy your quiet Sunday morning.."
    assert remove_stopwords_en(text) == "Sip rest: Enjoy quiet Sunday morning.."


def test_remove_stopwords_id():
    text = "Sesap dan istirahat: Nikmati pagi hari Minggumu yang tenang."
    assert remove_stopwords_id(text) == "Sesap istirahat: Nikmati pagi hari Minggumu tenang."


def test_ngrams():
    text = "Sabtu pagi saya dan istri pergi ke alun-alun"
    assert make_ngrams(text, 1) == ["Sabtu", "pagi", "saya", "dan", "istri", "pergi", "ke", "alun-alun"]
    assert make_ngrams(text, 2) == [
        "Sabtu pagi", "pagi saya", "saya dan", "dan istri", "istri pergi", "pergi ke", "ke alun-alun",
    ]
    assert make_ngrams(text, 3) == [
        "Sabtu pagi saya", "pagi saya dan", "saya dan istri", "dan istri pergi",
        "istri pergi ke", "pergi ke alun-alun",
    ]


def test_ngrams_rejects_invalid_n():
    try:
        make_ngrams("a b c", 0)
    except ValueError:
        return
    raise AssertionError("n=0 seharusnya ditolak")


def test_preprocess_id_output_is_clean():
    text = "Lihat https://contoh.com/halaman 123 untuk Sehari-hari, yang ADA!"
    tokens = preprocess_id(text).split()
    assert tokens, "hasil tidak boleh kosong"
    for token in tokens:
        assert token.isalpha() and token.islower()
    assert "yang" not in tokens      # stopword terhapus
    assert "https" not in tokens     # URL terhapus
    assert "contoh" not in tokens


# ---------- Test fungsi murni (tanpa library eksternal) ----------
def test_normalize_text_lowercase_and_remove_symbols():
    assert normalize_text("Halo, Dunia! 123 :)") == "halo dunia"


def test_normalize_text_keeps_hyphenated_words_separate():
    # tanda hubung diganti spasi, bukan dihapus ("sehari-hari" != "seharihari")
    assert normalize_text("Sehari-hari") == "sehari hari"
    assert normalize_text("berlomba-lomba") == "berlomba lomba"


def test_normalize_text_collapses_whitespace():
    assert normalize_text("  a   \n\n b\t c  ") == "a b c"


def test_remove_urls():
    assert normalize_text(remove_urls("cek https://a.com/x?y=1 dan www.b.org/z ya")) == "cek dan ya"
    assert remove_urls("tanpa url") == "tanpa url"
