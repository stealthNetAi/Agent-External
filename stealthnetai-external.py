import time
import requests
import subprocess
import json
import threading
from queue import Queue

# API Key (Replace with your actual API key)
API_KEY = ""

API_BASE_URL = "https://api2-service-dot-gen-lang-client-0165304536.ue.r.appspot.com"
TASKS_ENDPOINT = f"{API_BASE_URL}/tasks"
HELPFILE_ENDPOINT = f"{API_BASE_URL}/helpfile"
RESULTS_ENDPOINT = f"{API_BASE_URL}/results"
LOGS_ENDPOINT = f"{API_BASE_URL}/logs"

def send_all_helpfiles_and_get_commands(task_id, help_files):
    data = {
        "task_id": task_id,
        "help_files": help_files,
    }
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post(HELPFILE_ENDPOINT, json=data, headers=headers)

    return json.loads(response.content)


def send_all_results(task_id, results):
    data = {
        "task_id": task_id,
        "results": results,
    }
    headers = {"Authorization": f"Bearer {API_KEY}"}
    requests.post(RESULTS_ENDPOINT, json=data, headers=headers)

def send_log(log,task_id):
    log_data = {
        "log": log,
        "task_id": task_id
    }
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post(LOGS_ENDPOINT, json=log_data, headers=headers)
    print(response.text)

def fetch_tasks():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(TASKS_ENDPOINT, headers=headers)
    tasks = response.json()
    if not 'task_id' in tasks:
        return []
    return tasks

def run_tool_with_timeout(command, timeout=600):
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        return result.stdout, result.stderr
    except subprocess.TimeoutExpired as e:
        return e.stdout, f"Command timed out: {str(e)}"
    except Exception as e:
        return "", f"Command failed: {str(e)}"


def main():
    sleep_time = 2.5
    while True:
        try:
            task = fetch_tasks()
            if task:
                print(task)
                sleep_time = 2.5 
                task_id = task["task_id"]
                tools = task["tools"]
                tools_str = ", ".join([tool['name'] for tool in tools])
                send_log(f"Received task: {tools_str}", task_id)
                
                # Collect help files for all tools
                help_files = []
                for tool in tools:
                    print(tool)
                    tool_id = tool['id']
                    tool_name = tool['name']
                    tool_input = tool['input']
                    help_command = f"{tool_name} --help"
                    help_output, error = run_tool_with_timeout(help_command)
                    help_files.append({
                        "tool_id": tool_id,
                        "tool_name": tool_name,
                        "tool_input": tool_input,
                        "help_file": help_output or error,
                    })
                
                # Send all help files at once and get commands
                commands = send_all_helpfiles_and_get_commands(task_id, help_files)
                # Process and execute commands for each tool
                results = []
                def worker(queue, results):
                    while True:
                        command = queue.get()
                        if command is None:
                            break
                        send_log(f"Executing command: {command}", task_id)
                        output, error = run_tool_with_timeout(command)
                        results.append({
                            "tool_name": command,
                            "output": output or error,
                        })
                        send_log(f"Command finished: {command}", task_id)
                        queue.task_done()

                # Create a queue to hold the commands
                command_queue = Queue()
                results = []

                # Start 5 worker threads
                threads = []
                for _ in range(5):
                    thread = threading.Thread(target=worker, args=(command_queue, results))
                    thread.start()
                    threads.append(thread)

                # Put all commands in the queue
                for command in commands:
                    command_queue.put(command)

                # Block until all tasks are done
                command_queue.join()

                # Stop the worker threads
                for _ in range(5):
                    command_queue.put(None)
                for thread in threads:
                    thread.join()
                
                # Send all results at once
                send_all_results(task_id, results)
                send_log(f"Task completed: {tools_str}", task_id)
            else:
                sleep_time = min(sleep_time + 0.25, 15)  # Increase sleep time up to a max of 15 seconds

        except requests.RequestException as e:
            print(f"API error: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
        time.sleep(sleep_time)
        

if __name__ == "__main__":
    main()
