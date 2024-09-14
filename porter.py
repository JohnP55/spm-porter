from lst import LST
import os

class Match:
    def __init__(self, source_start, source_end, target_start, target_end) -> None:
        self.source_start = source_start
        self.source_end = source_end
        self.target_start = target_start
        self.target_end = target_end
        assert self.source_end - self.source_start == self.target_end - self.target_start, "Invalid match"
        self.size = self.source_end - self.source_start
    
    def source_contains(self, address):
        return self.source_start <= address < self.source_end

    def target_contains(self, address):
        return self.target_start <= address < self.target_end

def fwdport(address):
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

def init_matches(csvfilename):
    global matches
    matches = []

    with open(csvfilename) as f:
        data = f.read().splitlines()
    for line in data[1:]:
        attrs = [int(attr, base=16) for attr in line.split(',')]
        matches.append(Match(*attrs))

def batch_port(source_lst, portfunc):
    ported_syms = []

    for symbol in source_lst.symbols:
        if symbol.address > 0x8031beff:
            print(f"Skipping {symbol.name} (outside of .text)")
            continue # after .text
        
        ported = portfunc(symbol.address)
        
        if ported > 0x0:
            ported_syms.append(f"{hex(ported)}:{symbol.name}")
        else:
            print(f"Skipping {symbol.name} (failed to port)")
            
    return ported_syms
    

matches = []

def main():
    csv = input("Matches csv file: ")
    init_matches(csv)
    
    should_backport = input("Port backwards? (from target to source) (y/N) ") == 'y'
    lst_file = input("LST entries file: ")
    source_lst = LST(lst_file)

    print()
    
    ported_syms = batch_port(source_lst, backport if should_backport else fwdport)

    print()
    print('\n'.join(ported_syms))

if __name__ == '__main__':
    main()
