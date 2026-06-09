# gothicr_picklockhelper
Picklock helper for Gothic Remake

Requires: Gothic, Python 3 (v3.11+ tested)

# HoWto

```
python lockpick2.py 
```

# Use

After launching the helper you will test each spring on the lock and make a note
on how it is affected. 

Imagine each spring has its pins numbered 1-7, with 4 being the middle.

You then move spring 1 RIGHT (Say from position 4 to 3).
You notice that spring 2 moves LEFT when you do this (position 3 to 4, for example).

This is described in the app as: S1 -, S2+
So you enter the following at the "Rule 1" prompt.

```
Rule 1: S1 -, S2+
```

You then notice that Spring 2 can be moved without affecting any other springs, 
So you do not enter anything for this spring.

You observe the following on spring 3.

You move it LEFT (Say from position 4 to 5) also moves spring 2 LEFT (position 5 to 6)
and spring 1 RIGHT (Position 3 to 2)

This is described as: S3 +, S2+, S1-

```
Rule 2: S3 +, S2+, S1-
```

Spring 4 is not affected by any other springs, and can move independently. 

To get to the next phase, you just press enter on an empty rule

```
Rule 1: S1 -, S2+
Rule 2: S3 +, S2+, S1-
Rule 3:

[INFO] Rules loaded. Sliders: ['S1', 'S2', 'S3']
[INFO] Independent sliders: ['S2']
[INFO] One-way rules only (no automatic inverses).
```

You will now press the 'reset' button in the lockpick minigame and note the original starting position
of the springs. 

You observe the following in the game:

Spring 1 is at 4 (unlocked)
Spring 2 is at 3
Spring 3 is at 1 (The furthest position to the left)
Spring 4 is at 5 

You enter this as

```
Current State: S1 4, S2 3, S3 1, S4 5
```

And the application will then calculate the moves to reach unlock on all springs.

```
============================================================
SOLVING WITH A* SEARCH...
Initial: {'S1': 4, 'S2': 3, 'S3': 1, 'S4': 5}
Goal: All sliders = 4
============================================================

============================================================
OPTIMIZED SOLUTION FOUND
============================================================
Move            | State After Move
------------------------------------------------------------
1. S3 +           | S1=3, S2=4, S3=2, S4=5
2. S4 -           | S1=3, S2=4, S3=2, S4=4
3. S1 +           | S1=4, S2=3, S3=2, S4=4
4. S3 +           | S1=3, S2=4, S3=3, S4=4
5. S1 +           | S1=4, S2=3, S3=3, S4=4
6. S3 +           | S1=3, S2=4, S3=4, S4=4
7. S1 +           | S1=4, S2=3, S3=4, S4=4
8. S2 +           | S1=4, S2=4, S3=4, S4=4
------------------------------------------------------------
Total Moves: 8
============================================================
```

In the game now, you just follow the move list for each spring.  a "+" means you increase the position (say from 3 to 4 (unlocked)
and a "-" the other way.   Position 7 is the RIGHTMOST pin per spring, and Position 1 is the leftmost pin. 



