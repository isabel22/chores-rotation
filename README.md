# Chores Rotation

API endpoints to rotate, get and set a group of people or a single person in charge of the chores of a team.

## Endpoints 
* `/current-turn`:
  * Returns the pair of names of people that are currently on call
* `/next-turn`:
  * Sets the new pair of people that will be on call
  * Assigns the new pair of people to the Channels assigned in the environment variable `CHANNELS`
  * Returns their names
