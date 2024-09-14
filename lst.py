class Symbol:
    def __init__(self, plaintext) -> None:
        attrs = plaintext.split(":")
        self.address = int(attrs[0], base=16)
        self.name = attrs[1]


class LST:
    def __init__(self, path) -> None:
        with open(path) as f:
            self.symbols = [Symbol(e.strip()) for e in filter(lambda x: not (',' in x or x.startswith("//") or x.startswith("/*") or x.strip() == ""), f.read().splitlines())]
    
    def getSymbolByName(self, name:str) -> Symbol:
        for symbol in self.symbols:
            if symbol.name == name:
                return symbol
        return None