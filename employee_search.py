# Parses through the string of employees to find their names, titles, and
# locations
def employee_search(string: str):
    return_dict = {}
    location_and_job = []

    # Default location is Vancouver
    location = "VANCOUVER"

    # Information is separated by new lines, so as long as there are new line
    # characters then there is more info for the employee
    while string.count("\n") > 0:
        location_found = False
        ind = string.index("\n")
        string_tracker = string[:ind]

        # Location is the only part of the string with upper characters
        if string_tracker.isupper():
            location = string_tracker
            location_and_job.append(location)
            location_found = True

            # Cut out the part of the string that has already been parsed
            # through
            string = string[ind + 1:]

            # Find the next piece of information for the employee
            new_ind = string.find("\n")
            if new_ind == -1:
                string_tracker = string
            else:
                string_tracker = string[:new_ind]

        # Find the title for the employee
        if "Retired" in string_tracker:
            job = string_tracker[string_tracker.index("Retired"):]
            string_tracker = string_tracker[:string_tracker.index("Retired") - 1]
        elif "Architectural" in string_tracker:
            job = string_tracker[string_tracker.index("Architectural")]
            string_tracker = string_tracker[:string_tracker.index("Architectural") - 1]
        elif "Intern" in string_tracker:
            job = string_tracker[string_tracker.index("Intern"):]
            string_tracker = string_tracker[:string_tracker.index("Intern") - 1]
        elif "Architect" in string_tracker:
            job = string_tracker[string_tracker.index("Architect"):]
            string_tracker = string_tracker[:string_tracker.index("Architect") - 1]
        else:
            job = "Doesnt say"

        # Put the job and location into a list and then reverse it since they
        # are backwards
        location_and_job.append(job)
        location_and_job.reverse()

        # If there is only the job in the list, then the location of the
        # employee was not found, so go with the default location of
        # Vancouver
        if len(location_and_job) == 1:
            location_and_job.append(location)

        # Slice the location and job info list to stop aliasing
        return_dict[string_tracker] = location_and_job[:]
        location_and_job = []
        if location_found is True:
            ind = string.find("\n")
            if ind == -1:
                string = ""
                break
        string = string[ind + 1:]

    # At this point there are no more new line characters, so we are on the
    # last piece of information for the employee
    string_tracker = string
    if "Retired" in string_tracker:
        job = string_tracker[string_tracker.index("Retired"):]
        string_tracker = string_tracker[:string_tracker.index("Retired") - 1]
    elif "Architectural" in string_tracker:
        job = string_tracker[string_tracker.index("Architectural")]
        string_tracker = string_tracker[:string_tracker.index("Architectural") - 1]
    elif "Intern" in string_tracker:
        job = string_tracker[string_tracker.index("Intern"):]
        string_tracker = string_tracker[:string_tracker.index("Intern") - 1]
    elif "Architect" in string_tracker:
        job = string_tracker[string_tracker.index("Architect"):]
        string_tracker = string_tracker[:string_tracker.index("Architect") - 1]
    else:
        if string != "":
            job = "Doesnt say"
    if string != "":
        return_dict[string_tracker] = [job, location]

    return return_dict
