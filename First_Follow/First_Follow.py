import sys

class First_Follow():
    def __init__(self, grammar:dict):
        self.grammar = grammar
        self.non_terminals = grammar.keys()
        self.rules = [(head, body) for head, bodies in grammar.items() for body in bodies]
        
        
    def compute_first(self, variable):
        first = set()
        try:
            productions = [rule[1] for rule in self.rules if rule[0] == variable]
            for production in productions:
                if not production[0].isupper():
                    first.add(production[0]) 
                else:
                    first |= self.compute_first(production[0])
                    
            return first
        except Exception as e:
            print("Error: Grammer has left-recursive rule!!")
            sys.exit()
                    
    def compute_follow(self, variable):
        def find_key_by_value(value, default=None):
            for key, val in self.grammar.items():
                for pro in val:
                    if value in pro:
                        return key
        
        follow = set()
        
        if variable == 'S':
            follow.add('$')
        
        for rule in self.rules:
            for j, char in enumerate(rule[1]):
                if char == variable:
                    while j < len(rule[1]) - 1:
                        if not rule[1][j + 1].isupper():
                            follow.add(rule[1][j + 1])
                            break
                        else:
                            follow |= self.compute_first(rule[1][j + 1])
                            if 'ε' not in self.compute_first(rule[1][j + 1]):
                                break
                        j += 1
                    else:
                        head_of_rule = find_key_by_value(rule[1][j])
                        if head_of_rule != variable:
                            follow |= self.compute_follow(head_of_rule)
        follow.discard('ε')     
        return follow
            
        
    def print_sets(self):
        print("First Sets:")
        for non_terminal in self.non_terminals:
            print(f"{non_terminal}: {self.compute_first(non_terminal)}")

        print("\nFollow Sets:")
        for non_terminal in self.non_terminals:
            print(f"{non_terminal}: {self.compute_follow(non_terminal)}")
    
    
def main():
    
    example_grammar = {
    'S': ['TE' ],
    'E': ['+TE', 'ε'],
    'T': ['FH'],
    'H': ['*FH', 'ε'],
    'F': ['(S)', 'i']      # i = id
    }
    
    ff = First_Follow(example_grammar)
        
    ff.print_sets()

    

if __name__ == '__main__':
    main()