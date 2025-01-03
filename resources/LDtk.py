from dataclasses import dataclass
from enum import StrEnum
from typing import NamedTuple, Any
import json

@dataclass
class TilesetRect:
    h: int
    w: int
    x: int
    y: int
    tileset_uid: int

@dataclass
class EntityReferenceInfo:
    entity_iid: str
    layer_iid: str
    level_iid: str
    world_iid: str

class FieldType(StrEnum):
    INT = 'Int'
    FLOAT = 'Float' 
    STRING = 'String'
    BOOL = 'Bool'
    POINT = 'Point'
    TILE = 'Tile'
    ENTITY = 'EntityRef'
    FILE_PATH = 'FilePath'
    MULTILINE = 'Multilines'
    ARRAY = 'Array'
    ENUM = 'Enum'

@dataclass
class Field[V]:
    identifer: str
    tile: TilesetRect | None
    type: FieldType
    value: V | None
    def_uid: int

class TileRenderMode(StrEnum):
    COVER = 'Cover'
    FIT_INSIDE = 'FitInside'
    REPEAT = 'Repeat'
    STRETCH = 'Stretch'
    FULL_SIZE_CROPPED = 'FullSizeCropped'
    FULL_SIZE_UNCROPPED = 'FullSizeUncropped'
    NINE_SLICE = 'NineSlice'

@dataclass
class EntityDefinition:
    color: str
    height: int
    width: int
    identifier: str
    nine_slice_borders: list[int]
    pivot_x: float
    pivot_y: float
    tile_rect: TilesetRect
    tile_render_mode: TileRenderMode
    tileset_id: int | None
    ui_tile_rect: TilesetRect | None
    uid: int

@dataclass
class EnumValueDefintion:
    color: int
    id: str
    tile_rect: TilesetRect

@dataclass
class EnumDefinition:
    external_rel_path: str | None
    icon_tileset_uid: int | None
    identifier: str
    tags: list[str]
    uid: int
    values: list[EnumValueDefintion]

class LayerType(StrEnum):
    INT_GRID = 'IntGrid'
    ENTITIES = 'Entities'
    TILES = 'Tiles'
    AUTO_LAYER = 'AutoLayer'

@dataclass
class GridValueObj:
    color: str
    group_uid: int
    identifier: str | None
    tile: TilesetRect | None
    value: int

@dataclass
class GridValueGroupObj:
    color: str | None
    identifier: str | None
    uid: int

@dataclass
class LayerDefintion:
    type: LayerType
    auto_source_layer_def_uid: int | None
    display_opacity: float
    grid_size: int
    identifier: str
    int_grid_values: list[GridValueObj]
    int_grid_values_groups: list[GridValueGroupObj]
    parallax_factor_x: float
    parallax_factor_y: float
    parallax_scaling: bool
    px_offset_x: int
    px_offset_y: int
    tileset_def_uid: int
    uid: int

@dataclass
class CustomDataObj:
    data: str
    tile_id: int

class EmbedAtlas(StrEnum):
    LDTK_ICONS = 'LdtkIcons'

@dataclass
class EnumTagObj:
    enum_value_id: str
    tile_ids: list[int]

@dataclass
class TilesetDefintion:
    c_height: int
    c_width: int
    custom_data: list[CustomDataObj]
    embed_atlas: EmbedAtlas | None
    enum_tags: EnumTagObj
    identifier: str
    padding: int
    px_height: int
    px_width: int
    rel_path: str | None
    spacing: int
    tags: list[str]
    tag_source_enum_id: int | None
    tile_grid_size: int
    uid: int

@dataclass
class Definitions:
    entities: list[EntityDefinition]
    enums: list[EnumDefinition]
    external_enums: list[EnumDefinition]
    layers: list[LayerDefintion]
    tilesets: list[TilesetDefintion]

@dataclass
class bgCropObj:
    crop_x: float
    crop_y: float
    crop_width: float
    crop_height: float
    scale_x: float
    scale_y: float
    top_left: tuple[int, int]

    @property
    def crop_rect(self) -> tuple[float, float, float, float]:
        return self.crop_x, self.crop_y, self.crop_width, self.crop_height

    @property
    def scale(self) -> tuple[float, float]:
        return self.scale_x, self.scale_y

