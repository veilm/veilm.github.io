#!/usr/bin/env python3
import argparse
import html
import re
from pathlib import Path


def parse_entries(path, with_dates=False):
    src = path.read_text(encoding='utf-8', errors='ignore')
    entry_re = re.compile(
        r'<a\s+href="([^"]+)"[^>]*class="animetitle"[^>]*>\s*<span>(.*?)</span>',
        re.S,
    )
    entries = []
    for href, title in entry_re.findall(src):
        title = html.unescape(title.strip())
        match = re.search(r'/anime/(\d+)', href)
        if not match:
            continue
        anime_id = match.group(1)
        note_re = re.compile(rf'id="noteRowEdit{anime_id}"\s+data-note="(.*?)"', re.S)
        note_match = note_re.search(src)
        note = ''
        if note_match:
            note = html.unescape(note_match.group(1).strip())
        if href.startswith('/'):
            href = 'https://myanimelist.net' + href
        start_date = ''
        end_date = ''
        if with_dates:
            row_re = re.compile(
                rf'(<tr>.*?<a[^>]+/anime/{anime_id}[^>]*>.*?</tr>)', re.S
            )
            row_match = row_re.search(src)
            if row_match:
                row = row_match.group(1)
                dates = re.findall(
                    r'<td class="td[12]"[^>]*width="90"[^>]*>\s*(.*?)\s*</td>',
                    row,
                    re.S,
                )
                if len(dates) >= 2:
                    start_date = html.unescape(dates[-2].strip())
                    end_date = html.unescape(dates[-1].strip())
        entries.append((title, href, note, start_date, end_date))

    seen = set()
    unique_entries = []
    for title, href, note, start_date, end_date in entries:
        key = (title, href)
        if key in seen:
            continue
        seen.add(key)
        unique_entries.append((title, href, note, start_date, end_date))
    return unique_entries


def render_note(note):
    safe = html.escape(note)
    return safe.replace('\r\n', '\n').replace('\r', '\n').replace('\n', '<br>')

def format_date(value):
    value = value.strip()
    if not value or value == '-':
        return value
    match = re.match(r'^(\d{2})-(\d{2})-(\d{2})$', value)
    if not match:
        return value
    month, day, year = match.groups()
    return f'20{year}-{month}-{day}'


def build_html(sections):
    html_out = [
        '<!doctype html>',
        '<html lang="en">',
        '<head>',
        '  <meta charset="utf-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1">',
        '  <title>Anime List</title>',
        '  <style>',
        '    :root { color-scheme: light; }',
        '    body { font-family: Georgia, "Times New Roman", serif; margin: 24px; background: #f6f1e9; color: #2b1d18; }',
        '    h1 { margin: 0 0 16px; }',
        '    details { margin-bottom: 16px; border: 1px solid #d9c6b6; background: #fbf6ef; padding: 10px 12px; border-radius: 6px; }',
        '    summary { cursor: pointer; font-weight: bold; }',
        '    summary::-webkit-details-marker { color: #7a1f1f; }',
        '    ul { list-style: none; padding: 0; margin: 12px 0 0; }',
        '    li { padding: 10px 0; border-bottom: 1px solid #d9c6b6; }',
        '    li:last-child { border-bottom: none; }',
        '    a { color: #7a1f1f; text-decoration: none; }',
        '    a:hover { text-decoration: underline; }',
        '    .note { margin-top: 6px; color: #5b463c; font-size: 0.95em; }',
        '    .dates { margin-top: 6px; color: #5b463c; font-size: 0.9em; }',
        '    .count { color: #6b5b53; font-size: 0.95em; margin-left: 8px; }',
        '  </style>',
        '</head>',
        '<body>',
        '  <h1>Anime List</h1>',
    ]

    for title, entries, with_dates in sections:
        html_out.append('  <details>')
        html_out.append(
            f'    <summary>{html.escape(title)}<span class="count">({len(entries)})</span></summary>'
        )
        html_out.append('    <ul>')
        for entry_title, href, note, start_date, end_date in entries:
            safe_title = html.escape(entry_title)
            html_out.append('      <li>')
            html_out.append(
                f'        <a href="{href}" target="_blank" rel="noopener noreferrer">{safe_title}</a>'
            )
            if note:
                html_out.append(f'        <div class="note">{render_note(note)}</div>')
            if with_dates:
                start_label = html.escape(format_date(start_date or '-'))
                end_label = html.escape(format_date(end_date or '-'))
                html_out.append(
                    f'        <div class="dates">Started: {start_label} | Finished: {end_label}</div>'
                )
            html_out.append('      </li>')
        html_out.append('    </ul>')
        html_out.append('  </details>')

    html_out += [
        '</body>',
        '</html>',
    ]

    return '\n'.join(html_out)


def main():
    parser = argparse.ArgumentParser(description='Generate a simplified MAL list HTML.')
    parser.add_argument('--watching', default='out-watching', help='Watching HTML export path')
    parser.add_argument('--ptw', default='out-ptw', help='Plan to Watch HTML export path')
    parser.add_argument('--completed', default='out-complete', help='Completed HTML export path')
    parser.add_argument('--output', default='index.html', help='Output HTML path')
    args = parser.parse_args()

    watching_path = Path(args.watching)
    ptw_path = Path(args.ptw)
    completed_path = Path(args.completed)

    sections = [
        ('Currently Watching', parse_entries(watching_path, with_dates=True), True),
        ('Completed', parse_entries(completed_path, with_dates=True), True),
        ('Plan to Watch', parse_entries(ptw_path, with_dates=False), False),
    ]

    output_html = build_html(sections)
    Path(args.output).write_text(output_html, encoding='utf-8')


if __name__ == '__main__':
    main()
