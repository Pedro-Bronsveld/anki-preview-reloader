from markdown import markdownFromFile, Extension, Markdown
from markdown.blockprocessors import BlockProcessor
from markdown.treeprocessors import Treeprocessor
from urllib.parse import urljoin
import xml.etree.ElementTree as etree
from pathlib import Path
import re
import io
from bs4 import BeautifulSoup

# Converts README.md to an html subset that can be used as add-on description on Anki Web.

class HeadingBlockProcessor(BlockProcessor):
    re_heading_start: str = r'^#+'

    def test(self, parent: etree.Element, block: str) -> bool:
        return re.match(self.re_heading_start, block)
    
    def run(self, parent: etree.Element, blocks: list[str]) -> bool | None:
        block = blocks[0]
        element = etree.SubElement(parent, "b")
        element.text = block[re.match(self.re_heading_start, block).end():].strip()
        blocks.pop(0)
        return True

class ImgSrcPrefixer(Treeprocessor):
    url_base: str = "https://raw.githubusercontent.com/Pedro-Bronsveld/anki-preview-reloader/main/"
    
    def run(self, root: etree.Element) -> etree.Element | None:
        for img in root.iter('img'):
            img.set('src', urljoin(self.url_base, img.get('src')))

class AnkiWebExtension(Extension):    
    def extendMarkdown(self, md: Markdown):
        md.parser.blockprocessors.register(HeadingBlockProcessor(md.parser), "description", 175)
        md.treeprocessors.register(ImgSrcPrefixer(md), "imgprefixer", 10)

def main():
    root_directory = Path(__file__).parent
    readme_path = root_directory.parent.joinpath("README.md")
    description_html = root_directory.joinpath("ankiweb_description.html")
    
    html_bytes = io.BytesIO()
    print(f"Converting markdown from {readme_path} to html in {description_html}")
    markdownFromFile(input=str(readme_path.absolute()), output=html_bytes, extensions=[AnkiWebExtension()])

    soup = BeautifulSoup(html_bytes.getvalue().decode("utf-8"), 'html.parser')

    output_html = ""
    for tag in soup.children:
        tag_str = str(tag)
        output_html += tag_str if tag_str == "\n" else tag_str + "\n"

    with open(description_html, 'w') as output_file:
        output_file.write(output_html)

    print("Converting done")
    print(f"Output file: {description_html.absolute()}")

if __name__ == "__main__":
    main()
