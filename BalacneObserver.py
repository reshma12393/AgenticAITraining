import os, random, re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
# Load env file
load_dotenv()

# Read key
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


# 1. --- TOOLS ---
def get_account_balance(query):
    balance = random.randint(5000, 10000)
    return f"${balance}"

def get_greeting(query):
    greetings = ["Hello! How can I help you today?", "Hi there! Need some assistance?", "Greetings!"]
    return random.choice(greetings)


def llm_fallback(query):
    # This acts as the "general knowledge" tool
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    return llm.invoke(query).content


# Mapping tools for the agent to use
TOOLS = {
    "get_account_balance": get_account_balance,
    "get_greeting": get_greeting,
    "llm_fallback": llm_fallback
}

# 2. --- PROMPT TEMPLATE ---
SYSTEM_PROMPT = """
You are a helpful assistant. Solve the user's request using this cycle:
Thought: Reason about what to do.
Action: tool_name[query]
Observation: result of the tool
Final Answer: your final response to the user.

Available Tools:
- get_account_balance: Use this ONLY if the user asks for their balance.
- get_greeting: Use this if the user says hi, hello, or greets you.
- llm_fallback: Use this for any other general questions.

Question: {input}
"""


# 3. --- AGENT LOGIC ---
def run_react_agent(user_input):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    prompt = SYSTEM_PROMPT.format(input=user_input)

    # Simple loop for ReAct (Max 3 turns)
    for _ in range(3):
        response = llm.invoke(prompt).content
        print(f"\n-- Agent Reasoning --\n{response}")

        if "Final Answer:" in response:
            return response.split("Final Answer:")[-1].strip()

        # Parse Action: tool_name[input]
        action_match = re.search(r"Action:\s*(\w+)\[(.*?)\]", response)
        if action_match:
            tool_name = action_match.group(1)
            tool_input = action_match.group(2)

            if tool_name in TOOLS:
                observation = TOOLS[tool_name](tool_input)
                prompt += f"\n{response}\nObservation: {observation}"
            else:
                prompt += f"\n{response}\nObservation: Tool {tool_name} not found."
        else:
            return response  # Fallback if formatting fails


# # 4. --- TEST CASES ---
# print("\n--- TEST 1: Greeting ---")
# print("RESULT:", run_react_agent("Hi there!"))

# print("\n--- TEST 2: Balance ---")
# print("RESULT:", run_react_agent("How much money do I have left?"))

# print("\n--- TEST 3: General Query ---")
# print("RESULT:", run_react_agent("What is the capital of France?"))
# input("****")
print("Hello! Ask me anything, or say bye / exit / quit when you're done.")
while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["exit", "quit", "q", "bye", "goodbye", "see you", "see ya"]:
        print("Exiting chat. Goodbye!")
        break
    result = run_react_agent(user_input)
    print("Agent:", result)


