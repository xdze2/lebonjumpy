import csv
import html
import os
from pprint import pprint

import click
from bs4 import BeautifulSoup


def parse_ad_item(soup):
    print("---")
    infos = dict()

    ad_target = soup.get("href")
    infos["target"] = ad_target.split("/")[-1]

    ad_title = soup.find(attrs={"data-qa-id": "aditem_title"})
    ad_title = html.unescape(ad_title.get("title"))
    infos["title"] = ad_title

    ad_price = soup.find(attrs={"data-qa-id": "aditem_price"})
    ad_price = html.unescape(ad_price.text)
    infos["price"] = int(ad_price.replace("\u202f", "").replace("\xa0€", ""))

    ad_params = soup.find(attrs={"data-test-id": "ad-params-light"})
    ad_params = html.unescape(ad_params.text)

    y, km, nrj, bv = ad_params.strip("·").split("·")
    infos["year"] = int(y)
    infos["km"] = int(km.replace(" km", ""))
    infos["nrj"] = nrj
    infos["bv"] = bv

    pprint(infos)

    return infos


def keep_only_aditem_container(html_code):
    soup = BeautifulSoup(html_code, "html.parser")

    aditem_container = soup.find_all(attrs={"data-qa-id": "aditem_container"})
    print(len(aditem_container), "items")

    records = list()
    for it in aditem_container:
        out = parse_ad_item(it)
        records.append(out)

    return records


def iter_html_pages(directory: str):
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            file_path = os.path.join(directory, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                yield file.read()


@click.command()
@click.argument("output_file", type=click.File("w"))
def filter_html(output_file):

    records = list()
    for html_code in iter_html_pages("pages"):
        new_records = keep_only_aditem_container(html_code)
        records.extend(new_records)

    writer = csv.DictWriter(output_file, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)

    print("")
    click.echo(f"Filtered content saved to {output_file.name}")


if __name__ == "__main__":
    filter_html()
