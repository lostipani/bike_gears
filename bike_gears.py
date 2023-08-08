import dash
import re
import plotly.express as px
import pandas as pd
import numpy as np


# instantiate components
app = dash.Dash(__name__)
inpFront = dash.dcc.Input(value='36, 50', type='text')
inpRear  = dash.dcc.Input(value='11, 13, 15, 17, 19, 21, 23, 25, 28', type='text')
heatmap  = dash.dcc.Graph(id="heatmap")

# set layout by putting together components
app.layout = dash.html.Div(id="layout",
                           children=[
                                     dash.html.H1(children='Bike: gear ratios', style={'font-family':'Arial, sans-serif'}), # title
                                     dash.html.Div(["Front chainrings", inpFront, "Rear sprockets", inpRear], style={'font-family':'Arial, sans-serif'}), # input fields
                                     dash.html.Br(), # newline
                                     heatmap # output field
                                    ]
                           )

# define callback function via decorator: set output/input to related components
@dash.callback(
    dash.Output(heatmap, 'figure'),
    dash.Input(inpFront, 'value'),
    dash.Input(inpRear, 'value')
)
def update_fig(inp_front, inp_rear):
    # subroutine to evaluate gear ratios
    def get_gear_ratio(frontGears: list, rearGears: list) -> np.ndarray:
      n_chainring = len(front_gears)
      n_sprocket  = len(rear_gears)
      gear_ratio  = np.zeros((n_chainring, n_sprocket), dtype=float)
      for i in range(n_chainring):
        for j in range(n_sprocket):
          gear_ratio[i, j] = np.format_float_positional(float(front_gears[i]/rear_gears[j]), precision=2)
      return gear_ratio

    # take input strings and convert to lists and create np.array for ticks
    front_gears = [int(n) for n in re.findall(r'\d+', inp_front)]
    rear_gears  = [int(n) for n in re.findall(r'\d+', inp_rear)]
    yticks = np.array(range(len(front_gears)))
    xticks = np.array(range(len(rear_gears)))

    # instantiate px.imshow obj
    fig = px.imshow(
                    get_gear_ratio(front_gears, rear_gears),
                    labels=dict(x="Rear sprocket", y="Front chainring", color="Ratio"),
                    x=xticks,
                    y=yticks,
                    text_auto=True,
                    aspect="auto"
                   )
    # cosmetics
    fig.update_layout(
                      xaxis=dict(tickmode='array', tickvals=xticks, ticktext = np.array(rear_gears)),
                      yaxis=dict(tickmode='array', tickvals=yticks, ticktext = np.array(front_gears))
                     )
    fig.add_shape(type="rect", xref="paper", yref="paper", x0=0, y0=0, x1=1.0, y1=1.0, line=dict(color="black", width=3))
    fig.update(layout_coloraxis_showscale=False)

    return fig

if __name__ == '__main__':
    app.run(debug=True)
