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


def build_article(md_path, template, output_dir):
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

    # Create output path
    article_name = md_path.stem
    article_dir = output_dir / article_name
    article_dir.mkdir(exist_ok=True)

    # Write HTML file
    output_path = article_dir / "index.html"
    with open(output_path, "w") as f:
        f.write(html)

    print(f"Built: {md_path.name} → {output_path}")
    return article_name, meta


def build_index(articles, template, output_dir):
    """Build the articles index page"""
    articles_html = "<ul>\n"

    # Sort by date (newest first)
    sorted_articles = sorted(articles, key=lambda x: x[1].get("date", ""), reverse=True)

    for slug, meta in sorted_articles:
        title = meta.get("title", slug)
        articles_html += f'  <li><a href="/articles/{slug}/">{title}</a></li>\n'

    articles_html += "</ul>"

    html = template.replace("{{ title }}", "Articles")
    html = html.replace("{{ content }}", articles_html)
    html = html.replace("{{ date }}", "")

    with open(output_dir / "index.html", "w") as f:
        f.write(html)

    print(f"Built articles index")


def main():
    # Setup paths
    vanilla_dir = Path(__file__).parent
    articles_dir = vanilla_dir / "articles"
    output_dir = vanilla_dir / "public" / "articles"
    template_file = vanilla_dir / "templates" / "article.html"

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

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
            slug, meta = build_article(md_file, template, output_dir)
            articles.append((slug, meta))

    # Build index page
    if articles:
        build_index(articles, template, output_dir)


if __name__ == "__main__":
    main()
