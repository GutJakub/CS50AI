import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        
        for key,val in self.domains.items():
            for word in set(val):
                if len(word) != key.length:
                    self.domains[key].remove(word)
        #raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        wspolrzedne=self.crossword.overlaps.get((x,y)) #get bezpieczniejsze bo nie rzuci bledem na dict()
        #print(f"WSPOLRZEDNE REVISE {wspolrzedne} dla {x} oraz {y}")

        if wspolrzedne is None:
            return False
        else:
            change=False
            possible_x=set()
            for word_x in set(self.domains[x]):
                if len(word_x)!=x.length:
                    continue
                consistent=False
                for word_y in self.domains[y]:
                    if word_x==word_y:
                        continue
                    try:
                        if len(word_y)!=y.length:
                            continue
                        #print(f"słowa {word_x}  {word_y} ")
                        litera_x=list(word_x)[wspolrzedne[0]]
                        litera_y=list(word_y)[wspolrzedne[1]]
                        #print(f"{litera_x} do {litera_y}")
                        
                        if litera_x == litera_y:
                            #jesli znajdzie jakikolwiek odpowiednik w Y to zostaje 
                            consistent=True
                            break
                    except IndexError:
                        pass
                if consistent:
                    possible_x.add(word_x)
                else:
                    change=True
                
            self.domains[x]=possible_x
            
            return change
           

        #raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        '''
        if arcs is None:
            arcs=[(variable,self.crossword.neighbors(variable)) for variable in self.crossword.variables]
        '''
        aL=False
        if arcs is None:
            arcs = []
            for x in self.domains:
                for y in self.domains:
                    if x != y:
                        arcs.append((x,y))
        else:
            print(f" arcs lista czy cos {arcs} ")
            aL=True
        while arcs:
            if aL:
                print(f"{arcs[0]}")
            x,y=arcs.pop(0)
            if self.revise(x,y):
                if self.domains[x]==set() or self.domains[x] is None or not self.domains[x]:
                    return False
                for neighbor in self.crossword.neighbors(x)-{y}:
                    arcs.append((neighbor,x)) #dolaczenie do nich tak jakby nowego x variable ale nie wiem jak ze slowami domains
        return True
        
        #print(f"{arcs}")

        
        '''
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }
        '''


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        logic=True
        for key in self.domains:
            if key not in assignment:
                logic=False
            for keya,val in assignment.items():
                if assignment[keya] is None :
                    logic=False
        return logic
        

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        if len(set(assignment.values()))==len(assignment.values()):
            for key,val in assignment.items():
                if val is not None:
                    if key.length==len(val):
                        neighbors=self.crossword.neighbors(key)
                        for neighbor in neighbors:
                            if neighbor not in assignment.keys():
                                continue
                            i,j=self.crossword.overlaps[key,neighbor]
                            if val[i] != assignment[neighbor][j]:
                                return False
                        
                    else:
                        return False
                else:
                    continue
            return True
        else:
            return False

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        words=self.domains[var]
        neighbors=self.crossword.neighbors(var)
        words_dict={word: 0 for word in words}
        for neighbor in neighbors:
            if neighbor in assignment.keys():
                continue
            i,j=self.crossword.overlaps[var,neighbor]
            for key,val in words_dict.items():
                for word_n in self.domains[neighbor]:
                    if key[i] != word_n[j]:
                        words_dict[key]+=1
                
        lista=list(sorted(words_dict.keys(),key=lambda word: words_dict[word]))

        return lista
    
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        var_slownik={v: len(self.domains[v]) for v in self.domains if v not in assignment}
        l=list(sorted(var_slownik.keys(),key=lambda word: (var_slownik[word],len(self.crossword.neighbors(word)) )) )
        return l[0]  

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        if self.assignment_complete(assignment):
            return assignment
        #po dodaniu inference
        v=self.select_unassigned_variable(assignment)
        queue=self.order_domain_values(v,assignment)
        for word in queue:
            assignment[v]=word
            if self.consistent(assignment):
                print(f"{assignment}")
                self.backtrack(assignment)
            else:
                continue
        if self.assignment_complete(assignment):
            return assignment


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)

    '''
    for x in creator.crossword.variables:
        for y in creator.crossword.variables:
            creator.ac3([x, y])   
    '''
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)

    
if __name__ == "__main__":
    main()
