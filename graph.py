import pandas as pd
import altair as alt

input_file = "out/extract.csv"
df = pd.read_csv(input_file)

# Create the bubble chart
bubble_chart = (
    alt.Chart(df)
    .mark_circle(size=60)
    .encode(
        x="mileage",
        y="price",
        color="brand:N",  # 'N' indicates the column is categorical (discrete)
        tooltip=[
            "brand",
            "model",
            "price",
            "mileage",
        ],  # Tooltip to show additional info on hover
        size="horse_power_din",  # Optional: use horsepower to size bubbles
    )
    .properties(width=600, height=400, title="Bubble Chart: Mileage vs Price")
)

# alt.renderers.enable("mimetype")
# # Display the chart
# bubble_chart.show()
bubble_chart.save("bubble_chart.html")
