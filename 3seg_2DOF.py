import math
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc

def calculateXY(L1,L2,A1,A2):
    p0 = [0,0]
    p1 = [p0[0]+L1*math.cos(A1*math.pi/180),p0[1]+L1*math.sin(A1*math.pi/180)]
    p2 = [p1[0]+L2*math.cos((A1+A2)*math.pi/180),p1[1]+L2*math.sin((A1+A2)*math.pi/180)]
    x, y = [],[]
    listPoints = [p0,p1,p2]
    for i in listPoints:
        x.append(i[0])
        y.append(i[1])
    return x, y

A1 = 45
A2 = 25

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])


fig = go.Figure(
    data=go.Scatter(x=[], y=[], line=dict(color="crimson")),
    layout=dict(title=dict(text="xxx"), width=400, height=400,margin=dict(l=30, r=30, t=30, b=30)),
)

app.layout = html.Div([
    dcc.Interval(
        id='timerJ',
        interval=40,    #25Hz
        n_intervals=-1,
    ),
    dbc.Row([
        dbc.Col([
            daq.Joystick(
                id='joystick1',
                label="L1 move",
                angle=0
            ),
            daq.Joystick(
                id='joystick2',
                label="L2 move",
                angle=0
            ),
        ],width='auto'),
        dbc.Col([
            daq.NumericInput(
                id='L1',
                label='L1 length : ',
                labelPosition='top',
                min=0,
                max=100,
                size=80,
                value=10,
                persistence=True,
            ),
            daq.NumericInput(
                id='L2',
                label='L2 length : ',
                labelPosition='top',
                min=0,
                max=100,
                size=80,
                value=20,
                persistence=True,
            ),
            daq.NumericInput(
                id='A1',
                label='L1 angle : ',
                labelPosition='top',
                min=-360,
                max=180,
                size=80,
                value=45,
                persistence=True,
            ),
            daq.NumericInput(
                id='A2',
                label='L2 angle : ',
                labelPosition='top',
                min=-360,
                max=360,
                size=80,
                value=5,
                persistence='value',
            ),
        ],width='auto'),
    ]),
    dbc.Row(dcc.Graph(id='graph',figure=fig,
                      config={
                            # 'scrollZoom': True,
                            # 'displaylogo': False,
                            # 'displayModeBar': False,
                            'staticPlot': True,
                        }),style={'padding':20})
],style={'padding':20})

@app.callback(
    Output('graph', 'figure'),
    Input('L1', 'value'),
    Input('L2', 'value'),
    Input('A1', 'value'),
    Input('A2', 'value'),
    State('graph', 'figure'),
)
def updateGraph(L1,L2,A11,A22,figure):
    global A1,A2
    x, y = calculateXY(L1,L2,A1,A2)
    figure['data'][0]['x']=x
    figure['data'][0]['y']=y
    figure['layout']['yaxis']={'range':[-(L1+L2)-2,(L1+L2)*1+2]}
    figure['layout']['xaxis']={'range':[-(L1+L2)-2,(L1+L2)*1+2]}
    figure['layout']['title']='x:{} y:{}'.format(round(x[2],1),round(y[2],1))
    return figure


@app.callback(
    Output('A1', 'value'),
    Output('A2', 'value'),

    # State('timerJ','n_intervals'),
    # Input('joystick1', 'angle'),
    # Input('joystick1', 'force'),

    Input('timerJ','n_intervals'),
    State('joystick1', 'angle'),
    State('joystick1', 'force'),

    State('L1', 'value'),
    State('L2', 'value'),
    State('A1', 'value'),
    State('A2', 'value'),
)
def updateAngle(interval,angle,force,L1,L2,A11,A22):
    global A1,A2
    xPrevious, yPrevious = calculateXY(L1,L2,A1,A2)
    x, y = calculateXY(L1,L2,A1,A2)
    if angle!=None and force!=None:
        if force > 1:
            force = 1
        if 315 <= angle or angle < 45:
            x[2] += force
            # print('x+')
        if 45 <= angle and angle < 135:
            y[2] += force
            # print('y+')
        if 135 <= angle and angle < 225:
            x[2] -=  force
            # print('x-')
        if 225 <= angle and angle < 315:
            y[2] -=  force
            # print('y-')

        if math.sqrt(x[2]**2+y[2]**2) > L1+L2 or math.sqrt(x[2]**2+y[2]**2) < abs(L1-L2):
            x[2] = xPrevious[2]
            y[2] = yPrevious[2]
            # print('!!! reach limit !!!',math.sqrt(x[2]**2+y[2]**2))
        
        if x[2]-L1-L2==0:
            x[2]=0.0001
            # print('x=0')
    
    # print("xP : {} yP : {}".format(xPrevious,yPrevious))
    # print("xF : {} yF : {}".format(x,y))
    L = math.sqrt(x[2]**2+y[2]**2)
    # print("A1 : {} \nA2 : {}".format(A1,A2))

    A1 = (math.atan(y[2]/x[2])-math.acos((L1**2+L**2-L2**2)/(2*L1*L)))/math.pi*180
    if x[2] < 0:
        A1 += 180
    A2 = (math.pi-math.acos((L1**2+L2**2-L**2)/(2*L1*L2)))/math.pi*180

    # print("A1 : {} \nA2 : {}\n---------".format(A1,A2))
    return A1,A2

if __name__ == '__main__':
    app.run_server(debug=True)