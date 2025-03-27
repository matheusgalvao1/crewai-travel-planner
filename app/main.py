import json
from travel_planner_crew import TravelPlannerCrew

# Create the crew without parameters
travel_crew = TravelPlannerCrew()

# Run the crew and pass inputs only during kickoff
result = travel_crew.travel_crew().kickoff(inputs={
    "city": "Porto",
    "days": 2,
    "num_attractions": 3
})

# Extract outputs from the crew result
raw_output = result.raw            # Unstructured full text output
json_output = result.json_dict     # JSON output as a dictionary (if available)
pydantic_output = result.pydantic  # Parsed and validated output (TravelItinerary)

# Print raw output
print("=== Raw Output ===")
print(raw_output)

# Print JSON output if available
print("\n=== JSON Output ===")
if json_output:
    print(json.dumps(json_output, indent=2))
else:
    print("No JSON output available.")

# Print Pydantic output if available
print("\n=== Pydantic Output ===")
if pydantic_output:
    # pydantic_output is a TravelItinerary object; you can access its attributes directly.
    print(pydantic_output)
else:
    print("No Pydantic output available.")