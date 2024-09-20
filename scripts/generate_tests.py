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

    # Ensure we are on the correct branch
    try:
        subprocess.run(["git", "checkout", branch_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error checking out branch {branch_name}: {e}")
        sys.exit(1)

    # Read the solution code from the .hidden_tasks directory
    solution_files = []
    try:
        for filename in os.listdir(".hidden_tasks"):
            if filename.endswith(".java"):
                with open(os.path.join(".hidden_tasks", filename), "r") as file:
                    solution_files.append(file.read())
    except FileNotFoundError:
        print("Error: Solution files not found in .hidden_tasks directory.")
        sys.exit(1)

    if not solution_files:
        print("Error: No Java solution files found in .hidden_tasks.")
        sys.exit(1)

    solution = "\n\n".join(solution_files)

    # Example tests to inspire the model (not to be directly copied)
    example_tests = """
    import org.junit.Before;
    import org.junit.Test;

    import static org.junit.Assert.assertEquals;

    /**
    * Tests for the Clock class
    *
    * @author Linus Östlund
    * @author Gabriel Skoglund
    */
    public class ClockTest {

        private Clock clock;

        @Before
        public void setUp() {
            clock = new Clock();
        }

        @Test
        public void zeroParameterConstructorSetsCorrectTime() {
            assertEquals(12, clock.getHours());
            assertEquals(0, clock.getMinutes());
            assertEquals(0, clock.getSeconds());
        }

        @Test
        public void parameterizedConstructorSetsCorrectTime() {
            clock = new Clock(8, 37, 5);
            assertEquals(8, clock.getHours());
            assertEquals(37, clock.getMinutes());
            assertEquals(5, clock.getSeconds());
        }

        @Test
        public void parameterizedConstructorDisregardsInvalidParameterValues() {
            clock = new Clock(-1, 99, 5);
            assertEquals(12, clock.getHours());
            assertEquals(0, clock.getMinutes());
            assertEquals(5, clock.getSeconds());
        }

        @Test
        public void setSecondsDoesNotAcceptValuesBelowZero() {
            clock.setSeconds(14);
            clock.setSeconds(-1);
            assertEquals(14, clock.getSeconds());
        }

        @Test
        public void setSecondsDoesNotAcceptValuesAbove59() {
            clock.setSeconds(10);
            clock.setSeconds(60);
            assertEquals(10, clock.getSeconds());
        }

        @Test
        public void setMinutesDoesNotAcceptValuesBelowZero() {
            clock.setMinutes(14);
            clock.setMinutes(-1);
            assertEquals(14, clock.getMinutes());
        }

        @Test
        public void setMinutesDoesNotAcceptValuesAbove59() {
            clock.setMinutes(10);
            clock.setMinutes(60);
            assertEquals(10, clock.getMinutes());
        }

        @Test
        public void setHoursDoesNotAcceptValuesBelowOne() {
            clock.setHours(5);
            clock.setHours(0);
            assertEquals(5, clock.getHours());
        }

        @Test
        public void setHoursDoesNotAcceptValuesAbove12() {
            clock.setHours(12);
            clock.setHours(13);
            assertEquals(12, clock.getHours());
        }

        @Test
        public void toStringOutputsCorrectFormat() {
            assertEquals("12:00:00", clock.toString().trim());

            clock = new Clock(8, 11, 7);
            assertEquals("08:11:07", clock.toString().trim());
        }

        @Test
        public void tickIncrementsSecondsByOne() {
            clock.tick();
            assertEquals(1, clock.getSeconds());
        }

        @Test
        public void clockTicksFrom125959to010000() {
            clock = new Clock(12, 59, 59);
            clock.tick();
            assertEquals(1, clock.getHours());
            assertEquals(0, clock.getMinutes());
            assertEquals(0, clock.getSeconds());
        }

        @Test
        public void tickIncrementsCorrectNumberOfSeconds() {
            clock = new Clock(8, 37, 14);
            clock.tick(57);
            assertEquals(8, clock.getHours());
            assertEquals(38, clock.getMinutes());
            assertEquals(11, clock.getSeconds());
        }
    }



    import org.junit.Before;
    import org.junit.Ignore;
    import org.junit.Test;

    import static org.junit.Assert.assertEquals;

    import java.io.ByteArrayOutputStream;
    import java.io.PrintStream;

    /**
    * Tests for the Loop class
    *
    * @author Linus Östlund
    * @author Gabriel Skoglund
    */
    public class LoopsTest {

        Loops loops;

        @Before
        public void setUp() {
            loops = new Loops();
        }

        @Test
        @Ignore // FIXME: There appears to be an issue with tests redirecting stdout and testing with repobee,
                // skip this test until we figure it out.
        public void multipleOfSevenIsCorrect() {
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            System.setOut(new PrintStream(out));
            loops.multiplesOfSeven();
            String[] lines = out.toString().trim().split("\\n");

            assertEquals(lines.length, 15); // there are 15 multiples, including 0
            for (int i = 0; i * 7 < 100; i++) {
                assertEquals(i * 7, Integer.parseInt(lines[i]));
            }

        }

        @Test
        public void sumUpToSumsAllIntegersTo100() {
            int sum = loops.sumUpTo(100);
            assertEquals(100*101/2, sum); // use closed form
        }

        @Test
        public void sumUpToSumsReturnsZeroIfZeroIsInput() {
            int sum = loops.sumUpTo(0);
            assertEquals(0, sum);
        }

        @Test
        public void sumUpToSumsReturnsZeroIfNegativeInput() {
            int sum = loops.sumUpTo(-5);
            assertEquals(0, sum);
        }

        @Test
        public void sumInBetweenReturns33When10and12IsPassedAsArgument() {
            int sum = loops.sumBetween(10, 12);
            assertEquals(33, sum);
        }

        @Test
        public void sumInBetweenReturnsZeroIfMinIsGreaterThanMax() {
            int sum = loops.sumBetween(12, 10);
            assertEquals(0, sum);
        }

        @Test
        public void sumInBetweenReturnsMinOrMaxIfTheyAreEqual() {
            int sum = loops.sumBetween(12, 12);
            assertEquals(12, sum);
        }

        @Test
        public void sumSquaresWorksUpTo100() {
            int sum = 0;
            for (int i = 0; i <= 100; i++) {
                sum += i * i;
                assertEquals(sum, loops.sumSquares(i));
            }
        }

        @Test
        public void sumReciprocalsWorksUpTo100() {
            double sum = 0;
            for (int i = 1; i <= 100; i++) {
                sum += 1.0 / i;
                assertEquals(sum, loops.sumReciprocals(i), 1e-14);
            }
        }
    }


    """

    # Combine the solution into a single prompt for test generation
    prompt = (
        f"Given the following Java solution, generate a set of high-quality unit tests. "
        f"Ensure the tests are thorough, robust, and cover all edge cases, including invalid inputs, boundary conditions, and performance considerations. "
        f"Ensure the tests use the correct imports and that each class is placed in the correct file as per Java naming conventions.\n\n"
        f"### Solution\n{solution}\n\n"
        f"### Example Tests (for inspiration only)\n{example_tests}\n\n"
        "IMPORTANT: The response must be plain Java code with no markdown formatting or ```java blocks. Ensure that the response is ready to be saved directly as a .java file."
        "Make sure all the right imports are always included."
    )

    response_content = generate_with_retries(client, prompt, max_retries=3)
    if response_content is None:
        print("Error: Failed to generate the tests after multiple retries.")
        sys.exit(1)

    # Write the generated tests to appropriate Java files in the gen_test directory
    gen_test_dir = os.path.join("gen_test")
    write_generated_tests_to_files(gen_test_dir, response_content)

    # Commit and push changes
    commit_and_push_changes(branch_name, gen_test_dir)

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
            print(f"Error generating the tests: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
    return None

def write_generated_tests_to_files(directory, code_content):
    """
    Write generated Java tests to separate files based on class names.
    Handles cases where leftover comments or initializations are present.
    Also ensures that import statements and public class declarations are captured.
    """
    leftover_content = ""  # To capture leftover content before the first class
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

        # Construct the file content
        package_declaration = "package test;\n\n"
        imports = (
            "import org.junit.Before;\n"
            "import org.junit.Test;\n"
            "import static org.junit.Assert.*;\n\n"
        )
        file_content = package_declaration + imports + "class " + block

        file_name = f"{class_name}Test.java"
        file_path = os.path.join(directory, file_name)

        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)

        try:
            with open(file_path, "w") as java_file:
                java_file.write(file_content)
            print(f"Successfully wrote {file_name}")
        except IOError as e:
            print(f"Error writing file {file_name}: {e}")

def commit_and_push_changes(branch_name, directory):
    try:
        subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "github-actions"], check=True)

        subprocess.run(["git", "add", directory], check=True)
        subprocess.run(["git", "commit", "-m", "Add generated tests"], check=True)
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
