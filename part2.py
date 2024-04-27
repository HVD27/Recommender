from pymongo import MongoClient
import numpy as np

mongo_client = MongoClient('localhost', 27017)
db = mongo_client['recommendation_system']

def calculate_personality(preferences):
    personality_traits = {
        'openness': len(preferences['songs']) * 0.5,
        'conscientiousness': len(preferences['books']) * 0.5,
        'extraversion': len(preferences['movies']) * 0.5,
        'agreeableness': (len(preferences['songs']) + len(preferences['books'])) * 0.2,
        'neuroticism': (len(preferences['movies']) + len(preferences['songs'])) * 0.2
    }
    return personality_traits

def find_matches(user_traits, all_users):
    matches = []
    for user in all_users:
        if user['username'] == username:
            continue
        score_diff = np.sqrt(sum((user_traits[trait] - user['personality_traits'][trait])**2 for trait in user_traits))
        if score_diff < 10:  # Example threshold
            matches.append(user['username'])
    return matches

def personality_analysis_and_matching(username):
    user_data = db.users.find_one({"username": username})
    if not user_data:
        print("User not found.")
        return
    
    user_preferences = user_data['preferences']
    user_traits = calculate_personality(user_preferences)
    all_users = list(db.users.find({}))

    matches = find_matches(user_traits, all_users)
    print(f"Matches for {username}: {matches}")

if __name__ == "__main__":
    username = input("Enter your username: ")
    personality_analysis_and_matching(username)
