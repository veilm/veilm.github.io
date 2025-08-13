#!/usr/bin/env python3
import os
import re
from pathlib import Path
import markdown
from datetime import datetime


def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown content"""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    frontmatter = {}
    for line in parts[1].strip().split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip().strip('"')

    return frontmatter, parts[2]


def build_article(md_path, template):
    """Convert a markdown file to HTML"""
    with open(md_path, "r") as f:
        content = f.read()

    meta, md_content = parse_frontmatter(content)

    # Convert markdown to HTML with smart quotes
    html_content = markdown.markdown(md_content, extensions=["extra", "codehilite", "smarty"])

    # Build the HTML page
    html = template.replace("{{ title }}", meta.get("title", "Untitled"))
    html = html.replace("{{ content }}", html_content)
    
    # Add author/date line if date exists
    date = meta.get("date", "")
    if date and "T" in date:
        date_only = date.split("T")[0]
        author_date = f'<p>by Michael Skyba<br>(Initially written on {date_only})</p>'
    else:
        author_date = ""
    html = html.replace("{{ author_date }}", author_date)

    # Create directory for the article
    article_dir = md_path.parent / md_path.stem
    article_dir.mkdir(exist_ok=True)
    
    # Write index.html inside the article directory
    output_path = article_dir / "index.html"
    with open(output_path, "w") as f:
        f.write(html)

    print(f"Built: {md_path.name} → {article_dir.name}/index.html")
    return md_path.stem, meta


def build_index(articles, template, articles_dir):
    """Build the articles index page"""
    # Add description text - use HTML entities for smart quotes
    description = """<p>These posts are most likely of insufficient quality to live up to the
implications of the word &ldquo;article&rdquo;, but maybe they can still be better than
nothing.</p>
<a href="..">Home</a>
<hr>
"""
    
    articles_html = description + "<ul>\n"

    # Sort by date (newest first)
    sorted_articles = sorted(articles, key=lambda x: x[1].get("date", ""), reverse=True)

    for slug, meta in sorted_articles:
        title = meta.get("title", slug)
        date = meta.get("date", "")
        # Extract just the date part (YYYY-MM-DD) from the full date string
        if date and "T" in date:
            date = date.split("T")[0]
        
        # Format with date if available
        if date:
            articles_html += f'  <li>{date}: <a href="{slug}/">{title}</a></li>\n'
        else:
            articles_html += f'  <li><a href="{slug}/">{title}</a></li>\n'

    articles_html += "</ul>"

    # For the index page, use a simpler structure without header/nav
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, height=device-height, initial-scale=1">
    <title>Articles | Michael Skyba</title>
    <link rel="icon" href="/static/favicon.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=PT+Serif:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/sakura.css">
    <link rel="stylesheet" href="/static/main.css">
</head>
<body>
<h1>Articles</h1>
{articles_html}
</body>
</html>"""

    with open(articles_dir / "index.html", "w") as f:
        f.write(html)

    print(f"Built articles index")


def main():
    # Setup paths
    vanilla_dir = Path(__file__).parent
    articles_dir = vanilla_dir / "articles"
    template_file = vanilla_dir / "templates" / "article.html"

    # Load template
    if not template_file.exists():
        print(f"ERROR: Template not found at {template_file}")
        exit(1)

    with open(template_file, "r") as f:
        template = f.read()

    # Build all articles
    articles = []
    for md_file in articles_dir.glob("*.md"):
        if md_file.name != "_index.md":
            slug, meta = build_article(md_file, template)
            articles.append((slug, meta))

    # Build index page
    if articles:
        build_index(articles, template, articles_dir)


if __name__ == "__main__":
    main()
