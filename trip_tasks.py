# from crewai import Task
# from textwrap import dedent

# class TripTasks():
#     def __validate_inputs(self, origin, cities, interests, date_range):
#         if not origin or not cities or not interests or not date_range:
#             raise ValueError("All input parameters must be provided")
#         return True

#     # 🧭 STEP 1: Identify the best city
#     def identify_task(self, agent, origin, cities, interests, range):
#         self.__validate_inputs(origin, cities, interests, range)

#         return Task(
#             description=dedent(f"""
#                 🧠 **Role**: You are an expert *AI Travel Advisor*.

#                 ✈️ **Goal**: From the given city list {cities}, 
#                 choose the **most suitable destination** for a trip 
#                 starting from **{origin}** during **{range}**, 
#                 perfectly aligned with the traveler’s interest in **{interests}**.

#                 💡 **Consider these key factors**:
#                 1. Weather suitability for {interests}
#                 2. Major attractions that match {interests}
#                 3. Estimated travel cost (flight + 3-night hotel average)

#                 🗂️ **Your Output Must Include**:
#                 - Highlighted destination (with a clear reason for choice)
#                 - Top 3 attractions
#                 - Estimated overall trip cost (USD or local currency)

#                 {self.__tip_section()}
#             """),
#             expected_output="A short, formatted travel report recommending one city with top attractions and estimated total cost.",
#             agent=agent,
#             output_key="chosen_city"
#         )

#     # 🏙️ STEP 2: Create a City Guide
#     def gather_task(self, agent, origin, interests, range):
#         return Task(
#             description=dedent(f"""
#                 🌍 **Role**: You are a *Travel Insights Curator*.

#                 🎯 **Goal**: Create a **concise city guide** for the selected city (‘chosen_city’) 
#                 that gives travelers a sense of excitement and readiness.

#                 🗺️ **Include These Sections**:
#                 - ✨ **City Overview**: 2–3 engaging sentences that capture the city’s vibe.
#                 - 🏛️ **Top 5 Attractions**: Each with a short reason why it’s worth visiting.
#                 - 🍽️ **Top 3 Food Experiences**: Must-try local dishes or restaurants.
#                 - 🎉 **Seasonal Highlights**: Events, festivals, or activities during **{range}**.

#                 Keep it **clear, useful, and traveler-friendly** — like a professional brochure.

#                 {self.__tip_section()}
#             """),
#             expected_output="A practical, engaging city guide with overview, attractions, food, and events.",
#             agent=agent,
#             depends_on=["chosen_city"],
#             output_key="city_guide"
#         )

#     # 🗓️ STEP 3: Design the Itinerary
#     def plan_task(self, agent, origin, interests, range):
#         return Task(
#             description=dedent(f"""
#                 🧭 **Role**: You are a *Travel Experience Designer*.

#                 🎯 **Goal**: Using the ‘city_guide’, create a **3–5 day personalized itinerary** 
#                 for a traveler departing from **{origin}** during **{range}**, 
#                 focused on **{interests}**.

#                 📋 **Itinerary Structure**:
#                 - 🕰️ **Daily Activities** (morning, afternoon, evening)
#                 - 🍴 **Recommended Restaurants** (1–2 per day)
#                 - 🏨 **Accommodation Suggestion**
#                 - 💰 **Estimated Daily Cost**

#                 💵 **Budget Breakdown**:
#                 - Flights ✈️
#                 - Hotels 🏨
#                 - Meals 🍜
#                 - Local Transport 🚗
#                 - Attractions 🎟️
#                 - Total 💵

#                 🆓 **Free Activities**: Include scenic or cultural spots with no entry fee.  
#                 💸 **Paid Activities**: List approximate costs.  
#                 🛡️ **Travel Tips & Safety Notes**: Health, customs, and smart local behavior.

#                 Format it neatly with clear titles and short actionable bullet points.  
#                 Focus on making it *feel like a real trip plan.*

#                 {self.__tip_section()}
#             """),
#             expected_output="A well-formatted 3–5 day travel itinerary with activities, food, accommodation, budget, and safety tips.",
#             agent=agent,
#             depends_on=["chosen_city", "city_guide"],
#             output_key="final_itinerary"
#         )

