import streamlit as st
import sqlite3

# Set the page title
st.set_page_config(page_title="Travel Buddy Dashboard", layout="wide")

# Sidebar for Navigation
st.sidebar.title("🔗 Travel Buddy Sidebar")
st.sidebar.markdown("Navigate through the dashboard:")
nav_option = st.sidebar.radio(
    "Choose a Section", 
    ["Dashboard", "View Database", "Chatbot"]
)

# Connect to Database
conn = sqlite3.connect("travel_buddy.db")
c = conn.cursor()

# Create a Table
def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS travel_data 
                 (client_name TEXT, user_code TEXT, start_date TEXT, end_date TEXT, 
                  budget INTEGER, event_type TEXT, country TEXT, 
                  state TEXT, city TEXT, major_location TEXT, preferences TEXT)''')

create_table()

# Insert Data
def insert_data(client_name, user_code, start_date, end_date, budget, event_type, 
                country, state, city, major_location, preferences):
    c.execute('''INSERT INTO travel_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
              (client_name, user_code, start_date, end_date, budget, event_type, 
               country, state, city, major_location, preferences))
    conn.commit()

# Main Application
if nav_option == "Dashboard":
    st.title("🧳 Travel Buddy Dashboard")
    st.subheader("Plan your perfect travel experience with ease!")

    # User Input Section
    with st.expander("Enter Client Details"):
        client_name = st.text_input("Client Name", placeholder="Enter your name here...")
        user_code = st.text_input("User Code", placeholder="Enter your unique user code...")
        start_date = st.date_input("Start Date", help="Select the trip's starting date.")
        end_date = st.date_input("End Date", help="Select the trip's ending date.")
        st.markdown("---")

    # Travel Preferences
    st.markdown("### User Travel Preferences")
    budget = st.slider("Select Your Budget", min_value=0, max_value=100000, value=50000, step=1000)
    event_type = st.radio("Select the Event Type", 
                          options=["Wedding", "Shopping", "Official Meeting", "Other Events", "Vacation"], 
                          horizontal=True)
    country = st.selectbox("Country", ["India", "USA", "France", "Japan", "Other"])
    state = st.selectbox("State", ["Maharashtra", "California", "Tokyo", "Other"])
    city = st.selectbox("City", ["Mumbai", "Los Angeles", "Paris", "Other"])
    major_location = st.selectbox("Any major location", ["Beach", "Mountain", "Desert", "Other"])
    preferences = st.text_area("User Suggestions and Preferences", 
                                placeholder="Enter any specific preferences (e.g., beach-facing hotel, high-rated food)...")

    # Submit Button
    if st.button("Generate Travel Summary"):
        insert_data(client_name, user_code, start_date, end_date, budget, event_type, 
                    country, state, city, major_location, preferences)
        st.success("Travel Summary Generated and Saved to Database! 🎉")

        # Display the Summary
        st.markdown("### Travel Plan Overview")
        st.write(f"**Client Name:** {client_name}")
        st.write(f"**User Code:** {user_code}")
        st.write(f"**Start Date:** {start_date}")
        st.write(f"**End Date:** {end_date}")
        st.write(f"**Budget:** ₹{budget}")
        st.write(f"**Event Type:** {event_type}")
        st.write(f"**Country:** {country}")
        st.write(f"**State:** {state}")
        st.write(f"**City:** {city}")
        st.write(f"**Major Location:** {major_location}")
        st.write(f"**Preferences:** {preferences}")

elif nav_option == "View Database":
    st.title("📂 View Saved Travel Plans")
    c.execute("SELECT * FROM travel_data")
    rows = c.fetchall()
    if rows:
        for row in rows:
            st.write(f"**Client Name:** {row[0]}, **User Code:** {row[1]}, **Start Date:** {row[2]}, **End Date:** {row[3]}, " 
                     f"**Budget:** ₹{row[4]}, **Event Type:** {row[5]}, **Country:** {row[6]}, **State:** {row[7]}, " 
                     f"**City:** {row[8]}, **Major Location:** {row[9]}, **Preferences:** {row[10]}")
    else:
        st.info("No data found in the database.")

