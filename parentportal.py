from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

# File path of chrome driver
PATH = "C:\Program Files (x86)\chromedriver.exe"

# Website you want to go to
driver = webdriver.Chrome(PATH)

# Insert URL here
url = "URL"
driver.get(url)

# Logs in to the portal
portal_code = driver.find_element_by_name("portalcode")
portal_code.send_keys("insert portal code") # Enter your portal code
username = driver.find_element_by_name("username")
username.send_keys("username") # Enter your username
password = driver.find_element_by_name("password")
password.send_keys("password") # Enter your password
password.send_keys(Keys.RETURN)

#if averages:
# Wait until the specified element is found before proceeding
try:
    nav = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "nav"))
    )

    gradebook_link = driver.find_element_by_link_text("Gradebook")
    gradebook_link.click()

    # Input for which subject you want the program to calculate average in
    subject = input("Enter the subject you want to know the grade of: ")
    subject_link = driver.find_element_by_link_text(subject)
    subject_link.click()

    grades = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "grades"))
    )

    # Grades in each category of the gradebook
    grade = []

    # Weightage of each category
    percentages = []

    # Gets grades in each category from the portal and appends them all to a list
    pull_rights = driver.find_elements_by_class_name("pull-right")
    for pull_right in pull_rights:
        try:
            colon = pull_right.text.index(":")
        except:
            continue
        slice_object = slice(colon + 2, len(pull_right.text) - 1)
        grade.append(float(pull_right.text[slice_object]))

    # Gets weightages of each category from the portal and appends them all to a list
    finedetailwhts = driver.find_elements_by_class_name("finedetailwht")
    for finedetailwht in finedetailwhts:
        try:
            hyphen = finedetailwht.text.index("-")
            percent = finedetailwht.text.index("%")
        except:
            continue
        slice_object = slice(hyphen + 2, percent)
        percentages.append(float(finedetailwht.text[slice_object]))

    # Calculates your average by traversing percentages and grade list
    average = 0
    for i in range(len(percentages)):
        average += percentages[i] / 100 * grade[i]
    print("Average in " + subject + ": " + str(average))
except:
    driver.quit()