#     # ✨ Motivational Tip Section
#     def __tip_section(self):
#         return dedent("""
#             🚀 **Tip**: Make the output visually clear — use section titles, emojis, and bullet points.  
#             Always ensure readability, excitement, and travel clarity.  
#             This plan should inspire the traveler to pack their bags right away!
#         """)
# ============================================================






# from crewai import Task
# from textwrap import dedent

# class TripTasks():
#     def __validate_inputs(self, origin, cities, interests, date_range):
#         if not origin or not cities or not interests or not date_range:
#             raise ValueError("All input parameters must be provided")
#         return True

#     # 🧭 STEP 1: Identify the best city (FAST VERSION)
#     def identify_task(self, agent, origin, cities, interests, range):
#         self.__validate_inputs(origin, cities, interests, range)

#         return Task(
#             description=dedent(f"""
#                 Role: Expert Travel Advisor.

#                 Goal:
#                 From city list {cities}, select the best destination for a trip 
#                 starting from {origin} during {range}, matching interests: {interests}.

#                 Evaluate:
#                 - Weather suitability
#                 - Attractions related to {interests}
#                 - Travel cost (flight + 3-night hotel)

#                 Output:
#                 - Final chosen city + clear reason
#                 - Top 3 attractions
#                 - Estimated total trip cost
#             """),
#             expected_output="A short travel recommendation with chosen city, attraction summary, and cost estimate.",
#             agent=agent,
#             output_key="chosen_city",
#             # TOKEN LIMITS FOR SPEED
#             max_output_tokens=800
#         )

#     # 🏙️ STEP 2: Create a City Guide (FAST VERSION)
#     def gather_task(self, agent, origin, interests, range):
#         return Task(
#             description=dedent(f"""
#                 Role: Travel Insights Curator.

#                 Goal:
#                 Create a concise city guide for 'chosen_city'.

#                 Include:
#                 - 2–3 sentence city overview
#                 - Top 5 attractions (short reason each)
#                 - Top 3 food experiences
#                 - Seasonal highlights during {range}

#                 Keep it concise, structured and easy to read.
#             """),
#             expected_output="A clear, readable city guide with overview, attractions, food, and seasonal tips.",
#             agent=agent,
#             depends_on=["chosen_city"],
#             output_key="city_guide",
#             max_output_tokens=900
#         )

#     # 🗓️ STEP 3: Design the Itinerary (FAST VERSION)
#     def plan_task(self, agent, origin, interests, range):
#         return Task(
#             description=dedent(f"""
#                 Role: Travel Itinerary Designer.

#                 Goal:
#                 Using 'city_guide', create a 3–5 day itinerary for a traveler 
#                 departing from {origin} during {range}, focused on {interests}.

#                 Include:
#                 - Daily activities (morning, afternoon, evening)
#                 - 1–2 restaurants per day
#                 - Accommodation suggestion
#                 - Estimated daily cost + full budget breakdown
#                 - Free & paid activities with approx costs
#                 - Travel tips + safety notes

#                 Format clearly with titles + bullet points.
#             """),
#             expected_output="A clean, structured 3–5 day itinerary with activities, food, budget and tips.",
#             agent=agent,
#             depends_on=["chosen_city", "city_guide"],
#             output_key="final_itinerary",
#             max_output_tokens=1800  # Main heavy output — still controlled
#         )
#     def __tip_section(self):
#         return dedent("""
#             ✨ **Motivational Tip**

#             🚀 Make the output visually clear — use section titles, emojis, and bullet points.  
#             🌍 Ensure readability, excitement, and travel clarity.  
#             🧳 This plan should inspire the traveler to pack their bags right away!
#         """)
       


from crewai import Task
from textwrap import dedent

