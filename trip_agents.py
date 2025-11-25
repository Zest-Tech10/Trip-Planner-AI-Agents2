# import re
# import os
# import logging
# from crewai import Agent, LLM
# from langchain_core.language_models.chat_models import BaseChatModel
# from tools.browser_tools import BrowserTools
# from tools.calculator_tools import CalculatorTools
# from tools.search_tools import SearchTools

# # ---------------------------
# # 🔧 LOGGING CONFIGURATION
# # ---------------------------
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(message)s",
#     handlers=[
#         # logging.FileHandler("trip_agents.log"),
#         logging.StreamHandler()
#     ]
# )

# # ---------------------------
# # 🧠 AGENTS CLASS
# # ---------------------------
# class TripAgents():
#     def __init__(self, llm: BaseChatModel = None):
#         if llm is None:
#             # ✅ Always use OpenAI model
#             try:
#                 self.llm = LLM(
#                     model="gpt-5-mini",  # or gpt-4o-mini, gpt-4o, etc.
#                     api_key=os.getenv("OPENAI_API_KEY")
#                 )
#                 logging.info("✅ OpenAI LLM (gpt-5-mini) initialized successfully.")
#             except Exception as e:
#                 logging.error(f"❌ Failed to initialize OpenAI model: {e}")
#                 raise e
#         else:
#             self.llm = llm
#             logging.info("Using provided LLM instance")

#         # Initialize tools
#         self.search_tool = SearchTools()
#         self.browser_tool = BrowserTools()
#         self.calculator_tool = CalculatorTools()
#         logging.info("✅ Tools initialized successfully")

#     def city_selection_agent(self):
#         logging.info("Creating City Selection Expert agent...")
#         return Agent(
#             role='City Selection Expert',
#             goal='Select the best city based on weather, season, and prices',
#             backstory='An expert in analyzing travel data to pick ideal destinations',
#             tools=[self.search_tool, self.browser_tool],
#             allow_delegation=False,
#             llm=self.llm,
#             verbose=True
#         )

#     def local_expert(self):
#         logging.info("Creating Local Expert agent...")
#         return Agent(
#             role='Local Expert at this city',
#             goal='Provide the BEST insights about the selected city',
#             backstory="""A knowledgeable local guide with extensive information
#         about the city, its attractions and customs""",
#             tools=[self.search_tool, self.browser_tool],
#             allow_delegation=False,
#             llm=self.llm,
#             verbose=True
#         )

#     def travel_concierge(self):
#         logging.info("Creating Amazing Travel Concierge agent...")
#         return Agent(
#             role='Amazing Travel Concierge',
#             goal="""Create the most amazing travel itineraries with budget and 
#         packing suggestions for the city""",
#             backstory="""Specialist in travel planning and logistics with 
#         decades of experience""",
#             tools=[self.search_tool, self.browser_tool, self.calculator_tool],
#             allow_delegation=False,
#             llm=self.llm,
#             verbose=True
#         )

# # ---------------------------
# # 🧾 STREAM (LOG) OUTPUT HANDLER
# # ---------------------------
# class StreamToConsole():
#     def __init__(self):
#         self.buffer = []
#         self.colors = ['\033[91m', '\033[92m', '\033[94m', '\033[93m']
#         self.color_index = 0
#         self.reset_color = '\033[0m'
#         logging.info("StreamToConsole initialized")

#     def write(self, data):
#         cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

#         task_match_object = re.search(r'\"task\"\s*:\s*\"(.*?)\"', cleaned_data, re.IGNORECASE)
#         task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
#         task_value = task_match_object.group(1) if task_match_object else (
#             task_match_input.group(1).strip() if task_match_input else None
#         )

#         if task_value:
#             message = f"🤖 Task Detected: {task_value}"
#             print(message)
#             logging.info(message)

#         if "Entering new CrewAgentExecutor chain" in cleaned_data:
#             self.color_index = (self.color_index + 1) % len(self.colors)
#             cleaned_data = cleaned_data.replace(
#                 "Entering new CrewAgentExecutor chain",
#                 f"{self.colors[self.color_index]}Entering new CrewAgentExecutor chain{self.reset_color}"
#             )

