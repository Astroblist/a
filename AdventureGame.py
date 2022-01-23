from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from GameObject import GameObject
import Achievements
import time

DOCK = 1
FORK_1 = 2
VILLAGE_SQUARE = 3
BRIDGE = 4
CASTLE_ENTRANCE = 5
CASTLE_INSIDE_1 = 6
CAVE_ENTRANCE = 7
CAVE_INSIDE_1 = 8
VILLAGE_HOUSE_1 = 9
VILLAGE_HOUSE_2 = 10
VILLAGE_HOUSE_3 = 11
DRAGON_LAIR = 12

SWORD_DAMAGE = 6
FIST_DAMAGE = 1
SHIELD_HEALTH = 100

PLAYER_HEALTH = 25

command_widget = None
image_label = None
description_widget = None
inventory_widget = None
north_button = None
south_button = None
east_button = None
west_button = None
map_button = None
root = None

command_input = ""

refresh_location = True
refresh_objects_visible = True

current_location = DOCK
end_of_game = False

map_clicked = False
map_inventory = False
map_uses = 0

sword_pickup = False
shield_pickup = False


class Entity:
    def __init__(self, maxhealth, health, damage):
        self.maxhealth = maxhealth
        self.health = health
        self.damage = damage


e_guard = Entity(10, 10, 2)
e_dragon = Entity(50, 50, 10)
e_king = Entity(20, 20, 5)

entities = [e_guard, e_dragon, e_king]

sword = GameObject("Sword", VILLAGE_HOUSE_1, True, True, False, False, "A sword for 'self defense'")
shield = GameObject("Shield", VILLAGE_HOUSE_2, True, True, False, False, "A shield for too defend from attacks")
map_object = GameObject("Map", VILLAGE_SQUARE, True, True, False, False, "A map_object of the island")
king = GameObject("King", CASTLE_INSIDE_1, False, True, False, True,
                  "Name - Paul Genge, Height - 5'8, Build - Different")
key = GameObject("Key", CASTLE_ENTRANCE, False, False, False, False, "A key to open the castle")
guard = GameObject("Guard", CASTLE_ENTRANCE, False, True, False, True, "He does not let you enter")
torch = GameObject("Torch", CAVE_INSIDE_1, True, True, False, False, "A shield for too defend from attacks")
dragon = GameObject("DRAGON", DRAGON_LAIR, False, True, False, True, "A Ferocious beast hides the treasure!")

game_objects = [sword, shield, map_object, key, torch, king, guard, dragon]


def perform_command(verb, noun):
    global command_input
    command_input = verb

    if verb == "GO":
        perform_go_command(noun)
    elif (verb == "N") or (verb == "S") or (verb == "E") or (verb == "W"):
        perform_go_command(verb)
    elif (verb == "NORTH") or (verb == "SOUTH") or (verb == "EAST") or (verb == "WEST"):
        perform_go_command(verb)
    elif verb == "GET":
        perform_get_command(noun)
    elif verb == "PUT":
        perform_put_command(noun)
    elif verb == "LOOK":
        perform_look_command(noun)
    elif (verb == "READ"):
        perform_read_command(noun)
    elif (verb == "OPEN"):
        perform_open_command(noun)
    elif (verb == "MAP"):
        preform_map_command()
    elif (verb == "ATTACK"):
        preform_attack_command(noun)
    elif (verb == "BLOCK"):
        perform_block_command(noun)
    elif (verb == "ACHIEVEMENTS"):
        print_achievement_list()
    elif verb == "HEAL":
        preform_heal_command()
    else:
        print_to_description("huh?")


def perform_go_command(direction):
    global current_location
    global refresh_location

    if "N" == direction or direction == "NORTH":
        new_location = get_location_to_north()
    elif direction == "S" or direction == "SOUTH":
        new_location = get_location_to_south()
    elif (direction == "E" or direction == "EAST"):
        new_location = get_location_to_east()
    elif (direction == "W" or direction == "WEST"):
        new_location = get_location_to_west()
    else:
        new_location = 0

    if (new_location == 0):
        print_to_description("You can't go that way!")
    else:
        current_location = new_location
        refresh_location = True


