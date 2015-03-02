from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import psutil, sys

class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if "liveserver" in arg:
                cls.server_url = "http://" + arg.split("=")[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url
        
    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()
        
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("test-type")
        self.browser = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:\Python34\Scripts\chromedriver.exe")
        self.browser.implicitly_wait(2)

        
    def tearDown(self):
        self.browser.quit()
        
    def check_for_row_in_load_table(self, field_text, id_text):
        table = self.browser.find_element_by_id(id_text)
        fields = table.find_elements_by_tag_name('td')
                
        self.assertIn(field_text, [field.text for field in fields])
                
    def test_can_execute_a_mem_test_and_see_results(self):
        #Engineer visits the page / 
        self.browser.get(self.server_url)
        
        #she sees a title "Gear Testing"
        self.assertIn('Gear Testing', self.browser.title)
                      
        # There is a bold header announcing the Gear Testing application
        header_text = self.browser.find_element_by_tag_name('h1')
        self.assertEqual('This is the homepage!!-->Welcome to the Gear Testing application', header_text.text)
        
        # she notes that there is a link on the page saying something about Memory Consumption
        memoryconsumer_link = self.browser.find_element_by_id('id_memoryconsumer')
        self.assertEqual('To use the memory consumer application go to this link', 
            memoryconsumer_link.text
        )
        
        # she notes that there is a link on the page saying something about Memory Consumption
        admin_link = self.browser.find_element_by_id('id_admin_link')
        self.assertEqual('To administer this application login onto admin page', admin_link.text)
        
        # There is a link in the test 'memoryconsumer' application. She clicks on the link.
        memcon_page_link = self.browser.find_element_by_link_text("this link")
        memcon_page_link.click()
        memcon_page_title = self.browser.find_element_by_tag_name('h1')
        self.assertIn("Memory consumption application", memcon_page_title.text)
        
        # She sees a description of the application and instructions for use
        app_usage = self.browser.find_element_by_id("id_app_usage").text
        self.assertIn("Use this application to create memory allocation within the running python process.", app_usage)
            
        # She sees an input box that invites her to start a test by inputing an amount of RAM that should be consumed by the application
        inputbox = self.browser.find_element_by_id("id_new_mem")
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            "# of 400KB blocks"
        )
        
        # She also sees some table headings that indicate memory stat columns. But there are no stats
        
        # She enters an amount of RAM memory in 1000 40KB units and keys in ENTER. The page updates
        # and shows a table with resulting stats on memory that was consumed by the input
        inputbox.send_keys('1000')
        inputbox.send_keys(Keys.ENTER)
        
        engineer_1_memconpage_url = self.browser.current_url
        
        # She notes that the page url has changed and she bookmarks the URL
        self.assertRegex(engineer_1_memconpage_url, '/memoryconsumer/exp_page/.+')
        
        # She also notes that the table shows the memory load that was input 
        # as well as the amount of available OS memory
        self.check_for_row_in_load_table('1000', 'id_table_mem_stats')
        
        # There is still a test box inviting her to submit a memory load. She enters "2000" an presses ENTER 
        inputbox = self.browser.find_element_by_id("id_new_mem")
        
     
        inputbox.send_keys('2000')
        inputbox.send_keys(Keys.ENTER)
        
        # The page updates again, and now shows both items on her list
        
        
        self.check_for_row_in_load_table('1000', 'id_table_mem_stats')
        self.check_for_row_in_load_table('2000', 'id_table_mem_stats')
        
        # Now another engineer comes along to the site.
        ## We use a new browser session to make sure that no information
        ## of the first engineer is coming through from cookies etc..
        
        self.browser.quit()
        self.setUp()
        self.browser.get(self.server_url)
        
        # Engineer #2 visits the geartest homepage and clicks through to the Memoryconsumer page. 
        # There is no sign of the data from Engineer #1 on the memoryconsumer page
        self.browser.get(self.server_url)
        memcon_page_link = self.browser.find_element_by_link_text("this link")
        memcon_page_link.click()
        
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("1000", page_text)
        self.assertNotIn("2000", page_text)

        # Engineer #2 starts a new list by entering a new item. 
        # He is less interesting that Engineer #1
        
        inputbox = self.browser.find_element_by_id("id_new_mem")
        inputbox.send_keys("2000")
        inputbox.send_keys(Keys.ENTER)
        
        # Engineer #2 gets his own unique URL
        
        engineer_2_memconpage_url = self.browser.current_url
        self.assertRegex(engineer_2_memconpage_url, '/memoryconsumer/exp_page/.+')
        self.assertNotEqual(engineer_2_memconpage_url, engineer_1_memconpage_url)
        
        # Again there is no sign of engineer #1 on the memoryconsumer page
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("1000", page_text)
                
    def test_layout_and_styling(self):
        # Engineer goes to the home page
        self.browser.get(self.server_url)
        memcon_page_link = self.browser.find_element_by_link_text("this link")
        memcon_page_link.click()
        self.browser.set_window_size(1024, 768)
        
        # Engineer notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id("id_new_mem")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta = 10
        )
        
        # The engineer starts a new experiment and sees that the input is nicely centered too
        inputbox.send_keys("1000")
        inputbox.send_keys(Keys.ENTER)
        inputbox = self.browser.find_element_by_id("id_new_mem")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta = 20
        )
    


