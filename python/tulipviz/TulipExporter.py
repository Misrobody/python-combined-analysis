from tulip import tlp

class TulipExporter:
    def __init__(self, output):             
        tlp.initTulipLib()
        tlp.loadPlugins()  
              
        self._output = output
        
    def _export_graph(self, graph):
        self.export_svg(graph, self._output)
        
    def export_svg(self, graph, name):
        params = tlp.getDefaultPluginParameters("SVG Export", graph)
        params['edge color interpolation'] = False
        params['edge size interpolation'] = False
        params['edge extremities'] = True
        params['no background'] = False
        params['makes SVG output human readable'] = False
        params['export edge labels'] = True
        params['export metanode labels'] = True
        tlp.exportGraph("SVG Export", graph, name, params)