def perform_get_command(object_name):
    global refresh_objects_visible
    global sword_pickup
    global shield_pickup

    game_object = get_game_object(object_name)

    if not (game_object is None):
        if game_object.location != current_location or not game_object.visible:
            print_to_description("You don't see one of those here!")
        elif not game_object.movable:
            print_to_description("You can't pick it up!")
        elif game_object.carried:
            print_to_description("You are already carrying it")
        else:
            if guard.alive and current_location == CASTLE_ENTRANCE:
                print_to_description("The guard is holding the key")
            else:
                # pick up the object
                game_object.carried = True
                game_object.visible = False
                refresh_objects_visible = True
    else:
        print_to_description("You don't see one of those here!")


def perform_put_command(object_name):
    global refresh_objects_visible
    game_object = get_game_object(object_name)

    if not (game_object is None):
        if game_object.carried == False:
            print_to_description("You are not carrying one of those.")
        else:
            # put down the object
            game_object.location = current_location
            game_object.carried = False
            game_object.visible = True
            refresh_objects_visible = True
    else:
        print_to_description("You are not carrying one of those!")


#
def perform_look_command(object_name):
    global refresh_location
    global refresh_objects_visible
    global game_objects

    game_object = get_game_object(object_name)

    if not (game_object is None):

        if (game_object.carried == True) or (game_object.visible and game_object.location == current_location):
            print_to_description(game_object.description)
        else:
            # recognized but not visible
            print_to_description("You can't see one of those!")

        # special cases - when certain objects are looked at, others are revealed!
        if guard and GUARD_HEALTH > 0:
            print_to_description("The guard is carrying a key")
            key.visible = True
            global refresh_objects_visible
            refresh_objects_visible = True

    else:
        if object_name == "":
            # generic LOOK
            refresh_location = True
            refresh_objects_visible = True
        else:
            # not visible recognized
            print_to_description("You can't see one of those!")


def fight(object_name):
    global refresh_objects_visible
    global refresh_location
    global PLAYER_HEALTH
    global SHIELD_HEALTH

    game_object = object_name

    if not (game_object is None):
        if game_object.name == 'Guard':
            if guard.alive and PLAYER_HEALTH > 0:
                print_to_description('So you want to fight?')
                print_to_description("The blunt sword of the guard is weak")
                print_to_description("Do you want to block the attack")

                if command_input == 'Yes':
                    SHIELD_HEALTH -= e_guard.damage
                    print_to_description('You have ' + str(PLAYER_HEALTH) + ' health remaining')

        elif game_object.name == "King":
            pass

        else:
            pass


def preform_attack_command(object_name):
    global refresh_objects_visible
    global refresh_location
    global SWORD_DAMAGE
    global FIST_DAMAGE

    game_object = get_game_object(object_name)

    if not (game_object is None):
        if game_object.name == "King":
            if e_king.health > 0 and (e_king.health - SWORD_DAMAGE) > 0:
                if sword.carried:
                    e_king.health -= SWORD_DAMAGE
                    print_to_description("You stab the king")
                    print_to_description("The king has " + str(e_king.health) + " health remaining")
                else:
                    e_king.health -= FIST_DAMAGE
                    print_to_description("You slap the king")
                    print_to_description("The guard has " + str(e_king.health) + " health remaining")
            else:
                print_to_description("You killed the king")
                print_to_description("You can no longer buy a boat from the king")
        elif game_object.name == "Guard":
            if sword.carried and ((e_guard.health - SWORD_DAMAGE) > 0) or not sword.carried and e_guard.health > 1:
                if sword.carried:
                    e_guard.health -= SWORD_DAMAGE
                    print_to_description("You stab the guard")
                    print_to_description("The guard has " + str(e_guard.health) + " health remaining")
                    fight(guard)
                else:
                    e_guard.health -= FIST_DAMAGE
                    print_to_description("You slap the guard")
                    print_to_description("The guard has " + str(e_guard.health) + " health remaining")
                    fight(guard)
            else:
                print_to_description("The guard has been slain")
                guard.alive = False
                guard.visible = False
                key.visible = True
                key.movable = True
                set_current_image()
        elif current_location == DRAGON_LAIR:
            if sword.carried:
                e_dragon.health -= SWORD_DAMAGE
            else:
                e_dragon.health -= FIST_DAMAGE
        else:
            print_to_description("There is nothing to attack!")
    else:
        # not visible recognized
        print_to_description("You can't kill what you can't see")


def perform_block_command(object_name):
    game_object = get_game_object(object_name)

    if not (game_object is None):
        if shield.carried:
            pass


def preform_heal_command():
    pass


