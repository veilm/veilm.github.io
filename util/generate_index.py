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
        row_re = re.compile(
            rf'(<tr>.*?<a[^>]+/anime/{anime_id}[^>]*>.*?</tr>)', re.S
        )
        row_match = row_re.search(src)
        row = row_match.group(1) if row_match else ''
        note_re = re.compile(rf'id="noteRowEdit{anime_id}"\s+data-note="(.*?)"', re.S)
        note_match = note_re.search(src)
        note = ''
        if note_match:
            note = html.unescape(note_match.group(1).strip())
        score = ''
        score_re = re.compile(
            rf'id="scoreval{anime_id}".*?<span class="score-label[^"]*">\s*([^<]*)\s*</span>',
            re.S,
        )
        score_match = score_re.search(src)
        if score_match:
            score = html.unescape(score_match.group(1).strip())
        if href.startswith('/'):
            href = 'https://myanimelist.net' + href
        start_date = ''
        end_date = ''
        if with_dates:
            dates = re.findall(
                r'<td class="td[12]"[^>]*width="90"[^>]*>\s*(.*?)\s*</td>',
                row,
                re.S,
            )
            if len(dates) >= 2:
                start_date = html.unescape(dates[-2].strip())
                end_date = html.unescape(dates[-1].strip())
        entries.append((title, href, note, start_date, end_date, score))

    seen = set()
    unique_entries = []
    for title, href, note, start_date, end_date, score in entries:
        key = (title, href)
        if key in seen:
            continue
        seen.add(key)
        unique_entries.append((title, href, note, start_date, end_date, score))
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


def parse_date_for_sort(value):
    value = value.strip()
    if not value or value == '-':
        return (1, 0)
    match_mmddyy = re.match(r'^(\d{2})-(\d{2})-(\d{2})$', value)
    if match_mmddyy:
        month, day, year = match_mmddyy.groups()
        return (0, int(f'20{year}{month}{day}'))
    match_yyyymmdd = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', value)
    if match_yyyymmdd:
        year, month, day = match_yyyymmdd.groups()
        return (0, int(f'{year}{month}{day}'))
    return (1, 0)


def sort_entries(entries):
    def sort_key(entry):
        title, _href, _note, start_date, end_date, _score = entry
        start_missing, start_value = parse_date_for_sort(start_date or '-')
        end_missing, end_value = parse_date_for_sort(end_date or '-')
        return (
            start_missing,
            -start_value,
            end_missing,
            -end_value,
            title.lower(),
        )

    return sorted(entries, key=sort_key)


def parse_favorites(path):
    src = path.read_text(encoding='utf-8', errors='ignore')

    def extract_block(block_id):
        start = src.find(f'id="{block_id}"')
        if start == -1:
            return ''
        end = src.find('<h5>', start)
        if end == -1:
            end = src.find('<div class="user-comments', start)
        if end == -1:
            end = len(src)
        return src[start:end]

    def extract_items(block):
        return re.findall(r'<li class="btn-fav".*?</li>', block, re.S)

    def absolute_link(href):
        if href.startswith('/'):
            return 'https://myanimelist.net' + href
        return href

    favorites = {'Anime': [], 'Characters': [], 'People': []}

    anime_block = extract_block('anime_favorites')
    for item in extract_items(anime_block):
        title_match = re.search(r'<span class="title[^"]*">\s*(.*?)\s*</span>', item, re.S)
        link_match = re.search(r'<a href="([^"]+)"', item)
        if not title_match or not link_match:
            continue
        title = html.unescape(title_match.group(1).strip())
        link = absolute_link(link_match.group(1).strip())
        favorites['Anime'].append((title, link))

    char_block = extract_block('character_favorites')
    for item in extract_items(char_block):
        name_match = re.search(r'<span class="title[^"]*">\s*(.*?)\s*</span>', item, re.S)
        work_match = re.search(r'<span class="users">\s*(.*?)\s*</span>', item, re.S)
        link_match = re.search(r'<a href="([^"]+)"', item)
        if not name_match or not work_match or not link_match:
            continue
        name = html.unescape(name_match.group(1).strip())
        work = html.unescape(work_match.group(1).strip())
        char_link = absolute_link(link_match.group(1).strip())
        favorites['Characters'].append((name, char_link, work))

    people_block = extract_block('person_favorites')
    for item in extract_items(people_block):
        name_match = re.search(r'<span class="title[^"]*">\s*(.*?)\s*</span>', item, re.S)
        link_match = re.search(r'<a href="([^"]+)"', item)
        if not name_match or not link_match:
            continue
        name = html.unescape(name_match.group(1).strip())
        link = absolute_link(link_match.group(1).strip())
        favorites['People'].append((name, link))

    return favorites


def build_html(sections, favorites):
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

    if favorites:
        html_out.append('  <details>')
        total_count = sum(len(items) for items in favorites.values())
        html_out.append(
            f'    <summary>Favorites<span class="count">({total_count})</span></summary>'
        )
        for label in ('Anime', 'Characters', 'People'):
            items = favorites.get(label, [])
            html_out.append(f'    <h3>{html.escape(label)}<span class="count">({len(items)})</span></h3>')
            html_out.append('    <ul>')
            if label == 'Characters':
                for name, link, work in items:
                    safe_name = html.escape(name)
                    safe_work = html.escape(work)
                    html_out.append('      <li>')
                    html_out.append(
                        f'        <a href="{link}" target="_blank" rel="noopener noreferrer">{safe_name}</a>'
                    )
                    html_out.append(
                        f'        <div class="note">From: {safe_work}</div>'
                    )
                    html_out.append('      </li>')
            else:
                for name, link in items:
                    safe_name = html.escape(name)
                    html_out.append('      <li>')
                    html_out.append(
                        f'        <a href="{link}" target="_blank" rel="noopener noreferrer">{safe_name}</a>'
                    )
                    html_out.append('      </li>')
            html_out.append('    </ul>')
        html_out.append('  </details>')

    for title, entries, with_dates in sections:
        entries = sort_entries(entries)
        html_out.append('  <details>')
        html_out.append(
            f'    <summary>{html.escape(title)}<span class="count">({len(entries)})</span></summary>'
        )
        html_out.append('    <ul>')
        for entry_title, href, note, start_date, end_date, score in entries:
            safe_title = html.escape(entry_title)
            score_label = html.escape(score or '-')
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
                    f'        <div class="dates">Score: {score_label} | Started: {start_label} | Finished: {end_label}</div>'
                )
            else:
                html_out.append(f'        <div class="dates">Score: {score_label}</div>')
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
    parser.add_argument('--profile', default='profile', help='Profile HTML export path')
    parser.add_argument('--output', default='index.html', help='Output HTML path')
    args = parser.parse_args()

    watching_path = Path(args.watching)
    ptw_path = Path(args.ptw)
    completed_path = Path(args.completed)
    profile_path = Path(args.profile)

    sections = [
        ('Currently Watching', parse_entries(watching_path, with_dates=True), True),
        ('Completed', parse_entries(completed_path, with_dates=True), True),
        ('Plan to Watch', parse_entries(ptw_path, with_dates=False), False),
    ]

    favorites = parse_favorites(profile_path)
    output_html = build_html(sections, favorites)
    Path(args.output).write_text(output_html, encoding='utf-8')


if __name__ == '__main__':
    main()
