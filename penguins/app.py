import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from palmerpenguins import load_penguins
from shiny import reactive, render, req
import seaborn as sns
import pandas as pd

# Use the built-in function to load the Palmer Penguins dataset
penguins_df = load_penguins()

# Sidebar and attribute selectize
ui.page_opts(title="Sean Penguin Data", fillable=True)
with ui.sidebar(open="open"):
    ui.h2("Inputs")
    ui.input_selectize(
        "selected_attribute",
        "Select Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )

    # Plotly bins number input
    ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 50)
    
    # seaborn bins slider
    ui.input_slider(
        "seaborn_bin_count",
        "Seaborn Bin Count",
        1,
        50,
        25,
    )
    
    # Species Selection
    ui.input_checkbox_group(
        "selected_species_list",
        "Select Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie"],
        inline=True,
    )
    
    # Horizontal Rule
    ui.hr()
    
    # Link
    ui.a(
        "GitHub",
        href="https://github.com/SMStclair/cintel-02-data",
        target="_blank",
    )
    
# Accordion Tabset (click on a band to expand) for data table and grid
with ui.accordion(id="acc", open="closed"):
    with ui.accordion_panel("Data Table"):
        @render.data_frame
        def penguin_datatable():
            return render.DataTable(penguins_df)

    with ui.accordion_panel("Data Grid"):
        @render.data_frame
        def penguin_datagrid():
            return render.DataGrid(penguins_df)

# Navigation Card Tabset (Click on a tab to show contents) for 3 charts
with ui.navset_card_tab(id="tab"):
    with ui.nav_panel("Plotly Histogram"):

        @render_plotly
        def plotly_histogram():
            plotly_hist = px.histogram(
                data_frame=filtered_data(),
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species",
            ).update_layout(
                title="Plotly Penguins Data",
                xaxis_title="Selected Attribute",
                yaxis_title="Count",
            )
            return plotly_hist

    with ui.nav_panel("Seaborn Histogram"):

        @render.plot
        def seaborn_histogram():
            seaborn_hist = sns.histplot(
                data=filtered_data(),
                x=input.selected_attribute(),
                bins=input.seaborn_bin_count(),
            )
            seaborn_hist.set_title("Seaborn Penguin Data")
            seaborn_hist.set_xlabel("Selected Attribute")
            seaborn_hist.set_ylabel("Count")

    with ui.nav_panel("Plotly Scatterplot"):
        ui.card_header("Plotly Scatterplot: Species")

        @render_plotly
        def plotly_scatterplot():
            plotly_scatter = px.scatter(
                filtered_data(),
                x="bill_depth_mm",
                y="bill_length_mm",
                color="species",
                size_max=8,
                labels={
                    "bill_depth_mm": "Bill Depth (mm)",
                    "bill_length_mm": "Bill Length(mm)",
                },
            )
            return plotly_scatter

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    return penguins_df[penguins_df["species"].isin(input.selected_species_list())]
