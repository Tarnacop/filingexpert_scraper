from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import selenium.webdriver.support.expected_conditions as EC

import sys
import getpass
import time
import random
import os
import csv
import configparser
import pdf_look_into
# ------------------------------------------------------- CONSTANTS ----------------------------------
path_to_download = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
path_to_chromedriver = "res/chromedriver.exe"
main_page = "http://uob-metalib.hosted.exlibrisgroup.com/V/?func=native-link&resource=BHM05857"
canvas_login_button_id = "j_submit"
canvas_login_username_field_id = "j_username"
canvas_login_password_field_id = "j_password"

pi_navigator_advanced_css_selector = "#advanced-link > a"
search_field_activate_css_selector = "body > div.row.no-gutters.advanced-search-row.ng-scope.active > div " \
                                     "> div.advanced-search > div.content.as-right-panel.guide-target-av-10 " \
                                     "> div > div.row.no-gutters.advanced-search-bar > div.col-md-8 > div " \
                                     "> div:nth-child(1) > button"
search_field_css_selector = "#asBox"

results_css_selector = "#lazyLoadSearchResult > div:nth-child(1) > div > div"
filters_css_selector = "#main-search-panel > div > div.row.no-gutters.criteria-box.message-container > " \
                       "div.col-md-10 > div > div > div > div.header-box-container > " \
                       "div.bool-box.guide-target-st-1.ng-isolate-scope > div > div > div > a"

search_button_css_selector = "body > div.row.no-gutters.advanced-search-row.ng-scope.active > div > " \
                             "div.advanced-search > div.content.as-right-panel.guide-target-av-10 > div " \
                             "> div.row.no-gutters.advanced-search-bar > div.col-md-4 > button"

country_of_incorporation_css_selector = "#cat_country > a"

companies_css_selector = "#cat_company > a"

country_first_result_css_selector = "body > div.row.no-gutters.advanced-search-row.ng-scope.active > div > " \
                                    "div.advanced-search > div.content.as-right-panel.guide-target-av-10 > div > " \
                                    "div.ng-scope > div > div.advanced-search-result.guide-target-av-6.ps-container > " \
                                    "div.ng-scope > div:nth-child(1) > span"

all_corporate_actions_css_selector = "#main-content-container > div:nth-child(3) > div > div.ng-scope > div > " \
                                      "div.facet-block-container.ng-isolate-scope > div:nth-child(2) > div > div > " \
                                      "span.text-elipsis-overflow.name.ng-binding.ng-scope"

company_filings_and_announcements_css_selector = "#scroll-container-1 > div.ng-scope > ul > li:nth-child(1) > " \
                                                 "facet-tree > div > a.constraint.text-elipsis-overflow.ng-binding"

article_page_results_css_selector = ".document-row.ng-scope"

go_to_result_pdf_css_selector = "div > div:nth-child(3) > div.guide-target-vd-6 > a.icon-link.pull-right.downloadLink.icon-pdf"

next_page_css_selector = "[ng-class=\"{disabled: noNext()}\"]"
# --------------------------------------------- END OF CONSTANTS ------------------------------------------------
# --------------------------------------------------------- FUNCTION DEFINITIONS --------------------------------


def load_main_page(url, type):
    # Set the url to the page
    browser.get(url)

    time.sleep(random.randint(1, 3))

    if type == 1:
        # Check if page loaded successfully
        try:
            WebDriverWait(browser, 120).until(EC.element_to_be_clickable((By.ID, canvas_login_button_id)))
        except TimeoutException:
            print("ERROR LOADING CANVAS PAGE: CHECK INTERNET CONNECTION")
            browser.quit()
            sys.exit(1)
    else:
        time.sleep(random.randint(4, 7))

    print("URL OPENED SUCCESSFULLY")
    print("CONFIGURATION PART")


def canvas_login(user, pwd):
    time.sleep(random.randint(1, 3))

    # Login to canvas using the username and password provided
    try:
        username_field = browser.find_element_by_id(canvas_login_username_field_id)
        username_field.clear()
        username_field.send_keys(user)
    except NoSuchElementException:
        return

    time.sleep(random.randint(1, 3))

    try:
        password_field = browser.find_element_by_id(canvas_login_password_field_id)
        password_field.clear()
        password_field.send_keys(pwd)
    except NoSuchElementException:
        print("ERROR WHILE TRYING TO FIND THE PASSWORD FIELD")
        browser.quit()
        sys.exit(1)

    time.sleep(random.randint(1, 3))

    try:
        browser.find_element_by_id(canvas_login_button_id).click()
    except NoSuchElementException:
        print("ERROR WHILE TRYING TO SUBMIT LOGIN")
        browser.quit()
        sys.exit(1)

    print("PI NAVIGATOR LOADED SUCCESSFULLY")


