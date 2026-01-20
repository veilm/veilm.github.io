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
    for match in entry_re.finditer(src):
        href, title = match.group(1), match.group(2)
        title = html.unescape(title.strip())
        id_match = re.search(r'/(?:anime|manga)/(\d+)', href)
        if not id_match:
            continue
        anime_id = id_match.group(1)
        link_pos = match.start()
        row_start = src.rfind('<tr', 0, link_pos)
        row_end = src.find('</tr>', link_pos)
        row = ''
        if row_start != -1 and row_end != -1:
            row = src[row_start:row_end + len('</tr>')]
        note_re = re.compile(rf'id="noteRowEdit{anime_id}"\s+data-note="(.*?)"', re.S)
        note_match = note_re.search(src)
        note = ''
        if note_match:
            note = html.unescape(note_match.group(1).strip())
        score = ''
        if row:
            score_match = re.search(
                r'<span class="score-label[^"]*">\s*([^<]*)\s*</span>', row
            )
            if score_match:
                score = html.unescape(score_match.group(1).strip())
        if href.startswith('/'):
            href = 'https://myanimelist.net' + href
        start_date = ''
        end_date = ''
        if with_dates:
            date_cells = re.findall(
                r'<td class="td[12]"[^>]*width="90"[^>]*>\s*(.*?)\s*</td>',
                row,
                re.S,
            )
            cleaned_dates = []
            for cell in date_cells:
                text = re.sub(r'<[^>]+>', '', cell)
                text = html.unescape(text).strip()
                if re.match(r'^\d{2}-\d{2}-\d{2}$', text) or text == '':
                    cleaned_dates.append(text)
            if len(cleaned_dates) >= 2:
                start_date = cleaned_dates[0]
                end_date = cleaned_dates[1]
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


def add_section(sections, title, path, with_dates):
    if path.exists():
        sections.append((title, parse_entries(path, with_dates=with_dates), with_dates))


def build_html(sections, favorites_sections):
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

    for title, favorites in favorites_sections:
        html_out.append('  <details>')
        total_count = sum(len(items) for items in favorites.values())
        html_out.append(
            f'    <summary>{html.escape(title)}<span class="count">({total_count})</span></summary>'
        )
        for label in ('Anime', 'Characters', 'People'):
            items = favorites.get(label, [])
            html_out.append(
                f'    <h3>{html.escape(label)}<span class="count">({len(items)})</span></h3>'
            )
            html_out.append('    <ul>')
            if label == 'Characters':
                for name, link, work in items:
                    safe_name = html.escape(name)
                    safe_work = html.escape(work)
                    html_out.append('      <li>')
                    html_out.append(
                        f'        <a href="{link}" target="_blank" rel="noopener noreferrer">{safe_name}</a>'
                    )
                    html_out.append(f'        <div class="note">From: {safe_work}</div>')
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
    parser.add_argument('--imm-watching', default='imm-watching', help='Immersion watching HTML export path')
    parser.add_argument('--imm-ptw', default='imm-ptw', help='Immersion plan to watch HTML export path')
    parser.add_argument('--imm-watched', default='imm-watched', help='Immersion completed HTML export path')
    parser.add_argument('--manga-ptw', default='manga-plantoread', help='Manga plan to read HTML export path')
    parser.add_argument('--profile-imm', default='profile-imm', help='Immersion profile HTML export path')
    parser.add_argument('--output', default='index.html', help='Output HTML path')
    args = parser.parse_args()

    watching_path = Path(args.watching)
    ptw_path = Path(args.ptw)
    completed_path = Path(args.completed)
    profile_path = Path(args.profile)
    imm_watching_path = Path(args.imm_watching)
    imm_ptw_path = Path(args.imm_ptw)
    imm_watched_path = Path(args.imm_watched)
    manga_ptw_path = Path(args.manga_ptw)
    profile_imm_path = Path(args.profile_imm)

    sections = [
        ('Currently Watching', parse_entries(watching_path, with_dates=True), True),
        ('Completed', parse_entries(completed_path, with_dates=True), True),
        ('Plan to Watch', parse_entries(ptw_path, with_dates=False), False),
    ]
    add_section(sections, 'Immersion Watching', imm_watching_path, True)
    add_section(sections, 'Immersion Completed', imm_watched_path, True)
    add_section(sections, 'Immersion Plan to Watch', imm_ptw_path, False)
    add_section(sections, 'Manga Plan to Read', manga_ptw_path, False)

    favorites_sections = []
    if profile_path.exists():
        favorites_sections.append(('Favorites', parse_favorites(profile_path)))
    if profile_imm_path.exists():
        favorites_sections.append(('Favorites (Immersion)', parse_favorites(profile_imm_path)))
    output_html = build_html(sections, favorites_sections)
    Path(args.output).write_text(output_html, encoding='utf-8')


if __name__ == '__main__':
    main()
