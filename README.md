# Cloud Economics Insights API

## Project Overview

Cloud Economics Insights API is a cloud-based RESTful application developed as part of the ECS781P – Cloud Computing module at Queen Mary University of London.

The application provides secure, programmatic access to real-world economic data through a RESTful interface. It integrates with an external public API to retrieve authoritative economic indicators and allows users to store and manage historical economic snapshots using a cloud-based backend.

The project demonstrates core cloud computing concepts, including RESTful service design, external API integration, cloud deployment readiness, and scalable application architecture.

⸻
## Project Motivation

Economic and financial data is widely available through public APIs, but raw access alone is often insufficient for analysis, comparison, or reuse. Existing services typically lack:
	•	User-specific data management
	•	Persistent storage of historical values
	•	Secure programmatic access
	•	Cloud-ready, extensible architecture

This project addresses these limitations by providing a cloud-native API that enables users to define economic indicators of interest, retrieve real-world data, and store historical snapshots for future use.

⸻

## System Architecture

The application follows a modular, cloud-ready architecture:
	•	Backend Framework: Python Flask
	•	External Data Source: World Bank Open Data API
	•	Persistence Layer: SQLAlchemy ORM with cloud database support
	•	Security: API key–based authentication
	•	Deployment Platform: Designed for Google Cloud Platform (GCP)

The system is structured to support scalability, maintainability, and secure access in a cloud environment.

⸻

## REST API Design

The application exposes a RESTful API that follows standard REST principles:
	•	Stateless requests
	•	Resource-oriented endpoints
	•	JSON request and response bodies
	•	Proper use of HTTP methods (GET, POST, PUT, DELETE)
	•	Meaningful HTTP status codes (200, 201, 400, 401, 404, 500)

Core Endpoints

Endpoint	Description
/auth	User registration and authentication
/indicators	CRUD operations for economic indicators
/snapshots	Fetching and storing economic data snapshots

Authentication is required for protected endpoints and is enforced using API keys passed in request headers.

⸻

## External REST Service Integration

The application integrates with the World Bank Open Data API, a public and authoritative source of global economic indicators.

Examples of supported indicators include:
	•	Gross Domestic Product (GDP)
	•	Inflation
	•	Economic growth rates

The external API is accessed dynamically at runtime, and responses are processed and returned through the application’s own REST interface. Retrieved data can also be persisted for historical tracking.

This integration satisfies the requirement for external REST service usage.

⸻

## Persistent Storage

The application uses a database layer implemented with SQLAlchemy, allowing seamless switching between local and cloud-hosted databases.

Key stored entities include:
	•	Users
	•	Economic indicators
	•	Historical economic snapshots

In production, the application is designed to use a cloud-managed database service (DBaaS) to ensure durability, scalability, and availability.

⸻

## Security Features

The system incorporates several security mechanisms:
	•	API key–based authentication
	•	Password hashing
	•	Protected routes requiring authentication
	•	Environment-variable–based configuration for secrets

These features ensure secure access to user-specific resources and protect sensitive data.

⸻

## Cloud Deployment

The application is designed for deployment in a cloud environment and has been developed and tested using Google Cloud Platform (GCP).

Cloud-related features include:
	•	Deployment on virtual machines
	•	Firewall configuration for controlled access
	•	Environment-based configuration
	•	HTTPS-ready architecture (via managed platforms or reverse proxies)

⸻

## Project Structure

cloud-econ-insights/
│
├── app.py                # Application entry point
├── config.py             # Configuration management
├── models.py             # Database models
├── external_api.py       # External API integration
├── auth.py               # Authentication utilities
├── requirements.txt      # Python dependencies
├── routes/
│   ├── __init__.py       # Blueprint registration
│   ├── auth_routes.py    # Authentication endpoints
│   ├── indicators.py    # Indicator CRUD endpoints
│   └── snapshots.py     # Snapshot management endpoints
├── README.md             # Project documentation
└── venv/                 # Development environment (local use)


⸻

## Running the Application

Prerequisites
	•	Python 3.9+
	•	pip
	•	Virtual environment support

Setup Instructions

git clone https://github.com/SHR-IM/cloud-econ-insights.git
cd cloud-econ-insights

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python app.py

The application will be available at:

http://localhost:5000/


⸻

## Team Project

This is a group project, with responsibilities shared across team members.
Development tasks were distributed across backend development, API integration, cloud configuration, and documentation.

⸻

##References
	•	World Bank Open Data API
https://data.worldbank.org/
	•	Flask Documentation
https://flask.palletsprojects.com/
	•	REST API Design Principles
https://restfulapi.net/

⸻

## Project Outcomes

This project successfully demonstrates:
	•	REST-based service design
	•	Integration with an external REST API
	•	Cloud-ready application architecture
	•	Secure access mechanisms
	•	Persistent data storage
	•	Deployment considerations in a cloud environment

⸻

