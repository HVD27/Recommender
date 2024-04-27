from pymongo import MongoClient
from langchain.chains import RetrieverGeneratorChain
from langchain.retrievers import ElasticsearchRetriever
from langchain.generators import OpenAIGenerator
from elasticsearch import Elasticsearch, ElasticsearchException
import openai

# Initialize MongoDB and Elasticsearch clients
mongo_client = MongoClient('localhost', 27017)
es = Elasticsearch()

# Error handling for MongoDB connection
def get_user_preferences(username):
    try:
        db = mongo_client['recommendation_system']
        user_data = db.users.find_one({"username": username})
        if user_data and 'preferences' in user_data:
            preferences = user_data['preferences']
            return ', '.join(preferences['songs'] + preferences['books'] + preferences['movies'])
        else:
            return None
    except Exception as e:
        print(f"Error accessing MongoDB: {e}")
        return None

# Setup Langchain with Elasticsearch and OpenAI GPT
def setup_langchain():
    try:
        retriever = ElasticsearchRetriever(es_client=es, index_name="media_index")
        generator = OpenAIGenerator(api_key="your-openai-api-key")
        rag_chain = RetrieverGeneratorChain(retriever=retriever, generator=generator)
        return rag_chain
    except Exception as e:
        print(f"Error setting up Langchain: {e}")
        return None

# Generate recommendations using Langchain
def generate_recommendations(chain, query):
    try:
        results = chain.run(query)
        return results
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return "Error in generating recommendations."

# Main function to automate the recommendation process
def main():
    username = "example_user"  # Adapt this to be dynamically set
    user_preferences = get_user_preferences(username)
    if not user_preferences:
        print("No preferences found for the user, or error in fetching data.")
        return

    rag_chain = setup_langchain()
    if not rag_chain:
        print("Failed to setup recommendation engine.")
        return

    recommendations = generate_recommendations(rag_chain, user_preferences)
    print("Recommendations:", recommendations)

if __name__ == "__main__":
    main()