def perform_read_command(object_name):
    game_object = get_game_object(object_name)

    if not (game_object is None):
        if (False):
            print_to_description("special condition")
        else:
            print_to_description("There is no text on it")
    else:
        print_to_description("I am not sure which " + object_name + "you are referring to")


def perform_open_command(object_name):
    global door_openend
    game_object = get_game_object(object_name)

    if not (game_object is None):
        if (False):
            print_to_description("special condition")
        else:
            print_to_description("You can't open one of those.")
    else:
        print_to_description("You don't see one of those here.")


def check_achievements(event):
    if event == "Map":
        Achievements.cartographer.status = "Complete"
        print_to_description("Achievement Complete!" + "  " + Achievements.cartographer.description)


def print_achievement_list():
    for Achievement in Achievements.Achievement:
        if Achievement.status:
            print_to_description(Achievement.name + ": " + Achievement.status)


def preform_map_command():
    global map_clicked
    global map_uses

    if not map_clicked and map_object.carried:
        if (current_location == DOCK):
            image_label.img = PhotoImage(file='res/dock_map.gif')
        elif (current_location == FORK_1):
            image_label.img = PhotoImage(file='res/fork_map.gif')
        elif (current_location == VILLAGE_SQUARE):
            image_label.img = PhotoImage(file='res/village_map.gif')
        elif (current_location == BRIDGE):
            image_label.img = PhotoImage(file='res/bridge_map.gif')
        elif current_location == CASTLE_ENTRANCE:
            image_label.img = PhotoImage(file='res/castle_map.gif')
        elif (current_location == CASTLE_INSIDE_1):
            image_label.img = PhotoImage(file='res/castle_map.gif')
        elif (current_location == CAVE_ENTRANCE):
            image_label.img = PhotoImage(file='res/cave_ent_maps.gif')
        elif (current_location == CASTLE_INSIDE_1):
            image_label.img = PhotoImage(file='res/cave_ent_map.gif')
        else:
            image_label.img = PhotoImage(file='res/Base Map.gif')
        map_clicked = True
        map_uses += 1
        if map_uses == 1:
            check_achievements("Map")
    else:
        set_current_image()
        map_clicked = False

    image_label.config(image=image_label.img)


def describe_current_location():
    if (current_location == DOCK):
        print_to_description("You find yourself at a dock, with a broken boat and no idea where you are.")
    elif (current_location == FORK_1):
        print_to_description("To the left, there is a bridge, and the right there is a village")
    elif (current_location == VILLAGE_SQUARE):
        print_to_description("A humble village with only a few houses")
    elif (current_location == BRIDGE):
        print_to_description("Would you dare cross this bridge to reach the castle?")
    elif (current_location == CASTLE_ENTRANCE):
        print_to_description("The entrance to a mighty castle")
    elif (current_location == CASTLE_INSIDE_1):
        print_to_description("The king will sell you a brand new ship for 100 gold")
    elif (current_location == CAVE_ENTRANCE):
        print_to_description("Its a very dark and scary cave")
    elif (current_location == CAVE_INSIDE_1):
        print_to_description("A very dark and eerie cave with something shiny at the end")
    elif (current_location == VILLAGE_HOUSE_1):
        print_to_description("A blacksmiths house")
    elif (current_location == VILLAGE_HOUSE_2):
        print_to_description("A merchant who sells all sorts of useful items")
    elif (current_location == VILLAGE_HOUSE_3):
        print_to_description("Do not enter, leave.")
    elif (current_location == DRAGON_LAIR):
        print_to_description("A dragon is awaits sitting atop his fortune")
    else:
        print_to_description("unknown location:" + current_location)


def set_current_image():
    global GUARD_HEALTH
    global KING_HEALTH
    global DRAGON_HEALTH

    if (current_location == DOCK):
        image_label.img = PhotoImage(file='res/dock.png')
    elif (current_location == FORK_1):
        image_label.img = PhotoImage(file='res/blank-2.gif')
    elif (current_location == VILLAGE_SQUARE):
        image_label.img = PhotoImage(file='res/village_square.png')
    elif (current_location == BRIDGE):
        image_label.img = PhotoImage(file='res/bridge.gif')
    elif current_location == CASTLE_ENTRANCE and guard.alive == True:
        image_label.img = PhotoImage(file='res/castle_with_guard.gif')
    elif current_location == CASTLE_ENTRANCE:
        image_label.img = PhotoImage(file='res/castle.gif')
    elif (current_location == CASTLE_INSIDE_1):
        image_label.img = PhotoImage(file='res/blank-3.gif')
    elif (current_location == CAVE_ENTRANCE):
        if torch.carried:
            image_label.img = PhotoImage(file='res/blank-1.gif')
        else:
            image_label.img = PhotoImage(file='res/cave_no_torch.png')
    elif (current_location == CASTLE_INSIDE_1):
        image_label.img = PhotoImage(file='res/blank-2.gif')
    else:
        image_label.img = PhotoImage(file='res/blank-1.gif')

    image_label.config(image=image_label.img)


