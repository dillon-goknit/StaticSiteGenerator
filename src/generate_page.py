import os

from extract_title import extract_title
from markdown_to_html import markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    content_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, "w") as f:
        f.write(page)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    for entry in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, entry)
        dst_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(src_path):
            if src_path.endswith(".md"):
                html_dst = dst_path[:-3] + ".html"
                generate_page(src_path, template_path, html_dst)
        else:
            generate_pages_recursive(src_path, template_path, dst_path)
