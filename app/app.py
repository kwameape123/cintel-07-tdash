"""This web app is reactive analytics app that allow users to visualize and analyze data
base on their inputs and selections"""
# Author: Arnold Atchoe
# Date:12/5/2024

# Import need dependencies and libraries.
# Note that libraries are install using pip install and requirements.txt file
import seaborn as sns
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins
import shinyswatch
from shinywidgets import render_plotly

# Assign the palmer penguins dataframe to the variable "df"
df = palmerpenguins.load_penguins()

# Assign a web app page title and theme.
ui.page_opts(title="Penguins dashboard", fillable=True,theme=shinyswatch.theme.darkly)

# Create a sidebar that allows users to submit their inputs.
# Sidebar also provides link to resources needed by users.
with ui.sidebar(title="Filter controls"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected="Adelie"
    )
    ui.input_selectize(
    "length", "Select variable",
    choices=["bill_length_mm", "bill_depth_mm"]
    )
    ui.hr()
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

##################
# OUTPUT SECTION
##################

# This section outputs various information about dataset base on user input.
# The first value box displays the number of penguins based on user selection.
# The second values box displays average penguin bill length in mm based on user selection.
# The second values box displays average penguin bill depth in mm based on user selection.
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds"),style="color:#FF8C00; font-family:'Roboto',sans-serif;"):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal"),style="color:#FF8C00; font-family:'Roboto',sans-serif;"):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical"),style="color:#FF8C00; font-family:'Roboto',sans-serif;"):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# A related histogram is displayed based on user selection under the "Select variable" label.
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth",style="color:#FF8C00; font-family:'Roboto',sans-serif;")

        @render_plotly
        def hist():
            import plotly.express as px
            from palmerpenguins import load_penguins
            df = load_penguins()
            return px.histogram(df, x=input.length())

# A related table of data is displayed based on user selection under the "Mass" and Species labels.
# Table has columns "species","island","bill_length_mm","bill depth_mm" and "body_mass_g".
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data",style="color:#FF8C00; font-family:'Roboto',sans-serif;")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


#ui.include_css(app_dir / "styles.css")

# Define a reactive decorator to contain a function that filters data base on "species"
# selected by user as well as "mass" indicated by user.
# Filtered data is used by other decorators.
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
