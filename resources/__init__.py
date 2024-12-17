from collections.abc import Sequence
import json
from .filefactory import make_file_opener, make_path_finder, make_string_opener
from arcade import (
    ArcadeContext,
    Sound,
    Texture,
    SpriteSheet,
    load_sound as _load_sound,
    load_texture as _load_texture,
    load_spritesheet as _load_spritesheet,
    load_font as _load_font
)
from arcade.hitbox import HitBoxAlgorithm
from arcade.gl import Program

import resources.audio as audio
import resources.data as data
import resources.fonts as fonts
import resources.images as images
import resources.shaders as shaders

__all__ = (
    'read_shader',
    'load_program',
    'get_png_path',
    'load_png',
    'load_png_sheet',
    'get_wav_path',
    'get_ogg_path',
    'load_wav',
    'load_ogg',
    'get_font_path',
    'load_font',
    'read_json',
    'open_json',
    'load_json',
    'dump_json'
)

# Shader methods
read_shader = make_string_opener(shaders, 'glsl')


def load_program(
        ctx: ArcadeContext,
        *,
        vertex_shader: str,
        fragment_shader: str | None = None,
        geometry_shader: str | None = None,
        tess_control_shader: str | None = None,
        tess_evaluation_shader: str | None = None,
        sub_directories: tuple[str, ...] = (),
        common: list[str] | None = None,
        defines: dict[str, str] | None = None,
        varyings: Sequence[str] | None = None,
        varyings_capture_mode: str = "interleaved"
    ) -> Program:
    """
    Load a glsl shader program by providing the names for the required shaders.

    Returns:
        an Arcade gl Program for use with gl Geometry.
    """
    vertex = read_shader(vertex_shader, sub_directories)
    fragment = None if fragment_shader is None else read_shader(fragment_shader, sub_directories)
    geometry = None if geometry_shader is None else read_shader(geometry_shader, sub_directories)
    tess_control = None if tess_control_shader is None else read_shader(tess_control_shader, sub_directories)
    tess_evaluation = None if tess_evaluation_shader is None else read_shader(tess_evaluation_shader, sub_directories)

    return ctx.program(
        vertex_shader=vertex,
        fragment_shader=fragment,
        geometry_shader=geometry,
        tess_control_shader=tess_control,
        tess_evaluation_shader=tess_evaluation,
        common=common,
        defines=defines,
        varyings=varyings,
        varyings_capture_mode=varyings_capture_mode
    )


# Texture methods
get_png_path = make_path_finder(images, 'png')
def load_png(name: str, sub_directories: tuple[str, ...] = (), *, hit_box_algorithm: HitBoxAlgorithm | None = None, hash: str | None = None) -> Texture:
    return _load_texture(get_png_path(name, sub_directories), hit_box_algorithm=hit_box_algorithm, hash=hash)

def load_png_sheet(name: str, sub_durectories: tuple[str, ...] = ()) -> SpriteSheet: return _load_spritesheet(get_png_path(name, sub_durectories))


# Sound Methods
get_wav_path = make_path_finder(audio, 'wav')
get_ogg_path = make_path_finder(audio, 'ogg')
def load_wav(name: str, streaming: bool = False, sub_directories: tuple[str, ...] = ()) -> Sound: return _load_sound(get_wav_path(str, sub_directories), streaming)
def load_ogg(name: str, streaming: bool = False, sub_directories: tuple[str, ...] = ()) -> Sound: return _load_sound(get_ogg_path(str, sub_directories), streaming)

# Font Methods
get_font_path = make_path_finder(fonts, 'ttf')
def load_font(name: str, sub_directories: tuple[str, ...] = ()) -> None: _load_font(get_font_path(name, sub_directories))

# Data Methods
read_json = make_string_opener(data, 'json')
open_json = make_file_opener(data, 'json')
def load_json(name: str, sub_directories: tuple[str, ...] = ()) -> dict: return json.loads(read_json(name, sub_directories))
def dump_json(name: str, data: dict, sub_directoreis: tuple[str, ...] = ()) -> None:
    with open_json(name, sub_directoreis, 'w') as fp:
        json.dump(data, fp)
