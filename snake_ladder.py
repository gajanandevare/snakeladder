#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║          🐍  SNAKE AND LADDER GAME  🪜                  ║
║          Modular, 2-Player Console Edition               ║
║          With Sound FX, Board View & Replay              ║
╚══════════════════════════════════════════════════════════╝

Usage:  python snake_ladder.py
"""

import random
import time
import sys


# ============================================================
# GAME CONSTANTS
# ============================================================

# Ladders: {bottom_square: top_square}
LADDERS = {
    2: 23,
    8: 34,
    20: 77,
    32: 68,
    41: 79,
    60: 91,
}

# Snakes: {head_square: tail_square}
SNAKES = {
    99: 10,
    95: 56,
    70: 55,
    52: 42,
    85: 7,
    30: 12,
}

BOARD_SIZE = 100
DICE_MIN   = 1
DICE_MAX   = 6


# ============================================================
# SOUND EFFECTS (cross-platform via terminal bell + ASCII art)
# ============================================================

def _beep(count: int = 1, delay: float = 0.12) -> None:
    """Emit terminal bell beeps."""
    for _ in range(count):
        sys.stdout.write("\a")
        sys.stdout.flush()
        if count > 1:
            time.sleep(delay)


def sound_dice_roll() -> None:
    """Sound: dice rolling animation."""
    print("  🎲 *rattle* *rattle* *rattle*", end="", flush=True)
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(0.18)
    print()
    _beep(1)


def sound_snake() -> None:
    """Sound: snake hiss — descending triple beep."""
    print("  🐍 *HISSSSSS* 🐍")
    _beep(3, delay=0.08)


def sound_ladder() -> None:
    """Sound: ladder whoosh — quick ascending beep."""
    print("  🪜 *WHOOOOSH* ↑↑↑ 🪜")
    _beep(2, delay=0.06)


def sound_extra_turn() -> None:
    """Sound: bonus ding for rolling a 6."""
    print("  🎯 *DING DING* — BONUS TURN! 🎯")
    _beep(2, delay=0.10)


def sound_win() -> None:
    """Sound: fanfare on winning."""
    print("  🎺 *FANFARE*  🥁 *DRUM ROLL*  🎊 *CONFETTI* 🎊")
    for _ in range(5):
        sys.stdout.write("\a")
        sys.stdout.flush()
        time.sleep(0.13)


# ============================================================
# DICE
# ============================================================

def roll_dice() -> int:
    """
    Animate a dice roll and return a random value 1-6.
    Displays spinning dice faces before revealing the result.
    """
    FACES = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]

    sound_dice_roll()

    # Spin animation
    for _ in range(6):
        face = FACES[random.randint(0, 5)]
        print(f"\r     {face}  spinning …", end="", flush=True)
        time.sleep(0.10)

    result = random.randint(DICE_MIN, DICE_MAX)
    print(f"\r     {FACES[result - 1]}  =  {result}          ")
    return result


# ============================================================
# MOVEMENT LOGIC
# ============================================================

def move_player(position: int, dice: int) -> int:
    """
    Compute new position after a dice roll.
    If the move would exceed 100, the player stays put (rule: exact landing required).
    """
    new_pos = position + dice
    if new_pos > BOARD_SIZE:
        print(f"  ⛔  Needs exactly {BOARD_SIZE - position} to win — rolled {dice}, stay at {position}.")
        return position
    return new_pos


def check_snake_or_ladder(position: int) -> tuple[int, str | None]:
    """
    Check whether position has a snake or ladder.
    Returns (final_position, description_message_or_None).
    """
    if position in LADDERS:
        dest = LADDERS[position]
        sound_ladder()
        msg = f"  🪜  LADDER at {position}! Climb UP → {dest}!"
        return dest, msg

    if position in SNAKES:
        dest = SNAKES[position]
        sound_snake()
        msg = f"  🐍  SNAKE HEAD at {position}! Slide DOWN → {dest}!"
        return dest, msg

    return position, None


# ============================================================
# BOARD VISUALISATION
# ============================================================

def draw_board(player_positions: dict[str, int]) -> None:
    """
    Print a 10×10 Snake and Ladder board.

    Legend:
      L## = bottom of a ladder
      S## = head of a snake
      [X] = player marker (first letter of name)
    """
    # Build reverse lookup: square → list of player initials
    sq_to_players: dict[int, list[str]] = {}
    for name, pos in player_positions.items():
        if pos > 0:
            sq_to_players.setdefault(pos, []).append(name[0].upper())

    WIDTH = 65
    print("\n" + "=" * WIDTH)
    print("                  🎮  SNAKE AND LADDER BOARD  🎮")
    print("=" * WIDTH)

    for row in range(10):
        # Alternate direction: row 0 → 100-91, row 1 → 81-90, ...
        base = BOARD_SIZE - row * 10
        if row % 2 == 0:
            squares = range(base, base - 10, -1)   # right-to-left
        else:
            squares = range(base - 9, base + 1)    # left-to-right

        line = "|"
        for sq in squares:
            # Choose cell label
            if sq in sq_to_players:
                label = "[" + "".join(sq_to_players[sq]) + "]"
            elif sq in LADDERS:
                label = f"L{sq}"
            elif sq in SNAKES:
                label = f"S{sq}"
            else:
                label = str(sq)
            line += f"{label:^6}|"

        print(line)
        print("-" * WIDTH)

    # Key
    print(f"  L## = Ladder bottom  |  S## = Snake head  |  [X] = Player")
    print("  Standings: ", end="")
    for name, pos in player_positions.items():
        bar_filled = int((pos / BOARD_SIZE) * 15)
        bar = "█" * bar_filled + "░" * (15 - bar_filled)
        print(f"  {name}: [{bar}] {pos}/100", end="")
    print()
    print("=" * WIDTH + "\n")


# ============================================================
# DISPLAY HELPERS
# ============================================================

def print_banner() -> None:
    """Print the game title banner."""
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║          🐍   SNAKE AND LADDER GAME   🪜                ║")
    print("║               2-Player Console Edition                  ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()


def print_turn_header(name: str, turn: int) -> None:
    """Print a styled header for each turn."""
    print("═" * 60)
    print(f"  🎮  Turn #{turn}  —  {name.upper()}'s turn")
    print("─" * 60)


def print_encounter_info() -> None:
    """Print snake/ladder positions at game start."""
    print("  🪜  Ladders (bottom → top):")
    for b, t in LADDERS.items():
        print(f"      {b:3} → {t}")
    print()
    print("  🐍  Snakes (head → tail):")
    for h, t in SNAKES.items():
        print(f"      {h:3} → {t}")
    print()


# ============================================================
# INPUT HELPERS
# ============================================================

def get_player_names() -> tuple[str, str]:
    """Prompt for two player names; use defaults if blank."""
    print("  Enter player names (press Enter to keep default):\n")
    name1 = input("  Player 1 name [Player 1]: ").strip() or "Player 1"
    name2 = input("  Player 2 name [Player 2]: ").strip() or "Player 2"
    if name1 == name2:
        name2 += " II"
    return name1, name2


def press_enter(prompt: str = "  ↵  Press Enter to roll the dice … ") -> None:
    """Block until the player presses Enter."""
    input(prompt)


def ask_replay() -> bool:
    """Ask players whether they want a rematch."""
    ans = input("\n  🔄  Play again? (y / n): ").strip().lower()
    return ans in ("y", "yes")


# ============================================================
# TURN LOGIC
# ============================================================

def take_turn(
    name: str,
    position: int,
    all_positions: dict[str, int],
    turn: int,
) -> tuple[int, bool]:
    """
    Execute one full turn for a player.

    Returns:
        (new_position, got_extra_turn)
    """
    print_turn_header(name, turn)

    # Show current standings
    print("  📊  Current positions:")
    for n, p in all_positions.items():
        marker = "► " if n == name else "  "
        print(f"   {marker}{n}: {p}")
    print()

    press_enter()

    # Roll dice
    dice = roll_dice()
    print(f"  🎲  {name} rolled: {dice}")

    old_pos = position

    # Apply move
    new_pos = move_player(old_pos, dice)

    if new_pos != old_pos:
        print(f"  📍  {name}: {old_pos} → {new_pos}")

        # Check snake / ladder
        final_pos, msg = check_snake_or_ladder(new_pos)
        if msg:
            print(msg)
            print(f"  📍  {name}: {new_pos} → {final_pos}")
            new_pos = final_pos

    # Extra turn on rolling 6 (only if not winning on this roll)
    extra_turn = dice == 6 and new_pos != BOARD_SIZE
    if extra_turn:
        sound_extra_turn()
        print(f"\n  ✨  {name} rolled 6 and gets a BONUS TURN!\n")

    return new_pos, extra_turn


# ============================================================
# WIN CHECK
# ============================================================

def check_winner(name: str, position: int) -> bool:
    """Return True (and display winner screen) if player reached 100."""
    if position == BOARD_SIZE:
        sound_win()
        print()
        print("╔══════════════════════════════════════════════════════════╗")
        win_line = f"  🏆  {name} WINS THE GAME!  🏆"
        print(f"║{win_line:^58}║")
        print("║          🎉  Congratulations!  🎊                       ║")
        print("╚══════════════════════════════════════════════════════════╝")
        return True
    return False


# ============================================================
# MAIN GAME FUNCTION
# ============================================================

def play_game() -> None:
    """Set up and run one complete game session."""
    print_banner()
    print_encounter_info()

    name1, name2 = get_player_names()
    print(f"\n  Welcome, {name1} and {name2}!")
    print(f"  Both players start at 0 — first to reach exactly {BOARD_SIZE} wins!\n")
    time.sleep(0.8)

    # State
    positions: dict[str, int] = {name1: 0, name2: 0}
    players = [name1, name2]
    idx = 0          # index of current player
    turn_count = 0
    game_over = False

    while not game_over:
        current = players[idx]
        turn_count += 1

        new_pos, extra = take_turn(current, positions[current], positions, turn_count)
        positions[current] = new_pos

        # Visualise board after every move
        draw_board(positions)

        # Check for winner
        if check_winner(current, new_pos):
            game_over = True
            break

        # Advance turn: same player if extra turn, else switch
        if not extra:
            idx = (idx + 1) % 2
        else:
            time.sleep(0.4)


# ============================================================
# ENTRY POINT
# ============================================================

def main() -> None:
    """Entry point — handles replay loop."""
    while True:
        play_game()
        if ask_replay():
            print("\n  🔄  Starting a new game …\n")
            time.sleep(0.8)
        else:
            print("\n  👋  Thanks for playing Snake and Ladder! Goodbye!\n")
            break


if __name__ == "__main__":
    main()
