import pandas as pd
import altair as alt

input_file = "output_3.csv"
df = pd.read_csv(input_file)

shape_scale = alt.Scale(
    domain=["XS", "M", "XL"], range=["diamond", "circle", "triangle"]
)
size_scale = alt.Scale(domain=[0, 200], range=[150, 800])


def generate_url(target):
    base_url = "https://www.leboncoin.fr/ad/utilitaires/"
    return f"{base_url}{target}"


df["url"] = df["target"].apply(generate_url)

# Create the bubble chart
bubble_chart = (
    alt.Chart(df)
    .mark_point(size=100, filled=True)
    .encode(
        x="mileage",
        y="price",
        shape=alt.Shape("size:N", scale=shape_scale),
        tooltip=[
            "price",
            "mileage",
            "title",
        ],
        # size=alt.Size("horse_power_din:Q", scale=size_scale),
        href="url:N",
    )
    .properties(width=900, height=600, title="Mileage vs Price")
)

output_file = "seaarch_chart.html"
bubble_chart.save(output_file)
print(f"graph saved to {output_file}")
