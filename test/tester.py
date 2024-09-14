import lst

class Match:
    def __init__(self, source_start, source_end, target_start, target_end) -> None:
        self.source_start = source_start
        self.source_end = source_end
        self.target_start = target_start
        self.target_end = target_end
        assert self.source_end - self.source_start == self.target_end - self.target_start, "Invalid match"
        self.size = self.source_end - self.source_start
    
    def contains(self, address):
        return self.source_start <= address < self.source_end

    def target_contains(self, address):
        return self.target_start <= address < self.target_end

def port(address):
    # OSGlobals will never change
    if address < 0x80004000:
        return address
    
    for match in matches:
        if not match.contains(address):
            continue
        return address - match.source_start + match.target_start
    return 0x0

def backport(address):
    # OSGlobals will never change
    if address < 0x80004000:
        return address
    
    for match in matches:
        if not match.target_contains(address):
            continue
        return address - match.target_start + match.source_start
    return 0x0

matches = []

with open("pal0-us0.csv") as f:
    data = f.read().splitlines()
    for line in data[1:]:
        attrs = [int(attr, base=16) for attr in line.split(',')]
        matches.append(Match(*attrs))

pal_lst = lst.LST("spm.eu0.lst")
us0_lst = lst.LST("spm.us0.lst")
for symbol in pal_lst.symbols:
    if symbol.address > 0x8031beff:
        continue # after .text
    chunk_ported = port(symbol.address)
    real_ported = us0_lst.getSymbolByName(symbol.name)
    if real_ported is None:
        print(f"{hex(symbol.address)} doesn't exist on the target")
    elif chunk_ported == 0:
        print(f"{hex(symbol.address)} failed to port")
    elif chunk_ported != real_ported.address:
        print(f"{hex(symbol.address)} was wrongly ported to {hex(chunk_ported)}, real address is {hex(real_ported)}")   
