# Simple Reflex Agent - Vacuum Cleaner for 2 Rooms

def vacuum_agent(room, status):
    if status == "Dirty":
        print("Room", room, "is dirty -> Suck")
        return "Suck"
    else:
        print("Room", room, "is clean -> Move")
        return "Move"


# Initial state of rooms
rooms = {"A": "Dirty","B": "Dirty"}
cost=0

a=input("Enter starting room(A/B): ")
current_room = a

print("\nInitial Room Status:", rooms)
print("\nAgent starts in Room", current_room , '\n')

# Clean both rooms
while "Dirty" in rooms.values():

    action = vacuum_agent(current_room, rooms[current_room])

    if action == "Suck":
        rooms[current_room] = "Clean"
        cost+=1

    elif action == "Move":
        if current_room == "A":
            current_room = "B"
        else:
            current_room = "A"
        cost+=1

    print("Current Room:", current_room)
    print("Room Status:", rooms)
    print()

print("All rooms are clean!")
print("Cost=",cost)
