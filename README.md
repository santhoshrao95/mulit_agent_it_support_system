# mulit_agent_it_support_systemMulti-agent IT Support System

Approach Summary:

I have designed a basic multi-agent system with three specialized agents coordinated by a Master agent. The Master agent makes decisions such as selection of agents and orchestrates conversations, while the other agents—user_intake_agent, resolution_agent, and escalation_agent—are solely responsible for their individual tasks. For demonstration purposes, I have created a user proxy instead of implementing real user interaction.

The Master agent is supplemented with a Memory DB that tracks issue frequency, enabling it to identify recurring problems through the check_issue_frequency() function. The resolution_agent leverages a Knowledge Base along with functions such as check_knowledge_base(), reset_password(), and reset_vpn() to resolve common IT issues as described in the flow chart. The escalation_agent has been equipped with create_it_ticket() and send_notification() functions to handle complex or recurring issues that require human intervention.

A key feature of this system is its ability to bypass the resolution process for frequently occurring issues (those occurring more than three times), routing them directly to the escalation team to address potential systemic problems. This intelligent routing enhances efficiency and ensures that widespread issues receive appropriate attention.

Challenges Faced:
Ideating and finding the optimal system design was difficult. I tried multiple approaches, including having an interactive user_intake_agent for getting more details from users. However, most attempts went off track as sometimes the master agent did not know when to stop the conversation or how to determine when sufficient information had been gathered. Hence, I resorted to a simpler approach.
Designing the system and making the master agent solely responsible for decisions like agent selection and conversation orchestration presented challenges. I used the GroupChat feature of PyAutoGen to overcome this issue, allowing for structured agent interactions.
Memory management across agents was challenging, particularly ensuring that the master agent could effectively track issue frequency while maintaining conversation context.
I found it difficult to reproduce authentic IT support scenarios, hence I relied on the provided examples only.
Sometimes when non-IT requests were given, the agents did not know how to respond appropriately. I addressed this by providing clear instructions to end the conversation politely in such cases.
Testing the system with edge cases revealed that even with clear instructions, language models sometimes deviated from expected behavior, requiring refinements to the system prompts.
Function calling between agents needed careful implementation to ensure proper error handling and consistent return values.

Bonus Task:
Implementing an interactive workflow to gather more information and act as an agent-aided support system for problem solving.
Building more modular yet clearly defined agents for different tasks like security, resolution, etc.
Creating a bigger yet clearer knowledge base for different kinds of issues and their resolutions.
Multi-state resolution agent which tries different approaches before concluding that it cannot resolve the issue.
More function implementations for the agents to utilize.


