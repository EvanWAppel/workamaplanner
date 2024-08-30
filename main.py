import utils

class caplan():
    def __init__(self):
        data = utils.assumptions()
        content = utils.get_call(assumptions = data,api_address = utils.assumptions.apis.emp_api.value)
        # Produce a list of employees and their identity keys
        employees = utils.employee_list(payload=content[1])
        # # For every employee, retrieve their timesheets
        # # Former employees will appear as 'Bad Requests'
        timedata = utils.timesheet_retrieval(employees = employees, data = data)
        ### 3m 33s
        timesheets = timedata['sheets']
        # # Pull the time entries out of the timesheets
        time_entries = timedata['time_entries']
        # # Rejoining names to time entries
        pre_tasks = utils.pre_tasker(sheets = timesheets, times = time_entries)
        # # Convert the time entries into tasks so that you can figure out the estimates.
        tasks = utils.tasker(base = pre_tasks)
        # # Create Estimates
        estimates = utils.estimator(tasks = tasks)
        # # Create List of All Projects
        custom_report = utils.cust_report(data = data)
        # # Get project numbers list
        project_numbers = utils.proj_numbers(project_table = custom_report["project_table"],data = data)
        # # Get tasks from projects
        task_collection = utils.get_tasks(projects = project_numbers, data = data)
        ### This is the really long one
        # # Apply estimates to full list of tasks
        estasks = utils.estimate_and_task_join(project_list = project_numbers,taskset = task_collection[0], estimates = estimates,data = data)
        # # Print full dataset as DATA to the capacity planner
        utils.summary_table(dataset = estasks, data = data)