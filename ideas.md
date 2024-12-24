# EOFJam

## Summary
Dungeon crawler with linear puzzle-focused rooms
Player can change scale smoothly
Changing scale changes attributes:
    - Hitbox
    - Health
    - Damage
    - Speed
    - Ability to move objects
    - Flow of time?

Certain obstacles are easier/harder, or impossible to pass/traverse when at certain size ranges

## Challenges
- Vector art
    - Making vector art
    - Rendering vector art
- Level design
- Level editor?
    - Tiled/LTK?
    - Layers?
- Making the puzzles fun
- Balancing combat with enemies and ensuring several size playstyles are valid

## Sizes
- Normal
    - Traditional game play
    - No gimmicks?
- Small
    - Fast
    - Low damage, high output
    - Can be crushed
    - Enemies have a hard time finding you
    - Attacks might miss
- Big
    - Slow
    - High damage, low output
    - Can crush
    - Easy target
    - Ricothet attacks

Speed: base * (1 + (1 / scale))
Health: base
Defense: base * scale
Attack: base * scale

1/4x: bullets miss
4x+: can crush opponent
6x+: can ricochet attacks
4x+: bullets -> aoe

energy bar to size change
emancipation grill to take energy away
