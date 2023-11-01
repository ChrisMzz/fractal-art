from glapp.pyoglapp import *
from glapp.utils import *
from glapp.gameobjects.mesh import *
from OpenGL.GL import *
from explorer_preprocessing import CustomFrctl
from zipfile import ZipFile
import sys, json, os

CWD = os.getcwd()

def load(path) -> CustomFrctl:
    os.chdir(os.path.abspath(os.path.dirname(path))) # dirname gives relative directory to file, abspath is in case that's ""
    filename = os.path.basename(path)
    with ZipFile(filename) as zipfile:
        metadata_file = open(zipfile.extract('metadata.json'))
        metadata = json.load(metadata_file)
        metadata_file.close()
        arr = np.load(zipfile.extract('function.npy'))
        os.remove(zipfile.extract("metadata.json"))
        os.remove(zipfile.extract("function.npy"))
        return CustomFrctl(arr, metadata)


class FractalViewer(PyOGLApp):
    def __init__(self, width, height, frag_name):
        super().__init__(0, 0, width, height)
        self.screen_plane = None
        self.frag_name = frag_name
        
        
    def initialise(self):
        self.program_id = create_program(open("shaders/vert.glsl", 'r').read(), open(f"shaders/frag_{self.frag_name}.glsl", 'r').read())
        self.screen_plane = Mesh(self.program_id)
        self.update_colouring(0)

    def display(self, speed):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        res_id = glGetUniformLocation(self.program_id, "iResolution")
        glUniform2f(res_id, self.screen_width, self.screen_height)
        self.screen_plane.draw(speed)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        frctl = load(sys.argv[1])
        os.chdir(CWD), os.chdir(os.path.abspath(sys.argv[0][:-16])) # sets cwd to executable / python filepath
        with open("shaders\\frag_frctl.glsl", "w") as fp:
            fp.write(frctl.parse())
    
    pygame.init()
    width, height = 720, 480
    pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.DOUBLEBUF|pygame.OPENGL|pygame.HWSURFACE)
    glViewport(0, 0, width, height)
    FractalViewer(width, height, "frctl").mainloop()
