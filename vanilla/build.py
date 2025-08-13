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

    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=["extra", "codehilite"])

    # Build the HTML page
    html = template.replace("{{ title }}", meta.get("title", "Untitled"))
    html = html.replace("{{ content }}", html_content)
    html = html.replace("{{ date }}", meta.get("date", ""))

    # Write HTML file next to the markdown file
    output_path = md_path.with_suffix(".html")
    with open(output_path, "w") as f:
        f.write(html)

    print(f"Built: {md_path.name} → {output_path.name}")
    return md_path.stem, meta


def build_index(articles, template, articles_dir):
    """Build the articles index page"""
    articles_html = "<ul>\n"

    # Sort by date (newest first)
    sorted_articles = sorted(articles, key=lambda x: x[1].get("date", ""), reverse=True)

    for slug, meta in sorted_articles:
        title = meta.get("title", slug)
        # Link to the .html file directly
        articles_html += f'  <li><a href="{slug}.html">{title}</a></li>\n'

    articles_html += "</ul>"

    html = template.replace("{{ title }}", "Articles")
    html = html.replace("{{ content }}", articles_html)
    html = html.replace("{{ date }}", "")

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
