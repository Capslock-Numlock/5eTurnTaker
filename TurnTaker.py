import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # For handling the D20 icon
import random  # For rolling initiative


class TurnTaker:
    def __init__(self, root):
        self.root = root
        self.root.title("5e Turn Taker Assistant")

        # List to store characters (as dictionaries)
        self.characters = []
        self.current_turn = 0
        self.total_turns = 1  # Start battle from turn 1

        # Pregenerated names
        self.pregenerated_names = ["Player01", "Player02", "Player03"]

        # UI Elements
        self.name_label = tk.Label(root, text="Name")
        self.name_label.grid(row=0, column=0)

        self.name_combobox = ttk.Combobox(root, values=self.pregenerated_names)
        self.name_combobox.grid(row=0, column=1)
        self.name_combobox.set("Enter or select a name")  # Default placeholder text

        self.initiative_label = tk.Label(root, text="Initiative")
        self.initiative_label.grid(row=0, column=2)

        self.initiative_entry = tk.Entry(root)
        self.initiative_entry.grid(row=0, column=3)

        # Load the D20 icon and create a button
        self.d20_image = Image.open("d20.png").resize((30, 34))  # D20 icon is 30x34 pixels
        self.d20_icon = ImageTk.PhotoImage(self.d20_image)
        self.roll_initiative_button = tk.Button(root, image=self.d20_icon, command=self.roll_initiative)
        self.roll_initiative_button.grid(row=0, column=4)

        self.hp_label = tk.Label(root, text="HP (Optional)")
        self.hp_label.grid(row=0, column=5)

        self.hp_entry = tk.Entry(root)
        self.hp_entry.grid(row=0, column=6)

        self.add_button = tk.Button(root, text="Add", command=self.add_character)
        self.add_button.grid(row=0, column=7)

        self.prev_button = tk.Button(root, text="Previous", command=self.prev_turn)
        self.prev_button.grid(row=1, column=0)

        self.next_button = tk.Button(root, text="Next", command=self.next_turn)
        self.next_button.grid(row=1, column=1)

        self.turns_label = tk.Label(root, text=f"Total Turns: {self.total_turns}")
        self.turns_label.grid(row=1, column=2, columnspan=2)

        self.update_list()

    def roll_initiative(self):
        """Roll a D20 for initiative and set it in the initiative_entry."""
        roll = random.randint(1, 20)
        self.initiative_entry.delete(0, tk.END)
        self.initiative_entry.insert(0, str(roll))

    def add_character(self):
        name = self.name_combobox.get()
        try:
            initiative = int(self.initiative_entry.get())
        except ValueError:
            # If initiative is not an integer, show an error and return
            return

        hp = self.hp_entry.get()  # Read the HP as a string
        max_hp = None
        if hp:
            try:
                max_hp = int(hp)
            except ValueError:
                return  # Ignore invalid HP input

        # Add a new character with an empty list for statuses
        self.characters.append({
            "name": name,
            "initiative": initiative,
            "hp": max_hp,
            "max_hp": max_hp,
            "statuses": []
        })
        self.characters.sort(key=lambda x: x["initiative"], reverse=True)
        self.update_list()

    def update_list(self):
        # Remove all widgets from rows > 1
        for widget in self.root.grid_slaves():
            if int(widget.grid_info()["row"]) > 1:
                widget.grid_forget()

        for i, character in enumerate(self.characters):
            bg_color = "yellow" if i == self.current_turn else "white"

            # Name and Initiative
            name_label = tk.Label(self.root, text=character["name"], bg=bg_color)
            name_label.grid(row=i + 2, column=0, sticky="w")

            initiative_label = tk.Label(self.root, text=character["initiative"], bg=bg_color)
            initiative_label.grid(row=i + 2, column=1, sticky="w")

            # HP display and controls (if HP is provided)
            if character["hp"] is not None:
                hp_label = tk.Label(self.root, text=f"{character['hp']}/{character['max_hp']}", bg=bg_color)
                hp_label.grid(row=i + 2, column=2, sticky="w")

                hp_percentage = int((character["hp"] / character["max_hp"]) * 100) if character["max_hp"] else 0
                hp_bar = ttk.Progressbar(self.root, length=100, maximum=100)
                hp_bar["value"] = hp_percentage
                hp_bar.grid(row=i + 2, column=3, sticky="w")

                if hp_percentage == 0:
                    hp_bar["style"] = "Black.Horizontal.TProgressbar"
                elif hp_percentage <= 25:
                    hp_bar["style"] = "Red.Horizontal.TProgressbar"
                elif hp_percentage <= 50:
                    hp_bar["style"] = "Orange.Horizontal.TProgressbar"
                else:
                    hp_bar["style"] = "Green.Horizontal.TProgressbar"

                hp_entry = tk.Entry(self.root, width=5)
                hp_entry.insert(0, character["hp"])
                hp_entry.grid(row=i + 2, column=4)
                hp_entry.bind("<Return>", lambda event, i=i, entry=hp_entry: self.manual_set_hp(i, entry))

                reduce_hp_button = tk.Button(self.root, text="-10%", command=lambda i=i: self.change_hp(i, -10))
                reduce_hp_button.grid(row=i + 2, column=5)

                increase_hp_button = tk.Button(self.root, text="+10%", command=lambda i=i: self.change_hp(i, 10))
                increase_hp_button.grid(row=i + 2, column=6)

            remove_button = tk.Button(self.root, text="Remove", command=lambda i=i: self.remove_character(i))
            remove_button.grid(row=i + 2, column=7)

            # Statuses display (if any)
            status_frame = tk.Frame(self.root, bg=bg_color)
            status_frame.grid(row=i + 2, column=8, sticky="w")
            statuses = character.get("statuses", [])
            for j, status in enumerate(statuses):
                status_text = f"{status['name']} ({status['turns']})"
                status_label = tk.Label(status_frame, text=status_text, bg=bg_color)
                status_label.grid(row=j, column=0, sticky="w")
                remove_status_button = tk.Button(
                    status_frame,
                    text="Remove",
                    command=lambda i=i, j=j: self.remove_status(i, j)
                )
                remove_status_button.grid(row=j, column=1)

            # Button to add a status to this character
            add_status_button = tk.Button(self.root, text="Add Status", command=lambda i=i: self.add_status_popup(i))
            add_status_button.grid(row=i + 2, column=9)

    def remove_character(self, index):
        self.characters.pop(index)
        if self.current_turn >= len(self.characters):
            self.current_turn = 0
        self.update_list()

    def change_hp(self, index, change_percentage):
        character = self.characters[index]
        if character["hp"] is not None:
            change_value = int(character["max_hp"] * (change_percentage / 100))
            character["hp"] = max(0, min(character["hp"] + change_value, character["max_hp"]))
            self.update_list()

    def manual_set_hp(self, index, entry):
        try:
            new_hp = int(entry.get())
            character = self.characters[index]
            if character["hp"] is not None:
                character["hp"] = max(0, min(new_hp, character["max_hp"]))
                self.update_list()
        except ValueError:
            pass  # Ignore invalid input

    def add_status_popup(self, index):
        """Open a popup to add a status (with a turn timer) to the character at the given index."""
        popup = tk.Toplevel(self.root)
        popup.title("Add Status")
        tk.Label(popup, text="Status Name:").grid(row=0, column=0)
        status_name_entry = tk.Entry(popup)
        status_name_entry.grid(row=0, column=1)
        tk.Label(popup, text="Turns:").grid(row=1, column=0)
        turns_entry = tk.Entry(popup)
        turns_entry.grid(row=1, column=1)

        def add_status_action():
            status_name = status_name_entry.get()
            try:
                turns = int(turns_entry.get())
            except ValueError:
                popup.destroy()
                return
            if status_name and turns > 0:
                self.characters[index]["statuses"].append({"name": status_name, "turns": turns})
            popup.destroy()
            self.update_list()

        add_button = tk.Button(popup, text="Add", command=add_status_action)
        add_button.grid(row=2, column=0, columnspan=2)

    def remove_status(self, char_index, status_index):
        """Remove a status from the specified character."""
        if "statuses" in self.characters[char_index]:
            del self.characters[char_index]["statuses"][status_index]
        self.update_list()

    def next_turn(self):
        # Update statuses for the current character by decrementing their turn counters.
        if self.characters:
            current_char = self.characters[self.current_turn]
            if "statuses" in current_char:
                new_statuses = []
                for status in current_char["statuses"]:
                    status["turns"] -= 1
                    if status["turns"] > 0:
                        new_statuses.append(status)
                current_char["statuses"] = new_statuses
        self.current_turn += 1
        if self.current_turn >= len(self.characters):
            self.current_turn = 0
            self.total_turns += 1
            self.turns_label.config(text=f"Total Turns: {self.total_turns}")
        self.update_list()

    def prev_turn(self):
        if self.current_turn == 0 and self.total_turns > 1:
            self.total_turns -= 1
            self.turns_label.config(text=f"Total Turns: {self.total_turns}")
        self.current_turn = (self.current_turn - 1) % len(self.characters)
        self.update_list()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Green.Horizontal.TProgressbar", background="green")
        style.configure("Orange.Horizontal.TProgressbar", background="orange")
        style.configure("Red.Horizontal.TProgressbar", background="red")
        style.configure("Black.Horizontal.TProgressbar", background="black")


if __name__ == "__main__":
    root = tk.Tk()
    app = TurnTaker(root)
    app.setup_styles()
    root.mainloop()
