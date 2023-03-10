import os
import datetime
import codecs

# Event format: dd.mm.yyyy. - <event name>

event_file_name = 'events.txt'


def main():
    def main_menu():
        viewing = True
        while viewing:
            events = load_events()
            print("Events:")
            for event in events:
                print("{} - {}".format(event["date"].strftime("%d.%m.%Y."),
                                       event["name"]))

            option_chosen = False
            option = 0
            while not option_chosen:
                print("\nWhat do you wish to do?")
                print("1. Add events")
                print("2. Delete events")
                print("3. Quit")
                option = input()
                if option not in ["1", "2", "3"]:
                    print("\nPlease input a valid number\n")
                else:
                    option_chosen = True
            print("")

            if option == "1":
                add_events_prompt()
            elif option == "2":
                delete_events_prompt()
            elif option == "3":
                viewing = False

    def add_events_prompt():
        print("Add events in the following format: \"dd.mm.YYYY. - <event name>\"")
        print("Enter an empty line to go back")

        adding = True
        while adding:
            event_string = input()
            if event_string == "":
                adding = False
            else:
                add_event(event_string)

    def delete_events_prompt():
        deleting = True
        while deleting:

            events = load_events()
            event_index = 1
            for event in events:
                print("{}. {} - {}".format(event_index,
                                           event["date"].strftime("%d.%m.%Y."),
                                           event["name"]))
                event_index += 1
        
            print("\nEnter the index of the event which you wish to delete")
            print("Enter an empty line to go back")
            
            event_index_string = input()
            if event_index_string == "":
                deleting = False
            else:
                delete_event(event_index_string)
        
    main_menu()


def load_events():
    events = []
    if os.path.isfile(event_file_name):
        events_file = codecs.open(event_file_name, 'r', "utf-8")
        for line in events_file:
            event_string = line[:-1]
            name_string = event_string[event_string.find('-')+2:]
            date_string = event_string[:event_string.find('-')-1]
            date_list = date_string.split('.')
            events.append({
                "date" : datetime.datetime(int(date_list[2]),
                                           int(date_list[1]),
                                           int(date_list[0])),
                "name" : name_string
                })
        events_file.close()
    return events


def save_events(events):
    def event_date(event):
        return event["date"]
    events.sort(key=event_date)
    
    events_file = codecs.open(event_file_name, 'w', "utf-8")
    for event in events:
        events_file.write("{} - {}\n".format(event["date"].strftime("%d.%m.%Y."),
                                             event["name"]))
    events_file.close()


def add_event(event_string):
    separator_index = event_string.find('-')
    if separator_index == -1:
        print("Invalid input: no separator between date and name")
        return
    date_string = event_string[:separator_index-1]
    date_list = date_string.split('.')
    if len(date_list) != 4 or date_list[3] != "":
        print("Invalid input: invalid date format")
        return
    try:
        date = datetime.datetime(int(date_list[2]),
                                 int(date_list[1]),
                                 int(date_list[0]))
    except ValueError:
        print("Invalid input: invalid date")
        return

    if len(event_string) < separator_index + 3:
        print("Invalid input: event has no name")
        return

    name = event_string[separator_index+2:]

    event = {
        "date" : date,
        "name" : name
        }

    events = load_events()
    events.append(event)

    save_events(events)
    print("Event added")


def delete_event(event_index_string):
    try:
        event_index = int(event_index_string)
    except ValueError:
        print("\nInvalid index\n")
        return
    
    events = load_events()
    
    if event_index > len(events):
        print("\nInvalid index\n")
        return
        
    events.pop(event_index-1)
    save_events(events)
    print("\nEvent deleted\n")


if __name__ == '__main__':
    main()
