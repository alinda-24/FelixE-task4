package test;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

class public class SimpleGameTest {
    
    private SimpleGame game;

    @Before
    public void setUp() {
        game = new SimpleGame();
    }

    @Test
    public void testInitialPositionAndSetup() {
        assertEquals(1, game.playerRow);
        assertEquals(1, game.playerCol);
        assertEquals(0, game.score);
        assertFalse(game.isGameOver);
    }

    @Test
    public void testValidMoveUp() {
        game.movePlayer('w');
        assertEquals(0, game.playerRow);
        assertEquals(1, game.playerCol);
        assertEquals(1, game.score);
        assertFalse(game.isGameOver);
    }

    @Test
    public void testValidMoveDown() {
        game.movePlayer('s');
        assertEquals(2, game.playerRow);
        assertEquals(1, game.playerCol);
        assertEquals(1, game.score);
        assertFalse(game.isGameOver);
    }

    @Test
    public void testValidMoveLeft() {
        game.movePlayer('a');
        assertEquals(1, game.playerRow);
        assertEquals(0, game.playerCol);
        assertEquals(1, game.score);
        assertFalse(game.isGameOver);
    }

    @Test
    public void testValidMoveRight() {
        game.movePlayer('d');
        assertEquals(1, game.playerRow);
        assertEquals(2, game.playerCol);
        assertEquals(1, game.score);
        assertFalse(game.isGameOver);
    }

    @Test
    public void testInvalidMoveNotOverwritingExistingPlayer() {
        game.movePlayer('z'); // Invalid move
        assertEquals(1, game.playerRow);
        assertEquals(1, game.playerCol);
        assertEquals(0, game.score);
        assertFalse(game.isGameOver);
    }
    
    @Test
    public void testInvalidMoveOutOfBoundsUp() {
        game.movePlayer('w');
        game.movePlayer('w'); // Out of bounds move
        assertEquals(0, game.playerRow);
        assertEquals(1, game.playerCol);
    }

    @Test
    public void testInvalidMoveOutOfBoundsDown() {
        game.movePlayer('s');
        game.movePlayer('s');
        game.movePlayer('s'); // Out of bounds move
        assertEquals(3, game.playerRow);
        assertEquals(1, game.playerCol);
    }

    @Test
    public void testInvalidMoveOutOfBoundsLeft() {
        game.movePlayer('a');
        game.movePlayer('a'); // Out of bounds move
        assertEquals(1, game.playerRow);
        assertEquals(0, game.playerCol);
    }

    @Test
    public void testInvalidMoveOutOfBoundsRight() {
        game.movePlayer('d');
        game.movePlayer('d');
        game.movePlayer('d'); // Out of bounds move
        assertEquals(1, game.playerRow);
        assertEquals(3, game.playerCol);
    }

    @Test
    public void testMoveIntoEnemyEndsGame() {
        game.movePlayer('d'); // Move right into enemy
        game.movePlayer('d'); // Moves into the enemy at (1,3)
        assertTrue(game.isGameOver);
    }

    @Test
    public void testWinGameByMaxScore() {
        // Moves the player to win the game
        game.movePlayer('d');
        game.movePlayer('d');
        game.movePlayer('s'); // Need to ensure not hitting an enemy
        game.movePlayer('s');
        game.movePlayer('a');
        game.movePlayer('a'); // Should reach maxScore
        assertEquals(game.maxScore, game.score);
        assertFalse(game.isGameOver);  // Should win by score, not game over
    }
}