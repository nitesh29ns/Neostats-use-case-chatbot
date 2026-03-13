import arxiv
from config.config import MAX_RESEARCH_SUGGESTIONS
from utils.logger import lg

lg.info("=============================================================== RESEARCH PAPER SUGGESTIONS ===============================================================")

# Create an Arxiv client
client = arxiv.Client()

def top_3_suggestion(query:str):
    try:
        lg.info("Initializing Reseach paper search")
        # Perform the search
        search = arxiv.Search(
            query=query,
            max_results=MAX_RESEARCH_SUGGESTIONS,
            sort_by=arxiv.SortCriterion.Relevance
        )

        # Fetch results using client.results()
        results = []
        for result in client.results(search):
            paper_info = {
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "url": result.entry_id  # optional: link to paper
            }
            results.append(paper_info)

        # Display results
        # for i, paper in enumerate(results, 1):
        #     print(f"Paper {i}:")
        #     print(f"Title: {paper['title']}")
        #     print(f"Authors: {', '.join(paper['authors'])}")
        #     print(f"URL: {paper['url']}")
        #     print("-" * 80)

        lg.info("Reseach paper search successfully")
    
        return results
    except Exception as e:
        lg.error(f"Research Retrieved failed: {str(e)}")
        raise e