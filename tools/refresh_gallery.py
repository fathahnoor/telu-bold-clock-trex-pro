"""Use content-addressed preview URLs so changed images get fresh URLs."""
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    gallery = ROOT / 'out/gallery'
    gallery.mkdir(exist_ok=True)
    pages = {p: p.read_text(encoding='utf-8')
             for p in (ROOT / 'README.md', ROOT / 'preview.html')}
    for name in ('preview', 'preview_idle', 'preview_max', 'preview_zero', 'preview_sunrise'):
        data = (ROOT / 'out' / f'{name}.png').read_bytes()
        digest = hashlib.sha256(data).hexdigest()[:12]
        filename = f'{name}-{digest}.png'
        (gallery / filename).write_bytes(data)
        pattern = rf'(?:gallery/)?{name}(?:-[0-9a-f]{{12}})?\.png'
        pages = {p: re.sub(pattern, f'gallery/{filename}', text)
                 for p, text in pages.items()}
    for path, text in pages.items():
        path.write_text(text, encoding='utf-8')
    print('Gallery URLs refreshed from preview content hashes')


if __name__ == '__main__':
    main()
