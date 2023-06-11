from math import cos
from math import sin
from math import pi
import numpy as np

class MGD ():
    def __init__(self,parametres):

        self.matricesPassage = []
        for parametre in parametres:
            self.matricesPassage.append(np.array(self.getMatricePassage(parametre)))

        self.matricesPassageHomogene = []
        self.matricesPassageHomogene.append(self.matricesPassage[0])
        for index in range(len(self.matricesPassage)-1):
            self.matricesPassageHomogene.append(np.matmul(self.matricesPassageHomogene[-1],self.matricesPassage[index+1]))
    
    def getResults(self,matricesPassage=False,matricesPassageHomogene=False,coordonnees=False,arrondi=3):

        result = {}

        if matricesPassage:
            matricesPassageTemp = self.arrondiListMatrice(self.matricesPassage,arrondi)
            result["matricesPassage"] = {}
            for index in range(len(matricesPassageTemp)):
                result["matricesPassage"]["t{}{}".format(index,index+1)] = matricesPassageTemp[index]
        
        if matricesPassageHomogene:
            matricesPassageHomogeneTemp = self.arrondiListMatrice(self.matricesPassageHomogene,arrondi)
            result["matricesPassageHomogene"] = {}
            for index in range(len(matricesPassageHomogeneTemp)):
                result["matricesPassageHomogene"]["t0{}".format(index+1)] = matricesPassageHomogeneTemp[index]
        
        if coordonnees:

            if not(matricesPassageHomogene):
                matricesPassageHomogeneTemp = self.arrondiListMatrice(self.matricesPassageHomogene,arrondi)

            result["coordonnees"] = {}
            for index in range(len(matricesPassageHomogeneTemp)):
                result["coordonnees"]["p{}".format(index+1)] = matricesPassageHomogeneTemp[index][:3,3]

        return result
        

    def getMatricePassage(self,parametre):
        matricePassage = [[        cos(parametre[3])          ,          -sin(parametre[3])           ,          0         ,          parametre[2]           ],
                        [ cos(parametre[1])*sin(parametre[3]) , cos(parametre[1])*cos(parametre[3]) , -sin(parametre[1]) , -parametre[4]*sin(parametre[1]) ],
                        [ sin(parametre[1])*sin(parametre[3]) , sin(parametre[1])*cos(parametre[3]) ,  cos(parametre[1]) ,  parametre[4]*cos(parametre[1]) ],
                        [                 0                   ,                  0                  ,          0         ,               1                 ]]
        return matricePassage

    def arrondiMatrice(self,matrice,arrondi=3):
        for ligne in range(len(matrice)):
            for colonne in range(len(matrice[ligne])):
                matrice[ligne][colonne] = round(matrice[ligne][colonne],arrondi)
        return matrice
    
    def arrondiListMatrice(self,listMatrice,arrondi=3):
        for index in range(len(listMatrice)):
            listMatrice[index] = self.arrondiMatrice(listMatrice[index],arrondi)
        return listMatrice


# l1 = 10
# l2 = 20
# l3 = 30
# l4 = 40

# q1 = 0
# q2 = pi/2
# q3 = 0
# q4 = pi/2
# q5 = 0

# # [rotoide=0/prismatique=1 , alpha , d , deta , r ]
# parametres = [[0,    0,  0, q1, l1],
#               [0, pi/2,  0, q2,  0],
#               [0,    0, l2, q3,  0],
#               [0,    0, l3, q4,  0],
#               [0, pi/2,  0, q5, l4]]

# ooo = MGD(parametres)
# result = ooo.getResults(matricesPassage=0,matricesPassageHomogene=0,coordonnees=1,arrondi=3)
# # for i in result["matricesPassage"]:
# #     print(i)
# #     print(result["matricesPassage"][i])

# # for i in result["matricesPassageHomogene"]:
# #     print(i)
# #     print(result["matricesPassageHomogene"][i])

# for i in result["coordonnees"]:
#     print(i)
#     print(result["coordonnees"][i])

# p1 = result["coordonnees"]["p1"]
# p1[2] -= 10
# p2 = result["coordonnees"]["p2"]
# p3 = result["coordonnees"]["p3"]
# p4 = result["coordonnees"]["p4"]
# p5 = result["coordonnees"]["p5"]

# import plotly.graph_objects as go

# points = np.array([p1,p2,p3,p4,p5])

# fig = go.Figure(data=[go.Mesh3d(x=points[:,0],
#                                 y=points[:,1],
#                                 z=points[:,2],
#                                 color='rgba(244,22,100,0.6)'
#                                 )])

# fig = go.Figure(data=go.Scatter3d(
#     x=points[:,0], y=points[:,1], z=points[:,2],
#     marker=dict(
#         size=4,
#         colorscale='Viridis',
#     ),
#     line=dict(
#         color='darkblue',
#         width=2
#     )
# ))

# fig.show()