# Greenhack 2024

## Holographic 3D Scene of Energy Insights
Design a dynamic 3D scene model capturing time series parameters detailing the energy consumption. Motivate users to handle their energy streams in a sustainable way.

![logo](./images/1f0dd3ad-e968-47fa-9982-dc1b4d9b2e8c.jfif)

## Solution description
Unique art piece reflecting your home sustainability. Motivation to control your energy consumption by a reward system. Comprehensible insights of your data streams. Scalable for a large variety of prosumers (smart homes, green cities, modern factories, etc.).
Unlimited scalability of our solution is achieved through fractal generation over aggregated time series data (houses aggregated on district levels, company branches aggregated on a parent level, ...).

### Impact
Saving energy and money through electric grid optimization in a fun, artistic, and motivational manner. Discovering the root causes of your energy consumption.

### Feasibility
The complete solution is easily feasible since the design, observed metrics, and decision rules are already defined. The next steps involve an extrapolation from a 2D scene into the 3D. There is a one-time cost given by a graphical work. Possibility to define other metrics, reward system rules, and AI-driven insights.

### Next steps
Extrapolation of our 2D design into the 3D scene. Possibility to customize observed features and define your own rules. Incorporation of the weather data for the beautification of the scene, adapting the tree growth, and into actionable insights.



## Tree proposal
- fractal tree
- we need score s \in [0, 1].
- every time period (day?) we will split s branches and grow them.
- each branch has its timestamp, we prefer growing branches with lower timestamps.
- example: 
    - first day my score is 1. Therefore my tree with two branches fully grows into a bigger tree with four branches by spliting those two.
    - second day my score is 0.5, therefore I will grow only half of the tree :(

