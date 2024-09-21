import os
import shutil
import csv
import subprocess
import click
from pathlib import Path
import time
import numpy as np
import random
from bs4 import BeautifulSoup
import html
from pprint import pprint


def iter_html_files(directory: str, endswith: str = "html"):
    for filename in os.listdir(directory):
        if filename.endswith(endswith):
            file_path = os.path.join(directory, filename)
            yield file_path


def delete_except_jpg(directory):
    print(f"Cleaning dir {directory} ...")
    if not Path(directory).exists():
        return
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path) and not filename.lower().endswith(".jpg"):
            os.remove(file_path)

        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def extract_ad_page(html_code):
    soup = BeautifulSoup(html_code, "html.parser")

    infos = dict()
    infos_raw = dict()
    for criteria in soup.find_all(attrs={"data-test-id": "criteria"}):
        div_element = criteria.find("div")
        name = criteria.get("data-qa-id").replace("criteria_item_", "")
        value = div_element.get("title", None)
        infos_raw[name] = value

    infos["critair"] = int(infos_raw.get("critair", 0))
    infos["doors"] = int(infos_raw.get("doors", "0").replace("ou plus", ""))
    infos["fuel"] = infos_raw.get("fuel", "")
    infos["gearbox"] = infos_raw.get("gearbox")
    infos["horse_power_din"] = int(
        infos_raw.get("horse_power_din", "0").replace("Ch", "").strip()
    )
    infos["horsepower"] = int(
        infos_raw.get("horsepower", "0").replace("Cv", "").strip()
    )
    infos["mileage"] = int(infos_raw.get("mileage", "0").replace("km", "").strip())
    infos["year"] = int(infos_raw.get("regdate", "0").strip())
    infos["seats"] = int(infos_raw.get("seats", "0").strip())
    infos["model"] = infos_raw.get("u_utility_model", "").strip()
    infos["color"] = infos_raw.get("vehicule_color", "").strip()
    infos["brand"] = infos_raw.get("u_utility_brand", "").strip()

    ad_title = soup.find(attrs={"data-qa-id": "adview_title"})
    ad_title = html.unescape(ad_title.text)
    infos["title"] = ad_title

    # ad_price = soup.find(attrs={"data-qa-id": "aditem_price"})
    # ad_price = html.unescape(ad_price.text)
    # infos["price"] = int(ad_price.replace("\u202f", "").replace("\xa0€", ""))

    ad_price_div = soup.find("div", attrs={"data-qa-id": "adview_price"})
    ad_price = ad_price_div.find("p")
    ad_price = html.unescape(ad_price.text)
    infos["price"] = int(ad_price.replace("\u202f", "").replace("\xa0€", ""))

    if "xs" in ad_title.lower() or "l1" in ad_title.lower():
        infos["size"] = "XS"
    elif "xl" in ad_title.lower() or "l2" in ad_title.lower():
        infos["size"] = "XL"
    else:
        infos["size"] = "M"

    pprint(infos)
    return infos


@click.command()
def process_csv():

    # Clean dir
    for filepath in iter_html_files("out"):
        sub_dir = Path("out", f"{Path(filepath).stem}_fichiers")
        delete_except_jpg(sub_dir)

    records = list()
    for filepath in iter_html_files("out", ".html"):
        with open(filepath, "r") as f:
            html = f.read()

        try:
            infos = extract_ad_page(html)
            infos["target"] = Path(filepath).stem.split("_")[-1]
            records.append(infos)
        except Exception as err:
            print(err)
            print(filepath)
            raise

    output_file = "out/extract.csv"
    Path(output_file).parent.mkdir(exist_ok=True, parents=True)
    with open(output_file, "w") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
        print(f"file saved to {output_file}")


if __name__ == "__main__":
    process_csv()
