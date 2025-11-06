
# # import os
# # import logging
# # import traceback
# # from datetime import date, datetime
# # from functools import lru_cache
# # from typing import Optional

# # from fastapi import FastAPI, HTTPException, Depends
# # from fastapi.middleware.cors import CORSMiddleware
# # from pydantic import BaseModel, Field
# # from dotenv import load_dotenv

# # from crewai import Crew, LLM
# # from trip_agents import TripAgents
# # from trip_tasks import TripTasks

# # # ============================================================
# # # 🌍 ENVIRONMENT SETUP
# # # ============================================================
# # load_dotenv()

# # # ============================================================
# # # 🔧 LOGGING CONFIGURATION
# # # ============================================================
# # logging.basicConfig(
# #     level=logging.INFO,
# #     format="%(asctime)s [%(levelname)s] %(message)s",
# #     handlers=[
# #         logging.FileHandler("vacAIgent_api.log"),
# #         logging.StreamHandler()
# #     ]
# # )

# # logger = logging.getLogger(__name__)
# # logger.info("🚀 VacAIgent API starting (OpenAI only)...")

# # # ============================================================
# # # 🚀 FASTAPI CONFIGURATION
# # # ============================================================
# # app = FastAPI(
# #     title="VacAIgent API",
# #     description="AI-powered travel planning API using CrewAI and OpenAI",
# #     version="1.2.0"
# # )

# # # Enable CORS
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],  # ⚠️ Replace with trusted origins in production
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # ============================================================
# # # 📦 DATA MODELS
# # # ============================================================

# # class TripRequest(BaseModel):
# #     origin: str = Field(..., example="Bangalore, India", description="Your current location")
# #     destination: str = Field(..., example="Krabi, Thailand", description="Destination city and country")
# #     start_date: date = Field(..., example="2025-06-01", description="Start date of your trip")
# #     end_date: date = Field(..., example="2025-06-10", description="End date of your trip")
# #     interests: str = Field(..., example="2 adults who love swimming, hiking, shopping, and local food", description="Describe your interests and travel preferences")


# # class TripResponse(BaseModel):
# #     status: str
# #     message: str
# #     itinerary: Optional[str] = None
# #     error: Optional[str] = None


# # # ============================================================
# # # ⚙️ SETTINGS AND DEPENDENCIES
# # # ============================================================

# # class Settings:
# #     def __init__(self):
# #         self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# #         self.SERPER_API_KEY = os.getenv("SERPER_API_KEY")
# #         self.BROWSERLESS_API_KEY = os.getenv("BROWSERLESS_API_KEY")


# # @lru_cache()
# # def get_settings():
# #     return Settings()


# # def validate_api_keys(settings: Settings = Depends(get_settings)):
# #     """Ensure all required API keys exist before running."""
# #     required_keys = {
# #         'OPENAI_API_KEY': settings.OPENAI_API_KEY,
# #         'SERPER_API_KEY': settings.SERPER_API_KEY,
# #         'BROWSERLESS_API_KEY': settings.BROWSERLESS_API_KEY
# #     }
# #     missing = [k for k, v in required_keys.items() if not v]
# #     if missing:
# #         logger.error(f"❌ Missing API keys: {', '.join(missing)}")
# #         raise HTTPException(status_code=500, detail=f"Missing required API keys: {', '.join(missing)}")
# #     return settings


# # # ============================================================
# # # 🧩 LLM HANDLER (OpenAI only)
# # # ============================================================

# # class OpenAILLMHandler:
# #     """Handles OpenAI LLM creation and configuration."""

# #     def __init__(self, settings: Settings):
# #         self.openai_key = settings.OPENAI_API_KEY

# #     def create_llm(self):
# #         try:
# #             logger.info("🧠 Initializing OpenAI LLM (gpt-5-mini)...")
# #             return LLM(model="gpt-5-mini", api_key=self.openai_key)
# #         except Exception as e:
# #             logger.critical(f"❌ Failed to initialize OpenAI LLM: {e}")
# #             traceback.print_exc()
# #             raise HTTPException(status_code=500, detail=f"Failed to initialize OpenAI LLM: {e}")


