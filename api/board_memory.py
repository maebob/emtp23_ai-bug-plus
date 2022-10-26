class board_memory():
    def __init__(self, debug: bool= False) -> None:
        self.debug = debug
        self.conections = {}
        self.ports = {}
        self.bug_types = {}
    
    