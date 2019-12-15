```
After years of being captive in Markov’s prison you have decided it is time to
escape.

-> | 1  2  3  4|
   | 5  6  7  8|
   | 9 10 11 12|
   |13 14 15 16| ->

A sketch of the prison is shown above.  The path to freedom begins when you
enter room #1 and exit the prison through room #16.  Unfortunately there are
two very vigilant guards who are on duty and have been walking through the
rooms for years.  If you and a guard are in the same room at the same time you
will be caught and sentenced to life in prison.  Fortunately, over time, you
have observed that the guards’ movements are dictated by the following
probabilities:

Guard #1:
20% of the time he moves North
40% of the time he moves South
20% of the time he moves West
20% of the time he moves East
Guard #2:
40% of the time she moves North
10% of the time she moves South
20% of the time she moves West
30% of the time she moves East

Every second that passes, you and the guards each move to a new room.  If the
probability instructs a guard to move into a wall, the guard will simply stand
still for that iteration.  The guards, like you, cannot move diagonally.

Questions:
1.) Entering at room #1 and exiting the prison at room #16, what route will
give you the best chance of escape?
2.) What is the probability that you will be caught?
```