def pi_navigator_search(company_name, company_country):

    try:
        WebDriverWait(browser, 120).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, pi_navigator_advanced_css_selector)))
    except TimeoutException:
        print("ERROR WHILE LOADING THE PI NAVIGATOR PAGE - CHECK INTERNET CONNECTION")
        browser.quit()
        sys.exit(1)

    advanced_button = browser.find_element_by_css_selector(pi_navigator_advanced_css_selector)
    advanced_button.click()

    time.sleep(random.randint(1, 2))

    # Clear filters if needed
    try:
        while True:
            filter_applied = browser.find_element_by_css_selector(filters_css_selector)
            filter_applied.click()
    except NoSuchElementException:
        pass

    time.sleep(random.randint(1, 2))

    try:
        country_of_incorporation = browser.find_element_by_css_selector(country_of_incorporation_css_selector)
        country_of_incorporation.click()
    except Exception:
        print("ERROR WHILE TRYING TO FIND COUNTRY OF INCORPORATION")
        browser.quit()
        sys.exit(1)

    time.sleep(random.randint(1, 2))

    try:
        search_field_activate = browser.find_element_by_css_selector(search_field_activate_css_selector)
        search_field_activate.click()
    except Exception:
        print("ERROR WHILE TRYING TO FIND THE SEARCH FIELD")
        browser.quit()
        sys.exit(1)

    # Search for company country
    try:
        search_field = browser.find_element_by_css_selector(search_field_css_selector)
        search_field.clear()
        search_field.send_keys(company_country)
    except Exception:
        print("ERROR WHILE TRYING TO FIND THE SEARCH FIELD")
        browser.quit()
        sys.exit(1)

    time.sleep(random.randint(10, 20))

    try:
        country_result = browser.find_element_by_css_selector(country_first_result_css_selector)
        country_result.click()
    except Exception:
        pass

    time.sleep(random.randint(1, 2))

    try:
        companies = browser.find_element_by_css_selector(companies_css_selector)
        companies.click()
    except Exception:
        print("ERROR WHILE TRYING TO CLICK COMPANIES")
        browser.quit()
        sys.exit(1)

    time.sleep(random.randint(1, 2))

    try:
        search_field_activate = browser.find_element_by_css_selector(search_field_activate_css_selector)
        search_field_activate.click()
    except NoSuchElementException:
        print("ERROR WHILE TRYING TO FIND THE SEARCH FIELD")
        browser.quit()
        sys.exit(1)

    # Search company
    try:
        search_field = browser.find_element_by_css_selector(search_field_css_selector)
        search_field.clear()
        search_field.send_keys(company_name)
    except NoSuchElementException:
        print("ERROR WHILE TRYING TO FIND THE SEARCH FIELD")
        browser.quit()
        sys.exit(1)

    # Get results and check if there are any

    time.sleep(random.randint(10, 20))

    results = browser.find_elements_by_css_selector(results_css_selector)
    if len(results) == 0:
        print("NO RESULTS FOR COMPANY %s" % company_name)
        search_button = browser.find_element_by_css_selector(search_button_css_selector)
        search_button.click()
        return -1
    else:
        for result in results:
            browser.execute_script("arguments[0].scrollIntoView(true);", result)
            result.click()

    time.sleep(random.randint(1, 2))

    # PRESS SEARCH
    try:
        search_button = browser.find_element_by_css_selector(search_button_css_selector)
        search_button.click()
    except NoSuchElementException:
        try:
            clear_button = browser.find_element_by_css_selector("#center-panel-scroll-container > div.row.ng-scope > "
                                                                "div > div.form-title.form-button-bar > div")
            clear_button.click()
            return -1
        except NoSuchElementException:
            print("ERROR COULD NOT FIND SEARCH BUTTON")
            browser.quit()
            sys.exit(1)
    # WAIT FOR OTHER FILTERS TO APPEAR

    time.sleep(random.randint(1, 2))

    # FIRST TRY TO PRESS COMPANY FILINGS AND ANNOUNCEMENTS
    try:
        company_filings_and_announcements = browser.find_element_by_css_selector(company_filings_and_announcements_css_selector)
        company_filings_and_announcements.click()
    except:
        try:
            WebDriverWait(browser, 120).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, all_corporate_actions_css_selector)))
        except TimeoutException:
            print("ERROR COULD NOT FIND ALL CORPORATE ACTIONS FILTER FAMILY")
            browser.quit()
            sys.exit(1)
        all_corporate_actions = browser.find_element_by_css_selector(all_corporate_actions_css_selector)
        all_corporate_actions.click()
        time.sleep(5)
        company_filings_and_announcements = browser.find_element_by_css_selector(company_filings_and_announcements_css_selector)
        company_filings_and_announcements.click()
        time.sleep(5)

        os.makedirs(os.path.join(path_to_download, company_name), exist_ok=True)

    return 0