@dataclass
class NeighbourObj:
    dir: str
    level_iid: str

@dataclass
class Tile:
    alpha: float
    flip: int
    pos_x: int
    pos_y: int
    src_x: int
    src_y: int
    tile_id: int

    @property
    def pos(self) -> tuple[int, int]:
        return self.pos_x, self.pos_y
    
    @property
    def src(self) -> tuple[int, int]:
        return self.src_x, self.src_y

@dataclass
class Entity:
    grid_x: int
    grid_y: int
    identifier: str
    pivot_x: float
    pivot_y: float
    smart_color: str
    tags: list[str]
    tile: TilesetRect | None
    world_x: int | None
    world_y: int | None
    def_uid: int
    field_instances: list[Field]
    height: int
    width: int
    iid: str
    px_x: int
    px_y: int

    @property
    def grid(self) -> tuple[int, int]:
        return self.grid_x, self.grid_y
    
    @property
    def pivot(self) -> tuple[float, float]:
        return self.pivot_x, self.pivot_y
    
    @property
    def px(self) -> tuple[int, int]:
        return self.px_x, self.px_y

@dataclass
class Layer:
    c_height: int
    c_width: int
    grid_size: int
    identifier: str
    opacity: float
    px_total_offset_x: int
    px_total_offset_y: int
    tileset_def_uid: int | None
    tileset_rel_path: str | None
    type: LayerType
    auto_layer_tiles: list[Tile]
    entity_instances: list[Entity]
    grid_tiles: list[Tile]
    iid: str
    int_grid_csv: list[int]
    layer_def_uid: int
    level_id: int
    override_tileset_uid: int | None
    px_offset_x: int
    px_offset_y: int
    visible: bool

@dataclass
class Level:
    bg_color: str
    bg_pos: bgCropObj | None
    neighbours: list[NeighbourObj]
    bg_rel_path: str | None
    external_rel_path: str | None
    field_instance: list[Field]
    identifier: str
    iid: str
    layer_instances: list[Layer]
    px_height: int
    px_width: int
    uid: int
    world_depth: int
    world_x: int
    world_y: int


class WorldLayout(StrEnum):
    FREE = 'Free'
    GRID_VANIA = 'GridVania'
    LINEAR_HORIZONTAL = 'LinearHorizontal'
    LINEAR_VERTICAL = 'LinearVertical'

@dataclass
class World:
    idenitifer: str
    iid: str
    levels: list[Level]
    world_grid_height: int | None
    world_grid_width: int | None
    world_layout: WorldLayout

@dataclass
class InstanceDataObj:
    fields: Any
    height_px: int
    width_px: int
    world_x: int
    world_y: int
    iids: int

@dataclass
class TocObj:
    identifier: str
    instance_data: list[InstanceDataObj]

@dataclass
class LDtkRoot:
    bg_color: str
    defs: Definitions
    external_levels: bool
    iid: str
    json_version: str
    levels: list[Level]
    toc: list[TocObj]
    world_grid_height: int | None
    world_grid_width: int | None
    world_layout: WorldLayout | None
    worlds: list[World]

def _parse_LDtk_tileset_rect(data: dict[str, Any] | None) -> TilesetRect | None:
    if data is None:
        return data
    return TilesetRect(data['h'], data['w'], data['x'], data['y'], data['tilesetUid'])

def _parse_LDtk_entity_def(data: dict[str, Any]) -> EntityDefinition:
    return EntityDefinition(
        data['color'],
        data['height'],
        data['width'],
        data['identifier'],
        data['nineSliceBorders'],
        data['pivotX'],
        data['pivotY'],
        _parse_LDtk_tileset_rect(data['tileRect']),
        TileRenderMode(data['tileRenderMode']),
        data['tilesetId'],
        _parse_LDtk_tileset_rect(data['uiTileRect']),
        data['uid']
    )

def _parse_LDtk_enum_def(data: dict[str, Any]) -> EnumDefinition:
    return EnumDefinition(
        data['externalRelPath'],
        data['iconTilesetUid'],
        data['identifier'],
        data['tags'],
        data['uid'],
        [EnumValueDefintion(sub['color'], sub['id'], _parse_LDtk_tileset_rect(sub['tileRect'])) for sub in data['values']]
    )

