import re
import nltk
from nltk.tokenize import regexp_tokenize

class SymbolTable:
    def __init__(self):
        self.size = 50
        self.table = [None] * self.size

    def _hash(self, value):
        hash_value = 0
        for char in value:
            hash_value += ord(char)
        return hash_value % self.size

    def insert(self, key, value):
        hash_value = self._hash(value)
        if self.table[hash_value] is None:
            self.table[hash_value] = []
        self.table[hash_value].append((key, value))

    def lookup(self, value):
        hash_value = self._hash(value)
        if self.table[hash_value] is not None:
            for existing_key, existing_value in self.table[hash_value]:
                if existing_value == value:
                    return existing_key, existing_value 
        return None


class Scanner:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
    
    def tokenize(self, source_code):
        pattern = r'\w+|<<|>>|[^\w\s]'
        tokens = regexp_tokenize(source_code, pattern)  #regexp_tokenize now can handle >> and << by pattern of course, those which word_tokenize didn't
        return tokens
    
    def scan(self, source_code):
        output = ''
        tokens = self.tokenize(source_code)
        for token in tokens:
            if not token.strip():  
                continue
            result = self.symbol_table.lookup(token)
            if result:
                formatted_result = f'{self.symbol_table.lookup(token)}'
                output += formatted_result
            elif token.isalpha():
                self.symbol_table.insert('ID', token)
                formatted_result = f'{self.symbol_table.lookup(token)}'
                output += formatted_result
            elif token.isdigit():
                self.symbol_table.insert('num', token)
                formatted_result = f'{self.symbol_table.lookup(token)}'
                output += formatted_result
            else:
                None
        return output
                

def main():
    keywords = [("WRITE",r"write"), ("READ",r'read'), ("LOOP",r"loop"), ("UNTILL",r"until"), ("IF",r"if"), ("SO",r"so"), ("OpPr", r'('), ("ClPr", r")"), ("SC",r";"),
                ("OpBr", r"["), ("ClBr", r"]"), ("mod", r"%"), ("div",r"/"), ("sub",r"-"), ("sum", r"+"), ("star",r"*"), ("equal",r"=="), ("assign", r"="),
                ("cout", r"<<"), ("cin", r">>"), ("INT", r"int"), ("FLOAT", r"float"), ("DOUBLE", r"double"), ("BOOL", r"bool"), ("TRUE", r"true"), ("FALSE", r"false")]

    symbol_table = SymbolTable()
    for key, value in keywords:
        symbol_table.insert(key, value)
        
    scanner = Scanner(symbol_table)

    code = """int row,col;
    write <<”Enter Row : ”;
    read>>row;
    write<<”Enter Col : ”;
    read>>col;
    loop (int i=1 ; i<=row ; i++)
        {
            loop (int j=1 ; j<=col ; j++)
                {
                        write<<i*j<<”  ”;
                }
                write<<endl<<endl;

    }"""

    print(scanner.scan(code))
    

if __name__ == "__main__":
    main()