class TripTasks():

    # 🔍 Input Validator
    def __validate_inputs(self, origin, cities, interests, date_range):
        if not origin or not cities or not interests or not date_range:
            raise ValueError("All input parameters must be provided")
        return True

    # ✨ Motivational Tip Section
    def __tip_section(self):
        return dedent("""
            ✨ **Motivational Tip**

            🚀 Make the output visually clear — use section titles, emojis, and bullet points.  
            🌍 Ensure readability, excitement, and travel clarity.  
            🧳 This plan should inspire the traveler to pack their bags right away!
        """)

    # 🧭 STEP 1: Identify the Best City (FAST VERSION)
    def identify_task(self, agent, origin, cities, interests, range):
        self.__validate_inputs(origin, cities, interests, range)

        return Task(
            description=dedent(f"""
                Role: Expert Travel Advisor.

                Goal:
                From city list {cities}, select the best destination for a trip 
                starting from {origin} during {range}, matching interests: {interests}.

                Evaluate:
                - Weather suitability
                - Attractions related to {interests}
                - Travel cost (flight + 3-night hotel)

                Output:
                - Final chosen city + clear reason
                - Top 3 attractions
                - Estimated total trip cost

                {self.__tip_section()}
            """),
            expected_output="A short travel recommendation with chosen city, attraction summary, and cost estimate.",
            agent=agent,
            output_key="chosen_city",
            max_output_tokens=800  # Fast output
        )

    # 🏙️ STEP 2: Create a City Guide (FAST VERSION)
    def gather_task(self, agent, origin, interests, range):
        return Task(
            description=dedent(f"""
                Role: Travel Insights Curator.

                Goal:
                Create a concise city guide for 'chosen_city'.

                Include:
                - 2–3 sentence city overview
                - Top 5 attractions (short reason each)
                - Top 3 food experiences
                - Seasonal highlights during {range}

                Keep it concise, structured and easy to read.

                {self.__tip_section()}
            """),
            expected_output="A clear, readable city guide with overview, attractions, food, and seasonal tips.",
            agent=agent,
            depends_on=["chosen_city"],
            output_key="city_guide",
            max_output_tokens=900
        )

    # 🗓️ STEP 3: Design the Itinerary (FAST VERSION)
    # def plan_task(self, agent, origin, interests, range):
    #     return Task(
    #         description=dedent(f"""
    #             Role: Travel Itinerary Designer.

    #             Goal:
    #             Using 'city_guide', create a 3–5 day itinerary for a traveler 
    #             departing from {origin} during {range}, focused on {interests}.

    #             Include:
    #             - Daily activities (morning, afternoon, evening)
    #             - 1–2 restaurants per day
    #             - Accommodation suggestion
    #             - Estimated daily cost + full budget breakdown
    #             - Free & paid activities with approx costs
    #             - Travel tips + safety notes

    #             Format clearly with titles + bullet points.

    #             {self.__tip_section()}
    #         """),
    #         expected_output="A clean, structured 3–5 day itinerary with activities, food, budget and tips.",
    #         agent=agent,
    #         depends_on=["chosen_city", "city_guide"],
    #         output_key="final_itinerary",
    #         max_output_tokens=1800  # Heavy output but controlled
    #     )

    def plan_task(self, agent, origin, interests, range):
        return Task(
            description=dedent(f"""
                Role: Travel Itinerary Designer.

                Goal:
                Using 'city_guide', create a 3–5 day itinerary for a traveler 
                departing from {origin} during {range}, focused on {interests}.

                Include:
                - Daily activities (morning, afternoon, evening)
                - 1–2 restaurants per day
                - Accommodation suggestion
                - Estimated daily cost + full budget breakdown
                - Free & paid activities with approx costs
                - **A comparison table that separates FREE vs PAID activities**  
                - Travel tips + safety notes

                Table Format Requirement:
                | Activity | Type (Free/Paid) | Approx Cost | Notes |
                |----------|------------------|-------------|-------|

                Format clearly with titles + bullet points.

                {self.__tip_section()}
            """),
            expected_output="A clean, structured 3–5 day itinerary with activities, food, budget, tips, and a FREE vs PAID table.",
            agent=agent,
            depends_on=["chosen_city", "city_guide"],
            output_key="final_itinerary",
            max_output_tokens=1800
        )