def get_location_to_north():
    global refresh_location

    if (current_location == DOCK):
        return FORK_1
    elif (current_location == FORK_1):
        return VILLAGE_SQUARE
    elif (current_location == CASTLE_ENTRANCE):
        if key.carried:
            return CASTLE_INSIDE_1
        else:
            return 0
    elif (current_location == CAVE_ENTRANCE):
        return CAVE_INSIDE_1
    elif (current_location == VILLAGE_SQUARE):
        return VILLAGE_HOUSE_2
    elif current_location == CAVE_INSIDE_1:
        return DRAGON_LAIR
    else:
        return 0


def get_location_to_south():
    global refresh_location

    if (current_location == VILLAGE_SQUARE):
        return FORK_1
    elif (current_location == FORK_1):
        return DOCK
    elif (current_location == CASTLE_INSIDE_1):
        return CASTLE_ENTRANCE
    elif (current_location == CAVE_INSIDE_1):
        return CAVE_ENTRANCE
    elif (current_location == VILLAGE_HOUSE_2):
        return VILLAGE_SQUARE
    elif current_location == DRAGON_LAIR:
        return CAVE_INSIDE_1
    else:
        return 0


def get_location_to_west():
    global refresh_location

    if (current_location == CAVE_ENTRANCE):
        return FORK_1
    elif (current_location == FORK_1):
        return BRIDGE
    elif (current_location == BRIDGE):
        return CASTLE_ENTRANCE
    elif (current_location == VILLAGE_SQUARE):
        return VILLAGE_HOUSE_1
    elif (current_location == VILLAGE_HOUSE_3):
        return VILLAGE_SQUARE
    else:
        return 0


def get_location_to_east():
    global refresh_location

    if (current_location == FORK_1):
        return CAVE_ENTRANCE
    elif (current_location == BRIDGE):
        return FORK_1
    elif (current_location == CASTLE_ENTRANCE):
        return BRIDGE
    elif (current_location == VILLAGE_HOUSE_1):
        return VILLAGE_SQUARE
    elif (current_location == VILLAGE_SQUARE):
        return VILLAGE_HOUSE_3
    else:
        return 0


def get_game_object(object_name):
    sought_object = None
    for current_object in game_objects:
        if (current_object.name.upper() == object_name):
            sought_object = current_object
            break
    return sought_object


def describe_current_visible_objects():
    object_count = 0
    object_list = ""

    for current_object in game_objects:
        if ((current_object.location == current_location) and (current_object.visible == True) and (
                current_object.carried == False)):
            object_list = object_list + ("," if object_count > 0 else "") + current_object.name
            object_count = object_count + 1

    print_to_description("You see: " + (object_list + "." if object_count > 0 else "nothing special."))


def describe_current_inventory():
    object_count = 0
    object_list = ""

    for current_object in game_objects:
        if current_object.carried:
            object_list = object_list + ("," if object_count > 0 else "") + current_object.name
            object_count = object_count + 1

    inventory = "You are carrying: " + (object_list if object_count > 0 else "nothing")

    inventory_widget.config(state="normal")
    inventory_widget.delete(1.0, END)
    inventory_widget.insert(1.0, inventory)
    inventory_widget.config(state="disabled")


def handle_special_condition():
    global end_of_game

    if (False):
        print_to_description("GAME OVER")
        end_of_game = True


def print_to_description(output, user_input=False):
    description_widget.config(state='normal')
    description_widget.insert(END, output)
    if (user_input):
        description_widget.tag_add("blue_text", CURRENT + " linestart", END + "-1c")
        description_widget.tag_configure("blue_text", foreground='blue')
    description_widget.insert(END, '\n')
    description_widget.config(state='disabled')
    description_widget.see(END)


