import plotly.graph_objects as graphObj
import plotly.figure_factory as ff
import plotly.express as px
import pandas as pd


def get_bar_graph_stack(names, x_values, y_values):
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


def get_bar_graph_basic(x_values, y_values, text, colors):
    fig = graphObj.Figure([
        graphObj.Bar(
            x=x_values,
            y=y_values,
            text=y_values,
            textposition='outside',
            hovertext=text,
            marker_color=colors,
        )
    ])
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=400)
    return fig


def get_pie_chart(labels, values):
    fig = graphObj.Figure(data=[graphObj.Pie(labels=labels, values=values)])
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=450)
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


def get_speaker_arg_graph(table_data, x_values, y_values):
    fig = ff.create_table(table_data, height_constant=60)

    # create bar graph trace
    trace1 = graphObj.Bar(x=x_values, y=y_values, xaxis='x2', yaxis='y2',
                          marker=dict(color='#0099ff'),
                          name='# of Arguments<br>Per Speaker')

    # Add trace to figure
    fig.add_traces([trace1])

    fig['layout']['xaxis2'] = {}
    fig['layout']['yaxis2'] = {}

    # layout for subplots
    fig.layout.yaxis.update({'domain': [0, .45]})
    fig.layout.yaxis2.update({'domain': [.6, 1]})

    # Anchor yaxis2 to xaxis2 and vice versa
    fig.layout.yaxis2.update({'anchor': 'x2'})
    fig.layout.xaxis2.update({'anchor': 'y2'})
    fig.layout.yaxis2.update({'title': '# of Arguments Made'})

    fig.layout.margin.update({'t': 75, 'l': 50})
    fig.layout.update({'height': 1200})

    return fig


def get_speaker_table_dot_graph(speaker_names, x_values, y_values, arg_type):
    # create dataframe for graph of values
    df = pd.DataFrame(dict(total_arg=y_values, arg=x_values,
                           speakers=speaker_names))

    fig = px.scatter(df, x="arg", y="total_arg",
                     color="speakers",
                     title=arg_type + " Arguments per Speaker",
                     labels={
                         "arg": "# of " + arg_type + " Arguments per speaker",
                         "total_arg": "Total # of Arguments made by speaker",
                         "speakers": "Name"
                     })
    # make dots larger for visibility
    fig.update_traces(marker=dict(size=20))
    fig.layout.margin.update({'t': 75, 'l': 50})
    fig.layout.update({'height': 600})

    return fig
