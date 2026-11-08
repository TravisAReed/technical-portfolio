# B4G Hold'em poker bots

Python bots for the Poker Bot Challenge at the Build4Good 2025 Hackathon, played by the match engine in this folder. This entry placed 3rd. The event rules are in [README.md](README.md) and are unchanged.

<!-- TODO(Travis): Your role versus anyone else who wrote code in this folder, and whether this was a team entry. A comment in `winning_skeleton/player.py` marks one block as "my work" and attributes the hand-strength function to someone else. This page does not assign credit past those comments. The folder name `winning_skeleton` is only a directory name. -->

**[TODO: Say what you wrote and who else should be credited. The 3rd-place result is listed; the credit split is still open.]**

## Context

3rd Place, Poker Bot Challenge, Build4Good 2025 Hackathon.

[README.md](README.md) is the Build4Good 2025 handout. It describes B4G Hold'em: three hole cards, a betting round, a flop of two community cards, another betting round, then the last two community cards and a final betting round. Showdown uses Texas Hold'em hand rankings. A match is 5,000 hands. Each hand starts both players at 500 chips, with blinds of 5 and 10, and the per-hand stack change updates a bankroll that starts at 0. Each bot has 180 seconds for the whole match.

The same handout says the engine was forked from the MIT Pokerbots codebase, that `engine.py` should stay as provided, and that each bot is a `player.py` plus a copied `skeleton/` package. It allows numpy and numba, and it names `eval7` as an engine dependency. The two equity bots import `eval7` as well.

`config.py` currently points player A at `./winning_skeleton` and player B at `./allin_skeleton`.

## What I built

The engine, the per-bot `skeleton/` package, `player_chatbot/`, and the handout are the challenge materials. The bot logic that differs across folders is each `player.py`.

- `python_skeleton/player.py` is the starter policy. If a raise is legal, it raises to the minimum with probability 0.5. Otherwise it checks, or folds with probability 0.25 and calls the rest of the time.
- `all_in_bot/player.py` raises a random amount whenever a raise is legal, using the incremental cost bounds (`min_raise - my_pip` through `max_raise - my_pip`). Otherwise it checks, or folds with probability 0.25.
- `allin_skeleton/player.py` raises by that same maximum incremental cost whenever a raise is legal. Otherwise it checks, or folds with probability 0.25.
- `winning_skeleton/player.py` estimates hand strength with a Monte Carlo loop and `eval7`, then sizes a raise from that estimate. It records the pot at the start of each street. On every action it overwrites `BotHand.txt` with the estimate, the hole cards, and the board.
- `competing_skeleton copy/player.py` is the same strategy as `winning_skeleton/player.py`. The differences are blank lines and a comment on the call branch.
- `player_chatbot/player.py` is the handout's interface for playing the other bot from the terminal. `USE_GPT` is `False`, so it asks a person to type `Check`, `Fold`, `Call`, or `Raise <amount>`. The GPT-4 path is present and inactive, and the API key string is empty.

## Tech stack

What the bot and engine files in this folder actually import:

