import os
from OpenGL.GL import *
import pygame
from pygame.locals import *
import numpy as np
from time import gmtime

# from https://gist.github.com/NickBeeuwsaert/fec10bd5d63b618e9432
    
    

class PyOGLApp():
    def __init__(self, screen_posX, screen_posY, screen_width, screen_height):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (screen_posX, screen_posY)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screenshot_path = 'dump'
        self.zoom_amount = 1.2
        self.center = (0,0)
        self.iterparam = 50
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 32)
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE |pygame.DOUBLEBUF|pygame.OPENGL|pygame.HWSURFACE)
        pygame.display.set_caption("frctlexplorer")
        pygame_icon = pygame.image.load('Julia.ico')
        pygame.display.set_icon(pygame_icon)
        self.program_id = None
        self.clock = pygame.time.Clock()
        
      
      
    def update_colouring(self, n):
        self.colouring = n
        glUseProgram(self.program_id)
        colouring_id = glGetUniformLocation(self.program_id, "colouring")
        glUniform1i(colouring_id, self.colouring)
        
    def update_zoom(self):
        glUseProgram(self.program_id)
        zoom_amount_id = glGetUniformLocation(self.program_id, "zoom_amount")
        glUniform1f(zoom_amount_id, self.zoom_amount)
        center_id = glGetUniformLocation(self.program_id, "center")
        glUniform2f(center_id, *self.center)
        
    def update_iterparam(self):
        glUseProgram(self.program_id)
        iterparam_id = glGetUniformLocation(self.program_id, "iterParam")
        glUniform1i(iterparam_id, self.iterparam)
    
    def manage_events(self, states):
        running = states["running"]
        paused = states["paused"]
        speed = states["speed"]
        slowed = states["slowed"]
        itermodifier = states["itermodifier"]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                # Toggle fullscreen mode
                pygame.display.toggle_fullscreen()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = bool(1-paused)
            if event.type == pygame.KEYDOWN: # press o, arrow keys, screenshot, c or r
                if event.key == pygame.K_o:
                    self.make_open_window()                
                if event.key == pygame.K_RIGHT:
                    speed = 2
                elif event.key == pygame.K_LEFT:
                    speed = 1/2
                elif event.key == pygame.K_UP:
                    itermodifier = 1
                elif event.key == pygame.K_DOWN:
                    itermodifier = -1
                if event.key == pygame.K_LCTRL:
                    slowed = True
                if event.key == pygame.K_c:
                    colouring = np.random.randint(0,9)
                    while colouring == self.colouring:
                        colouring = np.random.randint(0,9)
                    self.update_colouring(colouring)
                if event.key == pygame.K_F12: # ~~find way to resize when taking screenshot~~ (not viable)
                    filepath = self.screenshot_path + '/'
                    screenshot_time = gmtime()
                    for n in screenshot_time[:6]: # YYYY-MM-DD-hh-mm-ss
                        filepath += str(n)
                    filepath += '.png'
                    buffer = glReadPixels(0, 0, self.screen_width, self.screen_height, GL_RGBA, GL_UNSIGNED_BYTE)
                    pygame.image.save(pygame.transform.flip(pygame.image.fromstring(buffer, (self.screen_width, self.screen_height), "RGBA"), False, True), filepath)
                if event.key == pygame.K_r:
                    lp_id, rp_id = glGetUniformLocation(self.program_id, "lp"), glGetUniformLocation(self.program_id, "rp")
                    cmapc_id= glGetUniformLocation(self.program_id, "cmapc")
                    rrp, rlp, glp, grp, blp, brp = np.random.rand(6)*4.9+0.1
                    R = lambda t :  (1-t)**rrp*t**rlp
                    G = lambda t :  (1-t)**grp*t**glp
                    B = lambda t :  (1-t)**brp*t**blp
                    x = np.linspace(0,1,50)
                    rc, gc, bc = 1/max(R(x)), 1/max(G(x)), 1/max(B(x))                    
                    glUniform3f(lp_id, rlp,glp,blp), glUniform3f(rp_id, rrp,grp,brp), glUniform3f(cmapc_id, rc,gc,bc)
                    self.update_colouring(-1)
            if event.type == pygame.MOUSEWHEEL:
                cx,cy = pygame.mouse.get_pos()
                self.center = ((cx/self.screen_width)*2-1)*2*self.zoom_amount*(self.screen_width/(2*self.screen_height))+self.center[0], (((-cy/self.screen_height)+1)*2-1)*self.zoom_amount+self.center[1]
                self.zoom_amount *= (1.25-0.75*event.y)
                self.update_zoom()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left click
                    w,h = pygame.mouse.get_pos()
                    print(((w/self.screen_width)*2-1)*2*self.zoom_amount*(self.screen_width/(2*self.screen_height))+self.center[0], (((-h/self.screen_height)+1)*2-1)*self.zoom_amount+self.center[1])
                if event.button == 2: # middle click
                    colouring = np.random.randint(0,9)
                    while colouring == self.colouring:
                        colouring = np.random.randint(0,9)
                    self.update_colouring(colouring)
            if event.type == pygame.KEYUP: # release arrow keys
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    speed = 1
                if event.key == pygame.K_LCTRL:
                    slowed = False
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    itermodifier = 0
            if event.type == pygame.VIDEORESIZE:
                self.screen_width, self.screen_height = event.w, event.h
        
        return {"running":running, "paused":paused, "speed":speed, "slowed":slowed, "itermodifier":itermodifier}
        
    def mainloop(self):
        states = {
            "running":True,
            "paused":False,
            "speed":1,
            "slowed":False,
            "itermodifier":0
        }
        running = states["running"]
        paused = states["paused"]
        speed = states["speed"]
        slowed = states["slowed"]
        itermodifier = states["itermodifier"]
        time_paused = 0
        slowed_amount = 0
        self.initialise()
        origin = 0
        self.update_zoom()
        while running:
            if slowed:
                slowed_amount += 1/35 # arbitrary
            origin += np.log2(speed)*0.2 # origin displacement allows smooth fast-forward / fast-backward time control
            ticks = pygame.time.get_ticks()*0.002 - time_paused + origin - slowed_amount
            states = self.manage_events(states)
            running = states["running"]
            paused = states["paused"]
            speed = states["speed"]
            slowed = states["slowed"]
            itermodifier = states["itermodifier"]
            #ticks *= speed
            self.iterparam += itermodifier
            if self.iterparam < 1: self.iterparam = 1
            self.update_iterparam()
            while paused:
                states = self.manage_events(states)
                running = states["running"]
                paused = states["paused"]
                itermodifier = states["itermodifier"]
                speed = 1
                self.iterparam += itermodifier
                if self.iterparam < 1: self.iterparam = 1
                self.update_iterparam()
                self.display(ticks)
                pygame.display.flip()
                if not running:
                    pygame.quit()
                if not paused:
                    time_paused = (pygame.time.get_ticks()*0.002 - ticks + origin - slowed_amount)
            self.display(ticks)
            pygame.display.flip()
            self.clock.tick(60)
            #x,y = pygame.mouse.get_pos()
            #print((x/self.screen_width)*2-1, (y/self.screen_height)*2-1)
        pygame.quit()




if __name__ == "__main__":
    width, height = 800, 600
    pygame.init()
    pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.DOUBLEBUF|pygame.OPENGL|pygame.HWSURFACE)
    

    glViewport(0, 0, width, height)
    
    shader = glCreateShader(GL_VERTEX_SHADER)
    info_log = glGetShaderInfoLog(shader)

    print(info_log)


    program = glCreateProgram()
    
    glAttachShader(program, shader)
    
    glLinkProgram(program)
    
    glUseProgram(program)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                # Toggle fullscreen mode
                pygame.display.toggle_fullscreen()
            pygame.display.flip()
        pygame.quit()
        

