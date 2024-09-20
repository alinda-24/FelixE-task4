import os
import sys
import subprocess
from datetime import datetime
from openai import OpenAI
import pytz
from pytz import timezone

def main(api_key):
    if not api_key:
        print("Error: OpenAI API key is missing.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    # Extract theme and language from environment variables
    theme = os.getenv("TASK_THEME", "Create a basic Java application with the following requirements.")
    language = os.getenv("TASK_LANGUAGE", "English")

    # Replace learning goals and original_structure with the new task description
    learning_goals = """
        "* `boolean` expressions and operators\n"
        "* `while` loops\n"
        "* `for` loops\n"
        "* Using JShell to try your Java program\n"
        "* Function overloading\n"
    """
    
    original_structure = """
            "# Looping\n\n"
            "A very important reason why computers are useful is that they can repeat the same operation time and\n"
            "time again without error or complaint. If I asked you to count up to 10 000, you might easily get bored or skip a number,\n"
            "but a computer will do so flawlessly every time. We call this concept _\"iteration\"_ or _\"looping\"_, and \n"
            "this week we will be looking at a couple of different ways of accomplishing this in Java.\n\n"

            "### 📝 Preparation\n\n"
            "- Review the [lecture slides](https://docs.google.com/presentation/d/1kcsmcuBBu4Jr3O_r6eNP6IFrP6DEITDWeRS5_7rtV30/edit#slide=id.p)\n"
            "- Read and answer all questions in: \n"
            "  - [Module 5: Looping with for-each](https://qbl.sys.kth.se/sections/dd1337_programming/page/looping_with_foreach)\n"
            "  - [Module 6: Iteration](https://qbl.sys.kth.se/sections/dd1337_programming/page/iteration__continued)\n\n"

            "### ✅ Learning Goals\n\n"
            "This week's learning goals include:\n\n"
            "* `boolean` expressions and operators\n"
            "* `while` loops\n"
            "* `for` loops\n"
            "* Using JShell to try your Java program\n"
            "* Function overloading\n\n"

            "### 🚨 Troubleshooting Guide\n\n"
            "If you have any questions or problems, follow this procedure: <br/>\n\n"
            "1. Look at this week's [posted issues](https://gits-15.sys.kth.se/inda-24/help/issues). Are other students asking about your problem?\n"
            "2. If not, post a question yourself by creating a [New Issue](https://gits-15.sys.kth.se/inda-24/help/issues/new). Add a descriptive title, beginning with \"Task _x_: _summary of problem here_\"\n"
            "3. Ask a TA in person during the [weekly lab](https://queue.csc.kth.se/Queue/INDA). Check your schedule to see when the next lab is.\n\n"

            "We encourage you to discuss with your course friends, **but do not share answers!** Similarly, use of any AI services 🤖 are great to help explain things, **but please do not submit AI-generated solutions** - you must be both responsible for your own solutions and must be able to explain them under examination.\n\n"

            "### 🏛 Assignment\n\n"
            "Before we look at how to write loops, we must be able to specify when the program should stop repeating the same thing over and over again.\n"
            "This is usually when a certain condition is met, such as when we have performed _n_ loops. In order to specify this\n"
            "we use _boolean expressions_, which you have already encountered when you wrote `if` statements in the previous task.\n"
            "The next couple of exercises will help you understand more complex boolean expressions.\n\n"

            "<details>\n"
            "<summary> 📚 Boolean values, expressions and operators </summary>\n"
            "<! -- requires a blank space -->\n\n"

            "A [boolean value](https://en.wikipedia.org/wiki/Boolean_data_type) is a value that is either true or false. Similarly, a [boolean expression](https://en.wikipedia.org/wiki/Boolean_expression) is a statement that when evaluated results in either true or false.\n"
            "You might claim that \"The capital of Mozambique is Maputo\", and this expression is either true or false, either it is the capital or it isn't.\n"
            "Similarly, you might consider a mathematical expression such as _2 = 5_ as either pure nonsense, or as a boolean expression that evaluates to false.\n\n"

            "In Java, `boolean` is one of the 8 [primitive types](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html), and can have the value `true` or `false` such as in\n"
            "```java\n"
            "theCapitalOfMozambiqueIsMaputo = true;\n"
            "twoEqualsFive = false;\n"
            "```\n\n"

            "Three fundamental boolean operators are the [\"and\"](https://en.wikipedia.org/wiki/Logical_conjunction), [\"or\"](https://en.wikipedia.org/wiki/Logical_disjunction) and [\"not\"](https://en.wikipedia.org/wiki/Negation) operators.\n"
            "In Java we write `&&` for \"and\", `||` for \"or\" and `!` for \"not\".\n\n"

            "Just like with ordinary arithmetic operators, we can use parentheses to change the order in which the operations are evaluated.\n"
            "In the same way that _3 - (2 - 3)_ does not evaluate to the same value as  _(3 - 2) - 3_, the boolean expression `true || (true && false)` will evaluate to `true`,\n"
            "while `(true || true) && false` will evaluate to `false`.\n\n"
            "</details>\n\n"

            "#### Exercise 4.1.1 (docs) -- Boolean expressions\n\n"

            "In [`docs/README.md`](docs/README.md) you will find a copy of the table below. Fill in the boolean value that each expression evaluates to:\n\n"

            "| Boolean expression | Value   |\n"
            "| ------------------ | ------- |\n"
            "| `2 == 5`           | `false` |\n"
            "| `2 > 5`            |         |\n"
            "| `11 == 11`         |         |\n"
            "| `7 <= 9`           |         |\n"
            "| `42 >= 7`          |         |\n"
            "| `false == true`    |         |\n\n"

            "#### Exercise 4.1.2 (docs) -- Boolean operators\n\n"

            "In [`docs/README.md`](docs/README.md) you will find a copy of the table below. Fill in the boolean value that each expression evaluates to:\n\n"

            "| Boolean expression   | Value |\n"
            "| -------------------- | ----- |\n"
            "| `2 == 3 && 2 == 2`   |       |\n"
            "| `2 == 3 || 2 == 2` |       |\n"
            "| `!true`              |       |\n"
            "| `!false`             |       |\n\n"

            "#### Exercise 4.1.3 (docs) -- Combining boolean operators\n\n"

            "In [`docs/README.md`](docs/README.md) you will find a copy of the table below. Fill in the boolean value that each expression evaluates to:\n\n"

            "| Boolean expression             | Value  |\n"
            "| ------------------------------ | ------ |\n"
            "| `true || (true && false)`    | `true` |\n"
            "| `false || (false || true)` |        |\n"
            "| `!(false && true) == true`     |        |\n"
            "| `!true && false`               |        |\n"
            "| `!(true && false)`             |        |\n\n"

            "> **Assistant's tip:** If you have a Java expression that you want to evaluate,\n"
            "> but you don't want two write a whole new class with main method and all,\n"
            "> consider using [JShell](https://docs.oracle.com/javase/9/jshell/introduction-jshell.htm).\n"
            "> JShell enables you to enter a java expression such as `2 == 5` and immediately\n"
            "> get the response that this evaluates to `false`.\n\n"

            "#### Exercise 4.2.1 -- The while-loop\n\n"

            "Begin this exercise by creating a file called `Loops.java` in your `src` folder. Add a method with the header\n"
            "```java\n"
            "public void multiplesOfSeven()\n"
            "```\n"
            "This method should use a while-loop to print all the multiples of seven between 0 and 100.\n\n"

            "<details>\n"
            "<summary> 📚 The while loop </summary>\n"
            "<! -- requires a blank space -->\n\n"

            "The [while-loop](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/while.html) is the most basic form of \n"
            "loop in Java, and every other form of loop can be seen as a variation of the while-loop.\n\n"

            "As the name suggests, a while loop just keeps doing something _while_ some expression is true, so the loop\n"
            "```java\n"
            "int count = 0;\n"
            "while (count < 5) {\n"
            "    count += 1;\n"
            "}\n"
            "```\n"
            "will keep adding `1` to the variable `count` while `count` is less than `5`. Take a moment and think about what the last value of `count` will be when the loop ends.\n"
            "You don't have to write this down anywhere, but it might be a good idea to test it if you are unsure.\n\n"
            "</details>\n\n"

            "#### Exercise 4.2.2 -- Summing with a while loop\n\n"

            "Add a method with the header\n"
            "```java\n"
            "public int sumUpTo(int max)\n"
            "```\n"
            "to your `Loops.java` file. This method should use a while loop to sum all integers between `0` and `max` and return this value.\n"
            "The upper bound should be _inclusive_, so that `sumUpTo(3)` should return `6` (_0 + 1 + 2 + 3_). If `max` is less than zero, the value `0` should be returned.\n\n"

            "#### Exercise 4.2.3 -- For-loops and summing a range\n\n"

            "Add a new method to your `Loops.java` file. This method should have the header\n"
            "```java\n"
            "public int sumBetween(int min, int max)\n"
            "```\n"
            "It should use a for-loop to calculate and return the sum of all integers between `min` and `max` (inclusive).\n"
            "As an example, `sumBetween(10, 12)` should return `33` (_10 + 11 + 12_). If `min` is greater than `max`, the value `0` should be returned.\n"
            "If `min == max`, the value of `min` (or `max`) should be returned.\n\n"

            "<details>\n"
            "<summary> 📚 The for loop </summary>\n"
            "<! -- requires a blank space -->\n\n"

            "The while loop is very useful, but another type of loop that is even more common is the [for-loop](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/for.html).\n"
            "In addition to a boolean expression that tells the loop when to stop, the for-loop also lets you declare an _index variable_\n"
            "and describe how this variable should change after each iteration. This means that instead of the while loop\n"
            "```java\n"
            "int i = 0;\n"
            "while (i < 10) {\n"
            "    System.out.println(i);\n"
            "    i += 1;\n"
            "}\n"
            "```\n"
            "you can get the same result using the more compact for-loop form:\n"
            "```java\n"
            "for (int i = 0; i < 10; i += 1) {\n"
            "    System.out.println(i);\n"
            "}\n"
            "```\n"
            "</details>\n\n"

            "#### Exercise 4.2.4 -- Loops and summation notation\n\n"

            "The summation, represented by the capital Greek letter sigma (Σ), is the mathematician's shorthand for iteration\n"
            "and can be implemented using for (or while) loops. The table below lists a few summations alongside Java method headers.\n"
            "You have already implemented the `sumUpTo` and `sumBetween` methods. Create two new methods called `sumSquares`\n"
            "and `sumReciprocals` based on the summations in the table.\n\n"

            "| Method header                             | Summation                                              |\n"
            "| ----------------------------------------- | ------------------------------------------------------ |\n"
            "| `public int sumUpTo(int max)`             | <img src='img/summation-sum-up-to.png' width=80>       |\n"
            "| `public int sumBetween(int min, int max)` | <img src='img/summation-sum-between.png' width=80>     |\n"
            "| `public int sumSquares(int max)`          | <img src='img/summation-sum-squares.png' width=80>     |\n"
            "| `public double sumReciprocals(int max)`   | <img src='img/summation-sum-reciprocals.png' width=80> |\n\n"

            "#### Exercise 4.3.1 -- A basic clock\n\n"

            "Now it's time to put what we've learned together and create a simple Java class representing a 12-hour clock.\n"
            "Start by creating a new class called `Clock.java` in your [`src`](/src) folder. You will need to keep track of _hours_, _minutes_ and _seconds_,\n"
            "so add fields for these values. Think about what the best data type for these fields is, and whether they should be `public` or `private`.\n"
            "Make sure to add `public` getter methods for all your fields. The getter method should be named with a get prefix and use camel casing, example: `getHours()`.\n\n"

            "> **Assistant's tip:** If you're not completely sure that a field should be `public`, it's a good idea to keep it `private` or package private (no modifier).\n"
            "> You can always change it later if you need to.\n\n"

            "#### Exercise 4.3.2 -- Validating input\n\n"

            "Add three new `public` setter methods to your `Clock.java` class. These should be called `setHours`, `setMinutes`, and `setSeconds`, and each should take an `int` as a parameter.\n"
            "As opposed to setter methods that you may have written previously, it is important that you _validate_ the input to these methods.\n"
            "This simply means that you should ensure that the value you are trying to set is sensible (so between 1 and 12 for the hours, 0 and 59 for the minutes and seconds).\n"
            "If the method is called with an incorrect input value, you shouldn't change the time on the clock at all,\n"
            "so if the `hours` is currently set to `11`, and a user calls the method `setHours(-3)` the value of `hours` should still be set to `11`.\n\n"

            "#### Exercise 4.3.3 -- Constructing constructors\n\n"

            "Add two constructors to your `Clock.java` class. The first one should have the header\n"
            "```java\n"
            "public Clock()\n"
            "```\n"
            "and simply set the `hours` to `12` and `minutes` and `seconds` to `0`. The second constructor should have the header\n\n"

            "```java\n"
            "public Clock(int hours, int minutes, int seconds)\n"
            "```\n"
            "this constructor should set the time to the values provided by the user, but only if they are valid.\n"
            "First set the fields as in the first constructor, then use the setter methods that you created in the previous task to update the fields with the parameters provided to the constructor.\n"
            "If the user tries to create a `Clock` with the call\n"
            "```java\n"
            "Clock clock = new Clock(51, 1, 23);\n"
            "```\n"
            "the result should be a clock with the time set to `12:01:23` since the hours do not have a valid value.\n\n"

            "> **Assistant's note:** How can two methods have the same name? 🤔 The concept is called [function overloading](https://en.wikipedia.org/wiki/Function_overloading) (or *Ad hoc polymorphism*).\n"
            "> Since the methods have different *numbers of input parameters* (or *arity*), it is fine to give them the same name.\n"
            "> It is also possible to have the same number of parameters, but of different types, such as `add(int n)` and `add(double n)`.\n\n"

            "#### Exercise 4.3.4 -- Presenting the time\n\n"

            "In Java, the `toString` method is a predefined method available in all classes. It is used to create a string representation of an object.\n"
            "By default, the toString method returns a string containing the class name, followed by an `@` symbol and the object's `hash code` which is sort of a unique identifier for the object.\n"
            "However, this default implementation may not provide meaningful information about the object's state or attributes.\n\n"

            "You can try this default implementation by navigating to the folder where your `Clock.java` file is and type the following in your terminal:\n"
            "```bash\n"
            "jshell Clock.java\n"
            "Clock myClock = new Clock();\n"
            "myClock.toString();\n"
            "```\n\n"

            "Fortunately, in Java, we have the ability to `override` the toString method in our custom classes. By overriding the method, we can provide a customized string representation that better reflects the object's properties or behavior.\n"
            "This allows us to create more informative and human-readable representations of objects when needed.\n\n"

            "To override the toString method, we can follow these steps:\n"
            "   1. Define a `toString` method in our class with the same signature as the one in the Object class: `public String toString()`.\n"
            "   2. Provide our own implementation of the method's body to return the desired string representation of the object.\n\n"

            "Your task is to implement this method and make it return a string representation of the object's current time.\n"
            "This should be a string in the format `HH:MM:SS`. Make it so that the returned string always prints two digits for each time unit, even if the field value only contains one digit.\n"
            "For example, if the current hour is 10, minute = 5 and second = 0 the output should be `10:05:00`. You should be able to do this using if statements.\n\n"

            "> **Assistant's tip:** If you are interested in more compact ways of returning a string like this, feel free to check the [`String.format` method](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/String.html#format(java.lang.String,java.lang.Object...)). Check the example below for an idea on how to use it.\n\n"

            "<details>\n"
            "<summary> 🛠 Example of String.format </summary>\n\n"

            "The following code can be used to print a user ID consisting of a maximum of 4 digits. The output will always be in the format `#XXXX` and will be padded with zeroes at the start if there are not enough digits in the ID itself.\n"
            "The code below will print `#0068` to the terminal.\n\n"

            "```java\n"
            "    public static void main(String[] args) {\n"
            "      // Example ID number\n"
            "      int id = 68; \n\n"
            "      /*  Format the ID number with leading zeros\n"
            "          - # is just the symbol we want at the start\n"
            "          - % indicates the place we want to insert whatever data comes later\n"
            "          - 04 tells Java that the formatted data should be at least 4 characters long and should be padded with zeros otherwise.\n"
            "          - d tells Java that it expects a digit (number) */\n"
            "      String formattedId = String.format(\"#%04d\", id);\n"
            "      // Print the formatted ID (\"#0068\")\n"
            "      System.out.println(formattedId);\n"
            "    }\n"
            "```\n"
            "</details>\n\n"

            "#### Exercise 4.3.5 -- Making it tick\n\n"
            "A clock is not much use if it doesn't tick, so it's time to add a `tick`-method to your `Clock.java` file. This method should have the header\n"
            "```java\n"
            "public void tick()\n"
            "```\n"
            "When called, the method should increment the seconds by one, and increment the minutes and seconds as needed.\n"
            "If the time is `02:13:59` and `tick` is called, the time should go to `02:14:00`. The convention for a 12-hour clock is that the minutes and seconds go from `00` to `59`, but the hours go from `01` to `12`.\n"
            "We expect your clock to follow that convention.\n\n"

            "> **Assistant's tip:** You could solve this exercise using if statements, but your code will be much simpler if you use the remainder (`%`) operator.\n"
            "> This binary operator gives you the remainder of the first argument after integer division with the second argument, so `15 % 4` gives you `3`, since _15 = 4*3 + 3_.\n"
            "> Similarly, `16 % 4` gives you `0`, since _16_ is divisible by _4_.\n\n"

            "Since there are 60 seconds in a minute, 60 minutes in an hour, and 12 hours until it resets, we need to check for these special cases.\n"
            "Looping back around the current time unit can be done using the remainder operator as mentioned above, and by using if statements the next time unit can be incremented.\n"
            "To figure out in what order things need to be done, think about the edge case when the clock is `12:59:59` and the tick method is called.\n\n"

            "#### Exercise 4.3.6 -- Tick tock\n\n"
            "Let's add a final method to the `Clock` class. This method should have the header\n"
            "```java\n"
            "public void tick(int seconds)\n"
            "```\n"
            "and should use a loop (you can choose if you want to use for loop or a while loop) to call `tick()` repeatedly.\n"
            "As an example, if the time is currently `08:37:14` and the call `tick(57)` is made, the time should go to `08:38:11`.\n"
            "Add a call to `System.out.println` that prints the current time after each time the seconds are incremented.\n\n"

            "> **Assistant's note:** This is yet another example of _method (or function) overloading_, and you will see many more as you continue your Java adventures.\n\n"

    """

    prompt = (f"Create a new programming task in {language} with the following theme: {theme}. "
              f"It is paramount that the generted task description includes and integrates the concepts of {learning_goals}"
              f"The task should follow a similar structure and format to the provided example {original_structure} , including detailed instructions, preparation steps, learning goals, and assignment description with exercises. "
              f"The generated task should also include the most important and pedagogical parts of {original_structure} while still focusing to integerate with the theme chosen by the student."
              f"Make sure to include the title, subtitle, and emojis for aesthetics. "
              f"The description should be detailed, well-structured, and aesthetically pleasing to provide thorough instructions for the students."
              "It will be fed in the next stage to the model to generate a solution so ensure the coding part of the task is rigourous enough to create a true challange for the studnets so that they have to learn more deeply and use the concepts discussed."
             )

    # Call OpenAI API to generate the task description
    response_content = generate_with_retries(client, prompt, max_retries=3)
    if response_content is None:
        print("Error: Failed to generate task description after multiple retries.")
        sys.exit(1)

    # Create a new branch with a unique name
    stockholm_tz = timezone('Europe/Stockholm')
    branch_name = f"task-{datetime.now(stockholm_tz).strftime('%Y%m%d%H%M%S')}"
    create_branch(branch_name)

    # Write the response content to a markdown file
    task_file_path = os.path.join("tasks", "new_task.md")
    with open(task_file_path, "w") as file:
        file.write(response_content)

    # Commit and push changes
    commit_and_push_changes(branch_name, task_file_path)

    # Output the branch name for the next job
    print(f"::set-output name=branch_name::{branch_name}")

def generate_with_retries(client, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating task description: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
    return None

def create_branch(branch_name):
    try:
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        subprocess.run(
            ["git", "push", "-u", "origin", branch_name],
            check=True,
            env=dict(os.environ, GIT_ASKPASS='echo', GIT_USERNAME='x-access-token', GIT_PASSWORD=os.getenv('GITHUB_TOKEN'))
        )
    except subprocess.CalledProcessError as e:
        print(f"Error creating branch: {e}")
        sys.exit(1)

def commit_and_push_changes(branch_name, task_file_path):
    try:
        subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "github-actions"], check=True)

        subprocess.run(["git", "add", task_file_path], check=True)
        subprocess.run(["git", "commit", "-m", f"Add new task description: {branch_name}"], check=True)
        subprocess.run(
            ["git", "push", "--set-upstream", "origin", branch_name],
            check=True,
            env=dict(os.environ, GIT_ASKPASS='echo', GIT_USERNAME='x-access-token', GIT_PASSWORD=os.getenv('GITHUB_TOKEN'))
        )
    except subprocess.CalledProcessError as e:
        print(f"Error committing and pushing changes: {e}")
        sys.exit(1)

if len(sys.argv) != 2:
    print("Error: Missing required command line argument 'api_key'")
    sys.exit(1)

api_key = sys.argv[1]

main(api_key)
