# LinkedInBot
this bot will apply to jobs for you on linkedin
READ ME


####################################################################################################################################
# GETTING STARTED
####################################################################################################################################

Unpack the zipfile to a directory of your choice.

## COVER LETTERS
1) Navigate to the cover_letters folder and edit the custom cover letter template. The fields in {{brackets}} will be replaced by the program
	a) Write the cover letter and choose your bracketed fields... by default the template will put in:
		i) 	date
		ii) 	your name
		iii)	job title
		iv)	company name
		v)	hiring manager (if found, otherwise will default to 'To Whom it May Concern'
	b) make sure your new cover letter is saved as 'master_cover_letter.docx' in the covver_letters folder
## RESUMES
2) Navigate to the resumes folder
	a) the program is structured so that you can create different resumes for different job titles--see how there's different folders?
	b) if you'd like to use different resumes based on the job title you're applying to, put different resumes in subfolders 
		i) 	i.e. if you're applying to jobs as a Chef, create a subfolder titled 'Chef' and put a resume in it
		ii)	if the program is unable to match the job title to a resume subfolder, it will default to choosing the resume
			that is in the 'Default' subfolder. 
		iii)	if you'd like to only use one resume, just delete the subfolders and put your resume in the 'Default' folder
		iv)	you must have ONE resume per subfolder--otherwise the program will get confused

## Setting up the the script


1) open linkedinbot.py and check that you have all the necessary packages installed.
	if you do not have a package, use 	pip install package_name  	to install it

2) open main.py in a text editor
	on line 25, the program sets the 'path' variable = 'C:\Program Files (x86)\chromedriver.exe'
	if that's where your chromedriver is installed, great!
	if you do not have your chromedriver installed there, you'll have to install it 
		and then change the path variable to match the install location
		webdriver can be found here.. https://chromedriver.chromium.org/downloads

3) once your path variable is set correctly, you should be good to run the program!

####################################################################################################################################
# RUNNING THE SCRIPT
####################################################################################################################################

1) open main.py in a python environment and run it (pycharm or virtual studio should work)

2) the script will start and load up your webdriver

3) the script will then present you with three options
	1) scraping jobs	-- this will navigate to linkedin and scrape all jobs with a desired criteria to a csv
	2) applying to jobs	-- this will load a previously-scraped csv and try to apply to all jobs on it	
	3) 'testing'		-- this can be used to see why a job failed--ignore this for now

A) SCRAPING JOBS
	1) TITLE: the bot will ask what job title you'd like to search for 
	2) LOCATION: and where you'd like to search in
		note that 'Remote' will search for remote jobs
	3) the bot will then search for your criteria on linkedin and maximize the browser window, and then check the 'easy apply' button
	4) the bot will next ask you how many pages of search results you'd like to scrape
	5) the bot will now scrape results from the search pages, and output them to a csv with the time and date of the job

B) Applying to jobs
	once you have a scraped jobs file, you can use the bot to iterate over it and apply to the jobs listed
	1) the bot will ask you for the filename you'd like to use
		a) if you can't remember the filename, the bot will list all available files
		b) select the number of the file to use
	2) the bot will now progress through the list of jobs and try applying to them
	3) the bot uses the 'stored_answers.csv' file to remember your previous answers
		a) if the bot encounters a new question, it will ask you to answer it.
			i) the bot will then save your answer so that it can answer the question successfully the next time
	4) the bot has about a 50/60% success rate when applying to jobs
	5) the bot will output a list of the jobs as jobs_list_output_ + time

C) Testing failed jobs

## THIS FUNCTIONALITY IS SOMEWHAT UNSTABLE--BEST USED WITH A FULL UNDERSTANDING OF THE PROGRAM.. 

	if you'd like to understand why the bot failed to apply to a job, you can use this functionality
	you'll need the url of a job that the bot failed to apply to...
	these 'failed urls' can be found in an output file--simply copy the url of a job that the bot was unable to complete
	
	1) the bot will ask you to input the url
	2) the bot will then navigate to that url and begin applying
	3) as the bot goes through the application, it will pause and ask if you want to continue
	4) if you notice that the bot is answering a question incorrectly, you can tell it to inspect the page
	5) the bot will then ask if there's a specific question it's getting wrong
	6) if you say yes, the bot will then ask which number question it got wrong
	7) you can input the question number and the bot will ask you to change its answer to said question
	8) the bot will then over-write the bad answer in the stored_answers.csv with your new response
	9) you can then continue applying

	

	