- Python standard library: `random`, `math`, `collections`, `threading`, `queue`, `time`, `json`, `subprocess`, `socket`, `sys`, `os`
- [`eval7`](https://pypi.org/project/eval7/), used by `engine.py` for showdown and by the two equity bots for hand strength
- `openai` is imported only inside `player_chatbot/player.py` when `USE_GPT` is true. It is false in the checked-in file.

The handout allows numpy and numba. The `player.py` files in this folder use the standard library and, in the two equity bots, `eval7`.

## How it works

The engine starts two bot processes from the paths in `config.py`, deals 5,000 hands (or whatever `NUM_ROUNDS` is set to), and writes `gamelog.txt`. Streets in `skeleton/states.py` start at 0 and advance by 2, and a street value of 4 ends the betting. Bots read the board as `round_state.deck[:street]`, so the board length is 0, 2, or 4 cards. `RaiseAction.amount` is the player's total chips in on that street. The engine accepts a raise only when that amount sits between the two values from `raise_bounds`.

`get_hand_strength` in `winning_skeleton/player.py` draws 10 random completions of the board out to 7 cards, and for each completion draws 10 random opposing hands of the same hole-card count. Cards come from a fixed 52-card list, rejected if they are already in use. `eval7.evaluate` compares the two 7-card hands. Ties increment the loss count. The returned value is wins divided by wins plus losses (100 comparisons when every draw finishes).

When a raise is legal and that value is above 0.5, the bot sets a desired pot increase since the start of the street to `ceil(1000 * (p - 0.5) ** 2)`, subtracts chips already added this street, clamps the result to `max_raise` when it is larger, and returns `RaiseAction` of that result. If the result is negative and a call is legal, it calls. If a raise is legal and the estimate is at most 0.5, it returns `CheckAction`. If a raise is not legal, it calls when a uniform random draw is below `p` and `p` is above 0.5, calls when the call costs 0, and otherwise folds.

## How to run

From this directory, with the engine's dependency installed:

```bash
pip install eval7
python engine.py
```

That plays the two paths in `config.py`. The handout says to point `PLAYER_2_PATH` at `./player_chatbot` to type actions against the other bot. `config.py` says `NUM_ROUNDS`, the blinds, and the stack may be changed for training or experimentation. The checked-in values are a 5,000-hand match and a 180-second clock (`ENFORCE_GAME_CLOCK` is true).

Each bot folder also has `commands.json` with `"run": ["python", "player.py"]`. The engine is what pairs two bots.

## Repo contents

`skeleton/bot.py`, `skeleton/runner.py`, and `commands.json` are the same file in every bot folder. `skeleton/actions.py` matches across folders except a deleted comment in `all_in_bot`. `skeleton/states.py` matches except whitespace in `player_chatbot`. Those files are the challenge skeleton the handout says not to edit.

| File | What it does |
|---|---|
| `README.md` | Build4Good 2025 rules handout. Left as the event wrote it. |
| `engine.py` | Match engine. Starts both bots, plays `NUM_ROUNDS` hands, writes `gamelog.txt`. |
| `config.py` | Bot paths and match parameters. Currently `winning_skeleton` versus `allin_skeleton`, 5,000 hands, 500-chip stacks, blinds 10 and 5, 180-second clock. |
| `.gitignore` | Ignores Python cache, `*.txt`, Java/class and IDE files. |
| `python_skeleton/player.py` | Starter bot. Minimum raise with probability 0.5, otherwise check, or a fold with probability 0.25. |
| `python_skeleton/commands.json` | Tells the engine to run `python player.py`. |
| `python_skeleton/skeleton/actions.py` | `Fold`, `Call`, `Check`, and `Raise` action types. |
| `python_skeleton/skeleton/bot.py` | `Bot` base class with the four methods a player implements. |
| `python_skeleton/skeleton/runner.py` | Parses arguments and connects a bot process to the engine. |
| `python_skeleton/skeleton/states.py` | Round state, legal actions, raise bounds, street advance, showdown. |
| `all_in_bot/player.py` | Raises a random incremental amount whenever a raise is legal. |
| `all_in_bot/commands.json` | Same run command as the other bot folders. |
| `all_in_bot/skeleton/actions.py` | Same action types, without one comment present in the other copies. |
| `all_in_bot/skeleton/bot.py` | Same `Bot` base class. |
| `all_in_bot/skeleton/runner.py` | Same bot process runner. |
| `all_in_bot/skeleton/states.py` | Same round-state code. |
| `allin_skeleton/player.py` | Raises the maximum incremental cost whenever a raise is legal. |
| `allin_skeleton/commands.json` | Same run command. |
| `allin_skeleton/skeleton/actions.py` | Same action types. |
| `allin_skeleton/skeleton/bot.py` | Same `Bot` base class. |
| `allin_skeleton/skeleton/runner.py` | Same bot process runner. |
| `allin_skeleton/skeleton/states.py` | Same round-state code. |
| `winning_skeleton/player.py` | Monte Carlo `eval7` hand strength and the pot-based raise size. Writes `BotHand.txt` each action. |
| `winning_skeleton/commands.json` | Same run command. |
| `winning_skeleton/skeleton/actions.py` | Same action types. |
| `winning_skeleton/skeleton/bot.py` | Same `Bot` base class. |
| `winning_skeleton/skeleton/runner.py` | Same bot process runner. |
| `winning_skeleton/skeleton/states.py` | Same round-state code. |
| `competing_skeleton copy/player.py` | Same strategy as `winning_skeleton/player.py`, aside from whitespace and one comment. |
| `competing_skeleton copy/commands.json` | Same run command. |
| `competing_skeleton copy/skeleton/actions.py` | Same action types. |
| `competing_skeleton copy/skeleton/bot.py` | Same `Bot` base class. |
| `competing_skeleton copy/skeleton/runner.py` | Same bot process runner. |
| `competing_skeleton copy/skeleton/states.py` | Same round-state code. |
| `player_chatbot/player.py` | Terminal opponent. Types actions by hand unless `USE_GPT` is turned on. |
| `player_chatbot/commands.json` | Same run command. |
| `player_chatbot/skeleton/actions.py` | Same action types. |
| `player_chatbot/skeleton/bot.py` | Same `Bot` base class. |
| `player_chatbot/skeleton/runner.py` | Same bot process runner. |
| `player_chatbot/skeleton/states.py` | Same round-state code, with extra whitespace on one blank line. |

## Notes / limitations

No match log or bankroll is checked in. The 3rd-place result above is not stored as a log in this folder. `.gitignore` ignores `*.txt`, which covers `gamelog.txt` and the `BotHand.txt` debug file the equity bot writes on every decision.

The stock comments inside `python_skeleton`, `all_in_bot`, `allin_skeleton`, and `winning_skeleton` still describe streets as 0, 3, 4, or 5. In this engine, `proceed_street` adds 2 and stops at 4. `player_chatbot` comments say 0, 2, or 4, which matches the street counter. Board length still comes from `deck[:street]`.

`winning_skeleton` passes `RaiseAction` a number computed as a change in pot, then clamps it only against `max_raise`. The engine's legal interval is the pair returned by `raise_bounds`, which is in total-contribution units. `all_in_bot` and `allin_skeleton` pass the incremental costs (`raise_bounds` minus `my_pip`) rather than those totals. `python_skeleton` passes `min_raise`, which is one of the `raise_bounds` values.

When a raise is legal and the equity estimate is at most 0.5, `winning_skeleton` returns `CheckAction` without checking that check is in the legal set. Facing a bet, the legal set is fold, call, and maybe raise.

The equity function's active loop uses 10×10 samples. A larger 100-sample loop sits in a comment underneath it. Sampling is with a random full deck and rejection, not an exact enumeration, so the estimate moves from call to call. Each decision rewrites `BotHand.txt` in the process working directory.

`competing_skeleton copy` repeats `winning_skeleton` and has a space in the folder name. `all_in_bot` and `allin_skeleton` are two different raise policies with similar names.

The handout's GPT prompt text inside `player_chatbot/player.py` describes a 400-chip stack and blinds of 1 and 2. `config.py` and the handout rules use 500 chips and blinds of 5 and 10. That prompt is used only if `USE_GPT` is set to true.

<!-- TODO(Travis): Which `player.py` should be presented as the bot? Was the equity function yours, a teammate's, or shared? Do you want the terminal `player_chatbot` and the duplicate `competing_skeleton copy` described as your work? Is there a team name or a more specific date you want added? -->

**[TODO: Which `player.py` is the featured bot, and how should credit be worded? Do not leave the "my work" comment as the public account of who wrote what.]**
