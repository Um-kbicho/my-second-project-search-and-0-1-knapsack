"""
utils/animator.py
──────────────────
Terminal animation helpers used throughout the project.

Animations:
  - typing_print     : types text character by character
  - spinner          : spinning indicator for short tasks
  - progress_bar     : live filling bar for DP table construction
  - reveal_result    : animated box reveal for final numbers
  - countdown        : 3-2-1 countdown before results
  - slide_in_table   : rows slide in one by one
"""

import sys
import time
import itertools


# ── Low-level helpers ──────────────────────────────────────────

def _flush(text: str) -> None:
    sys.stdout.write(text)
    sys.stdout.flush()


def _clear_line() -> None:
    _flush("\r\033[K")


# ── 1. Typing effect ───────────────────────────────────────────

def typing_print(text: str, delay: float = 0.03, newline: bool = True) -> None:
    """
    Print `text` one character at a time, like a typewriter.

    Parameters
    ----------
    text    : string to print
    delay   : seconds between each character (default 0.03)
    newline : whether to print a newline at the end
    """
    for ch in text:
        _flush(ch)
        time.sleep(delay)
    if newline:
        print()


# ── 2. Spinner ─────────────────────────────────────────────────

def spinner(label: str, duration: float = 1.0, style: str = "dots") -> None:
    """
    Show a spinning animation next to `label` for `duration` seconds.

    Styles: "dots", "braille", "arrows", "classic"
    """
    frames = {
        "dots"    : ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
        "braille" : ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"],
        "arrows"  : ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],
        "classic" : ["|", "/", "─", "\\"],
    }.get(style, ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])

    end_time = time.perf_counter() + duration
    for frame in itertools.cycle(frames):
        if time.perf_counter() >= end_time:
            break
        _flush(f"\r  {frame}  {label} ")
        time.sleep(0.08)

    _clear_line()
    _flush(f"\r  ✔  {label}\n")


# ── 3. Progress bar ────────────────────────────────────────────

def progress_bar(
    label: str,
    iterable,
    total: int,
    width: int = 40,
    fill: str = "█",
    empty: str = "░",
):
    """
    Wrap an iterable and display a live progress bar.

    Usage
    -----
        for i in progress_bar("Building DP table", range(n), n):
            ... do work for row i ...

    Parameters
    ----------
    label    : text shown to the left of the bar
    iterable : any iterable
    total    : total number of steps
    width    : character width of the bar
    fill     : character for completed portion
    empty    : character for remaining portion
    """
    start = time.perf_counter()

    for idx, item in enumerate(iterable, 1):
        yield item                          # let caller do its work

        pct      = idx / total
        filled   = int(width * pct)
        bar      = fill * filled + empty * (width - filled)
        elapsed  = time.perf_counter() - start
        eta      = (elapsed / idx) * (total - idx) if idx < total else 0

        _flush(
            f"\r  {label}  [{bar}]  "
            f"{pct*100:5.1f}%  "
            f"({idx}/{total})  "
            f"ETA {eta:.1f}s "
        )

    elapsed = time.perf_counter() - start
    _clear_line()
    _flush(f"\r  ✔  {label}  [{fill*width}]  100.0%  done in {elapsed:.2f}s\n")


# ── 4. Animated result box ─────────────────────────────────────

def reveal_result(label: str, value: str, color_code: str = "32") -> None:
    """
    Animate a result appearing inside a box, line by line.

    color_code : ANSI color (32=green, 33=yellow, 36=cyan, 31=red)
    """
    C  = f"\033[{color_code}m"   # color on
    R  = "\033[0m"               # reset
    W  = 50

    lines = [
        f"  ┌{'─'*W}┐",
        f"  │  {label:<{W-3}}│",
        f"  │  {C}{value:<{W-3}}{R}│",
        f"  └{'─'*W}┘",
    ]
    for line in lines:
        print(line)
        time.sleep(0.12)


# ── 5. Countdown ───────────────────────────────────────────────

def countdown(message: str = "Results in", start: int = 3) -> None:
    """Print a countdown then clear the line."""
    for i in range(start, 0, -1):
        _flush(f"\r  {message} {i}… ")
        time.sleep(0.6)
    _clear_line()


# ── 6. Slide-in table rows ─────────────────────────────────────

def slide_in_rows(rows: list[str], delay: float = 0.04) -> None:
    """
    Print each row in `rows` with a short delay so the table
    appears to slide in from the top.
    """
    for row in rows:
        print(row)
        time.sleep(delay)


# ── 7. Section header with typing effect ──────────────────────

def animated_section(title: str, width: int = 65) -> None:
    """
    Print a section header where the title types itself out.
    """
    print("\n" + "=" * width)
    typing_print(f"  {title}", delay=0.025)
    print("=" * width)
