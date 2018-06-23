# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Circle
import copy

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib 

def get_coordinates(column,line):
    x0 = 10
    y0 = 57

    w = 16.5
    h = 19.5
    
    incl = 10
    
    x = (column)*w + x0    
    if column<=5:
        y = line*h - incl*column + y0
    else:
        y0 = h - incl*5 + y0
        y = y0 + line*h -h - incl*(5-column)
    
    return (x,y)  

def print_board(board):
    img=mpimg.imread('board.png')
    
    ig,ax = plt.subplots(1)
    ax.set_aspect('equal')
    
    for column in range(0,len(board)):
        for line in range(0,len(board[column])):
            (x,y) = get_coordinates(column,line)
            if board[column][line] == 0:
                color = 'white'
            elif board[column][line] == 1:
                color = 'red'
            else:
                color = 'green'
            circ = Circle((x,y),5,color=color)
            ax.add_patch(circ)    
    plt.imshow(img)

class Game:
    board = []
    player = 1
    ended = False
    waiting_removal = False
    forbidden_moves = None
    movements = 0
    last_column = 0
    last_line = 0
    
    # Initialize the board. 0 is empty space. 1 and 2 are the players.
    def init_board(self):
        self.ended = False
        self.board = []
        self.player = 1
        self.waiting_removal = False
        self.forbidden_moves = None
        self.movements = 0

        self.last_column = -1
        self.last_line = -1
        
        for column in range(11):
            if column <= 5:
                height = 5+column
            else:
                height = 15 - column 
            self.board.append([0]*height)

    def get_position(self,column,line):
        return self.board[column-1][line-1]
    
    def set_position(self,column,line,state):
        b = copy.deepcopy(self.board)
        b[column-1][line-1] = state
        return b
            
    # Put a piece on a board. State is the player (or 0 to remove a piece)
    def place_piece(self, column, line, state):
        self.board = self.set_position(column,line,state)

    # Get a fixed-size list of neighbors: [top, top-right, top-left, down, down-right, down-left]. 
    # None at any of those places where there's no neighbor
    def neighbors(self,column,line):
        l = []

        if line>1:
            l.append((column,line-1)) # up
        else:
            l.append(None)

        if (column<6 or line>1) and (column<len(self.board)):
            if column>=6:
                l.append((column+1,line-1)) # upper right
            else:
                l.append((column+1,line)) # upper right
        else:
            l.append(None)
        if (column>6 or line>1) and (column>1):
            if column>6:
                l.append((column-1,line)) # upper left
            else:
                l.append((column-1,line-1)) # upper left
        else:
            l.append(None)

        if line<len(self.board[column-1]):
            l.append((column,line+1)) # down
        else:
            l.append(None)   

        if (column<6 or line<len(self.board[column-1])) and column<len(self.board):
            if column<6:
                l.append((column+1,line+1)) # down right
            else:
                l.append((column+1,line)) # down right
        else:
            l.append(None)

        if (column>6 or line<len(self.board[column-1])) and column>1:
            if column>6:
                l.append((column-1,line+1)) # down left
            else:
                l.append((column-1,line)) # down left
        else:
            l.append(None)

        return l

    # Check if there's any possible removal (trapped pieces)
    # Returns (player,[positions]), where [positions] is a list of the two possibilities to be removed
    def can_remove(self,player):
        removals = []
        
        # test vertical
        s = ""
        l = []
        for line in range(max(self.last_line-3,1), min(self.last_line+3,len(self.board[self.last_column-1]))+1):
            state = self.board[self.last_column-1][line-1]
            l.append((self.last_column,line))
            s += str(state)

            if "1221" in s and player==1:
                removals.append(l[-3:-1])
            if "2112" in s and player==2:
                removals.append(l[-3:-1])
                 

        # test upward diagonals
        diags = [(1,1),(1,2),(1,3),(1,4),(1,5),(2,6),(3,7),(4,8),(5,9),(6,10)]

        col = self.last_column
        line = self.last_line
        coords = (col, line)

        s = ""
        for i in range(0,4):
            column = coords[0]
            line = coords[1]
            state = self.board[column-1][line-1]
            l.append((column,line))
            s += str(state)
            if "1221" in s and player==1:
                removals.append(l[-3:-1]) 
            if "2112" in s and player==2:
                removals.append(l[-3:-1])   
            coords = self.neighbors(column,line)[1] 
            if coords==None:
                break

        col = self.last_column
        line = self.last_line
        coords = (col, line)

        s = ""
        for i in range(0,4):
            print(coords)
            column = coords[0]
            line = coords[1]
            state = self.board[column-1][line-1]
            l.append((column,line))
            s += str(state)
            print(s)
            if "1221" in s and player==1:
                removals.append(l[-3:-1]) 
            if "2112" in s and player==2:
                removals.append(l[-3:-1])   
            coords = self.neighbors(column,line)[5]
            if coords==None:
                break                
           

        # test downward diagonals
        diags = [(6,1),(5,1),(4,1),(3,1),(2,1),(1,1),(1,2),(1,3),(1,4),(1,5)]    

        col = self.last_column
        line = self.last_line
        coords = (col, line)

        s = ""
        for i in range(0,4):
            column = coords[0]
            line = coords[1]
            state = self.board[column-1][line-1]
            l.append((column,line))
            s += str(state)
            if "1221" in s and player==1:
                removals.append(l[-3:-1]) 
            if "2112" in s and player==2:
                removals.append(l[-3:-1])   
            coords = self.neighbors(column,line)[2] 
            if coords==None:
                break

        col = self.last_column
        line = self.last_line
        coords = (col, line)

        s = ""
        for i in range(0,4):
            print(coords)
            column = coords[0]
            line = coords[1]
            state = self.board[column-1][line-1]
            l.append((column,line))
            s += str(state)
            print(s)
            if "1221" in s and player==1:
                removals.append(l[-3:-1]) 
            if "2112" in s and player==2:
                removals.append(l[-3:-1])   
            coords = self.neighbors(column,line)[4]
            if coords==None:
                break   

        if len(removals)>0:
            removals = [item for sublist in removals for item in sublist]
            return removals
        else:
            return None

    # Check if a board is in an end-game state. Returns the winning player or None.
    def is_final_state(self):
        # test vertical
        for column in range(len(self.board)):
            s = ""
            for line in range(len(self.board[column])):
                state = self.board[column][line]
                s += str(state)
                if "11111" in s:
                    return 1
                if "22222" in s:
                    return 2

        # test upward diagonals
        diags = [(1,1),(1,2),(1,3),(1,4),(1,5),(2,6),(3,7),(4,8),(5,9),(6,10)]
        for column_0, line_0 in diags:
            s = ""
            coords = (column_0,line_0)
            while coords!=None:
                column = coords[0]
                line = coords[1]
                state = self.board[column-1][line-1]
                s += str(state)
                if "11111" in s:
                    return 1
                if "22222" in s:
                    return 2
                coords = self.neighbors(column,line)[1]              

        # test downward diagonals
        diags = [(6,1),(5,1),(4,1),(3,1),(2,1),(1,1),(1,2),(1,3),(1,4),(1,5)]    
        for column_0, line_0 in diags:
            s = ""
            coords = (column_0,line_0)
            while coords!=None:
                column = coords[0]
                line = coords[1]
                state = self.board[column-1][line-1]
                s += str(state)
                if "11111" in s:
                    return 1
                if "22222" in s:
                    return 2
                coords = self.neighbors(column,line)[4]    

        return None

    # Returns a list of positions available on a board
    def get_available_moves(self):
        l = []

        removal_options = self.can_remove(self.player)
        if removal_options!=None:
            self.waiting_removal = True
            return removal_options
        else:
            for column in range(len(self.board)):
                for line in range(len(self.board[column])):
                    if self.board[column][line]==0:
                        l.append((column+1,line+1))                    
            return l

    def get_available_boards(self):
        l = self.get_available_moves()
        possible_boards = []
        for (column,line) in l:
            possible_boards.append(self.set_position(column,line,self.player))
        return (self.player,possible_boards)
    
    def take_turn(self):
        if self.player==1:
            self.player=2
        else:
            self.player=1
        return self.player
    
    def make_move(self,player,column,line):
        if self.ended:
            return (-1,"Game is over")
        
        if player!=self.player:
            return (-1,"Not your turn")
        
        if column>len(self.board) or column<0:
            return (-1,"No such column")

        if line<0 or line>len(self.board[column-1]):
            return (-1,"No such line in column %d" % column)
        
        if (column,line) == self.forbidden_moves:
            return (-1, "Position not available")
        
        if self.get_position(column,line)==0 or self.waiting_removal:
            forbidden_just_set = False
            if self.waiting_removal:
                if (column,line) in self.can_remove(self.player):
                    state = 0
                    self.waiting_removal = False
                    self.forbidden_moves = (column,line)
                    forbidden_just_set = True
                else:
                    return (-1, "Invalid removal")
            else:
                state = player
            self.board = self.set_position(column,line,state)
            if not forbidden_just_set:
                self.forbidden_moves = None
        else:
            return (-1,"Position not available")
        
        f = self.is_final_state()
        if f != None:
            self.ended = True
            return (0,"%d wins" % f)
        
        self.last_line = line
        self.last_column = column

        # Check for sandwiches
        possible_states = []
        
        removal_options = self.can_remove(self.player)
        if removal_options!=None:
            self.waiting_removal = True
            return (2,"must remove")
            # for option in removal_options:
            #     possible_states.append(self.set_position(option[0],option[1],0))
            # return (player,possible_states)
        else:
            self.take_turn()

        self.movements += 1

        return (1,"ok")
        