def handle_search_results(function_company_term, is_download_completed, is_text_analysis_completed):

    if not is_download_completed:
        next_page = browser.find_element_by_css_selector(next_page_css_selector)

        while next_page.get_attribute("class") != "ng-scope disabled":

            article_page_results = browser.find_elements_by_css_selector(article_page_results_css_selector)
            for article_result in article_page_results:
                article_id = article_result.get_attribute("id")

                # Try to fetch pdf if available
                try:
                    go_to_result_pdf = browser.find_element_by_css_selector(
                        "#%s > %s" % (article_id, go_to_result_pdf_css_selector))

                    browser.execute_script("arguments[0].scrollIntoView(true);", go_to_result_pdf)

                    go_to_result_pdf.click()

                    time.sleep(random.randint(2, 5))

                    x1 = 0
                    while x1 == 0:
                        count = 0
                        li = os.listdir(path_to_download)
                        for x1 in li:
                            if x1.endswith(".crdownload"):
                                count = count + 1
                        if count == 0:
                            x1 = 1
                        else:
                            time.sleep(10)
                            x1 = 0

                    if len(browser.window_handles) > 5:
                        base = browser.current_window_handle
                        set = browser.window_handles

                        for item in set:
                            if item == base:
                                continue
                            browser.switch_to.window(item)
                            browser.close()

                        browser.switch_to.window(base)

                except NoSuchElementException:
                    pass
                except IOError:
                    print("An I/O error occurred while trying to download the file.")
                except OSError:
                    print("An OS error occurred while trying to download the file.")
                except Exception:
                    print("An error occurred while trying to download the file.")

            next_page.find_element_by_css_selector("a").click()

            time.sleep(random.randint(2, 4))

            next_page = browser.find_element_by_css_selector(next_page_css_selector)
            time.sleep(random.randint(1, 3))

        article_page_results = browser.find_elements_by_css_selector(article_page_results_css_selector)
        for article_result in article_page_results:
            article_id = article_result.get_attribute("id")

            # Try to fetch pdf if available
            try:
                go_to_result_pdf = browser.find_element_by_css_selector(
                    "#%s > %s" % (article_id, go_to_result_pdf_css_selector))

                browser.execute_script("arguments[0].scrollIntoView(true);", go_to_result_pdf)

                go_to_result_pdf.click()

                time.sleep(random.randint(2, 5))

                x1 = 0
                while x1 == 0:
                    count = 0
                    li = os.listdir(path_to_download)
                    for x1 in li:
                        if x1.endswith(".crdownload"):
                            count = count + 1
                    if count == 0:
                        x1 = 1
                    else:
                        time.sleep(10)
                        x1 = 0

                if len(browser.window_handles) > 5:
                    base = browser.current_window_handle
                    set = browser.window_handles

                    for item in set:
                        if item == base:
                            continue
                        browser.switch_to.window(item)
                        browser.close()

                    browser.switch_to.window(base)

            except NoSuchElementException:
                pass
            except IOError:
                print("An I/O error occurred while trying to download the file.")
            except OSError:
                print("An OS error occurred while trying to download the file.")
            except Exception:
                print("An error occurred while trying to download the file.")

        for f in os.listdir(path_to_download):
            if os.path.isfile(os.path.join(path_to_download, f)):
                os.rename(os.path.join(path_to_download, f), os.path.join(os.path.join(path_to_download, function_company_term), f))

        company_dir = os.path.join(path_to_download, function_company_term)
        for f in os.listdir(company_dir):
            if os.path.isfile(os.path.join(company_dir, f)):
                try:
                    os.makedirs(os.path.join(company_dir, f.rstrip(".pdf")), exist_ok=True)
                    os.rename(os.path.join(company_dir, f), os.path.join(os.path.join(company_dir, f.rstrip(".pdf")), f))
                except:
                    pass

        config["DEFAULT"]["DownloadCompleted"] = "True"
        with open("config.ini", "w") as configfile:
            config.write(configfile)

    # TODO - add check for text analysis etc
    #if not is_text_analysis_completed:
    #    files_with_information = 0
    #    company_dir = os.path.join(path_to_download, function_company_term)
    #    for directory in os.listdir(company_dir):
    #        pdf_path = "%s.pdf" % os.path.join(os.path.join(company_dir, directory), directory)
    #        pdf_has_information = pdf_look_into.get_summary(os.path.join(company_dir, directory), pdf_path,
    #                                                        "%s_summary.txt" % pdf_path.rstrip(".pdf"))
    #        if pdf_has_information:
    #            files_with_information += 1

        config["DEFAULT"]["TextAnalysisCompleted"] = "True"
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        return 0

    return -1
