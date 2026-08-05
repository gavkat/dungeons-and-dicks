#!/usr/bin/env python3
"""Extract a session-recap PDF's text layer AND render its pages to PNGs.

These recaps are typically one very tall page carrying prose *plus* illustrations
and a stylized title — details that live only in the artwork (species, scene,
the session title) never show up in the text layer, so we always render images too.

poppler / pdftotext is usually unavailable in this environment; we use pymupdf and
install it on demand rather than fighting the package manager.

Usage:
    python extract_pdf.py <file.pdf> [output_dir]

Writes <output_dir>/session_text.txt and <output_dir>/page-<n>.png, and prints a
per-page report (text length, embedded-image count) so you know where to look.
Default output_dir is the current directory.
"""
import os
import subprocess
import sys


def ensure_pymupdf():
    try:
        import fitz  # noqa: F401
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pymupdf"], check=True)


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: python extract_pdf.py <file.pdf> [output_dir]")
    pdf_path = sys.argv[1]
    out_dir = (sys.argv[2] if len(sys.argv) > 2 else "") or "."
    os.makedirs(out_dir, exist_ok=True)

    ensure_pymupdf()
    import fitz

    doc = fitz.open(pdf_path)
    print(f"page_count: {doc.page_count}")

    text_parts = []
    for i, page in enumerate(doc):
        txt = page.get_text()
        text_parts.append(f"===== PAGE {i + 1} =====\n{txt}")
        n_images = len(page.get_images())
        # Render at ~1.2x; enough to read a title and study character art.
        pix = page.get_pixmap(matrix=fitz.Matrix(1.2, 1.2))
        png_path = os.path.join(out_dir, f"page-{i + 1}.png")
        pix.save(png_path)
        print(f"page {i + 1}: text_len={len(txt)}, embedded_images={n_images}, "
              f"rendered -> {png_path} ({pix.width}x{pix.height})")

    text_path = os.path.join(out_dir, "session_text.txt")
    with open(text_path, "w") as f:
        f.write("\n".join(text_parts))
    print(f"\ntext layer -> {text_path}")
    print("NOTE: open the rendered PNG(s) with the Read tool — the title and art "
          "carry facts the text layer does not.")


if __name__ == "__main__":
    main()
