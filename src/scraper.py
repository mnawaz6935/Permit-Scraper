import time
import random
from selenium.webdriver.common.by import By
from bot_utils import (get_normal_driver, execute_script_based_click,
                       insert_value_and_press_enter, get_input_value,
                       get_element_text)

class PermitScraper:
    def __init__(self):
        self.driver = get_normal_driver()

    def start_scraping(self, baseUrl):
        self.driver.get(baseUrl)
        time.sleep(5)
        iframe = self.driver.find_element(By.XPATH, '(//iframe[contains(@src,"webpermits.dll")])[1]')
        self.driver.switch_to.frame(iframe)
        execute_script_based_click(self.driver, "//*[@id='BTNPERMITS']")
        time.sleep(2)
        self.scrape_permits()

    def scrape_permits(self):
        i = 0
        while i < 100:
            i += 1
            year = random.randint(2000, 2023)  # Generate a random year
            month = random.randint(1, 12)  # Generate a random month
            id_number = random.randint(1000, 9999)  # Generate a random ID number
            permit_number = f"{year:04d}{month:02d}{id_number:04d}"
            insert_value_and_press_enter(self.driver, '//input[@id="EDTPERMITNBR"]', permit_number, previous_clear=True)
            time.sleep(5)
            if self.driver.find_elements(By.XPATH, "//*[contains(text(),'No matching permit # found!')]"):
                execute_script_based_click(self.driver, "//*[@id='iwnotify-ok']")
                continue
            elif self.driver.find_elements(By.XPATH, "//*[contains(text(),'Enter Permit # or Address or Parcel ID')]"):
                continue
            else:
                print(f'Data found for {permit_number}!')
                time.sleep(3)
                permit_info = self.collect_permit_info()
                print(permit_info)
                time.sleep(3)

    def collect_permit_info(self):
        info = {
            'PermitNumber': get_input_value(self.driver, '//input[@id="EDTPERMITNBR"]'),
            'PermitStatus': get_input_value(self.driver, '//input[@id="IWDBEDIT2"]'),
            'Type1': get_input_value(self.driver, "//input[@id='IWDBEDIT12']"),
            'Type2': get_input_value(self.driver, "//input[@id='IWDBEDIT3']"),
            'Owner': get_input_value(self.driver, '//input[@id="IWDBEDIT4"]'),
            'ParcelNumber': get_input_value(self.driver, '//input[@id="IWDBEDIT5"]'),
            'DBA': get_input_value(self.driver, '//input[@id="IWDBEDIT6"]'),
            'JobDescription': get_input_value(self.driver, '//*[@id="IWDBMEMO1"]'),
            'ApplyDate': get_input_value(self.driver, '//input[@id="IWDBEDIT13"]'),
            'IssueDate': get_input_value(self.driver, '//input[@id="IWDBEDIT8"]'),
            'CODate': get_input_value(self.driver, '//input[@id="IWDBEDIT7"]'),
            'ExpirationDate': get_input_value(self.driver, '//input[@id="IWDBEDIT9"]'),
            'LastInspectionRequest': get_input_value(self.driver, '//input[@id="IWDBEDIT10"]'),
            'LastInspectionResult': get_input_value(self.driver, '//input[@id="IWDBEDIT11"]'),
            'Inspections': self.collect_related_info('RGNBTNVIEWINSPECTIONS', 'INSPGRID_'),
            'Reviews': self.collect_related_info('RGNBTNVIEWREVIEWS', 'REWGRID_'),
            'PermitHolds': self.collect_related_info('RGNBTNVIEWPERHOLDS', 'PHGRID_')
        }
        return info

    def collect_related_info(self, button_id, grid_id):
        details = []
        if int(self.driver.find_element(By.XPATH, f'//*[@id="{button_id}"]').get_attribute('data-badge')) > 0:
            execute_script_based_click(self.driver, f'//*[@id="{button_id}"]//input')
            time.sleep(3)
            rows = self.driver.find_elements(By.XPATH, f"//*[@id='{grid_id}']//tr[contains(@id,'row')]")
            for row in rows:
                if "display: none;" in row.get_attribute('style'):
                    break
                details.append({
                    'Code': get_element_text(self.driver, f"(//td)[1]", element=row),
                    'Description': get_element_text(self.driver, f"(//td)[2]", element=row),
                    'RequestDate': get_element_text(self.driver, f"(//td)[3]", element=row),
                    'ResultDate': get_element_text(self.driver, f"(//td)[4]", element=row),
                    'Result': get_element_text(self.driver, f"(//td)[5]", element=row),
                })
            execute_script_based_click(self.driver, "(//*[@id='IMGBACK'])[last()]")
            time.sleep(3)
        return details

    def close_browser(self):
        self.driver.quit()
