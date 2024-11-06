import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        #x=len(self.cells)
        #print(f"DLugosc setow {self} {x}, {self.count}")
        if len(self.cells)==self.count and self.count != 0:
            return self.cells
        else:
            return set()
        #raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count==0:
            return self.cells
        else:
            return set()
        #raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count=self.count-1
        
            
                
        #raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            
        #raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        offsets = [
            (-1, -1), (-1, 0), (-1, 1),  
            (0, -1),          (0, 1),    
            (1, -1), (1, 0), (1, 1)      
                ]
        neighbors=set()
        for di,dj in offsets:
            ni,nj=cell[0]+di,cell[1]+dj
            
            if 0<=ni<self.height and 0<=nj<self.width:
                if (ni,nj) not in self.moves_made or (ni,nj) in self.safes:
                    neighbors.add((ni,nj))
        s=Sentence(neighbors,count)
        for safe in list(s.known_safes()):
            self.mark_safe(safe)
        for mine in list(s.known_mines()):
            self.mark_mine(mine)

        for mine in self.mines:
            s.mark_mine(mine)
            
        self.knowledge.append(s)

        
        empty = Sentence(set(), 0)
        
        change=True
        while change:
            self.knowledge[:] = [x for x in self.knowledge if x != empty]
            self.knowledge[:] = [x for x in self.knowledge if x.cells != set()]
            change=False
            
            for sentence in self.knowledge:
                sentence.cells-=self.moves_made
                sentence.cells-=self.safes
                
                for bomb in self.mines:
                    sentence.mark_mine(bomb)

                for sf in list(sentence.known_safes()):
                    change=True
                    self.mark_safe(sf)
                    print(f"znane miejsce bezpieczne {sf}")
                for sb in list(sentence.known_mines()):
                    change=True
                    print(f"znana bomba {sb}")
                    self.mark_mine(sb)
                    
            #wszystkie mozliwe kombinacje bez wzgledu na kolejnosc
            for sentence,other in itertools.combinations(self.knowledge,2):
                if sentence.cells > other.cells:
                    temp_cells=sentence.cells-other.cells
                    temp_count=sentence.count-other.count
                    self.knowledge.append(Sentence(temp_cells,temp_count))
                elif sentence.cells < other.cells:
                    temp_cells=other.cells-sentence.cells
                    temp_count=other.count-sentence.count
                    self.knowledge.append(Sentence(temp_cells,temp_count))

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        #print(f"Ruchy zrobione {self.moves_made}")
        if self.safes-self.moves_made==set():
            return None
        else:
            print(f"Bezpieczne ruchy {list(self.safes-self.moves_made)}")
            print(f"Oznaczone pewne bombki {list(self.mines)}")
            print(f"Ruch wykonany {list(self.safes-self.moves_made)[0]}")
            return random.choice(list(self.safes-self.moves_made))
            
        #raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        '''
        print(f"Oznaczone pewne bombki {list(self.mines)}")
        for x in range(0,self.width):
            for y in range(0,self.height):
                c=(x,y)
                
                if c not in self.mines and c not in self.moves_made:
                
                    return c
                #else:    
        return None
        #raise NotImplementedError
        '''
        p_moves=[]
        print(f"Oznaczone pewne bombki {list(self.mines)}")
        for x in range(self.height):
            for y in range(self.width):
                c=(x,y)
                
                if c not in self.mines and c not in self.moves_made:
                    p_moves.append(c)
        if p_moves:
            return random.choice(p_moves)
        
        return None