# ------------------------------------------ END OF FUNCTION DEFINITION ---------------------------------------------


os.makedirs(path_to_download, exist_ok=True)
chrome_options = webdriver.ChromeOptions()
prefs = {"download.default_directory": path_to_download,
         "profile.default_content_setting_values.automatic_downloads": 1,
         "plugins.always_open_pdf_externally": True}
chrome_options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(executable_path=path_to_chromedriver, chrome_options=chrome_options)

config = configparser.ConfigParser()
current_firm_list = "firmlist.csv"
current_row = 0
download_completed = False
text_analysis_completed = False
run_loop = False

# Config defaults
if os.path.exists("config.ini"):
    config.read("config.ini")
    current_firm_list = config["DEFAULT"]["CurrentFirmList"]
    current_row = int(config["DEFAULT"]["CurrentRow"])
    download_completed = config["DEFAULT"].getboolean("DownloadCompleted")
    text_analysis_completed = config["DEFAULT"].getboolean("TextAnalysisCompleted")
    run_loop = config["DEFAULT"].getboolean("RunLoop")
else:
    config["DEFAULT"] = {
        "CurrentFirmList": current_firm_list,
        "CurrentRow": current_row,
        "DownloadCompleted": download_completed,
        "TextAnalysisCompleted": text_analysis_completed,
        "RunLoop": False
    }
    with open("config.ini", "w") as configfile:
        config.write(configfile)

#result_csv_file = "firmlist_results.csv"
#result_csv_fieldnames = ["COMPANY", "COUNTRY", "INFORMATION"]

#if not os.path.exists(result_csv_file):
#    with open(result_csv_file, "w") as output_csvfile:
#        writer = csv.DictWriter(output_csvfile, fieldnames=result_csv_fieldnames)
#        writer.writeheader()

print("------------------- LOG --------------------")

row_counter = 1

# Prompt for username and password
user = input("PROVIDE YOUR UOB ID: ")
print("YOUR USERNAME IS: %s" % user)

pwd = getpass.getpass("PROVIDE YOUR UOB PASSWORD: ")
print("PASSWORD PROVIDED")

with open(current_firm_list) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        config.read("config.ini")
        run_loop = config["DEFAULT"].getboolean("RunLoop")
        download_completed = config["DEFAULT"].getboolean("DownloadCompleted")
        text_analysis_completed = config["DEFAULT"].getboolean("TextAnalysisCompleted")
        if run_loop:
            input("Please press enter to continue")

        if row_counter <= current_row:
            row_counter = row_counter + 1
            continue
        else:
            row_counter = row_counter + 1

        load_main_page(main_page)

        canvas_login(user, pwd)

        company_term = row["Name"]
        company_country = row["C"]

        #result_csv_dict = dict()
        #result_csv_dict["COMPANY"] = company_term
        #result_csv_dict["COUNTRY"] = company_country

        if pi_navigator_search(company_term, company_country) == 0:
            has_information = handle_search_results(company_term, download_completed, text_analysis_completed)
            #if has_information > 0:
            #    result_csv_dict["INFORMATION"] = "YES"
            #elif has_information == 0:
            #    result_csv_dict["INFORMATION"] = "N\A"

        config["DEFAULT"]["CurrentRow"] = str(row_counter)
        download_completed = False
        text_analysis_completed = False
        config["DEFAULT"]["DownloadCompleted"] = str(download_completed)
        config["DEFAULT"]["TextAnalysisCompleted"] = str(text_analysis_completed)
        with open("config.ini", "w") as configfile:
            config.write(configfile)

        #with open(result_csv_file, "a") as output_csvfile:
        #    writer = csv.DictWriter(output_csvfile, fieldnames=result_csv_fieldnames)
        #    writer.writerow(result_csv_dict)
