from dataclasses import dataclass

import pyglet
from pyglet.gl import *
from pyglet.graphics import Batch
from pyglet.graphics.shader import ShaderProgram
from pyglet.graphics.vertexdomain import VertexList


from speelgrond.screen_shader.shader import make_shader
from speelgrond.screen_shader.quad import make_quad_vertex_list


@dataclass
class ScreenShaderRenderPack:
    shader: ShaderProgram
    batch: Batch
    vertex_list: VertexList

    def draw( self ):
        self.batch.draw()


def load_screen_shader( frag_shader_path, width, height ):
    shader = make_shader( frag_shader_path )
    batch = pyglet.graphics.Batch()
    vertex_list = make_quad_vertex_list(
        shader = shader,
        batch = batch,
        width = width,
        height = height
    )
    return ScreenShaderRenderPack( shader, batch, vertex_list )
