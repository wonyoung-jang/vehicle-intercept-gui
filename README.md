# Vehicle Interception Solver

This is an interactive Python application for simulating a drone interception problem and a car collision problem. PySide6 is used to create the GUI with dynamic visualizations.

## Table of Contents

- [Background](#background)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Background

I was haunted by these two problems after my brain short circuited while solving them on paper for an interview, and I haven't created anything with Qt in a while, so I made this for some practice.

## Features

### Drone Intercept

Calculates interception possibilities for drones.

Calculates interception distance and time, if possible.

Gives suggestions for successful interception when not possible.

![](assets/screenshot-drone-intercept.webp)

#### Input parameters: 

  - **Drone speed**: The speed of both drones in miles per hour.

  - **Radar range**: The radar detection range in miles.

  - **Reaction time**: The time it takes for the friendly drone to react and launch, in minutes.

### Car Collision

Calculates collision time for two cars driving in the same direction and lane.

![](assets/screenshot-car-collision.webp)

#### Input parameters:

  - **Car A speed**: The speed of Car A in miles per hour.

  - **Car B speed**: The speed of Car B in miles per hour.

  - **Initial distance**: The initial distance between the cars in miles.

## Requirements
- Python 3.x
- PySide6

## Installation

1. Clone this repository
2. Install dependencies: `pip install PySide6`

## Usage

1. Run the application: `python main.py`
2. Use the tabs to switch between simulations (ctrl + tab)
3. Adjust parameters using the input spinboxes
4. Adjust the units using the dropdowns (QComboBox)
5. Adjust the speed of the simulation using the slider

## License

[MIT License](LICENSE)
