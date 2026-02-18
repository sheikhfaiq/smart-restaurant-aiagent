🍽️ Smart Restaurant AI Chatbot & Agent

An intelligent AI-powered restaurant assistant built using FastAPI, LangChain, and SQLAlchemy that allows users to:

📋 Ask questions about the restaurant menu

🧾 Get detailed item descriptions

🛒 Place orders conversationally

💬 Interact naturally using AI

⚡ Process orders efficiently via backend APIs

🚀 Project Overview

The Smart Restaurant AI Chatbot is an AI-driven conversational system designed to enhance restaurant ordering experiences.

It enables customers to:

Ask about menu items

Check prices

Get recommendations

Customize orders

Place orders in natural language

Track order confirmation

The chatbot uses LangChain agents to interpret user intent and interact with backend APIs and the database.

🏗️ Architecture
🧠 AI Layer

LangChain Agent

Natural Language Processing

Tool calling for order placement

Intent recognition (menu query, recommendation, order placement)

⚡ Backend Layer

FastAPI

RESTful API endpoints

Order processing logic

Menu retrieval

🗄️ Database Layer

SQLAlchemy ORM

Menu table

Orders table

Order items table

Customer details (optional)

🛠️ Tech Stack

Python 3.10+

FastAPI

LangChain

OpenAI / LLM Provider

SQLAlchemy

SQLite / PostgreSQL

Uvicorn
