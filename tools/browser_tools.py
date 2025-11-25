# # tools/browser_tools.py
# import os
# import json
# import requests
# import logging
# from crewai.tools import BaseTool
# from pydantic import BaseModel, Field
# from unstructured.partition.html import partition_html
# from crewai import Agent, Task, LLM

# # ---------------------------
# # 🔧 LOGGING CONFIGURATION
# # ---------------------------
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(message)s",
#     handlers=[
#         # logging.FileHandler("browser_tools.log"),
#         logging.StreamHandler()
#     ]
# )

# # ---------------------------
# # 🧠 INPUT SCHEMA
# # ---------------------------
# class WebsiteInput(BaseModel):
#     website: str = Field(..., description="The website URL to scrape")

# # ---------------------------
# # 🌐 BROWSER TOOLS CLASS
# # ---------------------------
# class BrowserTools(BaseTool):
#     name: str = "Scrape website content"
#     description: str = "Useful to scrape and summarize website content"
#     args_schema: type[BaseModel] = WebsiteInput

#     def _run(self, website: str) -> str:
#         try:
#             logging.info(f"🌐 Starting scrape for: {website}")

#             # ✅ Browserless API Key (required)
#             api_key = os.getenv("BROWSERLESS_API_KEY")
#             if not api_key:
#                 logging.error("❌ Missing BROWSERLESS_API_KEY environment variable.")
#                 return "Error: Missing Browserless API key."

#             # Request website content via Browserless
#             url = f"https://chrome.browserless.io/content?token={api_key}"
#             payload = json.dumps({"url": website})
#             headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}

#             response = requests.post(url, headers=headers, data=payload)
#             if response.status_code != 200:
#                 error_msg = f"Error: Failed to fetch website content. Status code: {response.status_code}"
#                 logging.error(error_msg)
#                 return error_msg

#             # Extract readable content
#             elements = partition_html(text=response.text)
#             content = "\n\n".join([str(el) for el in elements])
#             logging.info(f"✅ Successfully scraped {len(content)} characters from {website}")

#             # Split content into chunks for summarization
#             content_chunks = [content[i:i + 8000] for i in range(0, len(content), 8000)]
#             summaries = []

#             # ✅ Use only OpenAI (no Gemini fallback)
#             llm = LLM(
#                 model="gpt-5-mini",  # You can change to gpt-4o, gpt-4o-mini, etc.
#                 api_key=os.getenv("OPENAI_API_KEY")
#             )
#             logging.info("✅ Using OpenAI LLM (gpt-5-mini) for summarization")

#             # Summarize each chunk
#             for i, chunk in enumerate(content_chunks, start=1):
#                 logging.info(f"🧠 Summarizing chunk {i}/{len(content_chunks)}...")

#                 agent = Agent(
#                     role='Principal Researcher',
#                     goal='Produce high-quality summaries of research materials.',
#                     backstory="You are an experienced research analyst who extracts and summarizes important insights from text.",
#                     allow_delegation=False,
#                     llm=llm
#                 )

#                 task_description = (
#                     f"Analyze and summarize the content below. Include only the most relevant information.\n\n"
#                     f"CONTENT\n----------\n{chunk}"
#                 )
#                 task = Task(description=task_description, agent=agent)

#                 try:
#                     summary = task.execute()
#                     summaries.append(summary)
#                     logging.info(f"✅ Chunk {i} summarized successfully")
#                 except Exception as e:
#                     error_msg = f"❌ Failed to summarize chunk {i}: {e}"
#                     logging.error(error_msg)
#                     summaries.append(error_msg)

#             # Combine summaries
#             full_summary = "\n\n".join(summaries)
#             logging.info("🏁 Website summarization complete.")
#             return full_summary

#         except Exception as e:
#             logging.exception(f"❌ Error while processing website: {e}")
#             return f"Error while processing website: {str(e)}"

#     async def _arun(self, website: str) -> str:
#         raise NotImplementedError("Async not implemented yet.")





import os
import sys
import json
import requests
import logging
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from unstructured.partition.html import partition_html
from crewai import Agent, Task, LLM

# ---------------------------
# 🔧 LOGGING CONFIGURATION
# ---------------------------
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(message)s",
#     handlers=[
#         logging.FileHandler("browser_tools.log"),
#         logging.StreamHandler()
#     ]
# )

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

# ---------------------------
# 🧠 INPUT SCHEMA
# ---------------------------
class WebsiteInput(BaseModel):
    website: str = Field(..., description="The website URL to scrape")

# ---------------------------
# 🌐 BROWSER TOOLS CLASS
# ---------------------------
class BrowserTools(BaseTool):
    name: str = "Scrape website content"
    description: str = "Useful to scrape and summarize website content"
    args_schema: type[BaseModel] = WebsiteInput

    def _run(self, website: str) -> str:
        try:
            logging.info(f"🌐 Starting scrape for: {website}")

            # ✅ Browserless API Key (required)
            api_key = os.getenv("BROWSERLESS_API_KEY")
            if not api_key:
                logging.error("❌ Missing BROWSERLESS_API_KEY environment variable.")
                return "Error: Missing Browserless API key."

            # Request website content via Browserless
            url = f"https://chrome.browserless.io/content?token={api_key}"
            payload = json.dumps({"url": website})
            headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}

            response = requests.post(url, headers=headers, data=payload)
            if response.status_code != 200:
                error_msg = f"Error: Failed to fetch website content. Status code: {response.status_code}"
                logging.error(error_msg)
                return error_msg

            # Extract readable content
            elements = partition_html(text=response.text)
            content = "\n\n".join([str(el) for el in elements])
            logging.info(f"✅ Successfully scraped {len(content)} characters from {website}")

            # Split content into chunks for summarization
            content_chunks = [content[i:i + 8000] for i in range(0, len(content), 8000)]
            summaries = []

            # ✅ Use only OpenAI (no Gemini fallback)
            llm = LLM(
                # model="gpt-5-mini",  # You can change to gpt-4o, gpt-4o-mini, etc.
                model="gpt-4.1-mini",  # You can change to gpt-4o, gpt-4o-mini, etc.
                api_key=os.getenv("OPENAI_API_KEY")
            )
            logging.info("✅ Using OpenAI LLM (gpt-5-mini) for summarization")

            # Summarize each chunk
            for i, chunk in enumerate(content_chunks, start=1):
                logging.info(f"🧠 Summarizing chunk {i}/{len(content_chunks)}...")

                agent = Agent(
                    role='Principal Researcher',
                    goal='Produce high-quality summaries of research materials.',
                    backstory="You are an experienced research analyst who extracts and summarizes important insights from text.",
                    allow_delegation=False,
                    llm=llm
                )

                task_description = (
                    f"Analyze and summarize the content below. Include only the most relevant information.\n\n"
                    f"CONTENT\n----------\n{chunk}"
                )
                task = Task(description=task_description, agent=agent)

                try:
                    summary = task.execute()
                    summaries.append(summary)
                    logging.info(f"✅ Chunk {i} summarized successfully")
                except Exception as e:
                    error_msg = f"❌ Failed to summarize chunk {i}: {e}"
                    logging.error(error_msg)
                    summaries.append(error_msg)

            # Combine summaries
            full_summary = "\n\n".join(summaries)
            logging.info("🏁 Website summarization complete.")
            return full_summary

        except Exception as e:
            logging.exception(f"❌ Error while processing website: {e}")
            return f"Error while processing website: {str(e)}"

    async def _arun(self, website: str) -> str:
        raise NotImplementedError("Async not implemented yet.")