import pandas as pd
import altair as alt
import click


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
def graph(input_file: str) -> None:

    df = pd.read_csv(input_file)

    shape_scale = alt.Scale(
        domain=["XS", "M", "XL"], range=["diamond", "circle", "triangle"]
    )
    size_scale = alt.Scale(domain=[0, 200], range=[150, 800])

    def generate_url(target):
        base_url = "https://www.leboncoin.fr/ad/utilitaires/"
        return f"{base_url}{target}"

    def get_size(ad_title):
        if "xs" in ad_title.lower() or "l1" in ad_title.lower():
            return "XS"
        elif "xl" in ad_title.lower() or "l2" in ad_title.lower():
            return "XL"
        else:
            return "M"

    MODELS = [
        "jumpy",
        "kangoo",
        "berlingo",
        "proace",
        "expert",
        "master",
        "nv300",
        "nv200",
        "crafter",
    ]

    def get_model(ad_title):
        return f"{ad_title['model']} {ad_title['size']}"

    def get_usage(row):
        return row["mileage"] / (2025 - row["year"])

    df["url"] = df["target"].apply(generate_url)
    df["size"] = df["title"].apply(get_size)
    df["model"] = df.apply(get_model, axis=1)
    df["usage"] = df.apply(get_usage, axis=1)

    df = df[(df["mileage"] > 0) & (df["price"] > 0)]

    model_selection = alt.selection_point(
        fields=["model"],
        value=[{"model": n} for n in df["model"].unique()],
        toggle=True,
        bind="legend",
    )

    cond = alt.condition(model_selection, alt.Color("model:N"), alt.value("lightgray"))

    bubble_chart = (
        alt.Chart(df)
        .mark_point(size=100, filled=True)
        .encode(
            x=alt.X("mileage:Q", scale=alt.Scale()),
            y=alt.Y("price:Q", scale=alt.Scale()),
            shape=alt.Shape("size:N", scale=shape_scale),
            color="model:N",
            tooltip=[
                "price",
                "mileage",
                "title",
            ],
            # size=alt.Size("horse_power_din:Q", scale=size_scale),
            href="url:N",
        )
        .add_params(model_selection)
        .encode(color=cond)
        .properties(width=900, height=600, title="Mileage vs Price")
    )

    output_file = "search_chart.html"
    bubble_chart.save(output_file)
    print(f"graph saved to {output_file}")


if __name__ == "__main__":
    graph()
