import math
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc

import os

def fowardKinematics(L1=1,L2=1,A1=0,A2=0):
    p0 = [0,0]
    p1 = [p0[0]+L1*math.cos(A1*math.pi/180),p0[1]+L1*math.sin(A1*math.pi/180)]
    p2 = [p1[0]+L2*math.cos((A1+A2)*math.pi/180),p1[1]+L2*math.sin((A1+A2)*math.pi/180)]
    x, y = [],[]
    listPoints = [p0,p1,p2]
    for i in listPoints:
        x.append(i[0])
        y.append(i[1])
    return x, y

# init value
A1 = 45
A2 = 25
moved=False
text = ""

# # plot all possibility
# import matplotlib.pyplot as plt
# xp, yp = [],[]
# for A1 in range(-90,180,5):
#     for A2 in range(0,181,5):
#         x, y = fowardKinematics(1,1,1,A1,A2)
#         xp.append(x[2])
#         yp.append(y[2])
# plt.plot(xp,yp,'ro')
# plt.show()

# init application
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],title='FK/IK dev',update_title=None)

# init figure of arms
fig = go.Figure(
    data=go.Scatter(x=[], y=[], line=dict(color="crimson")),
    layout=dict(title=dict(text="x: y: "), width=350, height=350,margin=dict(l=25, r=25, t=25, b=25)),
)

# create IU
app.layout = html.Div([

    # interval timer
    dcc.Interval(
        id='timerJ',
        interval=40,    #25Hz
        n_intervals=-1,
    ),

    dbc.Row([
        
        # 1st column
        dbc.Col([
            
            # Force limit
            dbc.Row(dbc.Col(
                daq.BooleanSwitch(
                    id='Force limit',
                    on=True,
                    label="Force limit",
                    labelPosition="top",
                    color="orange",
                ),
                width='auto',
                style={'paddingLeft':165,'paddingRight':10,'paddingTop':0,'paddingBottom':10},
            )),
            
            # Joystick 1
            dbc.Row(dbc.Col(
                daq.Joystick(
                    id='joystick1',
                    label="Sigle axis move",
                    angle=0
                ),
                width='auto',
                style={'paddingLeft':145,'paddingRight':20,'paddingTop':0,'paddingBottom':0},
            )),
            
            # Joystick 2
            dbc.Row(dbc.Col(
                daq.Joystick(
                    id='joystick2',
                    label="Double axis move",
                    angle=0,
                    # style={'border':'3px solid red'},
                ),
                width='auto',
                style={'paddingLeft':145,'paddingRight':20,'paddingTop':0,'paddingBottom':0},
            )),
            
            # Graph
            dbc.Row(
                dcc.Graph(
                    id='graph',
                    figure=fig,
                    config={
                        'scrollZoom': True,
                        'displaylogo': False,
                        'displayModeBar': False,
                        'staticPlot': True,
                    },
                ),
                style={'padding':10},
            ),
        
        ],width='auto'),
        
        # 2nd column
        dbc.Col([

            # 1st articulation lenght
            dbc.Row(
                daq.Slider(
                    id='L1',
                    handleLabel={"showCurrentValue": True,"label":"L1"},
                    marks={"1":"1","50":"50","99":"99"},
                    vertical=True,
                    min=1,
                    max=99,
                    size=195,
                    value=10,
                    step=1,
                    persistence=True,
                ),
                style={'paddingLeft':-40,'paddingRight':10,'paddingTop':15,'paddingBottom':15},
            ),

            # 2nd articulation lenght
            dbc.Row(
                daq.Slider(
                    id='L2',
                    handleLabel={"showCurrentValue": True,"label":"L2"},
                    marks={"1":"1","50":"50","99":"99"},
                    vertical=True,
                    min=1,
                    max=99,
                    size=195,
                    value=10,
                    step=1,
                    persistence=True,
                ),
                style={'paddingLeft':-40,'paddingRight':10,'paddingTop':15,'paddingBottom':15},
            ),
            
        ],width='auto'),
        
        # 3rd column
        dbc.Col([

            # A1
            dbc.Row(
                daq.Slider(
                    id='A1',
                    handleLabel={"showCurrentValue": True,"label":"A1"},
                    marks={"-270":"-270","0":"0","270":"270"},
                    vertical=True,
                    min=-270,
                    max=270,
                    size=195,
                    value=45,
                    step=0.1,
                    updatemode='drag',
                    persistence=True,
                ),
                style={'paddingLeft':60,'paddingRight':10,'paddingTop':15,'paddingBottom':15},
            ),
            
            # A2
            dbc.Row(
                daq.Slider(
                    id='A2',
                    handleLabel={"showCurrentValue": True,"label":"A2"},
                    marks={"0":"0","90":"90","180":"180"},
                    vertical=True,
                    min=0,
                    max=180,
                    size=195,
                    value=25,
                    step=0.1,
                    updatemode='drag',
                    persistence=True,
                ),
                style={'paddingLeft':60,'paddingRight':10,'paddingTop':15,'paddingBottom':15},
            ),
            
        ],width='auto'),
    ]),
],style={'paddingLeft':0,'paddingRight':0,'paddingTop':15,'paddingBottom':15},)


