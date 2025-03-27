import os
import yaml
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
from models import TravelItinerary
from custom_search_tool import CustomSearchTool

@CrewBase
class TravelPlannerCrew:
    """A crew for planning travel itineraries with two agents and two tasks"""
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    agents_config_path = os.path.join(base_dir, "config", "agents.yaml")
    tasks_config_path = os.path.join(base_dir, "config", "tasks.yaml")
    
    def __init__(self):
        with open(self.agents_config_path, 'r') as file:
            self.agents_data = yaml.safe_load(file)
            
        with open(self.tasks_config_path, 'r') as file:
            self.tasks_data = yaml.safe_load(file)
            
        self.search_tool = CustomSearchTool()
        self.web_scrape_tool = ScrapeWebsiteTool()

    @crew
    def travel_crew(self) -> Crew:
        """Creates the simplified travel planning crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=False
        )
    
    @agent
    def researcher(self) -> Agent:
        """Creates a researcher agent that gathers attraction data and local cultural insights"""
        return Agent(
            config=self.agents_data["researcher"],
            tools=[self.search_tool, self.web_scrape_tool]
        )
    
    @agent
    def planner(self) -> Agent:
        """Creates a planner agent that uses the research data to craft an itinerary"""
        return Agent(
            config=self.agents_data["planner"],
            tools=[self.search_tool]
        )
    
    @task
    def research_task(self) -> Task:
        """Creates a combined research task for attractions and local insights"""
        return Task(
            config=self.tasks_data["research_task"],
            agent=self.researcher()
            # Optionally, you could specify an output model if you create one (e.g., CombinedResearch)
        )
    
    @task
    def planning_task(self) -> Task:
        """Creates a planning task that uses the combined research data to build the itinerary"""
        return Task(
            config=self.tasks_data["planning_task"],
            agent=self.planner(),
            context=[self.research_task()],
            output_pydantic=TravelItinerary  # Validates the final itinerary output
        )
