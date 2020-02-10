import kivy
import pygame
kivy.require('1.0.6')

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from graph import Graph 
from algorithms import Algo 

N = 10
pygame.mixer.init()
block_sound = pygame.mixer.Sound('resources/media_block.wav')


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
        if int(self.text) in Node.clicked_list:
            self.background_color = 1.0, 1.0, 1.0, 1.0
            Node.click_cnt -= 1
            Node.clicked_list.remove(int(self.text))
        elif Node.click_cnt < 2:
            Node.click_cnt += 1
            Node.clicked_list.append(int(self.text))
            self.background_color = 0.0, 0.3, 1.0, 1.0

    def play_block(self, *args):
        pygame.mixer.Sound.play(block_sound)
        return True

    def change_my_color(self, *args):
        r,g,b,a = self.rgba.pop(0) # queue
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
        #self.weights = []
        
        for i in range(self.size_*self.size_):
            node = Node(text=f'{i}')
            if i == 0:            # Top left
                adjancency_list.append([i, [i+1, N+i], [1, 1]])
                #self.weights.append([1, 1])
            elif i == (N-1)*N:    # Bottom left
                adjancency_list.append([i, [i-N, i+1], [1, 1]])
                #self.weights.append([1, 1])
            elif i == N-1:        # Top Right
                adjancency_list.append([i, [i-1, i+N], [1, 1]])
                #self.weights.append([1, 1])
            elif i == (N*N)-1:    # Bottom Right
                adjancency_list.append([i, [i-N, i-1], [1, 1]])
                #self.weights.append([1, 1])
            elif i % N == 0:      # Mid Left
                adjancency_list.append([i, [i-N, i+1, i+N], [1, 1, 1]])
                #self.weights.append([1, 1, 1])
            elif i < N:           # Mid Top
                adjancency_list.append([i, [i-1, i+1, i+N], [1, 1, 1]])
                #self.weights.append([1, 1, 1])
            elif (i+1) % N == 0:  # Mid Right
                adjancency_list.append([i, [i-N, i-1, i+N], [1, 1, 1]])
                #self.weights.append([1, 1, 1])
            elif i > (N-1)*N:     # Mid Bottom
                adjancency_list.append([i, [i-N, i-1, i+1], [1, 1, 1]])
                #self.weights.append([1, 1, 1])
            else:                 # Else
                adjancency_list.append([i, [i-N, i-1, i+1, i+N], [1, 1, 1, 1]])
                #self.weights.append([1, 1, 1, 1])

            self.body.add_widget(node)

        self.add_widget(self.body)

        self.btn_dfs = Button(text='Depth-First Search', font_size=18)
        self.btn_dfs.bind(on_press=self.main_press)
        

        self.btn_bfs = Button(text='Breadth-First Search', font_size=18)
        self.btn_bfs.bind(on_press=self.main_press)
        

        self.btn_dijsk = Button(text='Dijkstra', font_size=18)
        self.btn_dijsk.bind(on_press=self.main_press)

        self.btn_a_star = Button(text='A*', font_size=18)
        self.btn_a_star.bind(on_press=self.main_press)

        self.btn_clr = Button(text='Clear', font_size=18)
        self.btn_clr.bind(on_press=self.main_press)

        self.menuBar = GridLayout(rows=1, cols=6)
        self.menuBar.add_widget(self.btn_dfs)
        self.menuBar.add_widget(self.btn_bfs)
        self.menuBar.add_widget(self.btn_dijsk)
        self.menuBar.add_widget(self.btn_a_star)
        self.menuBar.add_widget(self.btn_clr)
        self.add_widget(self.menuBar)
        self.graph = Graph(adjancency_list)  

        self.status = {'VISITING': [204.0/255.0, 255.0/255.0, 255.0/255.0, 1.0],
                       'VISITED': [0.5, 0.0, 0.0, 1.0],
                       'IDLE': [1.0, 1.0, 1.0, 1.0],
                       'RESULT': [76.0/255.0, 0.0/255.0, 153.0/255.0, 1.0]}


    def main_press(self, instance):
        if instance.text == 'Depth-First Search':
            self.dfs()
        elif instance.text == 'Breadth-First Search':
            self.bfs()
        elif instance.text == 'Dijkstra':
            self.dijsk()
        elif instance.text == 'A*':
            self.a_star()
        elif instance.text == 'Clear':
            self.clear_btns()
   
    def change_node_color(self, i, rgba, dt, play_sound=False):
        self.body.children[i].rgba.append(rgba)
        self.time2paint += dt
        if play_sound:
            Clock.schedule_once(self.body.children[i].play_block, self.time2paint)
            self.time2paint += block_sound.get_length()/2
        Clock.schedule_once(self.body.children[i].change_my_color, self.time2paint) 
        return True

    def dfs(self):
        root = Node.clicked_list[0]
        last = Node.clicked_list[1]
        Algo.dfs(root=root, 
                 last=last, 
                 graph=self.graph, 
                 callback=self.change_node_color, 
                 status=self.status, 
                 size=N)

    def bfs(self):
        root = Node.clicked_list[0]
        last = Node.clicked_list[1]
        Algo.bfs(root=root, 
                 last=last, 
                 graph=self.graph, 
                 callback=self.change_node_color, 
                 status=self.status, 
                 size=N)
        
    def dijsk(self): # ARRUMAR
        root = Node.clicked_list[0]
        last = Node.clicked_list[1]
        Algo.dijsktra(root=root, 
                      last=last, 
                      graph=self.graph, 
                      callback=self.change_node_color, 
                      status=self.status, 
                      size=N)

    def a_star(self): # ARRUMAR
        root = Node.clicked_list[0]
        last = Node.clicked_list[1]
        Algo.A_star(root=root, 
                    last=last, 
                    graph=self.graph, 
                    callback=self.change_node_color, 
                    status=self.status, 
                    size=N)
    
    def clear_btns(self):
         for v in range(len(self.body.children)):
            self.body.children[(N*N-1)-v].background_color = self.status['IDLE']
            Node.click_cnt = 0
            Node.clicked_list = []
            self.time2paint = 0

class MyApp(App):

    def build(self):
        return MyGrid()


if __name__ == '__main__':
    MyApp().run()
