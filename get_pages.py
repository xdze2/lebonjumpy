import csv
import subprocess
import click
from pathlib import Path
import time
import numpy as np
import random


@click.command()
@click.argument("csv_file", type=click.Path(exists=True))
def process_csv(csv_file):

    base_url = "https://www.leboncoin.fr/ad/utilitaires/"
    Path("out").mkdir(parents=True, exist_ok=True)
    with open(csv_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        records = [row for row in reader]

    random.shuffle(records)

    for row in records:
        target = row["target"]
        print(target)

        target_url = base_url + str(target)

        target_filename = f"out/ad_page_{target}.html"
        if Path(target_filename).exists():
            print(f"page {target} already done. skip.")
        subprocess.run(
            ["./download_page.sh", "-d", f"out/ad_page_{target}.html", target_url]
        )

        wait_time = np.random.poisson(5)
        print(f"waiting {wait_time}s before next download...")
        time.sleep(wait_time)
        break


if __name__ == "__main__":
    process_csv()
