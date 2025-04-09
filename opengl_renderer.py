import OpenGL.GL as gl
import OpenGL.GL.shaders as shaders
import pygame

def init_gl():
    """Initialize OpenGL settings for rendering."""
    gl.glClearColor(0.0, 0.0, 0.0, 0.0)  # Set background color
    vertex_shader = """
    #version 330
    in vec3 position;
    void main() {
       gl_Position = vec4(position, 1.0);
    }
    """
    fragment_shader = """
    #version 330
    out vec4 fragColor;
    void main() {
       fragColor = vec4(1.0, 1.0, 1.0, 1.0);
    }
    """
    shader = shaders.compileProgram(
        shaders.compileShader(vertex_shader, gl.GL_VERTEX_SHADER),
        shaders.compileShader(fragment_shader, gl.GL_FRAGMENT_SHADER)
    )
    gl.glUseProgram(shader)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

    init_gl()  # Initialize OpenGL

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
