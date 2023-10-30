import pygame
import numpy as np
from OpenGL.GL import *



class Mesh:
    def __init__(self, program_id):
        self.vertices = [
            [-1,-1,0],
            [-1,1,0],
            [1,-1,0],
            [1,-1,0],
            [-1,1,0],
            [1,1,0]
        ]

        self.vertex_uvs = [[0, 0], [0, 1], [1, 0], [1, 0], [0, 1], [1, 1]]
        self.program_id = program_id
        self.vao_ref = glGenVertexArrays(1)
        # vertex array object reference
        glBindVertexArray(self.vao_ref)
        position_ref = glGenBuffers(1)
        position_data = np.array(self.vertices, np.float32)
        position_id = glGetAttribLocation(self.program_id, "position")
        glBindBuffer(GL_ARRAY_BUFFER, position_ref)
        glVertexAttribPointer(position_id, 3, GL_FLOAT, False, 0, None)
        # 3 bc it's a vec3
        glEnableVertexAttribArray(position_id)
        glBindBuffer(GL_ARRAY_BUFFER, position_ref)
        glBufferData(GL_ARRAY_BUFFER, position_data.ravel(), GL_STATIC_DRAW)
        
        uvs_ref = glGenBuffers(1)
        uvs_data = np.array(self.vertex_uvs, np.float32)
        uvs_id = glGetAttribLocation(self.program_id, "vertex_uv")
        glBindBuffer(GL_ARRAY_BUFFER, uvs_ref)
        glVertexAttribPointer(uvs_id, 2, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(uvs_id)
        glBindBuffer(GL_ARRAY_BUFFER, uvs_ref)
        glBufferData(GL_ARRAY_BUFFER, uvs_data.ravel(), GL_STATIC_DRAW)
        
        
    def draw(self, frame):
        timer_id = glGetUniformLocation(self.program_id, "iTime")
        glUniform1f(timer_id, frame)
        mouse_id = glGetUniformLocation(self.program_id, "iMouse")
        glUniform2f(mouse_id, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        glBindVertexArray(self.vao_ref)
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices))

