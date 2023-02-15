from pyglet.gl import *
from pyglet.graphics import Batch
from pyglet.graphics.shader import ShaderProgram


_quad_indices = (0, 1, 2, 0, 2, 3)


def _make_quad_vertices( width: int, height: int ) -> tuple[int, ...]:
    x_min = 0
    x_max = width

    y_min = 0
    y_max = height

    return (
        x_min, y_min,   # bottom left
        x_max, y_min,   # bottom right
        x_max, y_max,   # top right
        x_min, y_max    # top left
    )


def make_quad_vertex_list( shader: ShaderProgram, batch: Batch, width: int, height: int ):
    vertex_positions = _make_quad_vertices( width, height )
    kwargs = { 'position': ('f', vertex_positions) }
    vertex_list = shader.vertex_list_indexed(
        4,
        GL_TRIANGLES,
        _quad_indices,
        batch,
        **kwargs
    )
    return vertex_list
