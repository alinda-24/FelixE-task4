import os
import re
import sys
import subprocess
from openai import OpenAI

def main(api_key, branch_name):
    if not api_key:
        print("Error: OpenAI API key is missing.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    # Read the new task description
    try:
        with open("tasks/new_task.md", "r") as file:
            task_description = file.read()
    except FileNotFoundError:
        print("Error: new_task.md file not found.")
        sys.exit(1)

    # Inspirational code snippet for the solution
    inspirational_code = """
        // Example of a simple class modeling a 12-hour clock
        /**
        * A simple class modelling a 12-hour clock
        * @author Linus Östlund
        * @author Gabriel Skoglund
        */
        public class Clock {
            private int hours;
            private int minutes;
            private int seconds;

            private static final int SECONDS_LOWER_LIMIT = 0;
            private static final int SECONDS_UPPER_LIMIT = 60;
            private static final int MINUTES_LOWER_LIMIT = 0;
            private static final int MINUTES_UPPER_LIMIT = 60;
            private static final int HOURS_LOWER_LIMIT = 1;
            private static final int HOURS_UPPER_LIMIT = 13;

            /**
            * Create a clock with the time set to 12:00:00
            */
            public Clock() {
                this.hours = 12;
                this.minutes = 0;
                this.seconds = 0;
            }

            /**
            * Create a new clock with the set time. The provided time units will only be used
            * if the fall in the correct span (1-12 for hours, 0-59 for minutes and seconds)
            * @param hours the hour to set the clock to
            * @param minutes the minute to set the clock to
            * @param seconds the second to set the clock to
            */
            public Clock(int hours, int minutes, int seconds) {
                this(); // Call the no argument constructor to set default values
                setHours(hours);
                setMinutes(minutes);
                setSeconds(seconds);
            }

            /**
            * Set the current hour of the clock, the time will only be updated if the provided
            * value is in the range 1-12 (inclusive)
            * @param hours the hour to set the clock to.
            */
            public void setHours(int hours) {
                this.hours = hours < HOURS_LOWER_LIMIT || hours >= HOURS_UPPER_LIMIT ? this.hours : hours;
            }

            /**
            * Set the current minute of the clock, the time will only be updated if the provided
            * value is in the range 0-60 (inclusive)
            * @param minutes the hour to set the clock to.
            */
            public void setMinutes(int minutes) {
                this.minutes = minutes < MINUTES_LOWER_LIMIT || minutes >= MINUTES_UPPER_LIMIT ? this.minutes : minutes;
            }

            /**
            * Set the current second of the clock, the time will only be updated if the provided
            * value is in the range 0-60 (inclusive)
            * @param seconds the hour to set the clock to.
            */
            public void setSeconds(int seconds) {
                this.seconds = seconds < SECONDS_LOWER_LIMIT || seconds >= SECONDS_UPPER_LIMIT ? this.seconds : seconds;
            }

            public int getHours() {
                return hours;
            }

            public int getMinutes() {
                return minutes;
            }

            public int getSeconds() {
                return seconds;
            }

            /**
            * @return A string representation of the current time of the form HH:MM:SS
            */
            @Override
            public String toString() {
                return (hours < 10 ? "0" + hours : hours) + ":" +
                    (minutes < 10 ? "0" + minutes : minutes) + ":" +
                    (seconds < 10 ? "0" + seconds : seconds);

                // Alternate version with format string
                // return "%02d:%02d:%02d".formatted(hours, minutes, seconds);
            }

            /**
            * Progress the time by one second
            */
            public void tick() {
                seconds++;
                if (seconds >= SECONDS_UPPER_LIMIT)
                    minutes++;
                if (minutes >= MINUTES_UPPER_LIMIT)
                    hours++;
                seconds %= SECONDS_UPPER_LIMIT;
                minutes %= MINUTES_UPPER_LIMIT;
                hours = hours >= HOURS_UPPER_LIMIT ? HOURS_LOWER_LIMIT : hours;
            }

            /**
            * Progress the time by the specified number of seconds. Will print the current time after each time
            * the seconds are updated.
            * @param seconds the number of seconds to increase the time by.
            */
            public void tick(int seconds) {
                for (int i = 0; i < seconds; i++) {
                    tick();
                    System.out.println(this);
                }
            }
        }

        // Example of a simple class using loops
        /**
        * A simple class for showing the usefulness of loops
        *
        * @author Linus Östlund
        * @author Gabriel Skoglund
        */
        public class Loops {

            /**
            * Print all multiples of seven between 0 and 100
            */
            public void multiplesOfSeven() {
                int multipleOfSeven = 0;
                while(multipleOfSeven < 100) {
                    System.out.println(multipleOfSeven);
                    multipleOfSeven += 7;
                }
            }

            /**
            * Sum integers between 0 and an upper bound
            * @param max the value to sum up to (inclusive)
            * @return the sum of all integers between 0 and the maximum
            */
            public int sumUpTo(int max) {
                if (max <= 0)
                    return 0;

                int sum = 0;
                int i = 1;
                while (i <= max) {
                    sum += i;
                    i++;
                }
                return sum;
            }

            /**
            * Sum a range of integers
            * @param min the value to start the sum at (inclusive)
            * @param max the value to end the sum at (inclusive)
            * @return the sum of all integers in the range min-max
            */
            public int sumBetween(int min, int max) {
                int sum = 0;
                for (int i = min; i <= max; i++) {
                    sum += i;
                }
                return sum;
            }

            /**
            * Sum all squares between 0 and a maximum
            * @param max the value to end the sum at (inclusive)
            * @return the sum of all squares between 0 and max
            */
            public int sumSquares(int max) {
                int sum = 0;
                for (int i = 0; i <= max; i++)
                    sum += i * i;
                return sum;
            }

            /**
            * Sum reciprocals (1/n) for all integers n between 0 and a maximum
            * @param max the value to end the sum at (inclusive)
            * @return the sum of all reciprocals between 0 and max
            */
            public double sumReciprocals(int max) {
                double sum = 0;
                for (int i = 1; i <= max; i++)
                    sum += 1.0 / i;
                return sum;
            }
        }

    """

    # Combine task description and inspirational code into a single prompt for solution generation
    prompt = (
        f"Based on the following task description, generate a complete and functional Java solution that meets all the requirements. "
        f"The solution should be well-structured, use meaningful variable names, include necessary comments for clarity, "
        f"and be ready to pass a comprehensive set of unit tests.\n\n"
        f"### Task Description\n\n"
        f"{task_description}\n\n"
        f"### Inspirational Code Snippet\n\n"
        f"{inspirational_code}\n\n"
        "IMPORTANT: The response must be plain Java code with no markdown formatting or ```java blocks. "
        "Ensure that each class is entirely self-contained and is not left incomplete. "
        "No part of the next file should be left in the current file. "
        "Ensure that each class is saved in its own appropriately named file, and that there are no 'leftover' initializers or class definitions from subsequent files."
        "Ensure all imports, public classes, and everything related to the class is included in the appropriate file."
        "Write NO TEXT beyond the code itself, whatsoever. "
    )

    # Call OpenAI API to generate the solution code
    response_content = generate_with_retries(client, prompt, max_retries=3)
    if response_content is None:
        print("Error: Failed to generate solution code after multiple retries.")
        sys.exit(1)

    # Ensure the .hidden_tasks directory exists
    hidden_tasks_dir = os.path.join(".hidden_tasks")
    os.makedirs(hidden_tasks_dir, exist_ok=True)

    # Write the generated code to Java files
    write_generated_code_to_files(hidden_tasks_dir, response_content)

    # Commit and push changes
    commit_and_push_changes(branch_name, hidden_tasks_dir)

def write_generated_code_to_files(directory, code_content):
    """
    Write generated Java code to appropriate files in the specified directory.
    Handles cases where leftover comments or initializations are present.
    Also ensures that import statements and public class declarations are captured.
    """
    leftover_content = ""  # To capture leftover content before the first class
    current_imports = ""   # To capture and carry over import statements
    file_blocks = re.split(r'\b(class|public\s+class|abstract\s+class|final\s+class)\b', code_content)  # Split on different class declarations

    for i in range(1, len(file_blocks), 2):  # Iterate over every class block
        class_declaration = file_blocks[i] + file_blocks[i + 1]  # Reattach split 'class' or 'public class'
        block = leftover_content + class_declaration

        # Extract class name
        class_name_match = re.search(r'class\s+([A-Za-z_]\w*)\s*{', block)  # Match 'class ClassName {'
        if class_name_match:
            class_name = class_name_match.group(1)  # Extract the class name
        else:
            print(f"Skipping block due to missing class name in block: {block[:50]}")
            continue

        # Clean up the block, removing content after the last closing brace
        cleaned_block = clean_class_block(block)

        # Ensure the necessary imports are included
        cleaned_block = check_and_add_missing_imports(cleaned_block)

        # Prepend any import statements (gathered from previous blocks)
        cleaned_block = current_imports + cleaned_block

        # Clear leftover and import content for the next file
        leftover_content = ""
        current_imports = ""

        # Write cleaned code to a file
        file_name = f"{class_name}.java"
        file_path = os.path.join(directory, file_name)

        try:
            with open(file_path, "w") as java_file:
                java_file.write(cleaned_block)
            print(f"Successfully wrote {file_name}")
        except IOError as e:
            print(f"Error writing file {file_name}: {e}")

def clean_class_block(block):
    """Ensure the block only contains content until the last closing brace."""
    
    # Find the position of the last closing brace '}' in the block
    last_closing_brace = block.rfind("}")
    
    if last_closing_brace != -1:
        # Truncate the block at the last closing brace
        block = block[:last_closing_brace + 1]
    
    return block

def check_and_add_missing_imports(block):
    """
    Check the class block for missing imports and add necessary imports based on the content.
    """
    required_imports = {
        "List": "import java.util.List;",
        "ArrayList": "import java.util.ArrayList;",
        "Map": "import java.util.Map;",
        "HashMap": "import java.util.HashMap;",
        "Scanner": "import java.util.Scanner;",
        "Set": "import java.util.Set;",
        "HashSet": "import java.util.HashSet;",
        "Random": "import java.util.Random;"
    }

    # Extract existing imports from the block
    existing_imports = re.findall(r'^\s*import .*;', block, re.MULTILINE)

    # Add missing imports
    imports_to_add = []
    for class_name, import_statement in required_imports.items():
        if class_name in block and import_statement not in existing_imports:
            imports_to_add.append(import_statement)

    # Prepend missing imports at the start of the block
    if imports_to_add:
        block = "\n".join(imports_to_add) + "\n\n" + block

    return block

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
            print(f"Error generating solution code: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
    return None

def commit_and_push_changes(branch_name, directory_path):
    try:
        subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "github-actions"], check=True)

        subprocess.run(["git", "add", directory_path], check=True)
        subprocess.run(["git", "commit", "-m", "Add generated solution"], check=True)
        subprocess.run(
            ["git", "push", "--set-upstream", "origin", branch_name],
            check=True,
            env=dict(os.environ, GIT_ASKPASS='echo', GIT_USERNAME='x-access-token', GIT_PASSWORD=os.getenv('GITHUB_TOKEN'))
        )
    except subprocess.CalledProcessError as e:
        print(f"Error committing and pushing changes: {e}")
        sys.exit(1)

if len(sys.argv) != 3:
    print("Error: Missing required command line arguments 'api_key' and 'branch_name'")
    sys.exit(1)

api_key = sys.argv[1]
branch_name = sys.argv[2]

main(api_key, branch_name)
