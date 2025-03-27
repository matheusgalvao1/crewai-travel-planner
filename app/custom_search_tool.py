from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchResults


# Define an input schema for the tool
class DuckDuckGoSearchInput(BaseModel):
    query: str = Field(..., description="The search query.")


# Create a custom tool by subclassing BaseTool
class CustomSearchTool(BaseTool):
    name: str = "DuckDuckGo Search Tool"
    description: str = "Search the web using DuckDuckGo (free)."
    args_schema: Type[BaseModel] = DuckDuckGoSearchInput

    def _run(self, query: str) -> str:
        # Instantiate the underlying LangChain tool
        ddg_tool = DuckDuckGoSearchResults()
        # Use the tool's method to perform the search; adjust if necessary
        response = ddg_tool.invoke(query)
        return response
