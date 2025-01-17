from __future__ import annotations

from queue import PriorityQueue

import arcade

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
    
    def __hash__(self):
        return hash(self.location)
    
    def __str__(self):
        return f"<{self.location[0]},{self.location[1]}>"

    def __repr__(self):
        return f"Node{self.location}[{','.join(str(n) for n in self.links)}]"
    
    def __eq__(self, value):
        return self.location == value.location
    
    def __lt__(self, value):
        return self.location < value.location


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
        x = int(round(location[0] / self.pixel_width - 0.5))
        y = int(round(location[1] / self.pixel_height - 0.5))
        return self.nodes[x][y]

    def get_path(self, source: tuple[float, float], target: tuple[float, float]) -> list[NavNode]:
        start = self.get_node(source)
        end = self.get_node(target)

        if not (start.links and end.links):
            # One or both nodes can't be reached ever so don't waste time
            return []

        frontier: PriorityQueue[tuple[int, NavNode]] = PriorityQueue()
        frontier.put((0, start))

        checked = set()
        checked.add(start)
        
        came_from: dict[NavNode, NavNode] = { start: None }
        cost_to: dict[NavNode, int] = { start: 0 }

        while not frontier.empty():
            _, current = frontier.get()

            if current == end:
                break

            for link in current.links:
                new_cost = cost_to[current] + 1
                if link not in cost_to or new_cost < cost_to[link]:
                    cost_to[link] = new_cost
                    priority = new_cost + (abs(current.location[0] - end.location[0]) + abs(current.location[1] - end.location[1])) # A* hueristic for better search speed
                    frontier.put((priority, link))
                    came_from[link] = current
    
        to = end
        path = [to]
        while to != start:
            to = came_from[to]
            path.append(to)
        return path[::-1] # reverse it because we started at the end and worked backward

    def clear(self):
        for node in self.nodes_flat:
            node.clear()
        self.nodes_flat = []
        self.nodes = []

    def draw(self):
        w, h = self.pixel_width, self.pixel_height
        h_w = w / 2.0
        h_h = h / 2.0

        linked = [(p.location[0] * w + h_w, p.location[1] * h + h_h) for p in self.nodes_flat if len(p.links) == 4]
        sewi = [(p.location[0] * w + h_w, p.location[1] * h + h_h) for p in self.nodes_flat if 0 < len(p.links) < 4]
        alone = [(p.location[0] * w + h_w, p.location[1] * h + h_h) for p in self.nodes_flat if len(p.links) == 0]

        arcade.draw_points(linked, arcade.color.RAZZLE_DAZZLE_ROSE, 20)
        arcade.draw_points(sewi, arcade.color.BLUE_GREEN, 20)
        arcade.draw_points(alone, arcade.color.ORANGE, 20)

