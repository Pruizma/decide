# Generated by Selenium IDE
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from base.tests import BaseTestCase
from authentication.models import UserProfile

class TestVotingDuplicateNameViewNegative(StaticLiveServerTestCase):
  def setUp(self):
    self.base = BaseTestCase()
    self.base.setUp()
    user_admin_superuser = UserProfile(username='adminsuper', sex='F', style='N', is_staff=True, is_superuser=True)
    user_admin_superuser.set_password('qwerty')
    user_admin_superuser.save()
    self.base.user_admin = user_admin_superuser

    self.driver = webdriver.Firefox()
    self.vars = {}
    self.driver.maximize_window() #For maximizing window
    self.driver.implicitly_wait(20) #gives an implicit wait for 20 seconds

    super().setUp() 
  
  def tearDown(self):
    super().tearDown()
    self.driver.quit()

    self.base.tearDown()

  def wait_for_window(self, timeout = 2):
    time.sleep(round(timeout / 1000))
    wh_now = self.driver.window_handles
    wh_then = self.vars["window_handles"]
    if len(wh_now) > len(wh_then):
      return set(wh_now).difference(set(wh_then)).pop()
  
  def test_duplicate_voting_name_view_positive(self):
    # Test name: test_voting_duplicate_name_positive
    # Step # | name | target | value
    # 1 | open | http://localhost:8000/admin/ | 
    self.driver.get(f'{self.live_server_url}/admin/')
    self.driver.find_element_by_id("id_username").send_keys("adminsuper")
    self.driver.find_element_by_id("id_password").send_keys("qwerty")
    self.driver.find_element_by_css_selector("div .submit-row input").click()
    # 3 | click | css=.model-voting .addlink | 
    self.driver.find_element(By.CSS_SELECTOR, ".model-voting .addlink").click()
    # 4 | type | id=id_name | name10
    self.driver.find_element(By.ID, "id_name").send_keys("name10")
    # 5 | click | id=id_desc | 
    self.driver.find_element(By.ID, "id_desc").click()
    # 6 | type | id=id_desc | name10
    self.driver.find_element(By.ID, "id_desc").send_keys("name10")
    # 7 | click | css=#add_id_question > img | 
    self.vars["window_handles"] = self.driver.window_handles
    # 8 | storeWindowHandle | root | 
    self.driver.find_element(By.CSS_SELECTOR, "#add_id_question > img").click()
    # 9 | selectWindow | handle=${win3316} | 
    self.vars["win3316"] = self.wait_for_window(2000)
    # 10 | click | id=id_desc | 
    self.vars["root"] = self.driver.current_window_handle
    # 11 | type | id=id_desc | name10
    self.driver.switch_to.window(self.vars["win3316"])
    # 12 | click | id=id_options-0-number | 
    self.driver.find_element(By.ID, "id_desc").click()
    # 13 | type | id=id_options-0-number | 1
    self.driver.find_element(By.ID, "id_desc").send_keys("name10")
    # 14 | click | id=id_options-0-option | 
    self.driver.find_element(By.ID, "id_options-0-number").click()
    # 15 | type | id=id_options-0-option | 1
    self.driver.find_element(By.ID, "id_options-0-number").send_keys("1")
    # 16 | click | id=id_options-1-number | 
    self.driver.find_element(By.ID, "id_options-0-option").click()
    # 17 | type | id=id_options-1-number | 2
    self.driver.find_element(By.ID, "id_options-0-option").send_keys("1")
    # 18 | click | id=id_options-1-option | 
    self.driver.find_element(By.ID, "id_options-1-number").click()
    # 19 | type | id=id_options-1-option | 2
    self.driver.find_element(By.ID, "id_options-1-number").send_keys("2")
    # 20 | click | name=_save | 
    self.driver.find_element(By.ID, "id_options-1-option").click()
    # 21 | close |  | 
    self.driver.find_element(By.ID, "id_options-1-option").send_keys("2")
    # 22 | selectWindow | handle=${root} | 
    self.driver.find_element(By.NAME, "_save").click()
    # 24 | type | id=id_name | name10
    self.vars["window_handles"] = self.driver.window_handles
    # 25 | click | id=id_url | 
    self.driver.switch_to.window(self.vars["root"])
    self.driver.find_element(By.CSS_SELECTOR, "#add_id_auths > img").click()
    # 26 | click | id=id_url | 
    self.vars["win6003"] = self.wait_for_window(2000)
    # 27 | type | id=id_url | http://localhost:8000
    self.driver.switch_to.window(self.vars["win6003"])
    # 28 | click | name=_save | 
    self.driver.find_element(By.ID, "id_name").send_keys("name10")
    # 29 | close |  | 
    self.driver.find_element(By.ID, "id_url").click()
    # 30 | selectWindow | handle=${root} | 
    self.driver.find_element(By.ID, "id_url").click()
    # 31 | click | id=id_autocenso | 
    self.driver.find_element(By.ID, "id_url").send_keys("http://localhost:8000")
    # 32 | click | name=_save | 
    self.driver.find_element(By.NAME, "_save").click()
    # 34 | type | id=id_name | name11
    self.driver.switch_to.window(self.vars["root"])
    # 35 | click | id=id_desc | 
    self.driver.find_element(By.ID, "id_autocenso").click()
    # 36 | type | id=id_desc | name11
    self.driver.find_element(By.NAME, "_save").click()
    # 37 | addSelection | id=id_question | label=name10
    self.driver.find_element(By.CSS_SELECTOR, ".addlink").click()
    # 38 | addSelection | id=id_auths | label=http://localhost:8000
    self.driver.find_element(By.ID, "id_name").send_keys("name11")
    # 39 | click | id=id_autocenso | 
    self.driver.find_element(By.ID, "id_desc").click()
    # 40 | click | name=_save | 
    self.driver.find_element(By.ID, "id_desc").send_keys("name11")
    # 41 | assertText | linkText=name10 | name10
    dropdown = self.driver.find_element(By.ID, "id_question")
    dropdown.find_element(By.XPATH, "//option[. = 'name10']").click()
    # 42 | assertText | css=.row1:nth-child(1) a | name11
    dropdown = self.driver.find_element(By.ID, "id_auths")
    dropdown.find_element(By.XPATH, "//option[. = 'http://localhost:8000']").click()
    self.driver.find_element(By.ID, "id_autocenso").click()
    self.driver.find_element(By.NAME, "_save").click()
    assert self.driver.find_element(By.LINK_TEXT, "name10").text == "name10"
    assert self.driver.find_element(By.CSS_SELECTOR, ".row1:nth-child(1) a").text == "name11"
  
