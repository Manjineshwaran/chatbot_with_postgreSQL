
import re
from config import groq_model
from database import create_tables, save_data, fetch_user_data
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage

create_tables()
memory = ConversationBufferMemory(return_messages=True)

def chat_with_groq(username, user_input):
    memory.chat_memory.add_user_message(user_input)
    goals_text, user_info_text = fetch_user_data(username)

    messages = [
        {"role": "system", "content": "You are an AI assistant that helps users based on their stored information."},
        {"role": "user", "content": f"User info: {user_info_text}"},
        {"role": "user", "content": f"User goals: {goals_text}"}
    ]

    for msg in memory.chat_memory.messages:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        messages.append({"role": role, "content": msg.content})
    #print("Messages:", messages)  

    try:
        ai_response = groq_model.invoke(messages).content  # ✅ Corrected Method

        #ai_response = groq_model(messages).content

        memory.chat_memory.add_ai_message(ai_response)
        return ai_response
    except Exception as e:
        return f"Error: Failed to connect to Groq API. Details: {e}"

def chatbot():
    print("Hello! What's your name?")
    username = input("Your Name: ").strip()

    print("\nWould you like to enter (1) Goals & Weightages or (2) Generic Data? Enter 1 or 2: or enter to skip")
    choice = input("Your Choice: ").strip()

    if choice == "1":
        goals = []
        while True:
            goal = input("Enter a key goal (or type 'done' to finish): ").strip()
            if goal.lower() == 'done':
                break
            weightage = int(input(f"Enter weightage for goal: "))
            goals.append((goal, weightage))

        total_weight = sum(w[1] for w in goals)
        while total_weight != 100:
            print("Total weightage must be 100%. Please re-enter only the weightages.")
            for i, (goal, _) in enumerate(goals):
                weightage = int(input(f"Enter weightage for '{goal}': "))
                goals[i] = (goal, weightage)
            total_weight = sum(w[1] for w in goals)
        for goal, weightage in goals:
            save_data("user_goals", {"username": username, "goal": goal, "weightage": weightage})
        print("Thank you! Your goals have been saved.")

    elif choice == "2":

        def is_valid_email(email):
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            return re.match(pattern, email)
        def is_valid_phone(phone):
            pattern = r'^\+?\d{7,15}$'  # Allows optional + at the start and 7-15 digits
            return re.match(pattern, phone)
        def is_valid_country(country):
            return country.isalpha()
        name = input("Enter your name: ").strip()
        while True:
            
            email = input("Enter your email: ").strip()
            if not is_valid_email(email):
                print("Invalid email. Please enter a valid email.")
                continue
            break
        while True:
            phone = input("Enter your phone number: ").strip()
            if not is_valid_phone(phone):
                print("Invalid phone number. Enter a valid phone number with digits only.")
                continue
            break
        while True:
            country = input("Enter your country: ").strip()
            if not is_valid_country(country):
                print("Invalid country name. Enter only letters (no numbers or symbols).")
                continue
            break
        save_data("user_info", {"username": username, "name": name, "email": email, "phone": phone,"country":country})  
        print("Your information has been saved.")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("AI: Goodbye!")
            break
        
        response = chat_with_groq(username, user_input)
        print(f"AI: {response}")

if __name__ == "__main__":
    chatbot()