def build_interface():
    global command_widget
    global image_label
    global description_widget
    global inventory_widget
    global north_button
    global south_button
    global east_button
    global west_button
    global root
    global map_button

    root = Tk()
    root.resizable(0, 0)
    root.configure(background="grey")

    style = ttk.Style()
    style.configure("BW.TLabel", foreground="black", background="white")

    image_label = ttk.Label(root)
    image_label.grid(row=0, column=0, columnspan=3, padx=2, pady=2)

    description_widget = Text(root, width=50, height=10, relief=GROOVE, wrap='word')
    description_widget.insert(1.0, "Welcome to my game\n\nGood Luck!. ")
    description_widget.config(state="disabled", background="light grey")
    description_widget.grid(row=1, column=0, columnspan=3, sticky=W, padx=2, pady=2)

    command_widget = ttk.Entry(root, width=25, style="BW.TLabel")
    command_widget.bind('<Return>', return_key_enter)
    command_widget.grid(row=2, column=0, padx=2, pady=2)
    command_widget.configure(background="light grey")

    button_frame = ttk.Frame(root)
    button_frame.config(height=150, width=150, relief=GROOVE)
    button_frame.grid(row=3, column=0, columnspan=1, padx=2, pady=2)

    north_button = ttk.Button(button_frame, text="N", width=5)
    north_button.grid(row=0, column=1, padx=2, pady=2)
    north_button.config(command=north_button_click)

    south_button = ttk.Button(button_frame, text="S", width=5)
    south_button.grid(row=2, column=1, padx=2, pady=2)
    south_button.config(command=south_button_click)

    east_button = ttk.Button(button_frame, text="E", width=5)
    east_button.grid(row=1, column=2, padx=2, pady=2)
    east_button.config(command=east_button_click)

    west_button = ttk.Button(button_frame, text="W", width=5)
    west_button.grid(row=1, column=0, padx=2, pady=2)
    west_button.config(command=west_button_click)

    inventory_widget = Text(root, width=30, height=8, relief=GROOVE, state=DISABLED)
    inventory_widget.grid(row=2, column=2, rowspan=2, padx=2, pady=2, sticky=W)
    inventory_widget.configure(background="light grey")

    map_button = ttk.Button(button_frame, text="Map", width=5)
    map_button.grid(row=1, column=1, padx=2, pady=1)
    map_button.config(command=preform_map_command)


def set_current_state():
    global refresh_location
    global refresh_objects_visible

    if (refresh_location):
        describe_current_location()
        set_current_image()

    if (refresh_location or refresh_objects_visible):
        describe_current_visible_objects()

    handle_special_condition()
    set_directions_to_move()

    if (end_of_game == False):
        describe_current_inventory()

    refresh_location = False
    refresh_objects_visible = False

    command_widget.config(state=("disabled" if end_of_game else "normal"))


def north_button_click():
    global map_clicked
    map_clicked = False

    print_to_description("N", True)
    perform_command("N", "")
    set_current_state()


def south_button_click():
    global map_clicked
    map_clicked = False

    print_to_description("S", True)
    perform_command("S", "")
    set_current_state()


def east_button_click():
    global map_clicked
    map_clicked = False

    print_to_description("E", True)
    perform_command("E", "")
    set_current_state()


def west_button_click():
    global map_clicked
    map_clicked = False

    print_to_description("W", True)
    perform_command("W", "")
    set_current_state()


def map_button_click():
    print_to_description("Map", True)
    perform_command("Map", "")
    set_current_state()


def return_key_enter(event):
    if (event.widget == command_widget):
        command_string = command_widget.get()
        print_to_description(command_string, True)

        command_widget.delete(0, END)
        words = command_string.split(' ', 1)
        verb = words[0]
        noun = (words[1] if (len(words) > 1) else "")
        perform_command(verb.upper(), noun.upper())

        set_current_state()


def set_directions_to_move():
    move_to_north = (get_location_to_north() > 0) and not end_of_game
    move_to_south = (get_location_to_south() > 0) and not end_of_game
    move_to_east = (get_location_to_east() > 0) and not end_of_game
    move_to_west = (get_location_to_west() > 0) and not end_of_game

    north_button.config(state=("normal" if move_to_north else "disabled"))
    south_button.config(state=("normal" if move_to_south else "disabled"))
    east_button.config(state=("normal" if move_to_east else "disabled"))
    west_button.config(state=("normal" if move_to_west else "disabled"))


def main():
    build_interface()
    set_current_state()
    root.mainloop()


main()
