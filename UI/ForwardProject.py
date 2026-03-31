# -*- coding: utf-8 -*-
import numpy as np
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
from UI.model import  Model
#
#
#
class GeoMagInfo:
    def __init__(self):
        self.T0=54000
        self.I0=90
        self.D0=0


class GridSetting:
    def __init__(self):
        self.rows=51
        self.cols=51
        self.xMin=-100
        self.xMax=100
        self.yMin=-100
        self.yMax=100


class DataComponentType:
    def __init__(self):
        self.DT=1
        self.Hax=2
        self.Hay=3
        self.Za=4
        self.Dg=5
    def nameOfComponentType(self,compType):
        if compType==self.DT:
            return '△T(nT)'
        elif compType==self.Hax:
            return 'Hax(nT)'
        elif compType==self.Hay:
            return 'Hay(nT)'
        elif compType==self.Za:
            return 'Za(nT)'
        elif compType==self.Dg:
            return '△g(g.u)'

class ForwardDataNode:#正演数据及UI
    def __init__(self,compType):
        self.m_componentType=compType
        self.forwardData=0
        self.displayUI=[]

class displayUI:
    def __init__(self):
        self.modelXZgraph=0#xz平面投影图
        self.modelXYgraph=1#xy平面投影图
        self.modelYZgraph=2#yz平面投影图
        self.model3Dgraph=3#三维图

        self.contourMap = 0  # 等值线图
        self.surface3D = 1  # 三维曲面

