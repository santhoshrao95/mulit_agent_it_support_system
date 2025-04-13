import datetime
import uuid
import autogen
import yaml

knowledge_base = {
    "email_access": {
        "password_incorrect": {
            "symptoms": ["password incorrect", "can't login", "access denied"],
            "solution": "reset_password",
            "description": "User is unable to login due to password issues. A password reset is required."
        }
    },
    "vpn_issue": {
        "connection_dropping": {
            "symptoms": ["connection dropping", "disconnects", "can't connect", "unstable"],
            "solution": "reset_vpn",
            "description": "VPN connection is unstable or fails to connect. VPN client reset required."
        },
        "connection_slow": {
            "symptoms": ["slow", "laggy", "poor performance", "timeout"],
            "solution": "reset_vpn",
            "description": "VPN connection is performing poorly. Reset VPN client to resolve speed issues."
        },
        "authentication_failed": {
            "symptoms": ["authentication failed", "credentials", "wrong password", "invalid login"],
            "solution": "reset_vpn",
            "description": "VPN authentication is failing. Reset VPN client to clear cached credentials."
        }
    }
}

# Enhanced memory database to track issue occurrences and provide issue statistics
class MemoryDB:
    def __init__(self):
        # Store user requests
        self.requests = []
        # Track issues by type for recurrence detection
        self.issue_occurrences = {}
        # Track issue frequency (number of times each issue has been reported)
        self.issue_frequency = {}
    
    def add_request(self, user_id, issue_type, description):
      
        request_id = str(uuid.uuid4())[:8]
        
        request = {
            "id": request_id,
            "user_id": user_id,
            "issue_type": issue_type,
            "description": description,
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "new",
            "resolution": None
        }
        
        self.requests.append(request)
        
        if issue_type in self.issue_occurrences:
            self.issue_occurrences[issue_type].append(user_id)
        else:
            self.issue_occurrences[issue_type] = [user_id]
        
        if issue_type in self.issue_frequency:
            self.issue_frequency[issue_type] += 1
        else:
            self.issue_frequency[issue_type] = 1
        
        return request_id
    
    def update_request(self, request_id, status, resolution=None):
        for request in self.requests:
            if request["id"] == request_id:
                request["status"] = status
                if resolution:
                    request["resolution"] = resolution
                return True
        return False
    
    def get_request(self, request_id):
        for request in self.requests:
            if request["id"] == request_id:
                return request
        return None
    
    def get_user_history(self, user_id):
        return [req for req in self.requests if req["user_id"] == user_id]
    
    def is_recurrent_issue(self, issue_type):
        if issue_type in self.issue_occurrences:
            unique_users = set(self.issue_occurrences[issue_type])
            return len(unique_users) >= 2
        return False
    
    def is_frequent_issue(self, issue_type, threshold=3):
        return self.issue_frequency.get(issue_type, 0) >= threshold
    
    def get_issue_statistics(self, issue_type=None):
        """Get statistics about issues in the database"""
        if issue_type:
            return {
                "type": issue_type,
                "occurrences": self.issue_frequency.get(issue_type, 0),
                "affected_users": len(set(self.issue_occurrences.get(issue_type, []))),
                "first_reported": min([req["timestamp"] for req in self.requests if req["issue_type"] == issue_type], default=None),
                "last_reported": max([req["timestamp"] for req in self.requests if req["issue_type"] == issue_type], default=None),
                "resolution_rate": len([req for req in self.requests if req["issue_type"] == issue_type and req["status"] == "resolved"]) / 
                                  max(1, len([req for req in self.requests if req["issue_type"] == issue_type]))
            }
        else:
            return {
                "total_requests": len(self.requests),
                "unique_issue_types": len(self.issue_frequency),
                "most_frequent_issue": max(self.issue_frequency.items(), key=lambda x: x[1])[0] if self.issue_frequency else None,
                "most_frequent_count": max(self.issue_frequency.values()) if self.issue_frequency else 0,
                "resolved_count": len([req for req in self.requests if req["status"] == "resolved"]),
                "resolution_rate": len([req for req in self.requests if req["status"] == "resolved"]) / max(1, len(self.requests))
            }

memory_db = MemoryDB()
memory_db.add_request("user1", "email_access", "Can't login to email")
memory_db.add_request("user2", "email_access", "Email password not working")
memory_db.add_request("user3", "email_access", "Email login problems")
memory_db.add_request("user4", "vpn_issue", "VPN connection dropping")
memory_db.add_request("user5", "vpn_issue", "VPN keeps disconnecting")
memory_db.add_request("user6", "vpn_issue", "Can't connect to VPN")
memory_db.add_request("user7", "vpn_issue", "VPN authentication failing")

def reset_password(user_id):
    print(f"Executing password reset for user {user_id}")
    return "Password reset successful. New password sent via SMS."

