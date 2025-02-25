# Project Overview
AI-powered chatbot using Groq AI and LangChain.
Stores user information and goals in PostgreSQL.
Uses memory-based conversations with ConversationBufferMemory.
# Tech Stack
Python, LangChain, Groq AI
PostgreSQL for user data storage
dotenv for environment variables
# Features
User Information & Goal Storage: Collects and stores user data.
Conversational Memory: Retains chat context using LangChain’s ConversationBufferMemory.
Groq AI Integration: Uses ChatGroq for intelligent responses.
Validated User Input: Checks for valid email, phone, and country.
Database Operations: PostgreSQL setup with CREATE TABLE, INSERT, and SELECT queries.
# work flow
- Creating tables
- Ask user to put goals and weightage
- Add personal information like mail, country, phone for generic chat agent (optional)
- Ask a query
- User information from database and query parsed to model
- Getting response from Model
