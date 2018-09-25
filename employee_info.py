# Searches through the string of employee text to find the relevant information
def info_search(target: str):

    # "Since" is how long the employee has been with AIBC for
    info = ["Phone", "Fax", "Email", "Since"]
    return_dict = {}
    info_num = [7, 5, 7, 6]

    # Loop through the list of basic criteria, the easiest to find
    for i in range(len(info)):
        if info[i] in target:
            ind = target.index(info[i])
            return_dict[info[i]] = target[ind + info_num[i]:
                                          target.find("\n", ind)].rstrip()
        else:
            return_dict[info[i]] = " "
    if "Home" in target and "Email" not in target and "Phone" not in target:
        return_dict["Email"] = target[target.index("Home") + 6:
                                      target.find("\n",target.index("Home"))]
    if "Direct" in target and "Phone" not in target:
        return_dict["Phone"] = target[target.index("Direct") + 8:
                                      target.find("\n", target.index("Direct"))]
    if "Cell" in target and "Phone" not in target:
        return_dict["Phone"] = target[target.index("Cell") + 6:
                                      target.find("\n", target.index("Cell"))]

    # Adjusting for typos from the website
    if return_dict["Email"][-1] == "c":
        return_dict["Email"] += "a"
    elif return_dict["Email"][-1] == "o":
        return_dict["Email"] += "m"

    return return_dict


# Navigates to the employee page, gathers the employee info, writes it to the
# excel sheet, and returns the updated row counter
def employee_info_update(row_counter: int, employee_list: dict, browser,
                         worksheet):

    for employee in employee_list:
        row_counter += 1
        link = browser.find_element_by_partial_link_text(employee)
        link.click()
        tables = browser.find_elements_by_tag_name("TABLE")
        target_table = tables[5].text
        employee_info1 = info_search(target_table)
        employee_info_list = [employee, employee_list[employee][0], employee_list[employee][1]]
        for key in employee_info1:
            employee_info_list.append(employee_info1[key])


        browser.back()
        for k in range(len(employee_info_list)):
            worksheet.write(row_counter, k + 1, employee_info_list[k])

    return row_counter