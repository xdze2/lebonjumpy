import csv
import html
import os
from pprint import pprint
from typing import Dict

import click
from bs4 import BeautifulSoup


def parse_ad_item(soup):

    infos = dict()

    ad_target = soup.get("href")
    infos["target"] = ad_target.split("/")[-1]

    ad_title = soup.find(attrs={"data-qa-id": "aditem_title"})
    ad_title = html.unescape(ad_title.get("title"))
    infos["title"] = ad_title.lower()

    ad_price = soup.find(attrs={"data-qa-id": "aditem_price"})
    ad_price = html.unescape(ad_price.text)
    infos["price"] = int(ad_price.replace("\u202f", "").replace("\xa0€", ""))

    ad_params = soup.find(attrs={"data-test-id": "ad-params-light"})
    ad_params = html.unescape(ad_params.text)

    y, km, nrj, bv = ad_params.strip("·").split("·")
    infos["year"] = int(y)
    infos["mileage"] = int(km.replace(" km", ""))
    infos["nrj"] = nrj.lower()
    infos["bv"] = bv

    # print("---")
    # pprint(infos)

    return infos


def parse_result_page(html_code) -> Dict:
    soup = BeautifulSoup(html_code, "html.parser")

    aditem_container = soup.find_all(attrs={"data-qa-id": "aditem_container"})
    print(len(aditem_container), "items")

    records = dict()
    for it in aditem_container:
        try:
            out = parse_ad_item(it)
            if out["target"] in records:
                print(f"duplicate {out['target']}: title {out['title']}")
                continue
            records[out["target"]] = out
        except AttributeError as err:
            print(f"AttributeError on out['target']: {err}. Ignored.")

    return list(records.values())


def iter_html_pages(directory: str):
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            yield os.path.join(directory, filename)


@click.command()
@click.argument("output_file", type=click.File("w"))
def filter_html(output_file):

    records = list()
    for file_path in iter_html_pages("pages"):
        with open(file_path, "r", encoding="utf-8") as file:
            html_code = file.read()
        try:
            new_records = parse_result_page(html_code)
            records.extend(new_records)
        except Exception as err:
            print(file_path)
            raise err

    writer = csv.DictWriter(output_file, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)

    print("")
    click.echo(f"Filtered content saved to {output_file.name}")


if __name__ == "__main__":
    filter_html()
