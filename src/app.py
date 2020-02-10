import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
#from kivy.core.audio import SoundLoader
import pygame

N = 10
pygame.mixer.init()
block_sound = pygame.mixer.Sound('resources/media_block.wav')

class GraphNode(object):
    
    def __init__(self, id, children):
        self.id = id
        self.children = sorted(children)
        
    def __str__(self):
        return f'{self.id} : children={self.children}'
    
    def __repr__(self):
        return f'{self.id} : children={self.children}'

class Graph(object):
    
    def __init__(self, adjancency):
        self.nodes = []
        
        self.build(adjancency)
        
    def build(self, adjancency):
        #logging.info('Adjacency Matrix: ')
        #print(' ************ ')
        for node, edges in adjancency:
            #print(node, edges)
            self.nodes.append(GraphNode(node, edges))        
        #print(' ************ ')
        #print(' ************ ')
    
    def __repr__(self):
        return f'{self.nodes}'
    
    def __str__(self):
        return f'{self.nodes}'



class Node(Button):
    click_cnt = 0
    clicked_list = []
    rock_list = []
    

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        self.text = kwargs.get('text')
        self.rock = 0    
        self.rgba = []

    def on_press(self):
        #if touch.button == 'left':
        if int(self.text) in Node.clicked_list:
            self.background_color = 1.0, 1.0, 1.0, 1.0
            Node.click_cnt -= 1
            Node.clicked_list.remove(int(self.text))
        elif Node.click_cnt < 2:
            Node.click_cnt += 1
            Node.clicked_list.append(int(self.text))
            self.background_color = 0.0, 0.3, 1.0, 1.0
        # elif touch.button == 'right':
        #     if int(self.text) in Node.rock_list:
        #         self.background_color = 1.0, 1.0, 1.0, 1.0
        #         Node.rock_list.remove(int(self.text))
        #     else:
        #         Node.rock_list.append(int(self.text))
        #         self.rock = 1
        #         self.background_color = 0.0, 0.5, 0.0, 1.0

    def play_block(self, *args):
        pygame.mixer.Sound.play(block_sound)
        return True

    def change_my_color(self, *args):
        r,g,b,a = self.rgba.pop(0) # queue
        #pygame.mixer.Sound.stop(block_sound)
        self.background_color = r, g, b, a
        return True


class MyGrid(GridLayout):

    def __init__(self, *args, **kwargs):
        super(MyGrid, self).__init__(*args, **kwargs)
        
        self.size_ = N
        self.cols = 1
        self.time2paint = 0
        self.body = GridLayout(rows=self.size_, cols=self.size_)
        adjancency_list = []
        for i in range(self.size_*self.size_):
            node = Node(text=f'{i}')
            if i == 0:            # Top left
                adjancency_list.append([i, [i+1, N+i]])
            elif i == (N-1)*N:    # Bottom left
                adjancency_list.append([i, [i-N, i+1]])
            elif i == N-1:        # Top Right
                adjancency_list.append([i, [i-1, i+N]])
            elif i == (N*N)-1:    # Bottom Right
                adjancency_list.append([i, [i-N, i-1]])
            elif i % N == 0:      # Mid Left
                adjancency_list.append([i, [i-N, i+1, i+N]])
            elif i < N:           # Mid Top
                adjancency_list.append([i, [i-1, i+1, i+N]])
            elif (i+1) % N == 0:  # Mid Right
                adjancency_list.append([i, [i-N, i-1, i+N]])
            elif i > (N-1)*N:     # Mid Bottom
                adjancency_list.append([i, [i-N, i-1, i+1]])
            else:                 # Else
                adjancency_list.append([i, [i-N, i-1, i+1, i+N]])

            #node.bind(on_press=self.node_press)
            self.body.add_widget(node)

        self.add_widget(self.body)

        self.btn_dfs = Button(text='Depth-First Search', font_size=18)
        self.btn_dfs.bind(on_press=self.main_press)
        

        self.btn_bfs = Button(text='Breadth-First Search', font_size=18)
        self.btn_bfs.bind(on_press=self.main_press)
        

        self.btn_dijsk = Button(text='Dijkstra', font_size=18)
        self.btn_dijsk.bind(on_press=self.main_press)

        self.btn_clr = Button(text='Clear', font_size=18)
        self.btn_clr.bind(on_press=self.main_press)

        self.menuBar = GridLayout(rows=1, cols=6)
        self.menuBar.add_widget(self.btn_dfs)
        self.menuBar.add_widget(self.btn_bfs)
        self.menuBar.add_widget(self.btn_dijsk)
        self.menuBar.add_widget(self.btn_clr)
        self.add_widget(self.menuBar)
        self.graph = Graph(adjancency_list)  


    def main_press(self, instance):
        if instance.text == 'Depth-First Search':
            self.dfs()
        elif instance.text == 'Breadth-First Search':
            self.bfs()
        elif instance.text == 'Dijkstra':
            self.dijsk()
        elif instance.text == 'Clear':
            self.clear_btns()

   
    def change_node_color(self, i, rgba, dt, play_sound=False):
        # call my_callback in 5 seconds
        #Clock.schedule_once(self.my_callback, 5)
        self.body.children[i].rgba.append(rgba)
        self.time2paint += dt
        if play_sound:
            Clock.schedule_once(self.body.children[i].play_block, self.time2paint)
            self.time2paint += block_sound.get_length()/2
        Clock.schedule_once(self.body.children[i].change_my_color, self.time2paint)
        
        return True
        #self.body.children[i].background_color = r,g,b,a


    def dfs(self):
        root = Node.clicked_list[0]
        last = Node.clicked_list[1]
        print(f'From: {root}')
        print(f'To: {last}')

        stack = []
        visited = []
        # Step 1: Insert the root node or starting node of a tree or a graph in the stack.
        stack.append(root)
        self.change_node_color((N*N-1)-root, [0.0, 0.5, 0.0, 1.0], 0.1, True)

        while stack: # while stack is not empty
            #Step 2: Pop the top item from the stack and add it to the visited list.
            node_id = stack.pop()
            # Now it's visited
            visited.append(node_id)
            self.change_node_color((N*N-1)-node_id, [0.5, 0.0, 0.0, 1.0], 0.1, True)
            #Step 3: Find all the adjacent nodes of the node marked visited 
            #        and add the ones that are not yet visited, to the stack.
            for n in self.graph.nodes[node_id].children:
                if (n==last):
                    visited.append(n)
                    stack = []
                    break
                else:
                    if n not in visited:
                        if n not in stack:
                            # Visiting status
                            stack.append(n)
                            self.change_node_color((N*N-1)-n, [204.0/255.0, 255.0/255.0, 255.0/255.0, 1.0], 0.1, True)
        print(f'{visited}')
        for v in visited:
            self.change_node_color((N*N-1)-v, [76.0/255.0, 0.0/255.0, 153.0/255.0, 1.0], 0.05)
            #self.body.children[(N*N-1)-v].background_color = 76.0/255.0, 0.0/255.0, 153.0/255.0, 1.0 # last
        print('End')

    def bfs(self):
        pass
        
    def dijsk(self):
        pass
    
    def clear_btns(self):
         for v in range(len(self.body.children)):
            self.body.children[(N*N-1)-v].background_color = 1.0, 1.0, 1.0, 1.0
            Node.click_cnt = 0
            Node.clicked_list = []
            self.time2paint = 0

class MyApp(App):

    def build(self):
        return MyGrid()


if __name__ == '__main__':
    MyApp().run()
