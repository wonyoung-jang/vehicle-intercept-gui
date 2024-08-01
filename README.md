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

Gives suggestions for successful intercepti

on when not possible.

https://github.com/user-attachments/assets/0f290bf4-4fd5-4440-abb2-319c9ec7028e

https://github.com/user-attachments/assets/062ec2a7-385d-4da9-9c4a-20597e6dc31e

#### Input parameters: 

  - **Drone speed**: The speed of both drones in miles per hour.

  - **Radar range**: The radar detection range in miles.

  - **Reaction time**: The time it takes for the friendly drone to react and launch, in minutes.

### Car Collision

Calculates collision time for two cars driving in the same direction and lane.

https://github.com/user-attachments/assets/d755a2ef-76f4-4959-8a9f-789a702beef1

https://github.com/user-attachments/assets/585c23cb-99eb-440b-8ad1-bfbc4f909bb0

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
