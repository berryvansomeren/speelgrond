import logging
from pathlib import Path

from pyglet.graphics.shader import Shader, ShaderProgram


# Define a basic Vertex Shader
# Note that depending on whether they are used,
# the tex_coords might be optimized out
_vertex_source = """#version 330 core
    in vec2 position;
    in vec3 tex_coords;
    out vec3 texture_coords;

    uniform WindowBlock 
    {                       // This UBO is defined on Window creation, and available
        mat4 projection;    // in all Shaders. You can modify these matrixes with the
        mat4 view;          // Window.view and Window.projection properties.
    } window;  

    void main()
    {
        gl_Position = window.projection * window.view * vec4(position, 1, 1);
        texture_coords = tex_coords;
    }
"""


def read_file_as_string( path: Path ) -> str:
    with open(path, 'r') as file:
        result = file.read()
    return result


def make_shader( frag_shader_path: Path) -> ShaderProgram:
    vert_shader = Shader(_vertex_source, 'vertex')
    frag_shader_source = read_file_as_string( frag_shader_path )
    frag_shader = Shader(frag_shader_source, 'fragment')
    shader_program = ShaderProgram(vert_shader, frag_shader)

    logging.info(f'Found {len(shader_program.attributes)} attributes in the shader program')
    for attribute in shader_program.attributes:
        logging.info(f'- {attribute}')

    logging.info(f'Found {len(shader_program.uniforms)} uniforms in the shader program')
    for uniform in shader_program.uniforms.items():
        logging.info(f'- {uniform}')

    return shader_program