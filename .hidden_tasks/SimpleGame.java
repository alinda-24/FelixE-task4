import java.util.Scanner;

public class SimpleGame {

    private char[][] board;
    private int playerRow;
    private int playerCol;
    private int score;
    private boolean isGameOver;
    private final int maxScore = 5;
    private Scanner scanner;

    public SimpleGame() {
        board = new char[][] {
            {'.', '.', '.', '.'},
            {'.', 'P', '.', 'E'},
            {'.', '.', '.', '.'},
            {'E', '.', '.', '.'}
        };
        playerRow = 1;
        playerCol = 1;
        score = 0;
        isGameOver = false;
        scanner = new Scanner(System.in);
    }

    public void playGame() {
        while (!isGameOver && score < maxScore) {
            printBoard();
            System.out.println("Score: " + score + ", Max Score to win: " + maxScore);
            System.out.print("Enter move (w/a/s/d): ");
            char direction = scanner.nextLine().charAt(0);
            movePlayer(direction);
        }
        if (isGameOver) {
            System.out.println("Game Over! You ran into an enemy.");
        } else {
            System.out.println("Congratulations! You achieved the maximum score.");
        }
    }

    private void printBoard() {
        for (char[] row : board) {
            for (char cell : row) {
                System.out.print(cell + " ");
            }
            System.out.println();
        }
    }

    public void movePlayer(char direction) {
        int newRow = playerRow;
        int newCol = playerCol;

        switch (direction) {
            case 'w':
                newRow--;
                break;
            case 's':
                newRow++;
                break;
            case 'a':
                newCol--;
                break;
            case 'd':
                newCol++;
                break;
            default:
                System.out.println("Invalid move. Use 'w', 'a', 's', or 'd'.");
                return;
        }

        if (!isValidMove(newRow, newCol)) {
            System.out.println("Invalid move. Out of bounds.");
            return;
        }

        if (board[newRow][newCol] == 'E') {
            isGameOver = true;
        } else {
            board[playerRow][playerCol] = '.';
            board[newRow][newCol] = 'P';
            playerRow = newRow;
            playerCol = newCol;
            score++;
        }
    }

    private boolean isValidMove(int row, int col) {
        return row >= 0 && row < board.length && col >= 0 && col < board[0].length;
    }

    public void movePlayer(int xOffset, int yOffset) {
        int newRow = playerRow + xOffset;
        int newCol = playerCol + yOffset;

        if (!isValidMove(newRow, newCol)) {
            System.out.println("Invalid move. Out of bounds.");
            return;
        }

        if (board[newRow][newCol] == 'E') {
            isGameOver = true;
        } else {
            board[playerRow][playerCol] = '.';
            board[newRow][newCol] = 'P';
            playerRow = newRow;
            playerCol = newCol;
            score++;
        }
    }

    public static void main(String[] args) {
        SimpleGame game = new SimpleGame();
        game.playGame();
    }
}