# # # ============================================================
# # # 🧳 TRIP CREW LOGIC
# # # ============================================================

# # class TripCrew:
# #     """Manages the CrewAI-based itinerary generation process."""

# #     def __init__(self, origin, destination, date_range, interests, settings: Settings):
# #         self.origin = origin
# #         self.destination = destination
# #         self.date_range = date_range
# #         self.interests = interests
# #         self.llm_handler = OpenAILLMHandler(settings)

# #     def _generate_itinerary(self, llm):
# #         """Internal CrewAI orchestration logic."""
# #         agents = TripAgents(llm=llm)
# #         tasks = TripTasks()

# #         # Create agents
# #         city_selector = agents.city_selection_agent()
# #         local_expert = agents.local_expert()
# #         concierge = agents.travel_concierge()

# #         # Create tasks
# #         identify_task = tasks.identify_task(city_selector, self.origin, self.destination, self.interests, self.date_range)
# #         gather_task = tasks.gather_task(local_expert, self.origin, self.interests, self.date_range)
# #         plan_task = tasks.plan_task(concierge, self.origin, self.interests, self.date_range)

# #         # Combine into a crew
# #         crew = Crew(
# #             agents=[city_selector, local_expert, concierge],
# #             tasks=[identify_task, gather_task, plan_task],
# #             verbose=True,
# #         )

# #         result = crew.kickoff()

# #         if hasattr(result, "output_text"):
# #             return result.output_text
# #         elif hasattr(result, "final_output"):
# #             return result.final_output
# #         return str(result)

# #     def run(self):
# #         """Run trip generation."""
# #         llm = self.llm_handler.create_llm()
# #         return self._generate_itinerary(llm)


# # # ============================================================
# # # 🌐 API ROUTES
# # # ============================================================

# # @app.get("/")
# # async def root():
# #     return {
# #         "message": "Welcome to VacAIgent API 🚀",
# #         "docs_url": "/docs",
# #         "version": "1.2.0"
# #     }


# # @app.post("/api/v1/plan-trip", response_model=TripResponse)
# # async def plan_trip(
# #     trip_request: TripRequest,
# #     settings: Settings = Depends(validate_api_keys)
# # ):
# #     """Generate a personalized travel itinerary."""
# #     logger.info(f"🧳 Received trip planning request: {trip_request}")

# #     if trip_request.end_date <= trip_request.start_date:
# #         raise HTTPException(status_code=400, detail="End date must be after start date")

# #     date_range = f"{trip_request.start_date} to {trip_request.end_date}"

# #     try:
# #         trip_crew = TripCrew(
# #             trip_request.origin,
# #             trip_request.destination,
# #             date_range,
# #             trip_request.interests,
# #             settings
# #         )

# #         itinerary = trip_crew.run()

# #         logger.info("✅ Trip itinerary successfully generated.")
# #         return TripResponse(
# #             status="success",
# #             message="Trip plan generated successfully",
# #             itinerary=itinerary
# #         )

# #     except HTTPException as e:
# #         logger.error(f"❌ HTTP Error: {e.detail}")
# #         raise e
# #     except Exception as e:
# #         logger.exception("❌ Unexpected error during itinerary generation.")
# #         return TripResponse(
# #             status="error",
# #             message="Failed to generate trip plan",
# #             error=str(e)
# #         )


# # @app.get("/api/v1/health")
# # async def health_check():
# #     """Health check endpoint."""
# #     return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# # # ============================================================
# # # 🚀 ENTRY POINT
# # # ============================================================
# # if __name__ == "__main__":
# #     import uvicorn
# #     logger.info("✅ Starting VacAIgent FastAPI server on port 8000...")
# #     uvicorn.run(app, host="0.0.0.0", port=8000)
    


