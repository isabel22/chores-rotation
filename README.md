# Support Rotation

Small script to rotate pair of users in charge of the support of the team.

## Endpoints 
* `/current-turn`:
  * Returns the pair of names of people that are currently on call
* `/next-turn`:
  * Sets the new pair of people that will be on call
  * Assigns the new pair of people to the Channels assigned in the environment variable `CHANNELS`
  * Returns their names