###### SERVER ######

game = Game()
game.init_board()

class myHandler(BaseHTTPRequestHandler):
    # Handler for the GET requests
    def display(self,message,content_type='text/plain'):
        self.send_response(200)        
        self.send_header('Content-type',content_type)
        self.end_headers()
        if isinstance(message, str):
            self.wfile.write(bytes(message, "utf-8"))
        else:
            self.wfile.write(message)

    def do_GET(self):
        print   ('Get request received')

        action = ""
        q = ""

        if "/" in self.path:
            action = self.path.split("/")[1]
            if "?" in action:
                s  = action.split("?")
                action = s[0]
                q = urllib.parse.parse_qs(s[1])

        print(action)

        if action=="minhavez":
            player = int(q['player'][0])
            if game.player!=player:
                self.display("-1")
            else:
                self.display("1")
            return

        if action=="jogador":
            self.display(str(game.player))
            return

        if action=="tabuleiro":
            self.display(str(game.board))
            return

        if action=="movimentos":
            self.display(str(game.get_available_moves()))
            return

        if action=="num_movimentos":
            self.display(str(game.movements))
            return    

        if action=="ultima_jogada":
            self.display(str((game.last_column,game.last_line)))
            return

        if action=="reiniciar":
            game.init_board()
            self.display("reiniciado")
            return

        if action=="move":
            coluna = int(q['coluna'][0])
            linha = int(q['linha'][0])
            player = int(q['player'][0])
            r = game.make_move(player,coluna,linha)
            self.display(str(r))
            return

        if action!="":
            try:
                filetype = action.split(".")[-1]
            except:
                filetype=""

            if filetype=='png':
                filecontent = open(action,"rb").read()
                self.display(filecontent,'image/png')
            elif filetype=='html' or filetype=='js':
                filecontent = open(action,"r").read()
                self.display(filecontent,'text/html')
            else:
                try:
                    filecontent = open(action,"r").read()
                    self.display(filecontent,'text/plain')
                except:
                    pass


        return


PORT_NUMBER = 8080

try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print ('Started httpserver on port ' , PORT_NUMBER)

    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print ('^C received, shutting down the web server')
    server.socket.close()
