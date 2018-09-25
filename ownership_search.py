# Parses through the string information of the ownership employees
def ownership_search(string: str) -> dict:

    return_dict = {}

    if string.count("\n") == 0:
        print("No Owners to be found here!")
    while string.count("\n") > 0:
        location_found = False
        ind = string.index("\n")
        person = string[:ind]
        if person.isupper():
            location_found = True
            string = string[ind + 1:]
            new_ind = string.find("\n")
            if new_ind == -1:
                person = string
            else:
                person = string[:new_ind]
        if "Intern" in person:
            job = person[person.index("Intern"):]
            person = person[:person.index("Intern") - 1]
        elif "Architect" in person:
            job = person[person.index("Architect"):]
            person = person[:person.index("Architect") - 1]
        else:
            job = "Doesnt say"
        return_dict[person] = job
        if location_found is True:
            ind = string.find("\n")
            if ind == -1:
                break
        string = string[ind + 1:]

    return return_dict
