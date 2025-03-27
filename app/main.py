import warnings
warnings.simplefilter("ignore")  # Ignores all warnings

import logging
logging.getLogger("pydantic").setLevel(logging.ERROR)

from travel_planner_crew import TravelPlannerCrew

# Create the crew without parameters
travel_crew = TravelPlannerCrew()

# Run the crew and pass inputs only during kickoff
result = travel_crew.travel_crew().kickoff(inputs={
    "city": "Vigo",
    "days": 2,
    "num_attractions": 3
})

# Access the raw result from the crew
itinerary_data = result.raw

# Print the itinerary data
print(itinerary_data)