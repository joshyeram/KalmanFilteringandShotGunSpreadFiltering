# Shot Gun Spread Filtering and Kalman Filtering #

## Kalman Filtering ##
Givne actions and observartion data set, the agent can be self localized better in comparison to just using the observations.
<p align="center">
  <img src="https://github.com/joshyeram/slam/blob/main/distrib/kf.png", width="600"/>
</p>
Given just the observations, the red trajectory is not smooth and seems as if the robot is oscillating. In conjunction with the action data set, the path is actual path is smoothed out.

## Shot Gun Spread Filtering ##
Instead of implementing the known particle filtering model, a new filtering method was developed: Shot Gun Spread Filtering. Given an action (direction and velocity), landmark observations, and an initial position, we can determine the best-predicted location of the robot and normalize it along with the observation point. 
1. It will "shoot out" n pellets of normally distributed sampled actions given
2. Find the closest pellet to the observation
3. Normalize all the other pellets using importance sampling
4. Find the top 10% of the pellets as a top generation shoot-out pellets from those points
5. Continue until actions run out
6. Find the best path using Viterbi's Most likely explanation.

## Landmarks ##
<p align="center">
  <img src="https://github.com/joshyeram/slam/blob/main/distrib/s1.png", width="1000"/>
</p>

## Ground Truth ##
<p align="center">
  <img src="https://github.com/joshyeram/slam/blob/main/distrib/s2.png", width="1000"/>
</p>

## Odometry ##
<p align="center">
  <img src="https://github.com/joshyeram/slam/blob/main/distrib/s3.png", width="1000"/>
</p>

## Shotgun/Particle Spread Filtering ##
<p align="center">
  <img src="https://github.com/joshyeram/slam/blob/main/distrib/s4.png", width="1000"/>
</p>
