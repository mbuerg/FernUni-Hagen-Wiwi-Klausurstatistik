# Visualisierung der Klausurdaten

#import plotly.graph_objects as go
import plotly.express as px
import klausurstatistik as kf
from dash import Dash, dcc, html, Input, Output

df = kf.klausurdaten

def berechne_durchschnitt(x):
    summen = [(i+1) * x[f"{j}"] for i, j in enumerate(df.iloc[0][4:9].index)]
    if x["Teilnehmer"] == 0:
        durchschnitt = 0
    else:
        durchschnitt = sum(summen) / x["Teilnehmer"]
    return durchschnitt
    

df["durchschnittsnote"] = df.apply(berechne_durchschnitt, axis = 1)


# App Layout **************************************************************

stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__, external_stylesheets = stylesheets)

app.layout = html.Div(
    [
        html.Div(
            html.H1(
                "Klausurstatistiken FernUni Hagen Wiwi", style = {"textAlign": 
                                                                "center"}
                    ), className = "row",
                ),
        html.Div(
            html.A(
                id = "my_link_1",
                children = "Fernuni Hagen Klausurstatistik Wiwi",
                href = "https://www.fernuni-hagen.de/wirtschaftswissen"\
                "schaft/studium/klausurstatistik.shtml",
                target = "_blank",
                style = {"textAlign": "center"},
                   ), className = "row",
                ),
        html.Div(dcc.Graph(id = "chart_1", figure = {}), className = "row"),
        html.Div(
            [
                html.Div(
                    dcc.Dropdown(
                        id = "dropdown_1",
                        multi = True,
                        options = [
                            {"label": x, "value": x}
                            for x in sorted(df["Modulnummer"].unique())
                                  ], value = [f"{df['Modulnummer'].min()}"],
                                ), className = "three columns",
                        ),
                html.Div(
                    dcc.Dropdown(
                        id = "dropdown_2",
                        multi = False,
                        options = [
                            {"label": x, "value": x}
                            for x in sorted(df.columns[3:])
                                  ], value = "Teilnehmer",
                                ), className = "three columns",
                        ),  
            ], className = "row",
            ),
    ]
)

    
# Callbacks ***************************************************************
@app.callback(
    Output(component_id = "chart_1", component_property = "figure"),
    [Input(component_id = "dropdown_1", component_property = "value"),
     Input(component_id = "dropdown_2", component_property = "value")],
)
def update_graph(chosen_value_1, chosen_value_2):

    if len(chosen_value_1) == 0:
        return {}
    else:
        df_filtered = df[df["Modulnummer"].isin(chosen_value_1)]
        fig = px.line(
            data_frame = df_filtered,
            x = "Semester",
            y = f"{chosen_value_2}",
            color = "Modulnummer",
            log_y = False,
            labels = {
                "Semester": "Semester",
                f"{chosen_value_2}": f"Anzahl {chosen_value_2}",
                "Modulname": "Modulnummer",
            },
        )
        return fig


if __name__ == "__main__":
    app.run_server(debug = False)