def _parse_LDtk_layer_def(data: dict[str, Any]) -> LayerDefintion:
    return LayerDefintion(
        LayerType(data['__type']),
        data['autoSourceLayerDefUid'],
        data['displayOpacity'],
        data['gridSize'],
        data['identifier'],
        [GridValueObj(sub['color'], sub['groupUid'], sub['identifier'], _parse_LDtk_tileset_rect(sub['tile']), sub['value']) for sub in data['intGridValues']],
        [GridValueGroupObj(sub['color'], sub['identifier'], sub['uid']) for sub in data['intGridValuesGroups']],
        data['parallaxFactorX'],
        data['parallaxFactorY'],
        data['parallaxScaling'],
        data['pxOffsetX'],
        data['pxOffsetY'],
        data['tilesetDefUid'],
        data['uid'],
    )

def _parse_LDtk_tileset_def(data: dict[str, Any]) -> TilesetDefintion:
    embed_atlas = data.get('embedAtlas', None)
    if embed_atlas is not None:
        embed_atlas = EmbedAtlas(embed_atlas)

    return TilesetDefintion(
        data['__cHei'],
        data['__cWid'],
        [CustomDataObj(sub['data'], sub['tileId']) for sub in data['customData']],
        embed_atlas,
        [EnumTagObj(sub['enumValueId'], sub['tileIds']) for sub in data['enumTags']],
        data['identifier'],
        data['padding'],
        data['pxHei'],
        data['pxWid'],
        data['relPath'],
        data['spacing'],
        data['tags'],
        data['tagsSourceEnumUid'],
        data['tileGridSize'],
        data['uid']
    )

def _parse_LDtk_defintions(data: dict[str, Any]) -> Definitions:
    return Definitions(
        [_parse_LDtk_entity_def(data) for data in data.get('entities', [])],
        [_parse_LDtk_enum_def(data) for data in data.get('enums', [])],
        [_parse_LDtk_enum_def(data) for data in data.get('externalEnums', [])],
        [_parse_LDtk_layer_def(data) for data in data.get('layers', [])],
        [_parse_LDtk_tileset_def(data) for data in data.get('tilesets', [])],
    )

def _parse_LDtk_entity_info(data: dict[str, str] | None) -> EntityReferenceInfo:
    if data is None:
        return data
    
    return EntityReferenceInfo(
        data['entityIid'],
        data['layerIid'],
        data['levelIid'],
        data['worldIid']
    )

def _convert_LDtk_field_type(type_string: str, data: Any | None) -> tuple[FieldType, type, Any]:
    if type_string in FieldType:
        typ = FieldType(type_string)
    elif type_string.startswith('LocalEnum'):
        typ = FieldType.ENUM
    elif type_string.startswith('Array'):
        typ = FieldType.ARRAY
    else:
        typ = None

    value = None
    match typ:
        case FieldType.INT:
            cls = int
        case FieldType.FLOAT:
            cls = float
        case FieldType.STRING:
            cls = str
        case FieldType.BOOL:
            cls = bool
        case FieldType.POINT:
            cls = tuple[float, float]
            if data is not None:
                value = data['cx'], data['cy']
        case FieldType.TILE:
            cls = TilesetRect
            value = _parse_LDtk_tileset_rect(data)
        case FieldType.ENTITY:
            cls = EntityReferenceInfo
            value = _parse_LDtk_entity_info(data)
        case FieldType.FILE_PATH:
            cls = str
        case FieldType.MULTILINE:
            cls = str
        case FieldType.ARRAY:
            sub = type_string.split('<')[-1].strip('>')
            _, sub_cls, _ = _convert_LDtk_field_type(sub, None)
            cls = list[sub_cls]
            if data is not None and sub_cls is not None:
                value = [sub_cls(v) for v in data]
        case FieldType.ENUM:
            cls = str
        case _:
            cls = None

    if value is None and cls is not None and data is not None:
        value = cls(data)
        
    return typ, cls, value

def _parse_LDtk_field(data: dict[str, Any]) -> Field:
    typ, cls, value = _convert_LDtk_field_type(data['__type'], data['__value'])

    return Field[cls](
        data['__identifier'],
        _parse_LDtk_tileset_rect(data['__tile']),
        typ,
        value,
        data['defUid']
    )