# graph angles and L update
@app.callback(
    Output('graph', 'figure'),
    Input('L1', 'value'),
    Input('L2', 'value'),
    Input('A1', 'value'),
    Input('A2', 'value'),
    State('graph', 'figure'),
)
def updateGraph(L1,L2,A11,A22,figure):
    global A1,A2,text
    A1=A11
    A2=A22
    x, y = fowardKinematics(L1,L2,A1,A2)
    figure['data'][0]['x']=x
    figure['data'][0]['y']=y
    figure['layout']['yaxis']={'range':[-(L1+L2)*1.05,(L1+L2)*1.05]}
    figure['layout']['xaxis']={'range':[-(L1+L2)*1.05,(L1+L2)*1.05]}
    figure['layout']['title']='| x:{} y:{} | {}'.format(round(x[2],2),round(y[2],2),text)
    text = ""
    return figure

# Joystick and Inverse Kinematics
@app.callback(
    Output('A1', 'value'),
    Output('A2', 'value'),

    # State('timerJ','n_intervals'),
    # Input('joystick1', 'angle'),
    # Input('joystick1', 'force'),
    # Input('joystick2', 'angle'),
    # Input('joystick2', 'force'),

    Input('timerJ','n_intervals'),
    State('joystick1', 'angle'),
    State('joystick1', 'force'),
    State('joystick2', 'angle'),
    State('joystick2', 'force'),

    State('Force limit', 'on'),
    State('L1', 'value'),
    State('L2', 'value'),
    State('A1', 'value'),
    State('A2', 'value'),
)
def updateAngle(interval,angle,force,angle2,force2,forceLimit,L1,L2,A11,A22):

    global A1,A2,moved
    xPrevious, yPrevious = fowardKinematics(L1,L2,A1,A2)
    x, y = fowardKinematics(L1,L2,A1,A2)

    # Sigle axis move Joystick
    # Get next x, y
    if angle!=None and force!=0 and force!=None:
        moved = True
        if force > 1 and forceLimit:
            force = 1
        if 315 <= angle or angle < 45:
            x[2] += force*(L1+L2)*0.01
        if 45 <= angle and angle < 135:
            y[2] += force*(L1+L2)*0.01
        if 135 <= angle and angle < 225:
            x[2] -=  force*(L1+L2)*0.01
        if 225 <= angle and angle < 315:
            y[2] -=  force*(L1+L2)*0.01
    
    # Double axis move Joystick
    # Get next x, y
    if angle2!=None and force2!=0 and force2!=None:
        moved = True
        if force2 > 1 and forceLimit:
            force2 = 1
        if 0 <= angle2 and angle2 < 90:
            x[2] += (force2*(L1+L2)*0.01)*(1-angle2/90)
            y[2] += (force2*(L1+L2)*0.01)*(angle2/90)
        if 90 <= angle2 and angle2 < 180:
            x[2] -= (force2*(L1+L2)*0.01)*((angle2-90)/90)
            y[2] += (force2*(L1+L2)*0.01)*(1-(angle2-90)/90)
        if 180 <= angle2 and angle2 < 270:
            x[2] -= (force2*(L1+L2)*0.01)*(1-(angle2-180)/90)
            y[2] -= (force2*(L1+L2)*0.01)*((angle2-180)/90)
        if 270 <= angle2 and angle2 <= 360:
            x[2] += (force2*(L1+L2)*0.01)*((angle2-270)/90)
            y[2] -= (force2*(L1+L2)*0.01)*(1-(angle2-270)/90)

    if moved:

        # check limite
        if math.sqrt(x[2]**2+y[2]**2) > L1+L2 or math.sqrt(x[2]**2+y[2]**2) < abs(L1-L2):
            x[2] = xPrevious[2]
            y[2] = yPrevious[2]
            global text
            text = "reach limit L={}".format(round(math.sqrt(x[2]**2+y[2]**2),2))

        # avoid singularity
        if x[2]==0:
            x[2]=0.0001
        
        # module of point 2
        L = math.sqrt(x[2]**2+y[2]**2)
        # avoid singularity
        if L==0:
            L=0.0001

        # inverse kinematic
        # A1 = (math.atan(y[2]/x[2])-math.acos((L1**2+L**2-L2**2)/(2*L1*L)))/math.pi*180
        # if x[2] < 0:
        #     A1 += 180

        A1 = (math.atan2(y[2],x[2])-math.acos((L1**2+L**2-L2**2)/(2*L1*L)))/math.pi*180
        A2 = (math.pi-math.acos((L1**2+L2**2-L**2)/(2*L1*L2)))/math.pi*180

        moved = False

    return round(A1,2),round(A2,2)



if __name__ == '__main__':
    app.run_server(debug=True)