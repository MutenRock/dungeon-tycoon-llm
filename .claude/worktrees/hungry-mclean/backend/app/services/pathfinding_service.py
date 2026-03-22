"""Pathfinding through the dungeon using door connections as graph edges."""

from __future__ import annotations

import networkx as nx

from backend.app.models.room import Room


class PathfindingService:
    """Builds a NetworkX graph from DoorConnection edges and finds paths."""

    def build_graph(self, rooms: list[Room]) -> nx.Graph:
        g = nx.Graph()
        for room in rooms:
            g.add_node(room.id, room=room)
        for room in rooms:
            for door in room.doors:
                if door.connects_to and g.has_node(door.connects_to):
                    g.add_edge(room.id, door.connects_to)
        return g

    def find_path(self, rooms: list[Room], start_id: str, end_id: str) -> list[str]:
        """Find shortest path between two rooms via connected doors."""
        g = self.build_graph(rooms)
        if not g.has_node(start_id) or not g.has_node(end_id):
            return []
        try:
            return nx.shortest_path(g, start_id, end_id)
        except nx.NetworkXNoPath:
            return []

    def build_simple_path(self, rooms: list[Room]) -> list[str]:
        """Fallback: sort rooms by position for a linear traversal path.

        Used when rooms lack door connections (early prototype).
        """
        non_boss = [r for r in rooms if r.type != "boss_room"]
        boss = [r for r in rooms if r.type == "boss_room"]
        sorted_rooms = sorted(non_boss, key=lambda r: (r.y, r.x))
        return [r.id for r in sorted_rooms + boss]
