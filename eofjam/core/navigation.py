from __future__ import annotations

class NavNode:
    
    def __init__(self, location: tuple[int, int]):
        self.location = location
        self.links = []

    def link(self, other: NavNode):
        if other in self.links:
            return
        self.links.append(other)
        other.links.append(self)

    def unlink(self, other: NavNode):
        if other not in self.links:
            return
        self.links.remove(other)
        other.links.remove(self)

    def clear(self):
        for link in self.links[:]:
            self.unlink(link)

    def __del__(self):
        for link in self.links:
            self.unlink(link)

    def __hash__(self):
        return hash(self.location)


class NavGrid:
    
    def __init__(self, grid_width: int, grid_height: int, pixel_width: int, pixel_height: int):
        self.nodes: list[list[NavNode]] = []
        self.nodes_flat: list[NavNode] = []
        
        # Because linking is two-way we only need to link 'backwards'
        for column in range(grid_width):
            column_list = []
            self.nodes.append(column_list)
            for row in range(grid_height):
                node = NavNode((column, row))
                if 0 <= column - 1:
                    node.link(self.nodes[column - 1][row])
                if 0 <= row - 1:
                    node.link(column_list[row - 1])
                column_list.append(node)
                self.nodes_flat.append(node)

        self.grid_width = grid_width
        self.grid_height = grid_height
        self.pixel_width = pixel_width
        self.pixel_height = pixel_height

    def get_node(self, location: tuple[float, float]) -> NavNode:
        x = int(round(location / self.pixel_width))
        y = int(round(location / self.pixel_height))
        return self.nodes[x][y]

    def get_path(self, source: tuple[float, float], target: tuple[float, float]):
        pass

    def clear(self):
        for node in self.nodes_flat:
            node.clear()
        self.nodes_flat = []
        self.nodes = []
