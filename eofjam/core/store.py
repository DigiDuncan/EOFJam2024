from dataclasses import dataclass, field

@dataclass(slots = True)
class Preferences:
    framerate: int = 60

@dataclass(slots = True)
class Persistent:
    ...

@dataclass(slots = True)
class Run:
    unlimited_scale: bool = False


@dataclass(slots = True)
class Game:
    preferences: Preferences = field(default_factory=Preferences)
    persistent: Persistent = field(default_factory=Persistent)
    run: Run = field(default_factory=Run)

# THIS IS A SINGLETON
# DO NOT CREATE MORE THAN ONE OF THESE
# IMPORT THIS ONE INSTEAD
# IT BREAKS EVERYTHING IF YOU F*** THIS UP
game = Game()