def reset_vpn(user_id):
    print(f"Resetting VPN connection for user {user_id}")
    return "VPN connection reset successfully. User will need to reconnect."

def create_it_ticket(issue_summary, priority):
    print(f"Creating IT support ticket with priority {priority}")
    ticket_id = f"IT-{str(uuid.uuid4())[:6]}"
    return f"Ticket {ticket_id} created with {priority} priority."

def send_notification(recipient, subject, message):
    print(f"Sending notification to {recipient}: {subject}")
    return f"Notification sent to {recipient} with subject: {subject}"

def check_knowledge_base(issue_type, description):
    print(f"Checking knowledge base for issue type: {issue_type}")
    
    if issue_type not in knowledge_base:
        return f"No knowledge base entries for {issue_type}"
    

    description_lower = description.lower()
    

    for issue_id, issue_info in knowledge_base[issue_type].items():
       
        for symptom in issue_info["symptoms"]:
            if symptom in description_lower:
                return f"Found solution: {issue_info['solution']} - {issue_info['description']}"
    
    return f"No matching issues found in knowledge base for {issue_type}"


def check_issue_frequency(issue_type):
    """Check how frequently an issue type has been reported"""
    print(f"Checking frequency for issue type: {issue_type}")
    
    frequency = memory_db.issue_frequency.get(issue_type, 0)
    is_frequent = memory_db.is_frequent_issue(issue_type)
    affected_users = len(set(memory_db.issue_occurrences.get(issue_type, [])))
    
    result = {
        "issue_type": issue_type,
        "frequency": frequency,
        "is_frequent": is_frequent,
        "affected_users": affected_users
    }
    
    if is_frequent:
        return f"FREQUENT ISSUE: {issue_type} has occurred {frequency} times affecting {affected_users} users. This requires escalation."
    else:
        return f"Issue frequency: {issue_type} has occurred {frequency} times affecting {affected_users} users."


