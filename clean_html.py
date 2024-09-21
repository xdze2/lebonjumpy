import click
from bs4 import BeautifulSoup


def remove_script_tags(html_code):
    soup = BeautifulSoup(html_code, "html.parser")

    to_remove = (
        "head",
        "esi-surround",
        "nav",
        "script",
        "svg",
        "noscript",
        "link",
        "path",
        "iframe",
        "svg",
    )

    for tag_name in to_remove:
        for script_tag in soup.find_all(tag_name):
            script_tag.decompose()

    return str(soup)


@click.command()
@click.argument("input_file", type=click.File("r"))
@click.argument("output_file", type=click.File("w"))
def clean_html(input_file, output_file=None):
    """Remove script tags from an HTML file and save the result to a new file."""
    html_code = input_file.read()
    cleaned_html = remove_script_tags(html_code)
    output_file.write(cleaned_html)
    click.echo(f"Script tags removed and output saved to {output_file.name}")


if __name__ == "__main__":
    clean_html()