class ForwardProject:
    projectType_Mag=0#磁
    projectType_Grv=1#重
    def __init__(self,projectType):
        self. m_gridSetting = GridSetting()
        self.m_projectType=projectType
        self.m_models = []
        self.modelGraphs=[]
        self. m_forwardDataNodes = []
        if self.m_projectType==self.projectType_Mag:
            #__init__中只能返回none
            self.m_geoMagInfo = GeoMagInfo()

    def type(self):
        return self.m_projectType

    def gridSetting(self):
        return self.m_gridSetting

    def setGridSetting(self,xyRanges,size):#设置网格参数
        self.m_gridSetting.xMin = xyRanges[0]
        self.m_gridSetting.xMax = xyRanges[1]
        self.m_gridSetting.yMin = xyRanges[2]
        self.m_gridSetting.yMax = xyRanges[3]
        self.m_gridSetting.rows = size[0]
        self.m_gridSetting.cols = size[1]

    def geoMagInfo(self):
        return self.m_geoMagInfo

    def setGeoMagInfo(self,T0,I0,D0):
        self.m_geoMagInfo.T0=T0
        self.m_geoMagInfo.I0=I0
        self.m_geoMagInfo.D0=D0

    def addModel(self,model):
        self.m_models.append(model)
        #重新计算正演数据
        if self.m_forwardDataNodes.__len__():
            for forwardDataNode in self.m_forwardDataNodes:
                compType=forwardDataNode.m_componentType
                self.calculateForwardData(forwardDataNode)
        # 对模型图调整
        if self.modelGraphs.__len__():
            for dlg in self.modelGraphs:
                if dlg.type==None:
                    self.modelGraphs.remove(dlg)#移除
                if dlg.type == displayUI().modelXZgraph:
                    dlg.XZgraphWgt.mpl.start_modelXZGraph(self.m_models)
                elif dlg.type == displayUI().modelXYgraph:
                    dlg.XYgraphWgt.mpl.start_modelXYGraph(self.m_models)
                elif dlg.type==displayUI().modelYZgraph:
                    dlg.YZgraphWgt.mpl.start_modelYZGraph(self.m_models)
                elif dlg.type==displayUI().model3Dgraph:
                    dlg.graph3DWgt.mpl.start_model3DGraph(self.m_models)

    def deleteModel(self,model):
        self.m_models.remove(model)
        del model
        # 重新计算正演数据
        if self.m_forwardDataNodes.__len__():
            for forwardDataNode in self.m_forwardDataNodes:
                compType=forwardDataNode.m_componentType
                self.calculateForwardData(forwardDataNode)
        # 对模型图调整
        if self.modelGraphs.__len__():
            for dlg in self.modelGraphs:
                if dlg.type==None:
                    self.modelGraphs.remove(dlg)#移除
                if dlg.type == displayUI().modelXZgraph:
                    dlg.XZgraphWgt.mpl.start_modelXZGraph(self.m_models)
                elif dlg.type == displayUI().modelXYgraph:
                    dlg.XYgraphWgt.mpl.start_modelXYGraph(self.m_models)
                elif dlg.type==displayUI().modelYZgraph:
                    dlg.YZgraphWgt.mpl.start_modelYZGraph(self.m_models)
                elif dlg.type==displayUI().model3Dgraph:
                    dlg.graph3DWgt.mpl.start_model3DGraph(self.m_models)

    def updateSphereModelParmeter(self,model,center,newRadius,newProperty):
        isGrv = self.type() == ForwardProject.projectType_Grv
        #变化前？model before change
        pass
        #改变模型参数
        if isGrv:
            model.density=newProperty
        else:
            model.K=newProperty
        model.m_geometry_center_x = center[0]
        model.m_geometry_center_y = center[1]
        model.m_geometry_center_z = center[2]
        model.m_geometry_radius = newRadius
        #变化后?model after change
        #对模型图调整
        if self.modelGraphs.__len__():
            for dlg in self.modelGraphs:
                if dlg.type==None:
                    self.modelGraphs.remove(dlg)#移除
                if dlg.type == displayUI().modelXZgraph:
                    dlg.XZgraphWgt.mpl.start_modelXZGraph(self.m_models)
                elif dlg.type == displayUI().modelXYgraph:
                    dlg.XYgraphWgt.mpl.start_modelXYGraph(self.m_models)
                elif dlg.type==displayUI().modelYZgraph:
                    dlg.YZgraphWgt.mpl.start_modelYZGraph(self.m_models)
                elif dlg.type==displayUI().model3Dgraph:
                    dlg.graph3DWgt.mpl.start_model3DGraph(self.m_models)

    def updateRectPrismModelParmeter(self, model, center, size, newProperty):
        isGrv = self.type() == ForwardProject.projectType_Grv
        # 变化前？model before change
        pass
        # 改变模型参数
        if isGrv:
            model.density = newProperty
        else:
            model.K = newProperty
        model.m_geometry_center_x = center[0]
        model.m_geometry_center_y = center[1]
        model.m_geometry_center_z = center[2]
        model.m_geometry_xLen = size[0]
        model.m_geometry_yLen=size[1]
        model.m_geometry_zLen=size[2]
        # 变化后?model after change
        # 对模型图调整
        if self.modelGraphs.__len__():
            for dlg in self.modelGraphs:
                if dlg.type==None:
                    self.modelGraphs.remove(dlg)#移除
                if dlg.type == displayUI().modelXZgraph:
                    dlg.XZgraphWgt.mpl.start_modelXZGraph(self.m_models)
                elif dlg.type == displayUI().modelXYgraph:
                    dlg.XYgraphWgt.mpl.start_modelXYGraph(self.m_models)
                elif dlg.type==displayUI().modelYZgraph:
                    dlg.YZgraphWgt.mpl.start_modelYZGraph(self.m_models)
                elif dlg.type==displayUI().model3Dgraph:
                    dlg.graph3DWgt.mpl.start_model3DGraph(self.m_models)

    def addForwardData(self,compType):
        #先判断是否已经存在，若已经存在则就不能添加
        if self.isExistingForwardData(compType):
            return None
        newNode=ForwardDataNode(compType)
        self.m_forwardDataNodes.append(newNode)
        self.calculateForwardData(newNode)
        return newNode

    def deleteForwardDataNode(self,compType):
        for forwardDataNode in self.m_forwardDataNodes:
            if forwardDataNode.m_componentType==compType:
                self.m_forwardDataNodes.remove(forwardDataNode)
                del forwardDataNode#

    def isExistingForwardData(self,compType):
        if self.m_forwardDataNodes.__len__():
            for dataNode in self.m_forwardDataNodes:
                if dataNode.m_componentType==compType:
                    return True
        return False

    def calculateForwardData(self,node):
        info=self.m_gridSetting#网格参数
        x = np.linspace(info.xMin, info.xMax, info.cols)
        y = np.linspace(info.yMin, info.yMax, info.rows)
        X, Y = np.meshgrid(x, y)
        z = 0
        # preForwardData=node.forwardData()#之前的正演数据
        node.forwardData = np.zeros([info.cols,info.rows])
        # print(node.forwardData)#做实验
        # 初始化，方便更新
        if node.m_componentType==DataComponentType().Dg:#dg分量
            G = 6.67e-11
            if self.m_models.__len__():#有模型
                for model in self.m_models:
                    if model.type()==model.modelType_Sphere:#球体模型
                        s_x, s_y, s_z, s_r, s_ρ = model.m_geometry_center_x,model.m_geometry_center_y,\
                                        model.m_geometry_center_z,model.m_geometry_radius,model.density
                        M = s_ρ * (4 * np.pi * s_r ** 3) / 3
                        node.forwardData += 1e9 * G * M * s_z / (((X - s_x) ** 2 + (Y - s_y) ** 2 + s_z ** 2) ** (3 / 2))
                        # print(node.forwardData)#做实验ok
                    if model.type()==model.modelType_RectPrism:#长方体模型
                        x1 = model.m_geometry_center_x - model.m_geometry_xLen / 2
                        x2 = model.m_geometry_center_x + model.m_geometry_xLen / 2
                        y1 = model.m_geometry_center_y - model.m_geometry_yLen / 2
                        y2 = model.m_geometry_center_y + model.m_geometry_yLen / 2
                        z1=model.m_geometry_center_z - model.m_geometry_zLen  / 2
                        z2=model.m_geometry_center_z + model.m_geometry_zLen / 2
                        r_ρ=model.density
                        for i in np.arange(0,info.rows):
                            for j in np.arange(0,info.cols):
                                tmp1 = my_fun_grv(x[j], y[i], z, x2, y2, z2)
                                tmp2 = my_fun_grv(x[j], y[i], z, x2, y2, z1)
                                tmp3 = my_fun_grv(x[j], y[i], z, x2, y1, z2)
                                tmp4 = my_fun_grv(x[j], y[i], z, x2, y1, z1)
                                tmp5 = my_fun_grv(x[j], y[i], z, x1, y2, z2)
                                tmp6 = my_fun_grv(x[j], y[i], z, x1, y2, z1)
                                tmp7 = my_fun_grv(x[j], y[i], z, x1, y1, z2)
                                tmp8 = my_fun_grv(x[j], y[i], z, x1, y1, z1)
                                node.forwardData[i][j]+=-G*r_ρ*(tmp1-tmp2-tmp3+tmp4-tmp5+tmp6+tmp7-tmp8)*1e9
        else:
            #磁化强度方向与地磁场一致
            if self.m_models.__len__():#有模型
                I,A=self.m_geoMagInfo.I0/180*np.pi,self.m_geoMagInfo.D0/180*np.pi
                for model in self.m_models:
                    if model.type()==model.modelType_Sphere:
                        s_x, s_y, s_z, s_r,M,K = model.m_geometry_center_x,model.m_geometry_center_y,\
                                        model.m_geometry_center_z,model.m_geometry_radius,model.M, model.K
                        u = 4 * np.pi * 10 ** (-7)*(1+K) #磁导率
                        # u=4*np.pi*10**(-7)
                        v=(4*np.pi*s_r**3)/3#体积
                        m=M*v#磁矩
                        figure = u * m / (4 * np.pi * ((X - s_x) ** 2 + (Y - s_y) ** 2 + s_z ** 2) ** (5 / 2))
                        if node.m_componentType == DataComponentType().DT:
                            node.forwardData += figure*\
                                                (((2*s_z**2-(X-s_x)**2-(Y-s_y)**2))*np.sin(I)**2+
                                                 (2*(X-s_x)**2-(Y-s_y)**2-s_z**2)*(np.cos(I)*np.cos(A))**2+
                                                 (2*(Y-s_y)**2-(X-s_x)**2-s_z**2)*(np.cos(I)*np.sin(A))**2-
                                                 3*(X-s_x)*s_z*np.sin(2*I)*np.cos(A)+
                                                 3*(X-s_x)*(Y-s_y)*np.cos(I)**2*np.sin(2*A)-
                                                 3*(Y-s_y)*s_z*np.sin(2*I)*np.sin(A))*10**9#单位nT
                        elif node.m_componentType== DataComponentType().Hax:
                            node.forwardData+=figure* \
                                              (( 2*(X - s_x) ** 2 - (Y - s_y) ** 2-s_z**2) * np.cos(I) * np.cos(A) -
                                               3*s_z*(X-s_x)*np.sin(I)+3*(Y-s_y)*(X-s_x)*np.cos(I)*np.sin(A))*10**9
                        elif node.m_componentType== DataComponentType().Hay:
                            node.forwardData += figure * \
                                                ((2*(Y - s_y) ** 2 -(X-s_x)**2- s_z ** 2) * np.cos(I) * np.sin(
                                                    A) -
                                                 3 * s_z * (Y - s_y) * np.sin(I) + 3 * (Y - s_y) * (X - s_x) * np.cos(
                                                            I) * np.cos(A)) * 10 ** 9
                        elif node.m_componentType==DataComponentType().Za:
                            node.forwardData += figure * \
                                                ((2*s_z ** 2- (X - s_x) ** 2 - (Y - s_y) ** 2 ) * np.sin(I) -
                                                 3 * s_z * (X - s_x) * np.cos(I)*np.cos(A) - 3 * (Y - s_y) * s_z * np.cos(
                                                            I) * np.sin(A)) * 10 ** 9
                            pass
                    elif model.type()==model.modelType_RectPrism:
                        x1 = model.m_geometry_center_x - model.m_geometry_xLen / 2
                        x2 = model.m_geometry_center_x + model.m_geometry_xLen / 2
                        y1 = model.m_geometry_center_y - model.m_geometry_yLen / 2
                        y2 = model.m_geometry_center_y + model.m_geometry_yLen / 2
                        z1=model.m_geometry_center_z - model.m_geometry_zLen  / 2
                        z2=model.m_geometry_center_z + model.m_geometry_zLen / 2
                        M,K=model.M,model.K
                        u=4 * np.pi * 10 ** (-7)*(1+K)#磁导率
                        # u=4*np.pi *10**(-7)
                        type=node.m_componentType
                        for i in np.arange(0,info.rows):
                            for j in np.arange(0,info.cols):
                                tmp1 = my_fun_mag(x[j], y[i], z, x2, y2, z2,type,I,A)
                                tmp2 = my_fun_mag(x[j], y[i], z, x2, y2, z1,type,I,A)
                                tmp3 = my_fun_mag(x[j], y[i], z, x2, y1, z2,type,I,A)
                                tmp4 = my_fun_mag(x[j], y[i], z, x2, y1, z1,type,I,A)
                                tmp5 = my_fun_mag(x[j], y[i], z, x1, y2, z2,type,I,A)
                                tmp6 = my_fun_mag(x[j], y[i], z, x1, y2, z1,type,I,A)
                                tmp7 = my_fun_mag(x[j], y[i], z, x1, y1, z2,type,I,A)
                                tmp8 = my_fun_mag(x[j], y[i], z, x1, y1, z1,type,I,A)
                                node.forwardData[i][j]+=u*M/(4*np.pi)*(tmp1-tmp2-tmp3+tmp4-tmp5+tmp6+tmp7-tmp8)*1e9
        if node.displayUI.__len__():
            for dlg in node.displayUI:
                if dlg.type==displayUI().contourMap:
                    dlg.contourMapWgt.mpl.start_contourMap(info,node.forwardData)
                elif dlg.type==displayUI().surface3D:
                    dlg.surface3DWgt.mpl.start_surface3D(info,
                                                         DataComponentType().nameOfComponentType(node.m_componentType),
                                                         node.forwardData)

    # def hasDisplayUI(self,node,type):
    #     if node.displayUI.__len__()==0:
    #         return False
    #     for dlg in node.displayUI:
    #         if dlg.type==type:
    #             return True#已存在
    #     return False

