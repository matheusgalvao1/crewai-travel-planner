import yaml
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import WebsiteSearchTool
from models import Attraction, TravelItinerary
from custom_search_tool import CustomSearchTool


@CrewBase
class TravelPlannerCrew:
    """A crew for planning travel itineraries with web search and scraping capabilities"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def __init__(self):
        # Load configurations from YAML files
        with open(self.agents_config, 'r') as file:
            self.agents_data = yaml.safe_load(file)
            
        with open(self.tasks_config, 'r') as file:
            self.tasks_data = yaml.safe_load(file)
            
        # Initialize tools
        self.search_tool = CustomSearchTool()
        self.web_rag_tool = WebsiteSearchTool()

    @crew
    def travel_crew(self) -> Crew:
        """Creates the travel planning crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=False
        )
    
    @agent
    def researcher(self) -> Agent:
        """Creates a researcher agent with web search and scraping capabilities"""
        return Agent(
            config=self.agents_data["researcher"],
            tools=[self.search_tool, self.web_rag_tool]
        )
    
    @agent
    def planner(self) -> Agent:
        """Creates a planner agent with web search capability"""
        return Agent(
            config=self.agents_data["planner"],
            tools=[self.search_tool]
        )
    
    @agent
    def local_expert(self) -> Agent:
        """Creates a local expert agent with web search and scraping capabilities"""
        return Agent(
            config=self.agents_data["local_expert"],
            tools=[self.search_tool, self.web_rag_tool]
        )
    
    @task
    def research_task(self) -> Task:
        """Creates a research task that utilizes web search and scraping"""
        return Task(
            config=self.tasks_data["research_task"],
            agent=self.researcher(),
            output_schema=Attraction
        )
    
    @task
    def local_insights_task(self) -> Task:
        """Creates a task for gathering local customs and insights"""
        return Task(
            config=self.tasks_data["local_insights_task"],
            agent=self.local_expert(),
            context=[self.research_task()]
        )
    
    @task
    def planning_task(self) -> Task:
        """Creates a planning task using researched information"""
        return Task(
            config=self.tasks_data["planning_task"],
            agent=self.planner(),
            context=[self.research_task(), self.local_insights_task()],
            output_pydantic=TravelItinerary
        )