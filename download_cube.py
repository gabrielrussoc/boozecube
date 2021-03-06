#!/usr/bin/env python3

from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
from contextlib import closing
from io import BytesIO
import tarfile
import json
import click
from pathlib import Path

# Downloads all the card images from http://theboozecube.blogspot.com and puts it into an archive (.tar.gz)

URLS = [
    "http://theboozecube.blogspot.com/p/white.html",  # White
    "http://theboozecube.blogspot.com/p/blue_25.html",  # Blue
    "http://theboozecube.blogspot.com/p/blog-page_25.html",  # Black
    "http://theboozecube.blogspot.com/p/red.html",  # Red
    "http://theboozecube.blogspot.com/p/blog-page_4334.html",  # Green
    "http://theboozecube.blogspot.com/p/blog-page_9031.html",  # Multicolor
    "http://theboozecube.blogspot.com/p/blog-page_3190.html",  # Split
    "http://theboozecube.blogspot.com/p/artifact.html",  # Artifact
    "http://theboozecube.blogspot.com/p/blog-page_5683.html",  # Land
    "http://theboozecube.blogspot.com/p/tokens.html",  # Tokens
    "http://theboozecube.blogspot.com/p/blog-page_19.html",  # Elder dragon hangover
]


@click.command()
def main() -> None:
    cards_urls = []

    for url in URLS:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        # Every card image seems to be inside an <a> tag and the URL contains '/s1600/'
        a_tags = soup.find_all('a')
        for a in a_tags:
            href = a.get("href")
            if href and "/s1600/" in href:
                cards_urls.append(href)

    # Dedupe
    cards_urls = sorted(set(cards_urls))

    output_filename = Path("cube.tar.gz")

    with click.progressbar(length=len(cards_urls), label=f"Downloading cube to {output_filename}") as bar:
        img_to_url = {}
        with tarfile.open(output_filename, "w:gz") as tar:
            for url in cards_urls:
                bar.update(1)
                with closing(BytesIO(urlopen(url).read())) as file_obj:
                    # http://2.bp.blogspot.com/-Ofpsm4x0D7o/Uw1MSdkxgLI/AAAAAAAAE7I/7bHNq0bvegM/s1600/Harsh+Comedown.jpg'
                    filename = url.split("/")[-1]
                    tarinfo = tarfile.TarInfo(filename)
                    tarinfo.size = len(file_obj.getvalue())
                    tar.addfile(tarinfo, fileobj=file_obj)
                    img_to_url[filename] = url
            with closing(BytesIO(json.dumps(img_to_url).encode())) as file_obj:
                tarinfo = tarfile.TarInfo("urls.json")
                tarinfo.size = len(file_obj.getvalue())
                tar.addfile(tarinfo, fileobj=file_obj)

    print("Finished downloading cube")


if __name__ == "__main__":
    main()
