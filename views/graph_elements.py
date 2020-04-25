import plotly.graph_objects as graphObj


def get_bar_graph(names, x_values, y_values):
    data = []
    for i in range(len(names)):
        data.append(graphObj.Bar(
            name=names[i],
            x=x_values,
            y=y_values[i],
            text=y_values[i]
        ))

    fig = graphObj.Figure(data)

    # Change the bar mode
    fig.update_layout(barmode='stack')
    # fig.show()
    return fig


def get_pie_chart(labels, values):
    fig = graphObj.Figure(data=[graphObj.Pie(labels=labels, values=values)])
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    return fig


def get_sunburst_graph(labels, parents, values):
    fig = graphObj.Figure(
        graphObj.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
        )
    )
    return fig
