import cozmo
import time
from cozmo.util import degrees, Pose
from CrimeInference import *

# Initialisation des variables globales
tap_counter = 0

def on_cube_tapped(event, **kwargs):
    global tap_counter
    if event.obj.cube_id == cozmo.objects.LightCube1Id:
        tap_counter = (tap_counter + event.tap_count) % 3
        print(f"Cube tap count: {tap_counter}")

detective = CrimeInference()

living_characters = ["Mustard", "Peacock", "Plum", "White"]

for character in living_characters:
    detective.add_clause(to_fol([f"{character} is alive"], 'grammars/person_alive.fcfg'))

def filter_out(elements, exclusion_list):
    return [e for e in elements if e not in exclusion_list]

def investigate_victim(robot):
    global tap_counter
    possible_victim = filter_out(detective.persons, living_characters)[0]
    robot.say_text(f"Is {possible_victim} the victim?").wait_for_completed()
    
    tap_counter = 0
    print("Waiting for a yes/no response...")
    time.sleep(3)

    if tap_counter == 1:
        detective.add_clause(to_fol([f"{possible_victim} is dead"], 'grammars/person_dead.fcfg'))
    tap_counter = 0

    robot.say_text("What is the name of this room?").wait_for_completed()
    room_name = input("Enter the room name:\n").strip().split()[-1]
    detective.add_clause(to_fol([f"{possible_victim} is in the {room_name}"], 'grammars/person_room.fcfg'))

    robot.say_text("How did they die?").wait_for_completed()
    robot.say_text(f"{detective.get_victim()} is riddled with bullets").wait_for_completed()
    detective.add_clause(to_fol([f"{detective.get_victim()} is riddled with bullets"], 'grammars/person_mark.fcfg'))

    robot.say_text("What was the time of death?").wait_for_completed()
    time_of_death = input("Enter the time of death (hours):\n").strip()
    detective.add_clause(to_fol([f"{possible_victim} died at {time_of_death}h"], 'grammars/person_dead_time.fcfg'))

    detective.add_clause(f"OneHourAfterCrime({int(time_of_death) + 1})")

def clue_one(robot):
    hour_after_crime = detective.get_crime_hour_plus_one()
    time_of_day = "this morning" if hour_after_crime < 12 else "this afternoon" if hour_after_crime < 18 else "this evening"
    robot.say_text("I see a knife in the kitchen").wait_for_completed()
    detective.add_clause(to_fol(["The knife is in the kitchen"], 'grammars/weapon_room.fcfg'))

    robot.say_text(f"Who was in the kitchen {time_of_day}?").wait_for_completed()
    person_name = input("Enter the person's name:\n").strip().split()[-1]
    detective.add_clause(to_fol([f"{person_name} was in the kitchen"], 'grammars/person_room.fcfg'))
    detective.add_clause(to_fol([f"{person_name} was in the kitchen at {hour_after_crime}h"], 'grammars/person_room_time.fcfg'))

def clue_two(robot):
    hour_after_crime = detective.get_crime_hour_plus_one()
    time_of_day = "this morning" if hour_after_crime < 12 else "this afternoon" if hour_after_crime < 18 else "this evening"
    robot.say_text("I see a rope in the garage").wait_for_completed()
    detective.add_clause(to_fol(["The rope is in the garage"], 'grammars/weapon_room.fcfg'))

    robot.say_text(f"Who was in the garage {time_of_day}?").wait_for_completed()
    person_name = input("Enter the person's name:\n").strip().split()[-1]
    detective.add_clause(to_fol([f"{person_name} was in the garage"], 'grammars/person_room.fcfg'))
    detective.add_clause(to_fol([f"{person_name} was in the garage at {hour_after_crime}h"], 'grammars/person_room_time.fcfg'))

def conclude_investigation():
    print("Crime Scene: ", detective.get_crime_room())
    print("Murder Weapon: ", detective.get_crime_weapon())
    print("Victim: ", detective.get_victim())
    print("Time of Death: ", detective.get_crime_hour())
    print("Culprit: ", detective.get_suspect())
    print("Innocent People: ", detective.get_innocent())

def cozmo_investigation(robot: cozmo.robot.Robot):
    robot.world.delete_all_custom_objects()
    robot.add_event_handler(cozmo.objects.EvtObjectTapped, on_cube_tapped)

    investigate_victim(robot)
    clue_one(robot)
    clue_two(robot)
    conclude_investigation()

# Uncomment below line to execute the program
# cozmo.run_program(cozmo_investigation)
