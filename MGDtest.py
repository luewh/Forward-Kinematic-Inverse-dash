import math
import plotly.graph_objects as go
import plotly.express as ep
from dash import Dash, html, dcc, Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import dash_auth

# video imports
from flask import Flask, Response
import cv2

from MGD import MGD
from math import pi
from math import radians as rad

import numpy as np

# video class
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

# video frame generator
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


VALID_USERNAME_PASSWORD_PAIRS = {
    'MKX7': 'SCAVENGER',
    'admin': ''
}

# init application
server = Flask(__name__)
app = Dash(__name__,server=server,external_stylesheets=[dbc.themes.BOOTSTRAP],title='IHM dev',update_title=None)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS,
)

# init figure of arms
fig = go.Figure(
    data=go.Scatter3d(x=[0,0,0,0,0], y=[0,0,0,0,0], z=[0,0,0,0,0],
                      line=dict(color="crimson",width=2),
                    #   range_x=[],range_y=[],range_z=[],
                      ),
    layout=dict(title=dict(text="x: y: z:"),
                width=500, height=500,
                margin=dict(l=25, r=25, t=25, b=25)),
)


# create IU
app.layout = html.Div([

    dbc.Row([
        
        # 1st column
        dbc.Col([

            # Graph
            dbc.Row(
                dcc.Graph(
                    id='graph',
                    figure=fig,
                    config={
                        'scrollZoom': True,
                        'displaylogo': False,
                        'displayModeBar': False,
                        # 'staticPlot': True,
                    },
                ),
                style={'padding':10},
            ),
        
        ],width="auto"),
        
        # 2nd column
        dbc.Col([

            # 1st articulation lenght
            dbc.Row(
                daq.Slider(
                    id='L1',
                    handleLabel={"showCurrentValue": True,"label":"L1"},
                    marks={"1":"1","25":"25","50":"50"},
                    vertical=True,
                    min=1,
                    max=50,
                    size=100,
                    value=10,
                    step=1,
                    updatemode='drag',
                    persistence=True,
                ),
                style={'paddingLeft':-40,'paddingRight':10,'paddingTop':15,'paddingBottom':15},
            ),

            # 2nd articulation lenght
            dbc.Row(
                daq.Slider(
                    id='L2',
                    handleLabel={"showCurrentValue": True,"label":"L2"},
                    marks={"1":"1","25":"25","50":"50"},
                    vertical=True,
                    min=1,
                    max=50,
                    size=100,
                    value=10,
                    step=1,
                    updatemode='drag',
                    persistence=True,
                ),
                style={'paddingLeft':-40,'paddingRight':10,'paddingTop':15,'paddingBottom':15},
            ),

            # 3rd articulation lenght
            dbc.Row(
                daq.Slider(
                    id='L3',
                    handleLabel={"showCurrentValue": True,"label":"L3"},
                    marks={"1":"1","25":"25","50":"50"},
                    vertical=True,
                    min=1,
                    max=50,
                    size=100,
                    value=10,
                    step=1,
                    updatemode='drag',
                    persistence=True,
                ),
                style={'paddingLeft':-40,'paddingRight':10,'paddingTop':15,'paddingBottom':15},
            ),

            # 4th articulation lenght
            dbc.Row(
                daq.Slider(
                    id='L4',
                    handleLabel={"showCurrentValue": True,"label":"L4"},
                    marks={"1":"1","25":"25","50":"50"},
                    vertical=True,
                    min=1,
                    max=50,
                    size=100,
                    value=10,
                    step=1,
                    updatemode='drag',
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
                    marks={"-180":"-180","0":"0","180":"180"},
                    vertical=True,
                    min=-180,
                    max=180,
                    size=100,
                    value=0,
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
                    marks={"-180":"-180","0":"0","180":"180"},
                    vertical=True,
                    min=-180,
                    max=180,
                    size=100,
                    value=0,
                    step=0.1,
                    updatemode='drag',
                    persistence=True,
                ),
                style={'paddingLeft':60,'paddingRight':10,'paddingTop':15,'paddingBottom':15},
            ),

            # A3
            dbc.Row(
                daq.Slider(
                    id='A3',
                    handleLabel={"showCurrentValue": True,"label":"A3"},
                    marks={"-180":"-180","0":"0","180":"180"},
                    vertical=True,
                    min=-180,
                    max=180,
                    size=100,
                    value=0,
                    step=0.1,
                    updatemode='drag',
                    persistence=True,
                ),
                style={'paddingLeft':60,'paddingRight':10,'paddingTop':15,'paddingBottom':15},
            ),

            # A4
            dbc.Row(
                daq.Slider(
                    id='A4',
                    handleLabel={"showCurrentValue": True,"label":"A4"},
                    marks={"-180":"-180","0":"0","180":"180"},
                    vertical=True,
                    min=-180,
                    max=180,
                    size=100,
                    value=0,
                    step=0.1,
                    updatemode='drag',
                    persistence=True,
                ),
                style={'paddingLeft':60,'paddingRight':10,'paddingTop':15,'paddingBottom':15},
            ),

            # A5
            dbc.Row(
                daq.Slider(
                    id='A5',
                    handleLabel={"showCurrentValue": True,"label":"A5"},
                    marks={"-180":"-180","0":"0","180":"180"},
                    vertical=True,
                    min=-180,
                    max=180,
                    size=100,
                    value=0,
                    step=0.1,
                    updatemode='drag',
                    persistence=True,
                ),
                style={'paddingLeft':60,'paddingRight':10,'paddingTop':15,'paddingBottom':15},
            ),
            
        ],width='auto'),
        
        # 4th column
        dbc.Col(
            # video stream
            html.Img(src="/video_feed"),
            width='auto',
            style={'paddingLeft':50,'paddingRight':10,'paddingTop':10,'paddingBottom':10},
            ),
    
    ]),
],style={'paddingLeft':0,'paddingRight':0,'paddingTop':15,'paddingBottom':15},)


