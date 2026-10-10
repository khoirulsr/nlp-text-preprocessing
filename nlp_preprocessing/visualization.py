"""Visualisasi WordCloud."""
from pathlib import Path

import matplotlib.pyplot as plt


def build_wordcloud(text: str, width: int = 800, height: int = 400):
    """Buat objek WordCloud dari teks yang sudah dibersihkan."""
    from wordcloud import WordCloud

    if not text.strip():
        raise ValueError("Teks kosong setelah preprocessing, tidak ada kata untuk divisualisasikan.")
    return WordCloud(
        width=width, height=height, background_color="white", collocations=False
    ).generate(text)


def save_wordcloud(wordcloud, path, title: str = "WordCloud Bahasa Indonesia", show: bool = False) -> None:
    """Simpan WordCloud ke file gambar; tampilkan di layar jika show=True."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)
