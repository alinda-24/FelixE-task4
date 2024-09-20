# Simple Game Development with Java

Creating games is a fun way to learn programming concepts. In this task, we will develop a simple terminal-based game in Java. We'll focus on player movement, scoring systems, and enemy interaction. By the end of this task, you should feel more comfortable with loops, boolean expressions, and handling user input.

### 📝 Preparation

- Review the [lecture on Java Basics](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/index.html)
- Go through:
  - [Java Loops](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/while.html)
  - [Boolean Expressions](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/op2.html)
  - [Java Function Overloading](https://www.geeksforgeeks.org/function-overloading-in-java/)

### ✅ Learning Goals

- Understand `boolean` expressions and operators.
- Implement `while` and `for` loops effectively.
- Use JShell to experiment with Java code.
- Apply function overloading in Java.

### 🚨 Troubleshooting Guide

1. Look at this week's [posted issues](https://gits-15.sys.kth.se/inda-24/help/issues) for similar questions.
2. Post a query if not yet asked, using [New Issue](https://gits-15.sys.kth.se/inda-24/help/issues/new).
3. Ask a TA in the [weekly lab](https://queue.csc.kth.se/Queue/INDA).

**Be a responsible learner!** Discuss with friends, but avoid sharing answers or submitting AI-generated solutions.

### 🏛 Assignment

This task involves building a simple console game where a player moves around a grid, collects points, and avoids enemies. Your journey in this task will cover loops, boolean expressions, and terminal inputs to build this game.

<details>
<summary> 📚 Basic Syntax and Concepts </summary>

Java provides various primitives like `int` and `boolean`, as well as constructs like loops (e.g., `while`, `for`) and conditionals (`if`, `else`). Operators like `&&`, `||`, and `!` help formulate boolean expressions.

</details>

#### Exercise 1: Designing the Game Board

1. Create a new Java class `SimpleGame.java`.
2. Define a 2D game board using a `char[][]` array in this class.
3. Initialize the board with characters representing the player `'P'`, empty space `'.'`, and enemies `'E'`.

```java
char[][] board = {
    {'.', '.', '.', '.'},
    {'.', 'P', '.', 'E'},
    {'.', '.', '.', '.'},
    {'E', '.', '.', '.'}
};
```

#### Exercise 2: Player Movement

Add a method `movePlayer` in `SimpleGame.java` that moves the player based on input (`w`, `a`, `s`, `d` for directions).

- Use a `switch` statement inside a `while` loop to process input.
- Update the board and reposition `'P'` accordingly, using boolean checks to ensure valid moves.

```java
public void movePlayer(char direction) {
    // Implement logic to change player position based on the direction
}
```

#### Exercise 3: Scoring System

Create a score variable to keep track of player achievements.

- Increment score on certain actions (e.g., moving to a new position safely).
- Use a `while` loop to repeatedly prompt and move the player until a certain score is achieved.

```java
int score = 0;

// Example: while loop for player moves
while(score < maxScore) {
    // Get user input and update the board
}
```

#### Exercise 4: Enemy Interaction

Enhance the game with enemy interactions:

- If the player moves to a space with `'E'`, end the game.
- Implement this using a boolean expression that checks the player’s future position.

```java
boolean isGameOver = false;

// Update loop condition using isGameOver
```

#### Exercise 5: Using JShell for Testing

1. Use [JShell](https://docs.oracle.com/javase/9/jshell/introduction-jshell.htm) to test small boolean expressions and loops separate from your main code.

```bash
jshell
jshell> int x = 5;
jshell> x > 3 && x < 8
```

#### Exercise 6: Function Overloading for Move

Introduce function overloading in your project by creating multiple versions of the `movePlayer` method, one taking `int` inputs for detailed control over moves.

```java
public void movePlayer(int xOffset, int yOffset) {
    // Implement to update the player's coordinates with offsets
}
```

### Final Touches

- Ensure the game runs smoothly from the terminal, responding to inputs in real time.
- Use the `System.console().readLine()` for reading inputs or scanners if needed.

By the end of this task, you'll have a small interactive game and a deeper understanding of Java basics, loops, and input handling.