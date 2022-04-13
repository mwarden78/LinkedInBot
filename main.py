from selenium import webdriver
from LI_BOT import Apply_Bot

def start_task_type():
    # validate that the user has actually inputted a valid integer, and once validated, return the int.
    while True:
        num = input("Please input a number corresponding to what you'd like to do today: \n 1 for scraping jobs"
                         "\n 2 for applying to jobs \n 3 for testing the program on a single job: \n 4 for scraping AND applying   \n ____ ")
        try:
            num = int(num)
            if num == 1:
                return num
            elif num == 2:
                return num
            elif num == 3:
                return num
            elif num == 4:
                return num
        except:
            print("Invalid input: you must select between 1 & 2")
            continue
# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    path = "C:\Program Files (x86)\chromedriver.exe"
    process_type = start_task_type()
    driver = webdriver.Chrome(path)
    bot = Apply_Bot(driver)
    if process_type == 1:
        print("Let's find you some jobs!")
        print(bot.ans_dict)
        bot.job_scraper()
    elif process_type == 2:
        print("Let's take a list of jobs and apply to them!")
        bot.apply_to_list()
    elif process_type == 3:
        print("Initiating testing on a previously failed job... ")
        bot.test_job()
    elif process_type == 4:
        bot.scrape_and_apply()
