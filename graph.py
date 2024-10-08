import pandas as pd
import altair as alt

input_file = "out/extract.csv"
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
        color="model:N",
        shape=alt.Shape("size:N", scale=shape_scale),
        tooltip=[
            "brand",
            "model",
            "price",
            "mileage",
            "size",
            "title",
            "horse_power_din",
        ],
        size=alt.Size("horse_power_din:Q", scale=size_scale),
        href="url:N",  # Add the URL column for clickability
    )
    .properties(width=900, height=600, title="Bubble Chart: Mileage vs Price")
)

# alt.renderers.enable("mimetype")
# # Display the chart
# bubble_chart.show()
output_file = "bubble_chart.html"
bubble_chart.save(output_file)
print(f"graph saved to {output_file}")
