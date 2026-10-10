"""Demo end-to-end preprocessing teks: stopword removal, pipeline + WordCloud, n-gram.

Jalankan:
    python main.py                         # pakai data/sample_text_ai.txt
    python main.py --input teks_saya.txt   # pakai teks sendiri
    python main.py --show                  # tampilkan WordCloud di layar juga
"""
import argparse
from collections import Counter
from pathlib import Path

from nlp_preprocessing import make_ngrams, preprocess_id, remove_stopwords_en, remove_stopwords_id
from nlp_preprocessing.visualization import build_wordcloud, save_wordcloud

BASE_DIR = Path(__file__).resolve().parent  # folder tempat main.py berada
OUTPUT_DIR = BASE_DIR / "outputs"
DEFAULT_INPUT = BASE_DIR / "data" / "sample_text_ai.txt"

lines = []  # semua yang dicetak juga disimpan ke outputs/results.txt


def rel(path: Path) -> str:
    """Path relatif terhadap folder project (untuk tampilan log)."""
    try:
        return Path(path).resolve().relative_to(BASE_DIR).as_posix()
    except ValueError:
        return str(path)


def log(text: str = "") -> None:
    print(text)
    lines.append(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Demo preprocessing teks NLP")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="file teks Bahasa Indonesia")
    parser.add_argument("--show", action="store_true", help="tampilkan WordCloud di layar")
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"File input tidak ditemukan: {args.input}")
    OUTPUT_DIR.mkdir(exist_ok=True)

    # 1. Stopword removal - Inggris
    en_text = "Sip and rest: Enjoy your quiet Sunday morning.."
    log("=== 1. Stopword Removal (Inggris, NLTK) ===")
    log(f"Input : {en_text}")
    log(f"Output: {remove_stopwords_en(en_text)}")

    # 2. Stopword removal - Indonesia
    id_text = "Sesap dan istirahat: Nikmati pagi hari Minggumu yang tenang."
    log("\n=== 2. Stopword Removal (Indonesia, Sastrawi) ===")
    log(f"Input : {id_text}")
    log(f"Output: {remove_stopwords_id(id_text)}")

    # 3. Pipeline lengkap + WordCloud
    log("\n=== 3. Pipeline Lengkap + WordCloud ===")
    raw_text = args.input.read_text(encoding="utf-8")
    log(f"File input        : {rel(args.input)} ({len(raw_text.split())} kata)")
    clean_text = preprocess_id(raw_text)
    tokens = clean_text.split()
    log(f"Setelah pipeline  : {len(tokens)} kata, {len(set(tokens))} kata unik")
    log("10 kata terbanyak :")
    for word, count in Counter(tokens).most_common(10):
        log(f"  {word:<15} {count}")

    wordcloud_path = OUTPUT_DIR / "wordcloud.png"
    save_wordcloud(build_wordcloud(clean_text), wordcloud_path, show=args.show)
    log(f"WordCloud disimpan: {rel(wordcloud_path)}")

    # 4. N-gram
    ngram_text = "Sabtu pagi saya dan istri pergi ke alun-alun"
    log("\n=== 4. N-Gram ===")
    log(f"Teks: {ngram_text}")
    for n, name in [(1, "Unigram"), (2, "Bigram"), (3, "Trigram")]:
        log(f"{name}: {make_ngrams(ngram_text, n)}")

    (OUTPUT_DIR / "results.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nHasil lengkap tersimpan di {rel(OUTPUT_DIR / 'results.txt')}")


if __name__ == "__main__":
    main()