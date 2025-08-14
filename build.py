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
    html_content = markdown.markdown(
        md_content, extensions=["extra", "codehilite", "smarty"]
    )

    # Build the HTML page
    html = template.replace("{{ title }}", meta.get("title", "Untitled"))
    html = html.replace("{{ content }}", html_content)

    # Add author/date line if date exists
    date = meta.get("date", "")
    if date and "T" in date:
        date_only = date.split("T")[0]
        author_date = f"<p>by Michael Skyba<br>(Initially written on {date_only})</p>"
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


def build_index(articles, index_template, articles_dir):
    """Build the articles index page"""
    articles_html = "<ul>\n"

    # Sort by date (newest first)
    sorted_articles = sorted(articles, key=lambda x: x[1].get("date", ""), reverse=True)

    for slug, meta in sorted_articles:
        title = meta.get("title", slug)
        date = meta.get("date", "")

        # Format date as "Aug 2025" if available
        if date:
            # Extract just the date part (YYYY-MM-DD) from the full date string
            if "T" in date:
                date = date.split("T")[0]

            # Parse and format as "Mon YYYY"
            try:
                dt = datetime.strptime(date, "%Y-%m-%d")
                formatted_date = dt.strftime("%b %Y")
                articles_html += f'  <li><span style="display: inline-block; width: 4.5em; text-align: right;">{formatted_date}</span>: <a href="{slug}/">{title}</a></li>\n'
            except ValueError:
                # Fallback if date parsing fails
                articles_html += f'  <li><a href="{slug}/">{title}</a></li>\n'
        else:
            articles_html += f'  <li><a href="{slug}/">{title}</a></li>\n'

    articles_html += "</ul>"

    # Replace placeholder in template
    html = index_template.replace("{{ articles_list }}", articles_html)

    with open(articles_dir / "index.html", "w") as f:
        f.write(html)

    print(f"Built articles index")


def main():
    # Setup paths
    vanilla_dir = Path(__file__).parent
    articles_dir = vanilla_dir / "articles"
    article_template_file = vanilla_dir / "templates" / "article.html"
    index_template_file = vanilla_dir / "templates" / "articles_index.html"

    # Load article template
    if not article_template_file.exists():
        print(f"ERROR: Article template not found at {article_template_file}")
        exit(1)

    with open(article_template_file, "r") as f:
        article_template = f.read()

    # Load index template
    if not index_template_file.exists():
        print(f"ERROR: Index template not found at {index_template_file}")
        exit(1)

    with open(index_template_file, "r") as f:
        index_template = f.read()

    # Build all articles
    articles = []
    for md_file in articles_dir.glob("*.md"):
        if md_file.name != "_index.md":
            slug, meta = build_article(md_file, article_template)
            articles.append((slug, meta))

    # Build index page
    if articles:
        build_index(articles, index_template, articles_dir)


if __name__ == "__main__":
    main()
