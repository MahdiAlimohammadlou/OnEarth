# OnEarth Project

## Overview

OnEarth is a real estate marketplace that enables the buying and selling of properties as NFTs (Non-Fungible Tokens). The platform allows users to search for properties based on country, city, and specific projects.

## Features

- **Property Search:** Easily find properties based on country, city, and specific real estate projects.
- **NFT Marketplace:** Buy and sell properties as NFTs.
- **Chatbot Integration:** Interact with a chatbot for customer support and assistance.

## Technologies Used

- **Backend:** Django, Django REST Framework
- **Database:** Redis (for caching and background tasks)
- **Containerization:** Docker, Docker Compose

## Requirements

To run this project, you only need to have Docker and Docker Compose installed on your machine.

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Mahdialimohammadlou/OnEarth.git
   cd onearth
   ```
2. Run the project using Docker Compose:
   ```bash
   docker-compose up --build -d
   ```