elif nav_option == "Chatbot":
    st.title("💬 Travel Buddy Chatbot")
    st.markdown("Use the chatbot below to interact with Travel Buddy for personalized travel recommendations!")

    from groq import Groq

    def initialize_groq_client(api_key):
        try:
            return Groq(api_key=api_key)
        except Exception as e:
            st.error(f"Error initializing Groq client: {e}")
            return None

    def travel_buddy_response(client, input_text, context=None):
        system_prompt = f"""
You are a highly intelligent assistant for Travel Buddy, an AI-powered sustainable travel platform. Your goal is to provide in-depth, personalized, and eco-conscious travel recommendations to users based on their preferences and travel plans. Your functionalities include:

1. **Personalized Destination Suggestions**:
   - Recommend destinations tailored to user preferences (e.g., budget, event type, preferred activities).
   - Suggest specific attractions and unique experiences for each destination.

2. **Sustainability Insights**:
   - Calculate and display the estimated carbon footprint for travel plans, including flights, accommodations, and activities.
   - Recommend eco-friendly travel options such as green-certified hotels, public transport options, or low-emission flights.

3. **Hotel Recommendations**:
   - Provide a curated list of hotels for the destination, including hotel names, ratings, price ranges, and eco-certifications (if applicable).
   - Highlight accommodations that align with sustainability practices (e.g., energy-efficient, water conservation measures).

4. **Travel Rewards and Discounts**:
   - Inform users about discounts and rewards for choosing sustainable options, such as digital badges or special offers for eco-friendly bookings.

5. **Real-Time Updates**:
   - Share the latest travel trends, seasonal attractions, and events at the chosen destination.
   - Offer insights on the best times to visit, considering factors like weather, crowd levels, and cultural events.

6. **Budget Estimation**:
   - Provide an estimated cost breakdown for the entire travel plan, including transportation, accommodation, food, and activities.
   - Offer options to adjust the plan to fit the user’s budget.

7. **Interactive Features**:
   - Answer user queries related to travel destinations, hotel details, or sustainability practices.
   - Assist in creating a complete travel itinerary, including the duration of stay, nearby attractions, and must-visit spots.

### User Expectations:
- Always ensure your responses are concise, accurate, and supported by reliable data.
- Tailor recommendations to maximize user satisfaction and promote eco-friendly choices.
- Be proactive in suggesting alternatives if user preferences cannot be fully met.

### Example Queries:
- "Suggest a sustainable travel plan for a family vacation in Japan with a budget of $5000."
- "Which hotels in Paris are eco-certified and fit within a $150 per night budget?"
- "What the estimated carbon footprint for a trip from New York to London?"
- "Can you recommend a vacation plan for a beach destination with minimal environmental impact?"
"""
        conversation = f"{context}\nUser: {input_text}\nAssistant:" if context else f"User: {input_text}\nAssistant:"
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": conversation}
                ],
                model="llama3-70b-8192",
                temperature=0.5
            )
            response = chat_completion.choices[0].message.content
            return response
        except Exception as e:
            st.error(f"Error generating chat completion: {e}")
            return "An error occurred while generating the response."

    # Initialize Chat
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Welcome to Travel Buddy! How can I assist you today?"}]

    # Display Chat History
    for msg in st.session_state["messages"]:
        if msg["role"] == "assistant":
            st.chat_message("assistant").write(msg["content"])
        elif msg["role"] == "user":
            st.chat_message("user").write(msg["content"])

    # User Input Section
    user_input = st.chat_input("Enter your travel question:")
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.chat_message("user")
        client_groq = initialize_groq_client("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")
        if client_groq is None:
            st.error("Failed to initialize the Groq client. Please check your API key.")
            st.stop()

        # Generate Response
        context = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state["messages"]])
        try:
            full_response = travel_buddy_response(client_groq, user_input, context=context)
            st.session_state["messages"].append({"role": "assistant", "content": full_response})
            st.chat_message("assistant").write(full_response)
        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")
