# 🧙 5e Turn Taker Assistant v0.3

A streamlined initiative tracker for in-person 5e sessions where the game and maps are shown on a screen or TV. Everyone at the table can see the turn order, (optional) HP status, status effects with turn timers, and combat progress at a glance.

Made for Game Masters running in-person sessions with digital displays.

## Features

- ✔️ Add characters with custom or preselected names
- ✔️ Roll initiative with a D20 button
- ✔️ Auto-sort characters by initiative order
- ✔️ Highlight the active turn in yellow
- ✔️ Track total rounds of combat
- ✔️ Adjust HP manually or by percentage
- ✔️ (Optional) Color-coded HP bar (green, orange, red, black)
- ✔️ Remove characters when needed
- 🆕 **v0.2:** Add statuses (e.g. spells or conditions) with turn timers to characters; they are removed automatically when they expire
- 🆕 **v0.3:** No longer depends on the PIL (Pillow) package, so the app uses only the Python standard library

## Requirements

- [Python 3.10](https://www.python.org/downloads/release/python-31011/) (with Tkinter, which is included in the standard Windows and macOS installers)

No `pip install` needed.

## Running

Keep `TurnTaker.py` and `d20.png` in the same folder (the script loads the icon from the current directory), then run from that folder:

```
python TurnTaker.py
```

## License

[MIT](LICENSE)
