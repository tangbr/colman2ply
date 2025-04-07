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
import argparse

def load_ply(filepath):
    try:
        plydata = PlyData.read(filepath)
        vertex_data = np.array([list(x) for x in plydata['vertex'].data], dtype=np.float32)
        return vertex_data
    except Exception as e:
        print(f"Failed to load .ply file: {e}")
        sys.exit(1)

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        info = glGetShaderInfoLog(shader).decode('utf-8')
        raise RuntimeError(f'Shader compilation failed:\n{info}')
    return shader

def load_shader(file_path):
    try:
        with open(file_path, 'r') as f:
            shader_src = f.read()
        return shader_src
    except IOError as e:
        print(f"Failed to load shader file: {e}")
        sys.exit(1)

def main(ply_file_path):
    device = "GPU" if torch.cuda.is_available() else "CPU"
    print(f"Running on {device}")

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption('Gaussian Splatting Example')

    vertex_data = load_ply(ply_file_path)
    vertex_count = len(vertex_data)

    glEnable(GL_DEPTH_TEST)
    glPointSize(5)

    vertex_src = load_shader("shaders/vertex_shader.glsl")
    fragment_src = load_shader("shaders/fragment_shader.glsl")

    shader = compileProgram(
        compile_shader(vertex_src, GL_VERTEX_SHADER),
        compile_shader(fragment_src, GL_FRAGMENT_SHADER)
    )

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

    position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

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
    parser = argparse.ArgumentParser()
    parser.add_argument("--ply_file_path", default="./model.ply", help="Path to the .ply file")
    args = parser.parse_args()
    main(args.ply_file_path)
