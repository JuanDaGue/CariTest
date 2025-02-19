# FAQ & AI Chat Assistant System

A FastAPI-based system that provides automated FAQ suggestions and integrates with Google's Gemini AI for chat functionality.

## Features

- **FAQ Suggestions**: Automatic responses based on a knowledge base
- **Chat with Gemini AI**: Integration with Google's generative AI
- **Greeting Detection**: Automatic response to common greetings
- **History Tracking**: In-memory query history storage
- **Docker Support**: Easy containerization

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Docker Deployment](#docker-deployment)
- [Testing](#testing)
- [Contributing](#contributing)

---

## Prerequisites

- Python 3.9+
- Docker (optional)
- Google API Key (for Gemini integration)
- [Get Gemini API Key](https://ai.google.dev/)

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/faq-chat-system.git
cd faq-chat-system