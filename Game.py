import random
import time


class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.attack = 20
        self.defense = 5
        self.inventory = ["rusty sword", "healing potion"]
        self.gold = 50
        self.level = 1
        self.experience = 0

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        return actual_damage

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def gain_exp(self, exp):
        self.experience += exp
        if self.experience >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_health += 20
        self.health = self.max_health
        self.attack += 5
        self.defense += 2
        print(f"\n🎉 Level up! You are now level {self.level}!")
        print(f"Health: {self.max_health}, Attack: {self.attack}, Defense: {self.defense}")


class Enemy:
    def __init__(self, name, health, attack, defense, exp_reward, gold_reward):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward


class Game:
    def __init__(self):
        self.player = None
        self.current_room = "entrance"
        self.game_over = False
        self.rooms_visited = set()

        # Define enemies
        self.enemies = {
            "goblin": Enemy("Goblin", 30, 15, 2, 25, 15),
            "orc": Enemy("Orc", 50, 25, 5, 50, 30),
            "skeleton": Enemy("Skeleton", 40, 20, 3, 35, 20),
            "dragon": Enemy("Ancient Dragon", 150, 40, 10, 200, 100)
        }

        # Define rooms and their connections
        self.rooms = {
            "entrance": {
                "description": "You stand at the entrance of a dark, mysterious dungeon. Ancient stones form an archway above you.",
                "exits": {"north": "corridor", "east": "armory"},
                "items": [],
                "enemy": None
            },
            "corridor": {
                "description": "A long, dimly lit corridor stretches before you. Water drips from the ceiling.",
                "exits": {"south": "entrance", "north": "treasure_room", "west": "goblin_den"},
                "items": ["torch"],
                "enemy": None
            },
            "armory": {
                "description": "An old armory filled with rusty weapons and armor scattered on the floor.",
                "exits": {"west": "entrance", "north": "skeleton_chamber"},
                "items": ["iron sword", "leather armor"],
                "enemy": None
            },
            "goblin_den": {
                "description": "A foul-smelling cave with bones scattered around. You hear growling in the darkness.",
                "exits": {"east": "corridor"},
                "items": ["healing potion"],
                "enemy": "goblin"
            },
            "skeleton_chamber": {
                "description": "A cold chamber with ancient tombs lining the walls. An eerie silence fills the air.",
                "exits": {"south": "armory", "west": "orc_lair"},
                "items": ["magic scroll"],
                "enemy": "skeleton"
            },
            "orc_lair": {
                "description": "A large cavern with primitive decorations. The smell of smoke and meat fills the air.",
                "exits": {"east": "skeleton_chamber"},
                "items": ["gold coins", "battle axe"],
                "enemy": "orc"
            },
            "treasure_room": {
                "description": "A magnificent chamber filled with glittering treasures and ancient artifacts.",
                "exits": {"south": "corridor", "north": "dragon_chamber"},
                "items": ["treasure chest", "golden sword", "healing potion"],
                "enemy": None
            },
            "dragon_chamber": {
                "description": "An enormous chamber with a high ceiling. Piles of gold surround an ancient dragon!",
                "exits": {"south": "treasure_room"},
                "items": ["dragon hoard"],
                "enemy": "dragon"
            }
        }

    def start_game(self):
        print("=" * 50)
        print("🏰 WELCOME TO THE DUNGEON ADVENTURE! 🏰")
        print("=" * 50)
        print("\nA mysterious dungeon has appeared near your village.")
        print("Legends speak of great treasures hidden within...")
        print("But beware - dangerous creatures guard these riches!")

        name = input("\nWhat is your name, brave adventurer? ").strip()
        if not name:
            name = "Hero"

        self.player = Player(name)
        print(f"\nWelcome, {self.player.name}! Your adventure begins now...")
        time.sleep(2)

        self.game_loop()

    def game_loop(self):
        while not self.game_over and self.player.health > 0:
            self.display_room()
            self.display_status()
            choice = self.get_user_input()
            self.process_choice(choice)

            if self.current_room == "dragon_chamber" and "dragon" not in [e.name.lower() for e in
                                                                          self.get_remaining_enemies()]:
                self.win_game()

    def display_room(self):
        room = self.rooms[self.current_room]
        print("\n" + "=" * 60)
        print(f"📍 Location: {self.current_room.replace('_', ' ').title()}")
        print("=" * 60)
        print(room["description"])

        if room["items"]:
            print(f"\n🎒 Items here: {', '.join(room['items'])}")

        if room["enemy"] and room["enemy"] in self.enemies:
            enemy = self.enemies[room["enemy"]]
            if enemy.health > 0:
                print(f"\n⚔️  A {enemy.name} blocks your path! (Health: {enemy.health})")

        print(f"\n🚪 Exits: {', '.join(room['exits'].keys())}")

    def display_status(self):
        print(f"\n💖 Health: {self.player.health}/{self.player.max_health}")
        print(f"⭐ Level: {self.player.level} (EXP: {self.player.experience})")
        print(f"💰 Gold: {self.player.gold}")
        print(f"🎒 Inventory: {', '.join(self.player.inventory)}")

    def get_user_input(self):
        print("\n" + "-" * 40)
        print("What would you like to do?")
        print("• move [direction] - Move to another room")
        print("• take [item] - Pick up an item")
        print("• use [item] - Use an item from inventory")
        print("• attack - Attack an enemy")
        print("• inventory - View detailed inventory")
        print("• quit - Exit the game")
        print("-" * 40)

        return input("Enter your choice: ").lower().strip()

    def process_choice(self, choice):
        if choice.startswith("move "):
            direction = choice[5:]
            self.move_player(direction)
        elif choice.startswith("take "):
            item = choice[5:]
            self.take_item(item)
        elif choice.startswith("use "):
            item = choice[4:]
            self.use_item(item)
        elif choice == "attack":
            self.combat()
        elif choice == "inventory":
            self.show_inventory()
        elif choice == "quit":
            self.quit_game()
        else:
            print("❌ Invalid command. Try again!")

    def move_player(self, direction):
        room = self.rooms[self.current_room]

        # Check if there's an enemy blocking the path
        if room["enemy"] and room["enemy"] in self.enemies:
            enemy = self.enemies[room["enemy"]]
            if enemy.health > 0:
                print(f"❌ The {enemy.name} blocks your path! You must defeat it first.")
                return

        if direction in room["exits"]:
            self.current_room = room["exits"][direction]
            self.rooms_visited.add(self.current_room)
            print(f"🚶 You move {direction}...")
            time.sleep(1)
        else:
            print("❌ You can't go that way!")

    def take_item(self, item):
        room = self.rooms[self.current_room]
        if item in room["items"]:
            room["items"].remove(item)
            self.player.inventory.append(item)
            print(f"✅ You picked up: {item}")

            # Special item effects
            if item == "gold coins":
                self.player.gold += 25
                print("💰 You gained 25 gold!")
        else:
            print("❌ That item is not here!")

    def use_item(self, item):
        if item not in self.player.inventory:
            print("❌ You don't have that item!")
            return

        if "healing potion" in item:
            self.player.heal(30)
            self.player.inventory.remove(item)
            print(f"💚 You drink the healing potion and recover 30 health!")
            print(f"Health: {self.player.health}/{self.player.max_health}")
        elif item == "magic scroll":
            self.player.attack += 10
            self.player.inventory.remove(item)
            print("✨ The magic scroll increases your attack power by 10!")
        elif item == "treasure chest":
            self.player.gold += 100
            self.player.inventory.remove(item)
            print("💰 You open the treasure chest and find 100 gold!")
        else:
            print(f"❌ You can't use {item} right now.")

    def combat(self):
        room = self.rooms[self.current_room]
        if not room["enemy"] or room["enemy"] not in self.enemies:
            print("❌ There's nothing to fight here!")
            return

        enemy = self.enemies[room["enemy"]]
        if enemy.health <= 0:
            print("❌ This enemy has already been defeated!")
            return

        print(f"\n⚔️  COMBAT: {self.player.name} vs {enemy.name}!")
        print("=" * 40)

        while enemy.health > 0 and self.player.health > 0:
            # Player attacks
            damage = random.randint(self.player.attack - 5, self.player.attack + 5)
            enemy_damage_taken = max(1, damage - enemy.defense)
            enemy.health -= enemy_damage_taken

            print(f"⚔️  You attack for {enemy_damage_taken} damage!")

            if enemy.health <= 0:
                print(f"🎉 You defeated the {enemy.name}!")
                self.player.gain_exp(enemy.exp_reward)
                self.player.gold += enemy.gold_reward
                print(f"💰 You gained {enemy.gold_reward} gold and {enemy.exp_reward} experience!")
                break

            # Enemy attacks
            enemy_damage = random.randint(enemy.attack - 3, enemy.attack + 3)
            player_damage_taken = self.player.take_damage(enemy_damage)

            print(f"💥 The {enemy.name} attacks you for {player_damage_taken} damage!")
            print(f"Your health: {self.player.health}/{self.player.max_health}")

            if self.player.health <= 0:
                self.game_over = True
                print("\n💀 You have been defeated! Game Over!")
                return

            time.sleep(1.5)

    def show_inventory(self):
        print("\n🎒 INVENTORY:")
        print("=" * 30)
        if self.player.inventory:
            for i, item in enumerate(self.player.inventory, 1):
                print(f"{i}. {item}")
        else:
            print("Your inventory is empty.")
        print(f"\n💰 Gold: {self.player.gold}")

    def get_remaining_enemies(self):
        return [enemy for enemy in self.enemies.values() if enemy.health > 0]

    def win_game(self):
        print("\n" + "=" * 60)
        print("🏆 CONGRATULATIONS! YOU HAVE CONQUERED THE DUNGEON! 🏆")
        print("=" * 60)
        print(f"You have successfully defeated all enemies and claimed the dragon's hoard!")
        print(f"Final Stats:")
        print(f"• Level: {self.player.level}")
        print(f"• Gold: {self.player.gold}")
        print(f"• Rooms Explored: {len(self.rooms_visited)}")
        print("\nThank you for playing!")
        self.game_over = True

    def quit_game(self):
        print("👋 Thanks for playing! Goodbye!")
        self.game_over = True


def main():
    game = Game()
    game.start_game()


if __name__ == "__main__":
    main()