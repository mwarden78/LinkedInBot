import os
import time, random, csv, pdb, traceback, sys, datetime, re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from datetime import date
from itertools import product
from docxtpl import DocxTemplate


class Apply_Bot:
    def __init__(self, driver):
        self.webdriver = driver
        self.ans_dict = self.answer_read()
        self.start_login()
        self.now = datetime.datetime.now()
        self.stringtime = self.now.strftime("%Y-%m-%d-%H-%M")
        self.filepath = os.getcwd() + '\\jobs_list_' + self.stringtime + '.csv'
        self.oldpath = os.getcwd() + '\\jobs_list_2022-04-03-22-59.csv'
        self.output_fp = os.getcwd() + '\\jobs_list_output_' + self.stringtime + '.csv'
        self.df_jobs = pd.DataFrame
        self.cv_path = ""
        self.cv_name = ""
        self.c_dir = ""
        self.r_dir = ""
        self.j_title = ""
        self.j_location = ""
        self.j_hiring_manager = ""
        self.j_company = ""
        self.link = ""
        self.search_url = ""

    def answer_read(self):
        with open("stored_answers.csv", 'r', encoding='utf-8', newline="") as f:
            reader = csv.reader(f)
            dict_from_csv = {rows[0]: rows[1] for rows in reader}
            return dict_from_csv

    def start_login(self):
        username = input("Please type your username/email exactly as it appears! : ")
        password = input("Please type your password exactly as it appears! : ")
        # navigate to linked in
        try:
            self.webdriver.get("https://www.linkedin.com/login")

            # login -- send password and username
            self.webdriver.find_element(By.ID, "username").send_keys(username)
            self.webdriver.find_element(By.ID, "password").send_keys(password)
            # click the login button
            self.webdriver.find_element(By.CSS_SELECTOR, ".btn__primary--large").click()
        except:
            print("Login already completed or failed")

    def job_search(self, job_keyword="Data Analyst", loc="Remote"):
        # set the job title and location to search for..
        self.webdriver.get("https://www.linkedin.com/jobs/")
        title = job_keyword
        location = loc

        # clear the previous search terms from the keyword and location spots
        try:
            # keyword button -- clear previous inputs
            self.webdriver.find_element(By.XPATH, "/html/body/div[5]/header/div/div/div/div[2]/div[1]/div/div/input[1]").clear()
            # location button -- clear previous inputs
            self.webdriver.find_element(By.XPATH, "/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div/input[1]").clear()
        except:
            pass

        # enter the keywords and locations to search for...
        try:
            self.webdriver.find_element(By.XPATH, "/html/body/div[5]/header/div/div/div/div[2]/div[1]/div/div/input[1]").send_keys(title)
            self.webdriver.find_element(By.XPATH, "/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div/input[1]").send_keys(location)
            # click on the search button
            self.webdriver.find_element(By.XPATH, "/html/body/div[5]/header/div/div/div/div[2]/button[1]").click()
        except:
            print('search/inputs failed... ')
            pass

        # turn the radio button for easy apply on
        try:
            # maximize window so that you can see the easy apply button, wait, and then click the buttom
            self.webdriver.maximize_window()
            time.sleep(random.uniform(1, 3))
            self.webdriver.find_element(By.XPATH,"/html/body/div[5]/div[3]/div[3]/section/div/div/div/ul/li[8]/div/button").click()
        except:
            pass

    def create_csv(self):
        # write the column names to the csv
        J_list = ['Title', 'Company', 'Location', 'Type', 'Link', 'Poster_Name', "Applied?", "Number_Applicants", "Description"]
        with open(self.filepath, 'w', encoding ='utf-8', newline = "") as f:
            writer = csv.writer(f)
            writer.writerow(J_list)

    def get_pages(self):
        # validate that the user has actually inputted a valid integer, and once validated, return the int.
        while True:
            page_num = input("Please input an integer betweenn 1-25 for the number of pages you want to scrape and apply to: ")
            try:
                page_num = int(page_num)
                if page_num >= 1 and page_num <= 25:
                    return page_num
            except:
                print("Invalid input: you must input an integer between 1-25")
                continue

    def number_applicants(self):
        el = self.webdriver.find_elements_by_class_name('jobs-unified-top-card__applicant-count')
        try:
            return el[0].text.split(' ')[0]
        except:
            return ""

    def get_description(self):
        el = self.webdriver.find_elements_by_class_name('jobs-description__content')
        try:
            return el[0].text
        except:
            return ""

    def get_jobs(self):
        # try to move through the list of jobs..
        actions = ActionChains(self.webdriver)
        # scroll to bottom and back up...
        self.search_url = self.webdriver.current_url

        try:
            # get list
            job_list = self.webdriver.find_elements_by_class_name('jobs-search-results__list')[0].find_elements_by_class_name('jobs-search-results__list-item')
            # move to bottom of the list
            bottom = len(job_list) - 1
            actions.move_to_element(job_list[bottom]).perform()
            time.sleep(1)
            actions.move_to_element(job_list[0]).perform()
        except:
            pass

        # get the full list of jobs from the page...
        job_list = self.webdriver.find_elements_by_class_name('jobs-search-results__list')[0].find_elements_by_class_name('jobs-search-results__list-item')
        for i in job_list:
            actions = ActionChains(self.webdriver)
            actions.move_to_element(i).perform()

        containers = self.webdriver.find_elements_by_class_name("job-card-container")
        c = 0
        i = 0

        # loop through the list of jobs
        for job_tile in job_list:
            # wait
            time.sleep(1.5)
            # try to click the next container
            try:
                containers[i].click()
            except:
                pass
            # move down the list of containers
            i = i + 1
            time.sleep(1.5)

            # if there is an apply button, scrape the information..
            button_active = self.webdriver.find_elements_by_class_name('jobs-apply-button')

            if len(button_active) > 0:
                c = c + 1
                # set the variables to placeholders
                job_title, company, job_location, apply_method, link, name, num, description = "", "", "", "", "", "", "", ""

                # try to grab the job title // scroll to it...
                try:
                    actions = ActionChains(self.webdriver)
                    actions.move_to_element(job_tile).perform()
                    job_title = job_tile.find_element_by_class_name('job-card-list__title').text
                    link = job_tile.find_element_by_class_name('job-card-list__title').get_attribute('href').split('?')[0]

                except:
                    pass

                num = self.number_applicants()
                try:
                    name = self.webdriver.find_element_by_class_name('jobs-poster__name').text
                except:
                    pass
                # try to grab the company
                try:
                    company = job_tile.find_element_by_class_name('job-card-container__company-name').text
                except:
                    pass
                # try to grab the location
                try:
                    job_location = job_tile.find_element_by_class_name('job-card-container__metadata-item').text
                except:
                    pass

                # try to grab the apply method
                try:
                    apply_method = job_tile.find_element_by_class_name('job-card-container__apply-method').text
                except:
                    pass
                try:
                    description = self.get_description()
                except:
                    pass
                # create a list of the elements found and print them to a CSV file for later use..
                J_list = [job_title, company, job_location, apply_method, link, name, "No", num, description]
                # write to the CSV
                with open(self.filepath, 'a', encoding='utf-8', newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(J_list)
        print(f"New Jobs Found on the page: {c}")

    def job_scrape(self):
        # iterate over the first x pages of results...
        self.create_csv()
        x = self.get_pages()
        for i in range(1, x + 1):
            self.search_url = self.webdriver.current_url
            # run the job-scraping program
            self.get_jobs()
            # find the next page button

            text = f"[aria-label= 'Page {i + 1}']"
            try:
                # move to the next page--scroll down
                actions = ActionChains(self.webdriver)
                elem = self.webdriver.find_element_by_css_selector(text)
                actions.move_to_element(elem).perform()
            except:
                print("Something wrong with the scraping url... might have navigated to a different page!")
                self.webdriver.get(self.search_url)
                x = x - 1
                continue
            # and click the next button
            try:
                elem.click()
            except:
                self.webdriver.find_element_by_css_selector(text).click()

            # wait 1-3 seconds
            time.sleep(random.uniform(2, 3))


    def apply_to_list(self):
        self.get_scraped_file()
        self.df_jobs = pd.read_csv(self.oldpath)
        self.jobs_list()
        print(self.df_jobs)

    def get_scraped_file(self):
        print("It looks like you're trying to apply to jobs from a scraped file. \n Make sure the file is in the same directory as this script")
        switch = True
        while switch:
            filename = input("type the name of the file.. it should be a .csv...")
            files = os.listdir()
            if filename in files:
                self.oldpath = os.getcwd() + "\\" + filename
                switch = False
                continue
            else:
                for i in range(0, len(files)):
                    print(f"File    {i}  : ", files[i])
                choose_list_files = input("I couldn't find a file with that name... would you like to select from the files I found? \n Yes or No?")
                if choose_list_files.lower() == "yes" or choose_list_files.lower() == "y":
                    choose_file = input("Input the number corresponding with the file you'd like to load.. if you input something incorrect I will pause:")
                    try:
                        choose_file = int(choose_file)
                        for i in range(0, len(files)):
                            if choose_file == i:
                                self.oldpath = os.getcwd() + "\\" + files[choose_file]
                            switch = False
                            continue
                    except:
                        print("i'm sorry, I didn't understand that input...")
                        switch = False
                        continue
                else:
                    print("hmm let's take a break then..")
                    switch = False
                    continue

####################################################################################################################################################
# NEXT FUNCTIONS
# jobs_apply_click() starts the application by clicking the easy apply button
# next_app_page() clicks the next button and returns False if completed to break a later loop

####################################################################################################################################################
# functions to progress the program through the application pages..
# jobs_apply_click clicks the 'apply' button when found on the page...
# apply button will not appear if the position is closed or has been already applied to
# returns a boolean telling the program to continue or not..
    def jobs_apply_click(self):
        time.sleep(random.uniform(2, 3))
        try:
            self.webdriver.find_element_by_class_name('jobs-apply-button').click()
            return True
        except:
            try:
                self.webdriver.find_element_by_class_name('jobs-apply-button').click()
                return True
            except:
                return False

    # next_app_page tries to progress the application once started
    # returns True when the application is finished...
    def next_app_page(self):
        next_button = self.webdriver.find_elements_by_class_name("artdeco-button--primary")
        for i in next_button:
            if i.text == "Next" or i.text == "Review":
                try:
                    i.click()
                    return True
                except:
                    continue
            if "submit" in i.text.lower():
                try:
                    i.click()
                    print("Submitting!")
                    time.sleep(5)
                    return False
                except:
                    continue

    # function to see if there is an answer, and if not, prompt the user & save the response
    def check_match(self, question):
        question = question.lower()
        match = self.ans_dict.get(question)
        if match:
            return match
        else:
            answer = input(question + " : ")
            self.ans_dict[question] = answer
            self.answer_add(question, answer)
            return answer

    # function to push the new response to csv
    def answer_add(self, question, answer):
        with open("stored_answers.csv", 'a', encoding='utf-8', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([question, answer])

    ####################################################################################################################################################
    # Radio Button answer
    # function takes an element that was previously flagged as a radio, finds the text, and searches for a stored answer
    # if no stored answer it prompts the user for one
    # input -- singular webelement
    # web element is searched for all radios inside, and then radios are checked for a match

    # Functions dealing with radio buttons

    ######### TESTING ON: https://www.linkedin.com/jobs/view/2958160500/

    # Functions dealing with radio buttons

    def radio_answer(self, element):
        # find the text from the element
        header = element.text.split('\n')[0].lower()
        # find the labels...
        options = element.find_elements_by_tag_name('label')
        match = self.ans_dict.get(header)
        if match:
            for i in options:
                try:
                    if match == i.text:
                        i.click()
                except:
                    continue
        else:
            ans = self.check_match(header)
            for i in options:
                try:
                    if ans == i.text:
                        i.click()
                except:
                    pass

    ####################################################################################################################################################
    # Drop Down answer

    def select_dropdown(self, element, text):
        select = Select(element)
        select.select_by_visible_text(text)

    def find_drop(self, element):
        drop = element.find_element_by_class_name('fb-dropdown__select')
        question_text = element.text.split("\n")[0].lower()
        try:
            match = self.ans_dict.get(question_text).title()
            self.select_dropdown(drop, match)
        except:
            try:
                ans = self.check_match(question_text)
                self.select_dropdown(drop, ans)
            except:
                print("DD failed!")
                pass

    def text_answer(self, element):
        txt_field = element.find_element_by_class_name('fb-single-line-text__input')
        question_text = element.text.split("\n")[0].lower()
        print(question_text)
        match = self.ans_dict.get(question_text)
        if match:
            txt_field.clear()
            txt_field.send_keys(match)
        else:
            txt_field.clear()
            new_ans = self.check_match(question_text)
            txt_field.send_keys(new_ans)

    def multi_text_answer(self, element):
        actions = ActionChains(self.webdriver)
        txt_field = element.find_element_by_class_name('fb-multi-line-text')
        txt_field.click()
        question_text = element.text.split("\n")[0].lower()
        print(question_text)
        match = self.ans_dict.get(question_text)
        # clear out old text answers...
        actions1 = ActionChains(self.webdriver)
        actions1.key_down(Keys.CONTROL).perform()
        actions1.send_keys("a").perform()
        actions1.key_up(Keys.CONTROL).perform()
        actions1.key_down(Keys.DELETE).perform()
        if "message" in question_text:
            text = f"I'm applying to the {self.j_title} position because I'm interested in the work you're doing at {self.j_company}. Thanks for looking over my application! I look forward to speaking with you regarding this role."
            actions.send_keys(text)
            actions.perform()
        elif match:
            actions.send_keys(match)
            actions.perform()
        else:
            new_ans = check_match(question_text)
            actions.send_keys(new_ans)
            actions.perform()


    def det_q_type(self, sing_elem):
        # if there are radios...
        if len(sing_elem.find_elements_by_class_name('fb-radio')) > 0:
            print("rad found")
            try:
                self.radio_answer(sing_elem)
            except:
                pass
        # if there are single text inputs
        elif len(sing_elem.find_elements_by_class_name('fb-single-line-text__input')) > 0:
            print("text input found")
            try:
                self.text_answer(sing_elem)
            except:
                pass
        # if there are drop down inputs
        elif len(sing_elem.find_elements_by_class_name('fb-dropdown__select')) > 0:
            print("DD input found")
            try:
                self.find_drop(sing_elem)
            except:
                pass
        elif len(sing_elem.find_elements_by_class_name('artdeco-typeahead__input')):
            print("City Input!")
            try:
                self.autofill_handler(sing_elem)
            except:
                pass

        elif len(sing_elem.find_elements_by_class_name('fb-checkboxes')) > 0:
            print("checkbox found!!")
            try:
                self.checkbox_handler(sing_elem)
                print("NO FAIL")
            except:
                print("fail")
                pass
        elif len(sing_elem.find_elements_by_class_name('fb-multi-line-text')) > 0:
            print("Multi-Line Answer...")
            try:
                self.multi_text_answer(sing_elem)
                print("Answered ML Text")
            except:
                print("something failed with ML Text")
                pass
        elif len(sing_elem.find_elements_by_class_name('fb-multi-line-text')) > 0:
            print("Multi-Line Answer...")
            try:
                self.multi_text_answer(sing_elem)
                print("Answered ML Text")
            except:
                print("something failed with ML Text")
                pass
        else:
            print("UNKNOWN ELEMENT DETECTED")
            pass

    def checkbox_handler(self, element):
        q_text = element.text.split('\n')[0].lower()
        print(q_text)
        checkboxes = element.find_elements_by_tag_name('label')
        if "privacy" in q_text.lower():
            for i in checkboxes:
                print(i.text)
                if "i agree" in i.text.lower() or "yes" in i.text.lower() or 'i understand' in i.text.lower():
                    i.click()
                else:
                    pass
        elif "confirm" in q_text.lower() or "certify" in q_text.lower():
            for i in checkboxes:
                if "i agree" in i.text.lower() or "yes" in i.text.lower() or "i understand" in i.text.lower() or "confirm" in i.text.lower():
                    i.click()
                else:
                    pass
        else:
            match = self.check_match(q_text)
            if match:
                for i in checkboxes:
                    if match in i.text:
                        i.click()
                    else:
                        pass

    def autofill_handler(self, element):
        q_text = element.text.split('\n')[0].lower()
        print(q_text)
        # will default to answering the location, as this is the most common question..
        if "city" in q_text:
            try:
                # will find the input box, clear it, and input the default city
                elem_2 = element.find_element_by_class_name('artdeco-typeahead__input')
                elem_2.clear()
                loc = self.ans_dict.get('city')
                elem_2.send_keys(loc)
                time.sleep(1)
            except:
                pass
            try:
                self.webdriver.find_element_by_class_name('artdeco-typeahead__result').click()
            except:
                pass
        else:
            try:
                elem_2 = element.find_element_by_class_name('artdeco-typeahead__input')
                elem_2.clear()
                ans = self.check_match(q_text)
                elem_2.send_keys(ans)
                time.sleep(1)
                self.webdriver.find_element_by_class_name('artdeco-typeahead__result').click()
            except:
                pass

    # function to upload files based on the job title--can select different resumes and cover letters based on input
    def file_choice(self):
        # tries to find the most common job titles applying to and use the relevant resume
        resume_folder = os.getcwd() + "\\resumes"
        list_subfolders = os.listdir(resume_folder)
        if self.j_title in list_subfolders:
            resume_dir = resume_folder + "\\" + self.j_title
            list_resume = os.listdir(resume_dir)
            self.r_dir = resume_dir + "\\" + list_resume[0]
        else:
            resume_dir = resume_folder + "\\" + "Default"
            list_resume = os.listdir(resume_dir)
            self.r_dir = resume_dir + "\\" + list_resume[0]
        self.c_dir = os.getcwd() + "\\cover_letters\\" + self.cv_name
        print(self.r_dir, self.c_dir)
    # function to actually upload the files if input buttons are detected..
    def upload_files(self):
        try:
            # remove previously-attached files..
            r_list = self.webdriver.find_elements_by_css_selector("[aria-label='Remove uploaded document']")
            for i in r_list:
                i.click()
        except:
            pass

        file_upload_elements = (By.CSS_SELECTOR, "input[name='file']")
        input_buttons = self.webdriver.find_elements(file_upload_elements[0], file_upload_elements[1])
        if len(input_buttons) > 0:
            # tries to find the most common job titles applying to and use the relevant resume
            self.file_choice()

            try:
                file_upload_elements = (By.CSS_SELECTOR, "input[name='file']")
                input_buttons = self.webdriver.find_elements(file_upload_elements[0], file_upload_elements[1])
                for upload_button in input_buttons:
                    upload_type = upload_button.find_element(By.XPATH, "..").find_element(By.XPATH,"preceding-sibling::*")
                    if 'resume' in upload_type.text.lower():
                        print("Resume detected!")
                        upload_button.send_keys(self.r_dir)
                    elif 'cover' in upload_type.text.lower():
                        print("CL detected!")
                        upload_button.send_keys(self.c_dir)
                    elif "additional" in upload_type.text.lower():
                        print("Additional--Will use for CL")
                        upload_button.send_keys(self.c_dir)
            except:
                pass
        else:
            pass

    def fill_up(self):
        file_upload_elements = (By.CSS_SELECTOR, "input[name='file']")
        r_list = self.webdriver.find_elements_by_css_selector("[aria-label='Remove uploaded document']")
        input_buttons = self.webdriver.find_elements(file_upload_elements[0], file_upload_elements[1])
        if len(input_buttons) > 0 or len(r_list) > 0:
            self.upload_files()
        # list all the groupings
        sec_grp = self.webdriver.find_elements_by_class_name('jobs-easy-apply-form-section__grouping')
        # if there are groupings, proceed
        if len(sec_grp) > 0:
            # for each grouping, iterate through group...
            for grp_pl in sec_grp:
                try:
                    print(grp_pl.text.split('\n')[0])
                    # find all the apply elements in the group...
                    elem_pls = grp_pl.find_elements_by_class_name('jobs-easy-apply-form-element')
                    # for each element in the group, identify the type and try to answer/fill in
                    for sing_elem in elem_pls:
                        self.det_q_type(sing_elem)
                except:
                    continue

    def apply_function(self):
        switch = True
        timeout = time.time() + 20  # 5 minutes from now
        while switch:
            print("LOOPING", timeout)
            if time.time() > timeout:
                switch = False
                return "Failure"
            try:
                self.fill_up()
            except:
                pass
            try:
                switch = self.next_app_page()
            except:
                continue
        return "Success"

    def job_apply_one(self):
        self.jobs_apply_click()
        time.sleep(3)
        success = self.apply_function()
        return success

    def cv_function(self):
        for i in range(0, len(self.df_jobs)):
            print(self.df_jobs["Company"][i])
            self.link = self.df_jobs["Link"][i]
            self.j_title = self.df_jobs['Title'][i]
            self.j_location = self.df_jobs['Location'][i]
            self.j_hiring_manager = self.df_jobs['Poster_Name'][i]
            if type(self.j_hiring_manager) == float:
                self.j_hiring_manager = "To Whom it May Concern"
            self.j_company = self.df_jobs['Company'][i]
            print(self.j_title, self.j_location, self.j_hiring_manager, self.j_company)
            print('spot 1: saved data')
            self.create_cv()
            print(self.cv_name)
            print(os.getcwd())
            print('spot 2: made new cv')

    #################################
    # CREATE A CV
    # PASS IN: j_company, j_title, j_hiring_manager
    #################################


    ##########################################################################################################################################
    # EDIT THESE FIELDS SO THAT THEY FIT YOUR INFORMATION!!!
    def create_cv(self, switch = 0):
        # Open our master template
        temp_cv_path = os.getcwd() + "\\cover_letters\\"
        doc = DocxTemplate(temp_cv_path + "master_cover_letter.docx")
        today_date = datetime.datetime.today().strftime('%m/%d/%Y')
        print("opened template!")
        my_name = "MY_NAME_HERE_EDIT"
        content2 = {'intro_their_name': self.j_hiring_manager, 'company_name': self.j_company, 'my_name': my_name,'position_name': self.j_title, 'today_date': today_date}
        company_clean = re.sub(r'\W+', ' ', self.j_company)
        # Load them up
        doc.render(content2)
        # Save the file with personalized filename
        self.cv_name = 'Cover_letter_' + company_clean + '.docx'
        doc.save(temp_cv_path + self.cv_name)
        print('finished_cv')

    def create_output_csv(self):
        # write the column names to the csv
        J_list = ['Title', 'Company', 'Location', 'Link', 'Poster_Name', "Applied?"]
        with open(self.output_fp, 'w', encoding='utf-8', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(J_list)

    def test_job(self):
        job_url = input("Give me the job URL for a job that was previously failed!")
        self.webdriver.get(job_url)
        time.sleep(2)
        self.link = job_url
        self.j_title = "Just a test!"
        self.j_location = "United States"
        self.j_hiring_manager = "To Whom it may concern"
        self.j_company = "Just a test!"
        self.create_cv()
        self.jobs_apply_click()
        switch = "Y"
        while switch == "Y":
            switch = input("Type Y to keep going... any other input will stop the progress..").upper()
            self.fill_up()
            investigate = input("Type Y to examine the elements on the page...")
            if investigate.lower() == "y":
                sections = self.webdriver.find_elements_by_class_name("jobs-easy-apply-form-section__grouping")
                for i in range(0, len(sections)):
                    print("I changed something!")
                    print(sections[i].text.split('\n')[0], " ", i)
                print("Can you see if one of these sections was answered incorrectly? if so, input the number... ")
                try:
                    num = int(input(" type number here... "))
                    for i in range(0, len(sections)):
                        if num == i:
                            print(sections[i].text.split('\n')[0])
                            wrong = input("is that the question I'm answering incorrectly? Y or N")
                            if wrong.lower() == "y":
                                elem = sections[i].text.split('\n')[0].lower()
                                del self.ans_dict[elem]
                                new_answer = input("Please Input the correct answer exactly as you see it on linkedIn... ")
                                self.ans_dict[elem] = new_answer
                                with open("stored_answers.csv", 'w', encoding='utf-8', newline="") as f:
                                    writer = csv.writer(f)
                                    for key, value in self.ans_dict.items():
                                        writer.writerow([key, value])
                                print("I've replaced the old answer with a new one!")
                                self.ans_dict = self.answer_read()
                except:
                    pass
            self.next_app_page()


    def jobs_list(self):
        self.create_output_csv()
        # read the csv of jobs from the scraping
        # for i in range(0, len(df_jobs)): #len(df_jobs)
        for i in range(0, len(self.df_jobs)):
            ### TESTING ###
            if 1 == 2:
                print(self.df_jobs['Title'][i])
            else:
                try:
                    if (self.df_jobs["Applied?"][i] == "No" or self.df_jobs["Applied?"][i] == "NO"):
                        self.webdriver.get(self.df_jobs["Link"][i])
                        time.sleep(5)
                        if len(self.webdriver.find_elements_by_class_name('jobs-apply-button')) == 0:
                            print("Was not able to apply to the job at : ", self.df_jobs['Title'][i])
                            continue
                        else:
                            self.jobs_apply_click()
                            print("spot 0: clicked")
                            self.link = self.df_jobs["Link"][i]
                            self.j_title = self.df_jobs['Title'][i]
                            self.j_location = self.df_jobs['Location'][i]
                            self.j_hiring_manager = self.df_jobs['Poster_Name'][i]
                            if type(self.j_hiring_manager) == float:
                                self.j_hiring_manager = "To Whom it May Concern"
                            self.j_company = self.df_jobs['Company'][i]
                            print(self.j_title, self.j_location, self.j_hiring_manager, self.j_company)
                            print('spot 1: saved data')
                            self.create_cv()
                            print(self.j_title, self.j_location, self.j_hiring_manager, self.j_company, self.cv_name)
                            print('spot 2: made new cv')
                            success = self.job_apply_one()
                            print('spot 3: applied//tried to apply')
                            if success == "Success":
                                print("flipped the applied to a yes")
                            J_list = [self.j_title, self.j_company, self.j_location, self.link, self.j_hiring_manager, success]
                            print("spot 4: stored values as a list")
                            with open(self.output_fp, 'a', encoding='utf-8', newline="") as f:
                                writer = csv.writer(f)
                                writer.writerow(J_list)
                            print('spot 5: wrote to output csv')

                except:
                    print("failed somewhere along the way... ")
                    time.sleep(random.uniform(1, 3))
