# Chores Rotation

API endpoints to rotate, get and set a group of people or a single person in charge of the chores of a team.

## Endpoints 
* `/current-turn`:
  * Returns the pair of names of people that are currently on call
* `/next-turn`:
  * Sets the new pair of people that will be on call
  * Assigns the new pair of people to the Channels assigned in the environment variable `CHANNELS`
  * Returns their names
* `/new-team`:
  * Creates a new team.
  * params:
    * `name`: String
* `/new-user`:
  * Creates a new user.
  * params:
    * `email`: String
    * `name`: String
    * `team`: String
* `/list-users`:
  * Returns all the users and its team_id
  ```
    user.name user.team_id\n
    user.name user.team_id\n
  ```
* `/list-teams`:
  * Returns all the team names
  ```
    team.name\n
    team.name\n
    team.name\n
  ```
* `/list-chores`:
  * Returns all the chores names
  ```
    chore.name\n
    chore.name\n
    chore.name\n
  ```
* `/assign-chore`:
  * Assigns a chore to a user
  * params:
    * `chore`: String
    * `email`: String