#         for role in ["City Selection Expert", "Local Expert at this city", "Amazing Travel Concierge"]:
#             if role in cleaned_data:
#                 cleaned_data = cleaned_data.replace(
#                     role, f"{self.colors[self.color_index]}{role}{self.reset_color}"
#                 )

#         if "Finished chain." in cleaned_data:
#             cleaned_data = cleaned_data.replace(
#                 "Finished chain.", f"{self.colors[self.color_index]}Finished chain.{self.reset_color}"
#             )

#         self.buffer.append(cleaned_data)
#         if "\n" in data:
#             print(''.join(self.buffer), end='')
#             self.buffer = []

#     def flush(self):
#         if self.buffer:
#             print(''.join(self.buffer))
#             self.buffer = []

#     def close(self):
#         self.flush()

# # Example usage
# if __name__ == "__main__":
#     trip = TripAgents()
#     stream = StreamToConsole()
#     test_data = """
#     {"task": "Selecting best city for travel"}
#     Entering new CrewAgentExecutor chain
#     City Selection Expert analyzing data...
#     Finished chain.
#     """
#     stream.write(test_data)
#     stream.close()




import re
import sys
import os
import logging
from crewai import Agent, LLM
from langchain_core.language_models.chat_models import BaseChatModel
from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools



# ---------------------------
# 🔧 LOGGING CONFIGURATION
# ---------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

# ---------------------------
# 🧠 AGENTS CLASS
# ---------------------------
# class TripAgents():
#     def __init__(self, llm: BaseChatModel = None):
#         if llm is None:
#             # ✅ Always use OpenAI model
#             try:
#                 self.llm = LLM(
#                     model="gpt-5-mini",  # or gpt-4o-mini, gpt-4o, etc.
#                     # api_key=os.getenv("OPENAI_API_KEY")
#                 )
#                 logging.info("✅ OpenAI LLM (gpt-5-mini) initialized successfully.")
#             except Exception as e:
#                 logging.error(f"❌ Failed to initialize OpenAI model: {e}")
#                 raise e
#         else:
#             self.llm = llm
#             logging.info("Using provided LLM instance")

#         # Initialize tools
#         self.search_tool = SearchTools()
#         self.browser_tool = BrowserTools()
#         self.calculator_tool = CalculatorTools()
#         logging.info("✅ Tools initialized successfully")

#     def city_selection_agent(self):
#         logging.info("Creating City Selection Expert agent...")
#         return Agent(
#             role='City Selection Expert',
#             goal='Select the best city based on weather, season, and prices',
#             backstory='An expert in analyzing travel data to pick ideal destinations',
#             tools=[self.search_tool, self.browser_tool],
#             allow_delegation=False,
#             llm=self.llm,
#             verbose=True
#         )

#     def local_expert(self):
#         logging.info("Creating Local Expert agent...")
#         return Agent(
#             role='Local Expert at this city',
#             goal='Provide the BEST insights about the selected city',
#             backstory="""A knowledgeable local guide with extensive information
#         about the city, its attractions and customs""",
#             tools=[self.search_tool, self.browser_tool],
#             allow_delegation=False,
#             llm=self.llm,
#             verbose=True
#         )

#     def travel_concierge(self):
#         logging.info("Creating Amazing Travel Concierge agent...")
#         return Agent(
#             role='Amazing Travel Concierge',
#             goal="""Create the most amazing travel itineraries with budget and 
#         packing suggestions for the city""",
#             backstory="""Specialist in travel planning and logistics with 
#         decades of experience""",
#             tools=[self.search_tool, self.browser_tool, self.calculator_tool],
#             allow_delegation=False,
#             llm=self.llm,
#             verbose=True
#         )

