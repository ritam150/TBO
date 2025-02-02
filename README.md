Travel Buddy Dashboard

Overview
The Travel Buddy Dashboard is an interactive and user-friendly travel planning application built using Streamlit and SQLite It allows users to plan trips manage travel details and receive personalized recommendations through an AI-powered chatbot

Features
Dashboard Users can enter trip details set preferences and generate a personalized travel summary
View Database Allows users to access saved travel plans and manage trip details
Chatbot AI-powered travel assistant that provides real-time suggestions and refinements based on user interactions

Technologies Used
Python
Streamlit
SQLite
Groq AI API for chatbot functionality

Installation
1 Clone the repository
   git clone httpsgithubcomyour-repotravel-buddy-dashboardgit
   cd travel-buddy-dashboard
2 Install the required dependencies
   pip install streamlit sqlite3
3 Run the application
   streamlit run apppy

How to Use
1 Dashboard
Enter client details name user code travel dates
Select budget and event type
Choose destination country state city major location
Input specific travel preferences
Click Generate Travel Summary to save and view the trip details

2 View Database
Displays all saved travel plans from the SQLite database
Users can review past travel details

3 Chatbot
Ask travel-related questions
Get personalized recommendations based on budget location and preferences
The chatbot provides eco-conscious travel insights

Database Schema
The SQLite database travel_buddydb contains a table travel_data with the following columns
client_name TEXT
user_code TEXT
start_date TEXT
end_date TEXT
budget INTEGER
event_type TEXT
country TEXT
state TEXT
city TEXT
major_location TEXT
preferences TEXT

API Integration Groq AI Chatbot
The chatbot utilizes Groq AI API for real-time travel assistance
Users can interact with the assistant for travel planning sustainability tips and itinerary suggestions

Future Enhancements
User authentication for secure access
Trip cost estimator based on real-time data
Multi-user collaboration for group trip planning
Integration with travel APIs for live hotel flight and activity bookings
