# Block Breaker Game

## Overview

This is a complete, fully-functional brick breaker (Breakout-style) arcade game built with Pygame. Players control a paddle to bounce a ball and destroy colorful blocks arranged in rows. The game features score tracking, game over detection, clear conditions, and restart functionality.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Game Engine
- **Framework**: Pygame (Python game development library)
- **Rendering**: 2D sprite-based rendering using Pygame's drawing primitives
- **Game Loop**: Fixed timestep loop running at 60 FPS

### Game Architecture
- **Design Pattern**: Object-oriented design with separate classes for game entities
- **Entity Classes**: 
  - `Paddle`: Player-controlled platform with collision boundaries and keyboard input
  - `Ball`: Moving projectile with velocity-based physics and collision detection
  - `Block`: Destructible bricks with color, points, and hit detection
- **Game States**: Running, Game Over, Game Clear with restart functionality
  
### Display System
- **Resolution**: 800x600 pixels fixed window
- **Color Palette**: Predefined color constants for consistent theming
- **Drawing**: Direct rendering to Pygame surface using primitive shapes (rectangles, circles)

### Input Handling
- **Control System**: Keyboard-based input for paddle movement
- **Movement**: Velocity-based paddle positioning with boundary collision detection

### Physics & Collision
- **Paddle Movement**: Speed-based horizontal movement (8 pixels per frame) with screen edge clamping
- **Ball Physics**: Velocity-based movement with wall bouncing and paddle deflection
- **Collision Detection**: 
  - Ball-wall collision with reflection
  - Ball-paddle collision with angle variation based on hit position
  - Ball-block collision with directional reflection and block destruction
- **Score System**: Points awarded based on block row position (higher rows = more points)

## External Dependencies

### Libraries
- **Pygame**: Core game development framework for rendering, input, and game loop management
- **Python Standard Library**: 
  - `sys`: System-level operations (likely for game exit)
  - `random`: Random number generation (likely for ball direction, block placement)

### No External Services
This is a standalone desktop game with no network connectivity, databases, or third-party API integrations required.