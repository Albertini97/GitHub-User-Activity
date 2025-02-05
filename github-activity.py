import sys
import urllib.request
import json

def fetch_github_activity(username):
    """
    Fetches the recent activity of a GitHub user using the GitHub API.
    """
    url = f"https://api.github.com/users/{username}/events"
    
    try:
        # Make the HTTP GET request to the GitHub API
        with urllib.request.urlopen(url) as response:
            if response.getcode() == 200:  # Check if the request was successful
                data = response.read().decode('utf-8')  # Read and decode the response
                return json.loads(data)  # Parse the JSON response
            else:
                print(f"Error: Unable to fetch data for user '{username}'. HTTP Status Code: {response.getcode()}")
                return None
    except urllib.error.HTTPError as e:
        # Handle HTTP errors (e.g., 404 for invalid username)
        print(f"HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        # Handle URL errors (e.g., no internet connection)
        print(f"URL Error: {e.reason}")
    except Exception as e:
        # Handle any other exceptions
        print(f"An unexpected error occurred: {str(e)}")
    
    return None

def display_activity(events):
    """
    Displays the parsed GitHub activity in a human-readable format.
    """
    if not events:
        print("No activity found.")
        return
    
    print("\nRecent Activity:")
    for event in events[:10]:  # Limit to the last 10 events for brevity
        event_type = event['type']
        repo_name = event['repo']['name']
        
        if event_type == 'PushEvent':
            commits = len(event['payload']['commits'])
            print(f"- Pushed {commits} commit(s) to {repo_name}")
        elif event_type == 'IssuesEvent':
            action = event['payload']['action']
            print(f"- {action.capitalize()} an issue in {repo_name}")
        elif event_type == 'WatchEvent':
            print(f"- Starred {repo_name}")
        elif event_type == 'CreateEvent':
            ref_type = event['payload']['ref_type']
            print(f"- Created a new {ref_type} in {repo_name}")
        elif event_type == 'PullRequestEvent':
            action = event['payload']['action']
            print(f"- {action.capitalize()} a pull request in {repo_name}")
        else:
            print(f"- Performed a {event_type} in {repo_name}")

def main():
    """
    Main function to handle command-line arguments and execute the program.
    """
    if len(sys.argv) != 2:
        print("Usage: python github-activity.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    print(f"Fetching recent activity for GitHub user: {username}")
    
    events = fetch_github_activity(username)
    if events:
        display_activity(events)
    else:
        print("Failed to fetch activity.")

if __name__ == "__main__":
    main()