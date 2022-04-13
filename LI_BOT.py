import os
import time, random, csv, datetime, re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from docxtpl import DocxTemplate

class Apply_Bot:
    def __init__(self, driver):
        self.webdriver = driver
        self.ans_dict = self.answer_read()
        self.login_info = self.read_login()
        self.start_login()
        self.now = datetime.datetime.now()
        self.stringtime = self.now.strftime("%Y-%m")
        self.filepath = os.getcwd() + '\\jobs_list_' + self.stringtime + '.csv'
        self.oldpath = os.getcwd() + '\\jobs_list_2022-04-03-22-59.csv'
        self.output_fp = os.getcwd() + '\\jobs_list_output' + self.stringtime + '.csv'
        self.df_jobs = pd.DataFrame
        self.cv_path = ""
        self.cv_name = ""
        self.c_dir = ""
        self.r_dir = ""
        self.j_title = ""
        self.j_location = ""
        self.j_hiring_manager = ""
        self.j_company = ""
        self.j_link = ""
        self.j_description = ""
        self.j_number_applicants = ""
        self.search_url = ""
        self.job_list = []
        self.j_type = "Easy Apply"
        self.j_result = "No"
        self.list_place = 0

    ####################################################################################################################################################
    # SETUP FUNCTIONS
    # answer_read imports the saved csv of questions and answers as a dictionary
    # read_login imports the saved csv of the users username and password
    # start_login initiates the login to linkedin using the username and password
    # job_search searches for the desired job title at the desired location
    # create_csv creates a csv for outputting SCRAPED jobs
    # create_output_csv creates a csv for outputting APPLIED jobs

    ####################################################################################################################################################

    # function to import the stored answers csv file from the main directory
    def answer_read(self):
        with open("stored_answers.csv", 'r', encoding='utf-8', newline="") as f:
            reader = csv.reader(f)
            dict_from_csv = {rows[0]: rows[1] for rows in reader}
            return dict_from_csv

    # function to import the stored login information from the login csv in the main directory
    def read_login(self):
        with open("login.csv", 'r', encoding='utf-8', newline="") as f:
            reader = csv.reader(f)
            dict_from_csv = {rows[0]: rows[1] for rows in reader}
            return dict_from_csv

    # function to initiate logging-in to linkedin, using the stored login information from read_login
    def start_login(self):
        username = self.login_info.get("username")
        password = self.login_info.get("password")
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

    # function to start the job search... defaults to searching for Data Analyst & Remote but these can be changed
    def job_search(self, job_keyword="Data Analyst", loc="Remote"):
        # set the job title and location to search for..
        self.webdriver.get("https://www.linkedin.com/jobs/")
        title = input("Please type the title of the job you'd like to search for \n -->")
        location = input("Please enter where you'd like to search for jobs... \n -->")

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

    # function creates an appropriate csv to write to if none exists...
    def create_csv(self):
        # write the column names to the csv
        if os.path.isfile(self.filepath) == False:
            J_list = ['Title', 'Company', 'Location', 'Type', 'Link', 'Poster_Name', "Applied?", "Number_Applicants", "Description"]
            with open(self.filepath, 'w', encoding ='utf-8', newline = "") as f:
                writer = csv.writer(f)
                writer.writerow(J_list)

    # function creates a csv for the output of applied jobs.
    def create_output_csv(self):
        # write the column names to the csv
        if os.path.isfile(self.output_fp) == False:
            J_list = ['Title', 'Company', 'Location', 'Link', 'Poster_Name', "Applied?"]
            with open(self.output_fp, 'a', encoding='utf-8', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(J_list)

    ####################################################################################################################################################
    # SCRAPING FUNCTIONS

    # get_pages takes the users input to determine a number of pages of results to scrape or apply to..
    # the 'find_X' functions search the webpage for required pieces of information
    # get_job_list, update_list, and move_through list all operate on the list of jobs on the current page of search results
    # find_apply_button checks to see if the current job is applicable
    # click_next_page moves to the next page of search results
    # job_scraper uses all these functions to scrape X number of search results for jobs

    ####################################################################################################################################################
    # function takes the user's input for the number of pages to scrape...
    def get_pages(self):
        # validate that the user has actually inputted a valid integer, and once validated, return the int.
        while True:
            page_num = input("Please input an integer betweenn 1-25 for the number of pages you want to scrape and apply to: ")
            try:
                page_num = int(page_num)
                if page_num >= 1 and page_num <= 50:
                    return page_num
            except:
                print("Invalid input: you must input an integer between 1-25")
                continue

    # function finds the number of applicants from the job page...
    def find_j_number_applicants(self):
        el = self.webdriver.find_elements_by_class_name('jobs-unified-top-card__applicant-count')
        try:
            self.j_number_applicants = el[0].text.split(' ')[0]
        except:
            self.j_number_applicants = ""

    # function to find the hiring manager for a job
    def find_j_hiring_manager(self):
        el = self.webdriver.find_elements_by_class_name("jobs-poster__name")
        try:
            self.j_hiring_manager = el[0].text
        except:
            self.j_hiring_manager = "To Whom it May Concern"

    # function finds the full description from the job page...
    def find_j_description(self):
        el = self.webdriver.find_elements_by_class_name('jobs-description__content')
        try:
            self.j_description = el[0].text
        except:
            print("unable to find the description")
            self.j_description = ""

    # function that finds the job_title
    def find_j_title(self):
        try:
            self.j_title = self.job_list[self.list_place].find_element_by_class_name('job-card-list__title').text
            self.j_title = self.j_title.split('\n')[0]
            self.j_title = re.split(r'\-', self.j_title)[0]
        except:
            self.j_title = ""
            print("Find j_title failed!")

    # find the link to the job posting
    def find_j_link(self):
        try:
            self.j_link = self.job_list[self.list_place].find_element_by_class_name('job-card-list__title').get_attribute('href').split('?')[0]
        except:
            self.j_link = ""
            print("find_j_link failed!")

    # find the job's location
    def find_j_loc(self):
        try:
            self.j_location = self.job_list[self.list_place].find_element_by_class_name('job-card-container__metadata-item').text
        except:
            self.j_location = ""
            print("find_j_loc failed!")

    # find the job's company name
    def find_j_company(self):
        # find the comapny name
        try:
            self.j_company = self.job_list[self.list_place].find_element_by_class_name('job-card-container__company-name').text
        except:
            self.j_company = ""
            print("find j_company failed!")

    # function finds the list of jobs from the page and moves to the bottom then back to the top of the list to start loading the elements
    def get_job_list(self):
        try:
            # get the list
            self.job_list = self.webdriver.find_elements_by_class_name('jobs-search-results__list')[0].find_elements_by_class_name('jobs-search-results__list-item')
            bottom = len(self.job_list) - 1
            actions = ActionChains(self.webdriver)
            # move to the bottom
            actions.move_to_element(self.job_list[bottom]).perform()
            # wait
            time.sleep(1)
            # move back to the top
            actions.move_to_element(self.job_list[0]).perform()
        except:
            print("get_job_list failed")

    # function moves through the list to load all the elements, then saves the completed list
    def update_list(self):
        # scroll through the list
        try:
            for k in self.job_list:
                actions = ActionChains(self.webdriver)
                actions.move_to_element(k).perform()
            # reload the list
            self.job_list = self.webdriver.find_elements_by_class_name('jobs-search-results__list')[0].find_elements_by_class_name('jobs-search-results__list-item')
        except:
            print("update_list failed")

    # function moves to the next element in the list, and, if the element is unable to be found, reloads the page and then moves to the element...
    def move_through_list(self, i):
        # gets the next element in the list and clicks on it
        try:
            actions = ActionChains(self.webdriver)
            actions.move_to_element(self.job_list[i]).perform()
            actions.click(self.job_list[i]).perform()
            print("i moved to the element!")
        except:
            # if the program is unable to find the next element, reloads the webpage and continues
            print("[1] somethings wrong with the url!")
            self.webdriver.get(self.search_url)
            time.sleep(2)
            self.job_list = self.webdriver.find_elements_by_class_name('jobs-search-results__list')[0].find_elements_by_class_name('jobs-search-results__list-item')
            self.update_list()
            actions = ActionChains(self.webdriver)
            actions.move_to_element(self.job_list[i]).perform()
            actions.click(self.job_list[i]).perform()
            print("[2] Had to reset the list... ")

    # function looks for the 'apply' button and returns true/false based on if it is findable
    def find_apply_button(self):
        time.sleep(3)
        button_active = self.webdriver.find_elements_by_class_name('jobs-apply-button')
        if len(button_active) > 0:
            return True
        else:
            return False

    # function to scrape all the job information--uses the other 'find' functions
    def find_all_j_info(self):
        # fill up all the fields with the information from the job posting..
        self.find_j_title()
        self.find_j_company()
        self.find_j_loc()
        self.find_j_link()
        self.find_j_hiring_manager()
        self.find_j_number_applicants()
        self.find_j_description()

    # finds the next page button and clicks it...
    def click_next_page(self, i):
        # label for the next page button
        text = f"[aria-label= 'Page {i + 1}']"
        # load action chains
        actions = ActionChains(self.webdriver)
        try:
            time.sleep(3)
            # find the next page element, move to it, and click it
            elem = self.webdriver.find_element_by_css_selector(text)
            actions.move_to_element(elem).perform()
            elem.click()
        except:
            # if something goes wrong, try the previous page (this is a failsafe)
            print("i couldn't find the page I was looking for!")
            text = f"[aria-label= 'Page {i}']"
            elem = self.webdriver.find_element_by_css_selector(text)
            actions.move_to_element(elem).perform()
            elem.click()

    # write a new row to the csv...
    def write_csv_row(self):
        try:
            J_list = [self.j_title, self.j_company, self.j_location, "Easy Apply", self.j_link, self.j_hiring_manager, self.j_result, self.j_number_applicants, self.j_description]
            with open(self.filepath, 'a', encoding='utf-8', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(J_list)
        except:
            print("write_csv_row failed!")

    # function searches and scrapes all jobs in the given page range
    def job_scraper(self):
        # initiate the search and get the number of pages to scrape
        self.job_search()
        pages = self.get_pages()
        # create a csv to save the results
        self.create_csv()
        for k in range(1, pages + 1):
            # set the base url to return to if problems are encountered...
            self.search_url = self.webdriver.current_url
            # while loop in case something breaks
            switch = True
            while switch == True:
                # get the list of jobs
                self.get_job_list()
                # load the correct values (populates job list that will initiatlly have blanks
                self.update_list()
                # for the length of the list, iterate through each job and apply
                for i in range(0, len(self.job_list)):
                    # set list_place equal to i (used to find certain values)
                    self.list_place = i
                    self.move_through_list(i)
                    # if the apply button appears, scrape the values (ignores jobs that have already been applied to)
                    if self.find_apply_button() == True:
                        self.find_all_j_info()
                        self.write_csv_row()
                # if successful, exit the while loop
                switch = False
                print("I think i finished a page of jobs!")
            # move to the next page
            self.click_next_page(k)

    ####################################################################################################################################################
    # Application FUNCTIONS

    # scrape_and_apply applies to all jobs in X number of pages of search results
    # create_cv creates a new cover letter based on information scraped from the job page or inputted from a csv
    # job_apply_one applies to a single job and returns the results of the applciation
    # jobs_list applies to a list of jobs
    # apply_to_list is the higher level function to apply to list

    ####################################################################################################################################################

    # function to both scrape and apply to jobs at the same time
    def scrape_and_apply(self):
        # initializing functions...
        self.job_search()
        pages = self.get_pages()
        self.create_csv()
        for k in range(1, pages + 1):
            # set the base url to return to if problems are encountered...
            self.search_url = self.webdriver.current_url
            switch = True
            while switch == True:
                self.get_job_list()
                self.update_list()
                for i in range(0, len(self.job_list)):
                    print(i)
                    self.move_through_list(i)
                    try:
                        if self.find_apply_button() == True:
                            self.find_all_j_info()
                            # let's create a cv!
                            try:
                                self.create_cv()
                            except:
                                pass
                            try:
                                self.webdriver.find_elements_by_class_name('jobs-apply-button')[0].click()
                            except:
                                pass
                            try:
                                self.j_result = self.job_apply_one()
                            except:
                                try:
                                    self.jobs_apply_click()
                                    self.j_result = self.job_apply_one()
                                except:
                                    pass
                            self.write_csv_row()
                            time.sleep(5)
                            try:
                                self.webdriver.find_element_by_class_name('artdeco-button__icon').click()
                            except:
                                try:
                                    time.sleep(3)
                                    self.webdriver.find_element_by_class_name('artdeco-button__icon').click()
                                except:
                                    pass
                    except:
                        print("job not applicable!")
                switch = False
            print("I think i finished a page of jobs!")
            self.click_next_page(k)
            # wait 1-3 seconds
            time.sleep(random.uniform(2, 3))

    # create a customized cover letter
    def create_cv(self):
        # Open our master template
        temp_cv_path = os.getcwd() + "\\cover_letters\\"
        doc = DocxTemplate(temp_cv_path + "master_cover_letter.docx")
        today_date = datetime.datetime.today().strftime('%m/%d/%Y')
        my_name = "Matt Warden"
        second_last = "Samoa taught me how to build community and how to leverage my communication skills for the common good."
        content2 = {'intro_their_name': self.j_hiring_manager, 'company_name': self.j_company, 'my_name': my_name,'position_name': self.j_title, 'today_date': today_date,'second_last_paragraph_final': second_last}
        company_clean = re.sub(r'\W+', ' ', self.j_company)
        # Load them up
        doc.render(content2)
        # Save the file with personalized filename
        self.cv_name = 'Cover_letter_' + company_clean + '.docx'
        doc.save(temp_cv_path + self.cv_name)

    # apply to a single job...
    def job_apply_one(self):
        self.jobs_apply_click()
        time.sleep(3)
        success = self.apply_function()
        return success

    # function to apply to a list of jobs
    def jobs_list(self):
        self.create_output_csv()
        # read the csv of jobs from the scraping
        # for i in range(0, len(df_jobs)): #len(df_jobs)
        for i in range(0, len(self.df_jobs)):
            try:
                if (self.df_jobs["Applied?"][i] == "No" or self.df_jobs["Applied?"][i] == "NO"):
                    self.webdriver.get(self.df_jobs["Link"][i])
                    time.sleep(15)
                    if len(self.webdriver.find_elements_by_class_name('jobs-apply-button')) == 0:
                        print("Was not able to apply to the job at : ", self.df_jobs['Title'][i])
                        continue
                    else:
                        print("spot 0: clicked")
                        self.j_link = self.df_jobs["Link"][i]
                        self.j_title = self.df_jobs['Title'][i]
                        self.j_location = self.df_jobs['Location'][i]
                        self.j_hiring_manager = self.df_jobs['Poster_Name'][i]
                        self.j_company = self.df_jobs['Company'][i]
                        self.create_cv()
                        self.j_result = self.job_apply_one()
                        J_list = [self.j_title, self.j_company, self.j_location, self.j_link, self.j_hiring_manager, self.j_result]
                        with open(self.output_fp, 'a', encoding='utf-8', newline="") as f:
                            writer = csv.writer(f)
                            writer.writerow(J_list)
            except:
                print("failed somewhere along the way... ")
                time.sleep(random.uniform(1, 3))

    # takes a scraped list of jobs and applies to all of them...
    def apply_to_list(self):
        self.get_scraped_file()
        self.jobs_list()

    # examines the directory and allows the user to choose the list to apply to...
    def get_scraped_file(self):
        print("It looks like you're trying to apply to jobs from a scraped file. \n Make sure the file is in the same directory as this script")
        switch = True
        while switch:
            filename = input("type the name of the file.. it should be a .csv... \n -->")
            files = os.listdir()
            if filename in files:
                self.oldpath = os.getcwd() + "\\" + filename
                switch = False
                continue
            else:
                for i in range(0, len(files)):
                    print(f"File    {i}  : ", files[i])
                choose_list_files = input("I couldn't find a file with that name... would you like to select from the files I found? \n Yes or No? \n -->")
                if choose_list_files.lower() == "yes" or choose_list_files.lower() == "y":
                    choose_file = input("Input the number corresponding with the file you'd like to load.. if you input something incorrect I will pause: \n -->")
                    try:
                        choose_file = int(choose_file)
                        for i in range(0, len(files)):
                            if choose_file == i:
                                self.oldpath = os.getcwd() + "\\" + files[choose_file]
                                self.df_jobs = pd.read_csv(self.oldpath)
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

    # starts the application by clicking the apply button
    def jobs_apply_click(self):
        time.sleep(random.uniform(2, 3))
        try:
            self.webdriver.find_element_by_class_name('jobs-apply-button').click()
            return True
        except:
            return False

    # function to fill up a page of an application with appropriate answers
    def fill_up(self):
        # save element text for later searching
        file_upload_elements = (By.CSS_SELECTOR, "input[name='file']")
        # see if there's the option to remove a resume
        r_list = self.webdriver.find_elements_by_css_selector("[aria-label='Remove uploaded document']")
        # search for upload buttons
        input_buttons = self.webdriver.find_elements(file_upload_elements[0], file_upload_elements[1])
        # if there are upload buttons OR the option to remove a previously uploaded file, use upload_files to replace them with new ones
        if len(input_buttons) > 0 or len(r_list) > 0:
            self.upload_files()
        # list all the groupings
        sec_grp = self.webdriver.find_elements_by_class_name('jobs-easy-apply-form-section__grouping')
        # if there are groupings, proceed
        if len(sec_grp) > 0:
            # for each grouping, iterate through group...
            for grp_pl in sec_grp:
                print(grp_pl.text.split('\n')[0])
                # find all the apply elements in the group...
                elem_pls = grp_pl.find_elements_by_class_name('jobs-easy-apply-form-element')
                # for each element in the group, identify the type and try to answer/fill in
                for sing_elem in elem_pls:
                    self.det_q_type(sing_elem)

    # function to apply to an application
    def apply_function(self):
        switch = True
        timeout = time.time() + 40  # 40 seconds from now
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

    # finds the next page on the application
    def next_app_page(self):
        next_button = self.webdriver.find_elements_by_class_name("artdeco-button--primary")
        for i in next_button:
            if "next" in i.text.lower() or "review" in i.text.lower():
                try:
                    i.click()
                    return True
                except:
                    pass
            elif "submit" in i.text.lower():
                try:
                    i.click()
                    print("Submitting!")
                    time.sleep(5)
                    return False
                except:
                    pass
            else:
                try:
                    i.click()
                    return True
                except:
                    continue

    ####################################################################################################################################################
    # QUESTION AND ANSWER FINDING AND STORING
    # functions for using the question/answer dictionary
    # check_match looks in the dictionary for a matched question/answer, and returns the match if it's found.
    #   if there is no match found it asks the user for their input and pushes the new q/a pair to the dictionary via answer_add
    # answer_add pushes the new answer to the csv of stored questions and answers
    ####################################################################################################################################################

    # finds the question in the answer dict and returns the matching answer
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
    # functions for answering questions on the application
    ####################################################################################################################################################

    # function for radio buttons
    def radio_answer(self, element):
        # find the text from the element
        header = element.text.split('\n')[0].lower()
        # find the labels...
        options = element.find_elements_by_tag_name('label')
        radio_flex = element.find_elements_by_class_name('fb-radio-buttons')
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

    # function to select drop downs
    def select_dropdown(self, element, text):
        select = Select(element)
        select.select_by_visible_text(text)

    # function for dropdowns
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

    # function for single line text box questions
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

    # function for multiline text box questions
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

    # function for question type determination
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

    # function for checkboxes
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

    # funtion to fill in autofill text boxes
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

    # testing functionality to change answers if they're causing problems...
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