from pymongo import MongoClient
import getpass  

db_client = MongoClient('localhost', 27017)
db = db_client['recommendation_system']

def register_or_login(username):
    """ Handle user registration or login """
    user = db.users.find_one({"username": username})
    if not user:
        print("Looks like you're new here! Let's get you set up.")
        preferences = {"songs": [], "books": [], "movies": []}
        db.users.insert_one({"username": username, "preferences": preferences})
        print("Registered successfully.")
    else:
        print("Welcome back!")

def update_preferences(username):
    """ Update user preferences for songs, books, and movies """
    category = input("Which category would you like to update? (songs, books, movies): ")
    if category not in ["songs", "books", "movies"]:
        print("Invalid category!")
        return
    new_prefs = input(f"Enter your favorite {category} (comma separated): ").split(',')
    db.users.update_one({"username": username}, {"$set": {f"preferences.{category}": new_prefs}})
    print("Preferences updated successfully.")

def display_recommendations(username):
    """ Fetch and display recommendations based on user preferences """
    print("Here are your recommendations based on your preferences...")

def display_matches(username):
    """ Find and display matches """
    print("Here are users with similar tastes...")

def main():
    print("Welcome to the Personalized Recommendation and Matching System!")
    username = input("Please enter your username: ")
    register_or_login(username)

    while True:
        print("\nMenu:")
        print("1. Update Preferences")
        print("2. Get Recommendations")
        print("3. Find Matches")
        print("4. Exit")
        choice = input("Please choose an option: ")

        if choice == '1':
            update_preferences(username)
        elif choice == '2':
            display_recommendations(username)
        elif choice == '3':
            display_matches(username)
        elif choice == '4':
            print("Thank you for using our system!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
