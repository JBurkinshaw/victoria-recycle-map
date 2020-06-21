from PyQt5.QtGui import *
from PyQt5.QtCore import * 

# Function to get a vector layer by it's name
def getVectorLayerByName( layerName ): 
  layerMap = QgsProject.instance().mapLayers() 
  for name, layer in iter(layerMap.items()):
    if layer.type() == QgsMapLayer.VectorLayer and layer.name() == layerName: 
      if layer.isValid(): 
        return layer 
      else: 
        return None 		

def getMarkerSymbol(layer):
  #properties = {u'symbol_height_map_unit_scale': u'0,0', u'fill_color': u'255,255,255,255', u'outline_style': u'solid', u'outline_width_unit': u'MM', u'symbol_width_unit': u'MM', u'size': u'0', u'angle': u'0', u'offset_unit': u'MM', u'size_unit': u'MM', u'size_map_unit_scale': u'0,0', u'offset_map_unit_scale': u'0,0', u'outline_width': u'0.8', u'symbol_width': u'4', u'offset': u'0,0', u'symbol_width_map_unit_scale': u'0,0', u'outline_color': u'98,76,89,255', u'vertical_anchor_point': u'1', u'symbol_name': u'circle', u'symbol_height_unit': u'MM', u'horizontal_anchor_point': u'1', u'outline_width_map_unit_scale': u'0,0', u'symbol_height': '4'}
  #symbol_layer = QgsEllipseSymbolLayerV2.create(properties)
  #marker_name = QString("RedMarker")
  #symbol = layer.rendererV2().symbols()[0]
  #symbol_layer.setPath("/usr/share/qgis/svg/symbol/red-marker.svg")
  svgStyle = {}
  svgStyle['name'] = '/usr/share/qgis/svg/symbol/blue-marker.svg'
  svgStyle['size'] = '45'
  svgSymbolLayer = QgsSvgMarkerSymbolLayer.create(svgStyle)
  #svgSymbolLayer.setOffset(QPointF(0.0,-20.0))
  # symbol = layer.renderer().symbols(layer.renderer())[0]#.changeSymbolLayer(0, svgSymbolLayer)
  symbol = layer.renderer().legendSymbolItems()[0].symbol()

  return symbol

def createHTMLAnnotation(layer, point):
  # The user interface
  ui = qgis.utils.iface
  
  # Get the map canvas
  mapCanvas = ui.mapCanvas()
  
  # Create the annotation
  # htmlAnno = QgsHtmlAnnotation(mapCanvas, layer)
  htmlAnno = QgsHtmlAnnotation()
  
  # htmlAnno.setHTMLPage('/media/sf_joe/Development/RecyclingMap/Data/Annotations/annotation.html')
  htmlAnno.setSourceFile(f"{os.getcwd()}/Annotations/annotation.html")
  htmlAnno.setMapLayer(layer)
  htmlAnno.setMapPosition(point)
  # htmlAnno.setAssociatedFeature(point)
  htmlAnno.setHasFixedMapPosition(True)
  
  # Size and position
  annoXSize = 375
  annoYSize = 400
  htmlAnno.setFrameSize(QSizeF(QSize(annoXSize,annoYSize)))
  htmlAnno.setFrameOffsetFromReferencePoint(QPointF((-annoXSize/2)-5, -annoYSize-110))
  # htmlAnno.setFrameBorderWidth(8)
  # htmlAnno.setFrameColor(QColor(23,143,82))
  #htmlAnno.setFrameColor(QColor(51,51,51))
  #htmlAnno.setFrameBackgroundColor(QColor(241, 229, 215, 250))
  htmlAnno.setMarkerSymbol(getMarkerSymbol(layer))
  print(f"reached end of createHTMLAnnotation for {point}")
  return htmlAnno

# Loop through the points in the layer
def createAnnotations():
  # Get the layer
  layer = getVectorLayerByName('facilities_product_categories')
  annoList = []
  # Get the points in the layer
  points = layer.getFeatures()
  for point in points:
    geom = point.geometry()
    if geom:
      point = point.geometry().asPoint()
      # Create html annotation item
      anno = createHTMLAnnotation(layer, point)
      annoList.append(anno)
  return annoList

# Delete all of the annotations
#def deleteAnnotations():

annoList = createAnnotations()