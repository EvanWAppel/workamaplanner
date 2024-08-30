# These tests are designed to assist in the development of the Brand Spend Data Model

import unittest
import pandas as pd
import utils
import os
import os.path
import main
from datetime import date , datetime
import requests

class util_tester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assumption = utils.assumptions(mode = utils.Mode.marcom)
        cls.emp_api_called = utils.get_call(assumptions = cls.assumption,api_address = utils.assumptions.apis.emp_api.value)
        cls.empl_list_assembled = utils.employee_list(payload = cls.emp_api_called[1])
        cls.sheets_and_times = utils.timesheet_retrieval(employees = cls.empl_list_assembled,data = cls.assumption)
        cls.timesheet_retrieved = cls.sheets_and_times['sheets']
        cls.time_entry_extracted = cls.sheets_and_times['time_entries']
        cls.pre_tasked = utils.pre_tasker(sheets = cls.timesheet_retrieved, times = cls.time_entry_extracted)
        cls.tasked = utils.tasker(base = cls.pre_tasked)
        cls.estimated = utils.estimator(tasks = cls.tasked)
        cls.custom_reported = utils.cust_report(data = cls.assumption)
        cls.projects_numbered = utils.proj_numbers(project_table = cls.custom_reported["project_table"],data = cls.assumption)
        cls.got_tasks = utils.get_tasks(projects = cls.projects_numbered[0:50],data = cls.assumption)
        cls.estimated_and_tasked = utils.estimate_and_task_join(project_list=cls.projects_numbered, taskset= cls.got_tasks[0], estimates = cls.estimated, data = cls.assumption)
    # UTILS
    def test_logger_type(self):
        self.assertIsInstance(utils.logger(),str)
    def test_assumptions(self):
        self.assertIsInstance(self.assumption.current_directory, str)
        self.assertIsInstance(utils.assumptions.apis.cust_report_str.value, str)
        self.assertIsInstance(self.assumption.default_end, datetime)
        self.assertIsInstance(self.assumption.default_start, datetime)
        self.assertIsInstance(self.assumption.dest_dir, str)
        self.assertIsInstance(utils.assumptions.apis.emp_api.value, str)
        self.assertIsInstance(self.assumption.headers, dict)
        self.assertIsInstance(self.assumption.history_in_days, int)
        self.assertIsInstance(self.assumption.last, int)
        self.assertIsInstance(self.assumption.month, int)
        self.assertIsInstance(self.assumption.month_two, int)
        #self.assertIsInstance(self.assumption.source_dir, str)
        self.assertIsInstance(utils.assumptions.apis.time_api.value, str)
        self.assertIsInstance(self.assumption.year, int)
        self.assertIsInstance(self.assumption.year_two, int)
    def test_get_call(self):
        self.assertIsInstance(self.emp_api_called,tuple)
        self.assertIsInstance(self.emp_api_called[0],requests.models.Response)
        self.assertIsInstance(self.emp_api_called[1],dict)
        self.assertTrue(self.emp_api_called[0].status_code,200)
        self.assertNotEqual(len(self.emp_api_called[1]),0)
    def test_employee_list(self):
        self.assertIsInstance(self.empl_list_assembled,list)
        self.assertNotEqual(len(self.empl_list_assembled),0)
    def test_timesheet_retrieval(self):
        self.assertIsInstance(self.sheets_and_times,dict)
        self.assertIsInstance(self.sheets_and_times["raw_response"],tuple)
        self.assertIsInstance(self.sheets_and_times["sheets"],pd.DataFrame)
        self.assertIsInstance(self.sheets_and_times["time_entries"],pd.DataFrame)
        self.assertNotEqual(len(self.timesheet_retrieved),0)
    # def test_time_entry_extractor(self):
    #     self.assertIsInstance(self.time_entry_extracted,pd.DataFrame)
    #     self.assertNotEqual(len(self.time_entry_extracted),0)
    def test_pre_tasker(self):
        self.assertIsInstance(self.pre_tasked,pd.DataFrame)
        self.assertNotEqual(len(self.pre_tasked),0)
    def test_tasker(self):
        self.assertIsInstance(self.tasked,pd.DataFrame)
        self.assertNotEqual(len(self.tasked),0)
    def test_estimated(self):
        self.assertIsInstance(self.estimated,pd.DataFrame)
        self.assertNotEqual(len(self.estimated),0)
    def test_api_cust(self):
        self.assertIsInstance(utils.api_cust(),str)
    def test_cust_report(self):
        self.assertIsInstance(self.custom_reported,dict)
        self.assertIsInstance(self.custom_reported["response"],tuple)
        self.assertIsInstance(self.custom_reported["project_table"],pd.DataFrame)
    def test_proj_numbers(self):
        self.assertIsInstance(utils.proj_numbers(project_table = self.custom_reported["project_table"],data = self.assumption),list)
        self.assertNotEqual(self.projects_numbered,0)
    def test_get_tasks(self):
        self.assertIsInstance(self.got_tasks,tuple)
        self.assertIsInstance(self.got_tasks[0],pd.DataFrame)
        self.assertIsInstance(self.got_tasks[1],dict)
    def test_estimate_and_task_join(self):
        self.assertIsInstance(self.estimated_and_tasked,dict)
        self.assertIsInstance(self.estimated_and_tasked['master'],pd.DataFrame)
        self.assertIsInstance(self.estimated_and_tasked['unassigned'],pd.DataFrame)



if __name__ == '__main__':
    unittest.main()
else:
    print("I have schlippdt my pants.")

