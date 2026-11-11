# 5e Turn Taker

A single-file combat tracker for in-person D&D 5e (2014 rules) sessions. Built for a DM running Foundry VTT on a projector: the DM view stays on the DM's screen and a separate, player-safe window can be shown to the table.

## Run it

Download `index.html` and double-click it (Edge or Chrome). No install, no build, no server. It also works from GitHub Pages if you enable it for this repo.

## Features

- Initiative order with DEX tie-breaks and drag-to-reorder (delay / ready actions)
- Round counter, session / fight / turn timers, optional turn limit
- HP with typed shortcuts (`-12`, `+5`, `t8` temp HP, `=20` set), group damage with per-target half / full / double
- Conditions with 2014 PHB text on hover and round-based durations
- Concentration save prompts, reaction tracker, legendary actions, recharge abilities
- Death saves with nat 20 / nat 1 buttons, massive-damage check
- Hidden monsters, DM-only notes
- Party roster (HP carries between fights), editable monster templates (Tomb of Annihilation starters)
- Encounter difficulty and XP calculator (2014 DMG)
- Player view window: cards or slim ribbon layout, next-up preview, turn flash and chime
- Autosave, undo / redo, JSON export / import, combat log export

## Notes

- Data is saved in the browser's local storage. Use Export to back up or move to another machine.
- Starter monster stats are from memory of the 2014 Monster Manual; check them against your book.

Released under the MIT License.
