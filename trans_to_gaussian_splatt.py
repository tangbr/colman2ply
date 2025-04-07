import os
import sys
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram
import pyrr
from plyfile import PlyData
import torch  # For checking GPU availability

# Define the path to the .ply file
ply_file_path = r"C:\Users\bruce\senecaAIG\output\model.ply"

def load_ply(filepath):
    try:
        plydata = PlyData.read(filepath)
        vertex_data = np.array([list(x) for x in plydata['vertex'].data], dtype=np.float32)
        return vertex_data
    except Exception as e:
        print(f"Failed to load .ply file: {e}")
        sys.exit(1)

def compile_shader(source, shader_type):
    """Compile a shader from source."""
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        info = glGetShaderInfoLog(shader).decode('utf-8')
        raise RuntimeError(f'Shader compilation failed:\n{info}')
    return shader

def main():
    # Check for GPU availability
    device = "GPU" if torch.cuda.is_available() else "CPU"
    print(f"Running on {device}")

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption('Gaussian Splatting Example')

    vertex_data = load_ply(ply_file_path)
    vertex_count = len(vertex_data)

    # OpenGL context settings
    glEnable(GL_DEPTH_TEST)
    glPointSize(5)

    # Load shaders
    try:
        with open("shaders/vertex_shader.glsl", 'r') as f:
            vertex_src = f.read()
        with open("shaders/fragment_shader.glsl", 'r') as f:
            fragment_src = f.read()
    except IOError as e:
        print(f"Failed to load shader files: {e}")
        sys.exit(1)

    shader = compileProgram(
        compile_shader(vertex_src, GL_VERTEX_SHADER),
        compile_shader(fragment_src, GL_FRAGMENT_SHADER)
    )

    # Buffer setup
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

    position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    # Projection and view matrices
    proj_matrix = pyrr.matrix44.create_perspective_projection_matrix(45, display[0]/display[1], 0.1, 1000)
    view_matrix = pyrr.matrix44.create_look_at(
        eye = np.array([0, 1, 3]),
        target = np.array([0, 0, 0]),
        up = np.array([0, 1, 0])
    )
    proj_loc = glGetUniformLocation(shader, "projection")
    view_loc = glGetUniformLocation(shader, "view")

    glUseProgram(shader)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, proj_matrix)
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view_matrix)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glDrawArrays(GL_POINTS, 0, vertex_count)
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