def setup_agents():
    with open('secrets.yaml', 'r') as f:
        secrets = yaml.safe_load(f)
        
    config_list = [
        {
            "model": secrets['openai']['model'],
            "api_key": secrets['openai']['api_key']
        }
    ]
    
    llm_config = {
        "config_list": config_list,
        "temperature": 0.1, 
        "timeout": 120,
        "cache_seed": 42 
    }
    
    master_agent = autogen.AssistantAgent(
        name="MasterAgent",
        llm_config={
            **llm_config,
            "functions": [
                {
                    "name": "check_issue_frequency",
                    "description": "Check how frequently an issue type has been reported in the system",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "issue_type": {
                                "type": "string",
                                "description": "Type of issue (email_access, vpn_issue, etc.)"
                            }
                        },
                        "required": ["issue_type"]
                    }
                }
            ]
        },
        system_message="""You are the Master Agent in an IT support system. Your responsibilities include:
1. Overseeing all agents and their interactions
2. Ensuring smooth collaboration between agents
3. Maintaining memory of user requests to identify recurring issues
4. Guiding the overall support process

Workflow:
1. If the issue is unrelated to IT, end the conversation politely.
2. If it's an IT issue, classify it by asking the User Intake Agent.
3. Once classified, use check_issue_frequency function to determine issue frequency.
4. If the issue has occurred more than 3 times (is_frequent=true), treat it as highly recurring and:
   a. Inform everyone this is a recurring issue affecting multiple users
   b. Skip the Resolution Agent and route directly to the Escalation Agent
   c. Request escalation to the IT support team with HIGH priority
5. For non-frequent issues, route to the Resolution Agent first.
6. If Resolution Agent cannot resolve the issue, route to Escalation Agent.

Always use the check_issue_frequency function before deciding whether to route to Resolution or Escalation agent.
Recurring issues (occurred > 3 times) should always go directly to the Escalation Agent."""
    )
    
    user_intake_agent = autogen.AssistantAgent(
        name="UserIntakeAgent",
        llm_config=llm_config,
        system_message="""You are the User Intake Agent in an IT support system. Your responsibilities include:
1. Receiving employee IT requests
2. Extracting key information from the request
3. Classifying the issue type (email_access, vpn_issue, software_issue, hardware_issue, etc.)
4. DO NOT attempt to resolve issues yourself
5. After classification, report back to the Master Agent

Focus on understanding the problem - not solving it. Be concise and direct in your communications."""
    )

    resolution_agent = autogen.AssistantAgent(
        name="ResolutionAgent",
        llm_config={
            **llm_config,
            "functions": [
                {
                    "name": "check_knowledge_base",
                    "description": "Check the knowledge base for solutions to an issue",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "issue_type": {
                                "type": "string",
                                "description": "Type of issue (email_access, vpn_issue, etc.)"
                            },
                            "description": {
                                "type": "string",
                                "description": "Description of the issue in the user's words"
                            }
                        },
                        "required": ["issue_type", "description"]
                    }
                },
                {
                    "name": "reset_password",
                    "description": "Reset a user's password",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "ID of the user whose password needs to be reset"
                            }
                        },
                        "required": ["user_id"]
                    }
                },
                {
                    "name": "reset_vpn",
                    "description": "Reset a user's VPN connection",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "ID of the user whose VPN needs to be reset"
                            }
                        },
                        "required": ["user_id"]
                    }
                }
            ]
        },
        system_message="""You are the Resolution Agent in an IT support system. Your responsibilities include:
1. First check the knowledge base using the check_knowledge_base function
2. Based on knowledge base results, attempt to resolve common IT issues
3. You can reset passwords for email issues using reset_password()
4. You can reset VPN connections using reset_vpn()
5. If the issue is too complex or not solvable with your functions, request escalation. Do not create a summary or ticket. Just pass the info to master agent.
6. Report the resolution outcome to the Master Agent

IMPORTANT: Always check the knowledge base first before taking any action.
If the knowledge base result contains "reset_password", use the reset_password function.
If the knowledge base result contains "reset_vpn", use the reset_vpn function.
If no solution is found in the knowledge base, use your judgment based on the issue type.

Focus on fixing problems within your capabilities."""
    )
    
    escalation_agent = autogen.AssistantAgent(
        name="EscalationAgent",
        llm_config={
            **llm_config,
            "functions": [
                {
                    "name": "create_it_ticket",
                    "description": "Create a ticket in the IT support system",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "issue_summary": {
                                "type": "string",
                                "description": "Summary of the issue"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high", "critical"],
                                "description": "Priority level of the issue"
                            }
                        },
                        "required": ["issue_summary", "priority"]
                    }
                },
                {
                    "name": "send_notification",
                    "description": "Send a notification to IT support",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "recipient": {
                                "type": "string",
                                "description": "Who should receive the notification"
                            },
                            "subject": {
                                "type": "string",
                                "description": "Subject of the notification"
                            },
                            "message": {
                                "type": "string",
                                "description": "Content of the notification"
                            }
                        },
                        "required": ["recipient", "subject", "message"]
                    }
                }
            ]
        },
        system_message="""You are the Escalation Agent in an IT support system. Your responsibilities include:
1. Handling complex issues that the Resolution Agent cannot solve
2. Handling recurring issues that affect multiple users (these come directly from the Master Agent)
3. Generating comprehensive issue summaries for IT support
4. Creating support tickets with appropriate priority levels
5. Sending notifications to the IT support team
6. Report the escalation outcome to the Master Agent

For frequent/recurring issues:
- Set the priority to "high" or "critical"
- Include in your summary that this is a recurring issue affecting multiple users
- Suggest that IT support investigate potential systemic problems

Your goal is to properly document and route complex issues to human IT support."""
    )
    
    user_proxy = autogen.UserProxyAgent(
        name="Employee",
        human_input_mode="NEVER",  
        system_message="You are an employee reporting an IT issue.",
        code_execution_config=False 
    )
    
    master_agent.register_function(
        function_map={
            "check_issue_frequency": check_issue_frequency
        }
    )
    
    resolution_agent.register_function(
        function_map={
            "check_knowledge_base": check_knowledge_base,
            "reset_password": reset_password,
            "reset_vpn": reset_vpn
        }
    )
    
    escalation_agent.register_function(
        function_map={
            "create_it_ticket": create_it_ticket,
            "send_notification": send_notification
        }
    )
    
    return master_agent, user_intake_agent, resolution_agent, escalation_agent, user_proxy

def process_request(user_id, issue_description):
    print(f"\n===== New IT Support Request =====")
    print(f"From: {user_id}")
    print(f"Issue: {issue_description}")
    print("==================================\n")
    
    agents = setup_agents()
    master_agent, user_intake_agent, resolution_agent, escalation_agent, user_proxy = agents
    
    groupchat = autogen.GroupChat(
        agents=[user_proxy, master_agent, user_intake_agent, resolution_agent, escalation_agent],
        messages=[],
        max_round=12
    )

    with open('secrets.yaml', 'r') as f:
        secrets = yaml.safe_load(f)
        
    config_list = [
        {
            "model": secrets['openai']['model'],
            "api_key": secrets['openai']['api_key']
        }
    ]
    
    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config={
            "config_list": config_list,
        }
    )
    
    user_proxy.initiate_chat(
        manager,
        message=f"I'm {user_id} and I have an IT issue: {issue_description}. Please help."
    )

if __name__ == "__main__":
    ## Example: Email issue (will be identified as a frequent issue needing direct escalation)
    process_request("user8", "I can't access my email. It keeps saying my password is incorrect.")
    
    ## Once the first request completes, uncomment to run other examples:
    # process_request("user9", "My VPN keeps disconnecting when I'm trying to work from home.")
    # process_request("user10", "My laptop keeps shutting down randomly.")
    # process_request("user11", "I need help with the printer.")