def _parse_LDtk_entity(data: dict[str, Any]) -> Entity:
    return Entity(
        data['__grid'][0],
        data['__grid'][1],
        data['__identifier'],
        data['__pivot'][0],
        data['__pivot'][1],
        data['__smartColor'],
        data['__tags'],
        _parse_LDtk_tileset_rect(data['__tile']),
        data['__worldX'],
        data['__worldY'],
        data['defUid'],
        [_parse_LDtk_field(field) for field in data['fieldInstances']],
        data['height'],
        data['width'],
        data['iid'],
        data['px'][0],
        data['px'][1]
    )

def _parse_LDtk_layer(data: dict[str, Any]) -> Layer:
    return Layer(
        data['__cHei'],
        data['__cWid'],
        data['__gridSize'],
        data['__identifier'],
        data['__opacity'],
        data['__pxTotalOffsetX'],
        data['__pxTotalOffsetY'],
        data['__tilesetDefUid'],
        data['__tilesetRelPath'],
        data['__type'],
        [Tile(tile['a'], tile['f'], *tile['px'], *tile['src'], tile['t']) for tile in data['autoLayerTiles']],
        [_parse_LDtk_entity(entity) for entity in data['entityInstances']],
        [Tile(tile['a'], tile['f'], *tile['px'], *tile['src'], tile['t']) for tile in data['gridTiles']],
        data['iid'],
        data['intGridCsv'],
        data['layerDefUid'],
        data['levelId'],
        data['overrideTilesetUid'],
        data['pxOffsetX'],
        data['pxOffsetY'],
        data['visible']
    )

def _parse_LDtk_level(data: dict[str, Any]) -> Level:
    bg_crop = data.get('__bgPos', None)
    if bg_crop is not None:
        bg_crop = bgCropObj(*bg_crop['cropRect'], *bg_crop['scale'], bg_crop['topLeftPx'])

    layer_instances = data.get('layerInstances', None)
    if layer_instances is not None:
        layer_instances = [_parse_LDtk_layer(layer) for layer in layer_instances]

    return Level(
        data['__bgColor'],
        bg_crop,
        [NeighbourObj(sub['dir'], sub['levelIid']) for sub in data['__neighbours']],
        data.get('bgRelPath', None),
        data.get('externalRelPath', None),
        [Field(field['__identifier'], field['__tile'], field['__type'], field['__value'], field['defUid']) for field in data['fieldInstances']],
        data['identifier'],
        data['iid'],
        layer_instances,
        data['pxHei'],
        data['pxWid'],
        data['uid'],
        data['worldDepth'],
        data['worldX'],
        data['worldY'],
    )

def _parse_LDtk_toc(data: dict[str, Any]) -> TocObj:
    return TocObj(
        data['identifier'],
        [InstanceDataObj(sub['fields'], sub['heiPx'], sub['heiPx'], sub['worldX'], sub['worldY'], sub['iids']) for sub in data['instancesData']],
    )

def _parse_LDtk_world(data: dict[str, Any]) -> World:
    return World(
        data['identifier'],
        data['iid'],
        [_parse_LDtk_level(level) for level in data['levels']],
        data.get('worldGridHeight', None),
        data.get('worldGridWidth', None),
        WorldLayout(data['worldLayout'])
    )

def parse_LDtk_file(path: str) -> LDtkRoot:
    with open(path, 'r') as fp:
        root_data = json.load(fp)

    world_layout = root_data.get('worldLayout', None)
    if world_layout is not None:
        world_layout = WorldLayout(world_layout)

    return LDtkRoot(
        root_data['bgColor'],
        _parse_LDtk_defintions(root_data['defs']),
        root_data['externalLevels'],
        root_data['iid'],
        root_data['jsonVersion'],
        [_parse_LDtk_level(level) for level in root_data['levels']],
        [_parse_LDtk_toc(toc) for toc in root_data['toc']],
        root_data.get('worldGridHeight', None),
        root_data.get('worldGridWidth', None),
        world_layout,
        [_parse_LDtk_world(world) for world in root_data['worlds']]
    )