# video stream
@server.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# graph angles and L update
@app.callback(
    Output('graph', 'figure'),
    Input('L1', 'value'),
    Input('L2', 'value'),
    Input('L3', 'value'),
    Input('L4', 'value'),
    Input('A1', 'value'),
    Input('A2', 'value'),
    Input('A3', 'value'),
    Input('A4', 'value'),
    Input('A5', 'value'),
    State('graph', 'figure'),
)
def updateGraph(L1,L2,L3,L4,A1,A2,A3,A4,A5,figure):


    parametres = [[0,    0,  0, rad(A1), L1],
                  [0, pi/2,  0, rad(A2)+pi/2,  0],
                  [0,    0, L2, rad(A3),  0],
                  [0,    0, L3, rad(A4)+pi/2,  0],
                  [0, pi/2,  0, rad(A5), L4]]

    robot = MGD(parametres)
    result = robot.getResults(matricesPassage=0,matricesPassageHomogene=0,coordonnees=1,arrondi=2)

    p1 = result["coordonnees"]["p1"]
    p1[2] -= L1
    p2 = result["coordonnees"]["p2"]
    p3 = result["coordonnees"]["p3"]
    p4 = result["coordonnees"]["p4"]
    p5 = result["coordonnees"]["p5"]
    points = np.array([p1,p2,p3,p4,p5])

    figure['data'][0]['x']=points[:,0]
    figure['data'][0]['y']=points[:,1]
    figure['data'][0]['z']=points[:,2]

    figure['layout']["scene"]["xaxis"] = {"range":[-(L1+L2+L3+L4)*1.05,(L1+L2+L3+L4)*1.05],
                                          "backgroundcolor":"rgb(200, 200, 230)",
                                          "zerolinecolor":"red",
                                          "showspikes":False}
    figure['layout']["scene"]["yaxis"] = {"range":[-(L1+L2+L3+L4)*1.05,(L1+L2+L3+L4)*1.05],
                                          "backgroundcolor":"rgb(230, 200,230)",
                                          "zerolinecolor":"red",
                                          "showspikes":False}
    figure['layout']["scene"]["zaxis"] = {"range":[0,(L1+L2+L3+L4)*1.05],
                                          "backgroundcolor":"rgb(230, 230,200)",
                                          "zerolinecolor":"red"}
    figure['layout']["scene"]["margin"] = dict(r=20, l=10, b=10, t=10)
    # manual / cube / data / auto
    figure['layout']["scene"]["aspectmode"] = "manual"
    figure['layout']["scene"]["camera"] = dict(eye=dict(x=1.2, y=1.2, z=0.2))
    figure['layout']['title']='| x:{} y:{} z:{}|'.format(points[-1,0],points[-1,1],points[-1,2])

    return figure



if __name__ == '__main__':
    app.run(
        debug=True,
        # debug=False,
        host="127.0.0.1",
        # host="159.31.103.60",
        # host="169.254.47.12",
        # host="0.0.0.0",
        port="8080",
        dev_tools_ui=False,
        dev_tools_silence_routes_logging=True,
        )
    