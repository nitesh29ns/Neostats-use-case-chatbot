from firecrawl import Firecrawl
from utils.logger import lg
from config.config import WEB_SEARCH_API


lg.info("=============================================================== WEB SEARCH ===============================================================")

app = Firecrawl(api_key=WEB_SEARCH_API)


def web_search(query:str,output_type:str)->str :
    try:
        lg.info("Initializing web search")

        if output_type == "Concise":
            chars = 1000
        else:
            chars = 3000

        scrape_opts = {
            "formats": ["markdown"],
            "max_chars": chars
        }

        results = app.search(
            query=query,
            limit=1,
            scrape_options=scrape_opts
        )

        lg.info("web search initialized successfully")

        return results.web[0].markdown
    
    except Exception as e:
        lg.error(f"Data from vectordb Retrieved failed: {str(e)}")
        raise e