class TripAgents():
    def __init__(self):
        logging.info("🔧 Initializing TripAgents...")

        # -------------------------------
        # ⚡ Different LLMs for Each Agent
        # -------------------------------

        # Ultra-fast for simple selection logic
        self.city_llm = LLM(model="gpt-4.1-mini")

        # Fast for city facts, attractions, food
        self.local_llm = LLM(model="gpt-4.1-mini")

        # Balanced: high-quality itineraries
        self.itinerary_llm = LLM(model="gpt-5-mini")  # or gpt-4.1 or gpt-4.1-pro

        logging.info("✅ LLMs initialized (city: gpt-4.1-mini, local: gpt-4.1-mini, concierge: gpt-5-mini)")

        # Tools
        self.search_tool = SearchTools()
        self.browser_tool = BrowserTools()
        self.calculator_tool = CalculatorTools()
        logging.info("🔧 Tools initialized successfully")

    # ------------------------------------------------------------
    # 1️⃣ City Selection Agent (uses fastest model)
    # ------------------------------------------------------------
    def city_selection_agent(self):
        logging.info("Creating City Selection Expert agent...")
        return Agent(
            role='City Selection Expert',
            goal='Select the best city based on weather, season, and prices',
            backstory='Expert at analyzing global travel patterns.',
            tools=[self.search_tool, self.browser_tool],
            allow_delegation=False,
            llm=self.city_llm,  # 🟢 FASTEST MODEL
            verbose=False
        )

    # ------------------------------------------------------------
    # 2️⃣ Local Expert Agent (mid-level model)
    # ------------------------------------------------------------
    def local_expert(self):
        logging.info("Creating Local Expert agent...")
        return Agent(
            role='Local Expert at this city',
            goal='Provide accurate insights about the selected city.',
            backstory='A local expert with deep cultural and historical knowledge.',
            tools=[self.search_tool, self.browser_tool],
            allow_delegation=False,
            llm=self.local_llm,  # 🟢 FAST + GOOD MODEL
            verbose=False
        )

    # ------------------------------------------------------------
    # 3️⃣ Travel Concierge Agent (most detailed work)
    # ------------------------------------------------------------
    def travel_concierge(self):
        logging.info("Creating Travel Concierge agent...")
        return Agent(
            role='Amazing Travel Concierge',
            goal='Create the most amazing itineraries with budget and tips.',
            backstory='A master in travel planning & logistics.',
            tools=[self.search_tool, self.browser_tool, self.calculator_tool],
            allow_delegation=False,
            llm=self.itinerary_llm,  # 🟡 HIGHER QUALITY MODEL
            verbose=False
        )


# ---------------------------
# 🧾 STREAM (LOG) OUTPUT HANDLER
# ---------------------------
class StreamToConsole():
    def __init__(self):
        self.buffer = []
        self.colors = ['\033[91m', '\033[92m', '\033[94m', '\033[93m']
        self.color_index = 0
        self.reset_color = '\033[0m'
        logging.info("StreamToConsole initialized")

    def write(self, data):
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        task_match_object = re.search(r'\"task\"\s*:\s*\"(.*?)\"', cleaned_data, re.IGNORECASE)
        task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        task_value = task_match_object.group(1) if task_match_object else (
            task_match_input.group(1).strip() if task_match_input else None
        )

        if task_value:
            message = f"🤖 Task Detected: {task_value}"
            print(message)
            logging.info(message)

        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            self.color_index = (self.color_index + 1) % len(self.colors)
            cleaned_data = cleaned_data.replace(
                "Entering new CrewAgentExecutor chain",
                f"{self.colors[self.color_index]}Entering new CrewAgentExecutor chain{self.reset_color}"
            )

        for role in ["City Selection Expert", "Local Expert at this city", "Amazing Travel Concierge"]:
            if role in cleaned_data:
                cleaned_data = cleaned_data.replace(
                    role, f"{self.colors[self.color_index]}{role}{self.reset_color}"
                )

        if "Finished chain." in cleaned_data:
            cleaned_data = cleaned_data.replace(
                "Finished chain.", f"{self.colors[self.color_index]}Finished chain.{self.reset_color}"
            )

        self.buffer.append(cleaned_data)
        if "\n" in data:
            print(''.join(self.buffer), end='')
            self.buffer = []

    def flush(self):
        if self.buffer:
            print(''.join(self.buffer))
            self.buffer = []

    def close(self):
        self.flush()

# Example usage
if __name__ == "__main__":
    trip = TripAgents()
    stream = StreamToConsole()
    test_data = """
    {"task": "Selecting best city for travel"}
    Entering new CrewAgentExecutor chain
    City Selection Expert analyzing data...
    Finished chain.
    """
    stream.write(test_data)
    stream.close()