def my_fun_grv(x,y,z,X,Y,Z):
    R=np.sqrt((X-x)**2+(Y-y)**2+(Z-z)**2)
    a = ((X - x) * np.log((Y - y) + R) + (Y - y) * np.log((X - x) + R) -(Z - z) * np.arctan((X - x) * (Y - y) / ((Z - z) * R)))
    return a
def my_fun_mag(x,y,z,X,Y,Z,type,I,A):
    r = np.sqrt((X - x) ** 2 + (Y - y) ** 2 + (Z - z) ** 2)
    if type==DataComponentType().Hax:
        a=-np.cos(I)*np.cos(A)*np.arctan((X-x)*(Y-y)/((X-x)**2+r*(Z-z)+(Z-z)**2))+np.cos(I)*np.sin(A)*np.log(r+(Z-z))+np.sin(I)*np.log(r+(Y-y))
    elif type==DataComponentType().Hay:
        a=np.cos(I)*np.cos(A)*np.log(r+(Z-z))-np.cos(I)*np.sin(A)*np.arctan((X-x)*(Y-y)/((Y-y)**2+r*(Z-z)+(Z-z)**2))+np.sin(I)*np.log(r+(X-x))
    elif type==DataComponentType().Za:
        a=np.cos(I)*np.cos(A)*np.log(r+(Y-y))+np.cos(I)*np.sin(A)*np.log(r+(X-x))-np.sin(I)*np.arctan((X-x)*(Y-y)/(r*(Z-z)))
    elif type==DataComponentType().DT:
        L0=np.cos(I)*np.cos(A)
        M0=np.cos(I)*np.sin(A)
        N0=np.sin(I)
        alpha =np.cos(I)*np.cos(A)
        beta=np.cos(I)*np.sin(A)
        gama = np.sin(I)
        k1=M0*gama+N0*beta
        k2=L0*gama+N0*alpha
        k3=L0*beta+M0*alpha
        k4=L0*alpha
        k5=M0*beta
        k6=-N0*gama
        a=k1*np.log(r+(X-x))+k2*np.log(r+(Y-y))+k3*np.log(r+(Z-z))+\
          k4*np.arctan((X-x)*(Y-y)/((X-x)**2+r*(Z-z)+(Z-z)**2))+\
          k5*np.arctan((X-x)*(Y-y)/((Y-y)**2+r*(Z-z)+(Z-z)**2))+\
          k6*np.arctan((X-x)*(Y-y)/(r*(Z-z)))
    return a