# # with redis caching added for high traffic scenarios handle multiple requests for same trip plans in below

# import os
# import logging
# import traceback
# from datetime import date, datetime
# from typing import Optional
# import hashlib
# import json
# import time
# from contextlib import contextmanager

# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel, Field
# from dotenv import load_dotenv

# import redis
# from crewai import Crew, LLM
# from trip_agents import TripAgents
# from trip_tasks import TripTasks

# # ============================================================
# # 🌍 ENVIRONMENT SETUP
# # ============================================================
# load_dotenv()

# # ============================================================
# # 🔧 LOGGING CONFIGURATION
# # ============================================================
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(message)s",
#     handlers=[
#         # logging.FileHandler("vacAIgent_api.log"),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)
# logger.info("🚀 VacAIgent API starting (OpenAI only)")

# # ============================================================
# # 🌐 FASTAPI CONFIGURATION
# # ============================================================
# app = FastAPI(
#     title="VacAIgent API",
#     description="AI-powered travel planning API using CrewAI and OpenAI with Redis caching",
#     version="1.3.0"
# )

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # ⚠️ Replace with trusted origins in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ============================================================
# # 📦 DATA MODELS
# # ============================================================
# class TripRequest(BaseModel):
#     origin: str = Field(..., example="Bangalore, India")
#     destination: str = Field(..., example="Krabi, Thailand")
#     start_date: date = Field(..., example="2025-06-01")
#     end_date: date = Field(..., example="2025-06-10")
#     interests: str = Field(..., example="2 adults who love swimming, hiking, shopping, and local food")

# class TripResponse(BaseModel):
#     status: str
#     message: str
#     itinerary: Optional[str] = None
#     error: Optional[str] = None

# # ============================================================
# # ⚙️ SETTINGS AND DEPENDENCIES
# # ============================================================
# class Settings:
#     def __init__(self):
#         self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#         self.SERPER_API_KEY = os.getenv("SERPER_API_KEY")
#         self.BROWSERLESS_API_KEY = os.getenv("BROWSERLESS_API_KEY")
#         self.REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# @lru_cache()
# def get_settings():
#     return Settings()

# def validate_api_keys(settings: Settings = Depends(get_settings)):
#     required_keys = {
#         'OPENAI_API_KEY': settings.OPENAI_API_KEY,
#         'SERPER_API_KEY': settings.SERPER_API_KEY,
#         'BROWSERLESS_API_KEY': settings.BROWSERLESS_API_KEY
#     }
#     missing = [k for k, v in required_keys.items() if not v]
#     if missing:
#         logger.error(f"❌ Missing API keys: {', '.join(missing)}")
#         raise HTTPException(status_code=500, detail=f"Missing required API keys: {', '.join(missing)}")
#     return settings

# # ============================================================
# # 🧩 REDIS CACHE HANDLER
# # ============================================================
# def get_redis_client(settings: Settings):
#     return redis.from_url(settings.REDIS_URL, decode_responses=True)

# def get_cache_key(origin, destination, interests, date_range):
#     key_str = f"{origin}-{destination}-{interests}-{date_range}"
#     return hashlib.sha256(key_str.encode()).hexdigest()

# @contextmanager
# def redis_lock(redis_client, key, timeout=30):
#     lock_key = f"lock:{key}"
#     got_lock = redis_client.set(lock_key, "1", nx=True, ex=timeout)
#     try:
#         if got_lock:
#             yield True
#         else:
#             yield False
#     finally:
#         if got_lock:
#             redis_client.delete(lock_key)

# # ============================================================
# # 🧩 LLM HANDLER (OpenAI only)
# # ============================================================
# class OpenAILLMHandler:
#     def __init__(self, settings: Settings):
#         self.openai_key = settings.OPENAI_API_KEY

