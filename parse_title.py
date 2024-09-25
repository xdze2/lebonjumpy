import re
import csv
import click
from dataclasses import dataclass, asdict


@dataclass
class ModelInfo:
    brand: str
    model: str
    engine_size: str
    horsepower: str
    transmission: str
    size: str

    def __repr__(self) -> str:
        return f"ModelInfo({self.brand} {self.model} {self.size} - {self.horsepower} Cv - engine_size={self.engine_size},  transmission={self.transmission})"


def extract_vehicle_info(line) -> ModelInfo:
    brands = [
        "citro[eë]n",
        "peugeot",
        "renault",
        "mercedes-benz",
        "ford",
        "fiat",
        "opel",
    ]
    models = [
        "jumpy",
        "kangoo",
        "partner",
        "berlingo",
        "scudo",
        "proace",
        "expert",
        "trafic",
        "vito",
        "vivaro",
        "transit custom",
        "transit connect",
        "citan",
        "zoe",
        "doblo",
    ]
    brand_pattern = rf"({'|'.join(brands)})"
    model_pattern = rf"({'|'.join(models)})"
    engine_size_pattern = r"(\d\.\d)"
    horsepower_pattern = r"(\d{2,3}) ?(cv|ch)"
    transmission_pattern = r"(bvm\d|eat\d|bva\d|manuel|automatic)"
    version_pattern = r"\s(xs|xl|m|l|l1h1|l2h1|l3h1)\s"

    brand = re.search(brand_pattern, line, re.IGNORECASE)
    model = re.search(model_pattern, line, re.IGNORECASE)
    engine_size = re.search(engine_size_pattern, line)
    horsepower = re.search(horsepower_pattern, line, re.IGNORECASE)
    transmission = re.search(transmission_pattern, line, re.IGNORECASE)
    version = re.search(version_pattern, line, re.IGNORECASE)

    info = ModelInfo(
        brand=brand.group(0).capitalize() if brand else None,
        model=model.group(0).capitalize() if model else None,
        engine_size=engine_size.group(0) if engine_size else None,
        horsepower=horsepower.group(1) if horsepower else None,
        transmission=transmission.group(0).upper() if transmission else None,
        size=version.group(1).upper() if version else None,
    )
    return info


@click.command()
@click.argument("input_file", type=click.File("r"))
@click.argument("output_file", type=click.File("w"))
def parse_csv(input_file, output_file):
    """Read a CSV file, apply parsing and save the result to another CSV file."""

    data = csv.DictReader(input_file)

    parsed_data = []
    for row in data:
        extra = extract_vehicle_info(row["title"])
        row.update(asdict(extra))

        parsed_data.append(row)

        print(row["title"])
        print(extra)
        print("-")

    fieldnames = list(parsed_data[0].keys())

    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(parsed_data)
    print(f"File saved to {output_file.name}")


if __name__ == "__main__":
    parse_csv()
