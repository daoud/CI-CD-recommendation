import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.knowledge.json import JSONKnowledgeBase
from phi.vectordb.pgvector import PgVector
from phi.tools.googlesearch import GoogleSearch
from phi.model.groq import Groq
from phi.embedder.sentence_transformer import SentenceTransformerEmbedder

# === Load environment variables from .env file ===
load_dotenv()

# === SentenceTransformer embedder ===
sentence_embedder = SentenceTransformerEmbedder(
    model="multi-qa-mpnet-base-dot-v1",  # Suitable for semantic search
    dimensions=768
)

# === Local Vector DB with JSON knowledge ===
knowledge_base = JSONKnowledgeBase(
    path="user_info.json",
    vector_db=PgVector(
        table_name="users",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
        embedder=sentence_embedder
    ),
)

# === LLM Model using Groq ===
groq_model = Groq(
    id="deepseek-r1-distill-llama-70b",
    api_key="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",
)

# === Skill Recommender Career Agent ===
career_agent = Agent(
    model=groq_model,
    knowledge=knowledge_base,
    search_knowledge=True,
    tools=[GoogleSearch()],
    description="Career Assistant specializing in skill recommendations and AI Career Coach with local embeddings",
    instructions=[
        "First retrieve user details from the knowledge base",
        "Show previous skills and role of the user from the database",
        "Analyze the user's current skills and job history",
        "Identify emerging trends in their field using Google Search",
        "Recommend 5-7 skills with market demand analysis",
        "Show recommended skills name seperately with new lines as points without any details",
        " OUTPUT FORMAT:",
        " Existing Profile:",
        " id:" ,
        "name:[exact name] ",
        "skill:[comma-separated] ",
        "experience: ",
        "current_role: [text]",
        "company: [text]",
        "location:[text] ",
        "   Recommended Skills:",
        "   - Skill 1",
        "   - Skill 2",
        "Provide concrete examples of how each skill can be applied",
        "Highlight potential career paths for each skill",
        "Maintain an encouraging, professional, and forward-thinking tone",
        "follow above instructions line by line strictly"
    ],
    add_chat_history_to_messages=True,
    add_datetime_to_instructions=True,
    debug_mode=False
)

# === Load knowledge base (first run? set recreate=True) ===
career_agent.knowledge.load(recreate=False)

# === Agent function to get recommendations ===
def get_skill_recommendations(user_name: str):
    query = f"Recommend new career skills for {user_name} based on their profile"
    print(f"\n🔍 Querying career plan for: {user_name}\n")
    career_agent.print_response(query, stream=True)


# === Run if file is executed directly ===
if __name__ == "__main__":
    # Example: Replace with real user name from your JSON file
    get_skill_recommendations("Siddharth Jain")