#     def create_llm(self):
#         try:
#             logger.info("🧠 Initializing OpenAI LLM (gpt-5-mini)...")
#             return LLM(model="gpt-5-mini", api_key=self.openai_key)
#         except Exception as e:
#             logger.critical(f"❌ Failed to initialize OpenAI LLM: {e}")
#             traceback.print_exc()
#             raise HTTPException(status_code=500, detail=f"Failed to initialize OpenAI LLM: {e}")

# # ============================================================
# # 🧳 TRIP CREW LOGIC
# # ============================================================
# class TripCrew:
#     def __init__(self, origin, destination, date_range, interests, settings: Settings):
#         self.origin = origin
#         self.destination = destination
#         self.date_range = date_range
#         self.interests = interests
#         self.llm_handler = OpenAILLMHandler(settings)

#     def _generate_itinerary(self, llm):
#         agents = TripAgents(llm=llm)
#         tasks = TripTasks()

#         city_selector = agents.city_selection_agent()
#         local_expert = agents.local_expert()
#         concierge = agents.travel_concierge()

#         identify_task = tasks.identify_task(city_selector, self.origin, self.destination, self.interests, self.date_range)
#         gather_task = tasks.gather_task(local_expert, self.origin, self.interests, self.date_range)
#         plan_task = tasks.plan_task(concierge, self.origin, self.interests, self.date_range)

#         crew = Crew(
#             agents=[city_selector, local_expert, concierge],
#             tasks=[identify_task, gather_task, plan_task],
#             verbose=True,
#         )

#         result = crew.kickoff()
#         if hasattr(result, "output_text"):
#             return result.output_text
#         elif hasattr(result, "final_output"):
#             return result.final_output
#         return str(result)

#     def run(self):
#         llm = self.llm_handler.create_llm()
#         return self._generate_itinerary(llm)

# # ============================================================
# # 🌐 API ROUTES
# # ============================================================
# @app.get("/")
# async def root():
#     return {"message": "Welcome to VacAIgent API 🚀", "docs_url": "/docs", "version": "1.3.0"}

# @app.post("/api/v1/plan-trip", response_model=TripResponse)
# async def plan_trip(trip_request: TripRequest, settings: Settings = Depends(validate_api_keys)):
#     logger.info(f"🧳 Received trip planning request: {trip_request}")

#     if trip_request.end_date <= trip_request.start_date:
#         raise HTTPException(status_code=400, detail="End date must be after start date")

#     date_range = f"{trip_request.start_date} to {trip_request.end_date}"
#     cache_key = get_cache_key(trip_request.origin, trip_request.destination, trip_request.interests, date_range)

#     redis_client = get_redis_client(settings)

#     # ✅ Check cache first
#     cached_result = redis_client.get(cache_key)
#     if cached_result:
#         logger.info("⚡ Returning cached itinerary result")
#         return TripResponse(
#             status="success",
#             message="Trip plan retrieved from cache",
#             itinerary=cached_result
#         )

#     try:
#         trip_crew = TripCrew(
#             trip_request.origin,
#             trip_request.destination,
#             date_range,
#             trip_request.interests,
#             settings
#         )

#         # ✅ Redis lock to prevent simultaneous generation of same itinerary
#         with redis_lock(redis_client, cache_key) as locked:
#             if locked:
#                 itinerary = trip_crew.run()
#                 redis_client.set(cache_key, itinerary, ex=86400)  # cache for 24 hours
#             else:
#                 # Wait until another request finishes generating
#                 time.sleep(2)
#                 itinerary = redis_client.get(cache_key) or trip_crew.run()
#                 redis_client.set(cache_key, itinerary, ex=86400)

#         logger.info("✅ Trip itinerary successfully generated and cached.")
#         return TripResponse(
#             status="success",
#             message="Trip plan generated successfully",
#             itinerary=itinerary
#         )

#     except HTTPException as e:
#         logger.error(f"❌ HTTP Error: {e.detail}")
#         raise e
#     except Exception as e:
#         logger.exception("❌ Unexpected error during itinerary generation.")
#         return TripResponse(
#             status="error",
#             message="Failed to generate trip plan",
#             error=str(e)
#         )

