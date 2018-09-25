from selenium import webdriver
from selenium.webdriver.support.ui import Select
from employee_info import *
from employee_search import *
from ownership_search import *
import xlsxwriter

# A webscraper created to search through different locations in BC, Canada,
# of an employee public database AIBC. It finds relevant information for the
# employees, where available, and enters them into an excel sheet for use with
# Resolution Reprographics ltd.


# Setting up the webdriver to be used for webscraping
browser = webdriver.Chrome("C://Users/ethan/Documents/driver/chromedriver.exe")

# The basic website URL to be scraped
browser.get("https://aibc.memberpro.net/main/body.cfm?menu=directory&submenu="
            "directoryBusiness&page_id=3045")

# Create a list of all the locations which will need to be searched through
cities = ["richmond", "burnaby", "Maple ridge", "vancouver", "Surrey",
          "abbotsford", "chilliwack", "langley", "coquitlam",
          "new westminster", "port coquitlam", "langford", "victoria"]

# Navigating through the correct fields of the website
search = browser.find_element_by_name("searchField")
select = Select(search)
select.select_by_value("city_nm")
Input = browser.find_element_by_name("search_value")

# Setting up the workbook and worksheet in excel to be written to
workbook = xlsxwriter.Workbook("test.xlsx")
worksheet = workbook.add_worksheet("Sheet2")
bold = workbook.add_format({"bold": True})
header = ["Company name", "Member", "Position", "Location", "Phone", "Fax",
          "Email", "Date started"]

# Writing the header into the excel sheet for the entire sheet
for h in range(len(header)):
    worksheet.write_rich_string(0, h, bold, header[h])

# Keep track of the row in excel we're writing to
row_counter = 1

for city in cities:

    Input.send_keys(city)
    button = browser.find_element_by_class_name("BUTTON_LARGE")
    button.submit()

    # The first page we search through has its table of companies begin in a
    # slightly different position which is why this is necessary
    first_page = True

    # Begin scraping through the website
    try:
        # 100 is used because the number of pages varies, and the program will
        # simply raise an exception once it reaches the end
        for n in range(100):

            # Navigating to each website on the search page
            test = browser.find_elements_by_tag_name("A")
            for i in range(0, 10):
                if first_page is True:
                    test[i+18].click()
                else:
                    test[i+20].click()

                # Now that we're in the company information on the website, we
                # need to keep track of the separate pieces of information
                company_name = browser.find_element_by_tag_name("H1").text
                company_header = [company_name, "Ownership", " ", " ", " ", " ", " ", " "]
                for column in range(len(company_header)):
                    worksheet.write_rich_string(row_counter, column, bold, company_header[column])

                # Find the section of the page that has information of the
                # owners of the company and keep track of where it is
                tables = browser.find_elements_by_tag_name("TABLE")
                for i in range(6, len(tables)):
                    if "Total Staff & Owners" in tables[i].text:
                        table_index = i
                        break
                string = tables[table_index].text

                # Search through the text of the owners for relevant
                # information, if any exists
                ownership_list = ownership_search(string)

                # Write the ownership information to the excel sheet
                for owner in ownership_list:
                    row_counter += 1
                    ownership_print = [" ", owner, ownership_list[owner], " ", " ", " ", " ", " "]
                    for z in range(len(ownership_print)):
                        worksheet.write(row_counter, z, ownership_print[z])

                # Make a break in the company info to separate for the
                # members & associates
                row_counter += 1
                header2 = [" ", "Members & Associates", " ", " ", " ", " ", " ", " "]
                for w in range(len(header2)):
                    worksheet.write_rich_string(row_counter, w, bold, header2[w])

                # Since members' info is just after ownerships' info, can use
                # the same index
                string = tables[table_index + 1].text

                # Search through employees for relevant information
                employee_list = employee_search(string)

                # Writes the employee info to the excel sheets and returns the
                # updated row counter
                row_counter = employee_info_update(row_counter, employee_list,
                                                   browser, worksheet)

                # Moves the row counter down in the excel sheet to make the
                # sheet more readable
                for q in range(5):
                    row_counter += 1
                    for p in range(8):
                        worksheet.write(row_counter, p, " ")
                browser.back()

            # Go to the next page
            next_page = browser.find_element_by_partial_link_text("Next Page")
            next_page.click()

    # When this exception is raised, there will be no next page and the program
    # will have reached its end
    except:
        raise IndexError("Done searching through the site!")







