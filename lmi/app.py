from lmi.components.abstract.component import Component


class App(Component):
    
    def serve(self, port: int):
        '''Serve the react app on the given port'''
        pass
    
    def cli(self):
        '''Run the app as interactive text in the command line'''
        pass
    
    def run(self, agent):
        '''Run the app as text against some langchain agent'''
        pass