# @app.get("/api/v1/health")
# async def health_check():
#     return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# # ============================================================
# # 🚀 ENTRY POINT
# # ============================================================
# if __name__ == "__main__":
#     import uvicorn
#     logger.info("✅ Starting VacAIgent FastAPI server on port 8000...")
#     uvicorn.run(app, host="0.0.0.0", port=8000)
    




# with redis caching added for high traffic scenarios handle multiple requests for same trip plans in below

import os
import sys
import logging
import traceback
from datetime import date, datetime
from typing import Optional
import hashlib
import json
import time
from contextlib import contextmanager
from functools import lru_cache

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

import redis
from crewai import Crew, LLM
from trip_agents import TripAgents
from trip_tasks import TripTasks

# ============================================================
# 🌍 ENVIRONMENT SETUP
# ============================================================
load_dotenv()

# 🛠 Ensure stdout and logging use UTF-8 to support emojis on Windows & Linux
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)
logger.info("🚀 VacAIgent API starting (OpenAI only)")

# ============================================================
# 🌐 FASTAPI CONFIGURATION
# ============================================================
app = FastAPI(
    title="VacAIgent API",
    description="AI-powered travel planning API using CrewAI and OpenAI with Redis caching",
    version="1.3.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Replace with trusted origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 📦 DATA MODELS
# ============================================================
class TripRequest(BaseModel):
    origin: str = Field(..., example="Bangalore, India")
    destination: str = Field(..., example="Krabi, Thailand")
    start_date: date = Field(..., example="2025-06-01")
    end_date: date = Field(..., example="2025-06-10")
    interests: str = Field(..., example="2 adults who love swimming, hiking, shopping, and local food")

class TripResponse(BaseModel):
    status: str
    message: str
    itinerary: Optional[str] = None
    error: Optional[str] = None

# ============================================================
# ⚙️ SETTINGS AND DEPENDENCIES
# ============================================================
class Settings:
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.SERPER_API_KEY = os.getenv("SERPER_API_KEY")
        self.BROWSERLESS_API_KEY = os.getenv("BROWSERLESS_API_KEY")
        self.REDIS_URL = os.getenv("REDIS_URL")

@lru_cache()
def get_settings():
    return Settings()

def validate_api_keys(settings: Settings = Depends(get_settings)):
    required_keys = {
        'OPENAI_API_KEY': settings.OPENAI_API_KEY,
        'SERPER_API_KEY': settings.SERPER_API_KEY,
        'BROWSERLESS_API_KEY': settings.BROWSERLESS_API_KEY
    }
    missing = [k for k, v in required_keys.items() if not v]
    if missing:
        logger.error(f"❌ Missing API keys: {', '.join(missing)}")
        raise HTTPException(status_code=500, detail=f"Missing required API keys: {', '.join(missing)}")
    return settings

# ============================================================
# 🧩 REDIS CACHE HANDLER
# ============================================================
def get_redis_client(settings: Settings):
    return redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_cache_key(origin, destination, interests, date_range):
    key_str = f"{origin}-{destination}-{interests}-{date_range}"
    return hashlib.sha256(key_str.encode()).hexdigest()

@contextmanager
def redis_lock(redis_client, key, timeout=30):
    lock_key = f"lock:{key}"
    got_lock = redis_client.set(lock_key, "1", nx=True, ex=timeout)
    try:
        if got_lock:
            yield True
        else:
            yield False
    finally:
        if got_lock:
            redis_client.delete(lock_key)

# ============================================================
# 🧩 LLM HANDLER (OpenAI only)
# ============================================================
class OpenAILLMHandler:
    def __init__(self, settings: Settings):
        self.openai_key = settings.OPENAI_API_KEY

    def create_llm(self):
        try:
            logger.info("🧠 Initializing OpenAI LLM (gpt-5-mini)...")
            return LLM(model="gpt-5-mini", api_key=self.openai_key)
        except Exception as e:
            logger.critical(f"❌ Failed to initialize OpenAI LLM: {e}")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Failed to initialize OpenAI LLM: {e}")

# ============================================================
# 🧳 TRIP CREW LOGIC
# ============================================================
class TripCrew:
    def __init__(self, origin, destination, date_range, interests, settings: Settings):
        self.origin = origin
        self.destination = destination
        self.date_range = date_range
        self.interests = interests
        self.llm_handler = OpenAILLMHandler(settings)

    def _generate_itinerary(self, llm):
        agents = TripAgents(llm=llm)
        tasks = TripTasks()

        city_selector = agents.city_selection_agent()
        local_expert = agents.local_expert()
        concierge = agents.travel_concierge()

        identify_task = tasks.identify_task(city_selector, self.origin, self.destination, self.interests, self.date_range)
        gather_task = tasks.gather_task(local_expert, self.origin, self.interests, self.date_range)
        plan_task = tasks.plan_task(concierge, self.origin, self.interests, self.date_range)

        crew = Crew(
            agents=[city_selector, local_expert, concierge],
            tasks=[identify_task, gather_task, plan_task],
            verbose=True,
        )

        result = crew.kickoff()
        if hasattr(result, "output_text"):
            return result.output_text
        elif hasattr(result, "final_output"):
            return result.final_output
        return str(result)

    def run(self):
        llm = self.llm_handler.create_llm()
        return self._generate_itinerary(llm)

# ============================================================
# 🌐 API ROUTES
# ============================================================
@app.get("/")
async def root():
    return {"message": "Welcome to VacAIgent API 🚀", "docs_url": "/docs", "version": "1.3.0"}

@app.post("/api/v1/plan-trip", response_model=TripResponse)
async def plan_trip(trip_request: TripRequest, settings: Settings = Depends(validate_api_keys)):
    logger.info(f"🧳 Received trip planning request: {trip_request}")

    if trip_request.end_date <= trip_request.start_date:
        raise HTTPException(status_code=400, detail="End date must be after start date")

    date_range = f"{trip_request.start_date} to {trip_request.end_date}"
    cache_key = get_cache_key(trip_request.origin, trip_request.destination, trip_request.interests, date_range)

    redis_client = get_redis_client(settings)

    # ✅ Check cache first
    cached_result = redis_client.get(cache_key)
    if cached_result:
        logger.info("⚡ Returning cached itinerary result")
        return TripResponse(
            status="success",
            message="Trip plan retrieved from cache",
            itinerary=cached_result
        )

    try:
        trip_crew = TripCrew(
            trip_request.origin,
            trip_request.destination,
            date_range,
            trip_request.interests,
            settings
        )

        # ✅ Redis lock to prevent simultaneous generation of same itinerary
        with redis_lock(redis_client, cache_key) as locked:
            if locked:
                itinerary = trip_crew.run()
                redis_client.set(cache_key, itinerary, ex=86400)  # cache for 24 hours
            else:
                # Wait until another request finishes generating
                time.sleep(2)
                itinerary = redis_client.get(cache_key) or trip_crew.run()
                redis_client.set(cache_key, itinerary, ex=86400)

        logger.info("✅ Trip itinerary successfully generated and cached.")
        return TripResponse(
            status="success",
            message="Trip plan generated successfully",
            itinerary=itinerary
        )

    except HTTPException as e:
        logger.error(f"❌ HTTP Error: {e.detail}")
        raise e
    except Exception as e:
        logger.exception("❌ Unexpected error during itinerary generation.")
        return TripResponse(
            status="error",
            message="Failed to generate trip plan",
            error=str(e)
        )

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# ============================================================
# 🚀 ENTRY POINT
# ============================================================
if __name__ == "__main__":
    import uvicorn
    logger.info("✅ Starting VacAIgent FastAPI server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
    