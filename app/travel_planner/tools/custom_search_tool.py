from crewai.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchResults


# Create a custom tool by subclassing BaseTool
class CustomSearchTool(BaseTool):
    name: str = "DuckDuckGo Search Tool"
    description: str = "Search the web using DuckDuckGo (free)."

    def _run(self, query: str) -> str:
        # Instantiate the underlying LangChain tool
        ddg_tool = DuckDuckGoSearchResults()
        # Use the tool to perform the search
        response = ddg_tool.invoke(query)
        return response