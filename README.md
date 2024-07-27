# Genieva AI Assistant

Genieva is an AI assistant developed to simplify Grab users' experience in making transactions for Grab Food, Grab Bike, Grab Car, and other Grab transportation services.

## Table of Contents
- [Technologies Used](#technologies-used)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Installation and Usage](#installation-and-usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Technologies Used

Genieva is built using a modern technology stack that includes:

- **FastAPI**: A fast Python framework for building high-performance APIs.
- **LangChain**: A library for developing applications powered by language models.
- **Gemini**: Google's AI model for natural language processing and text generation.
- **Google Maps API**: For location-related functionality and mapping.
- **SQL Agent**: For database interaction and complex queries.
- **Docker & Docker Compose**: For containerization and service orchestration.

## Key Features

1. **Food Ordering**: Assists users in ordering food through Grab Food with personalized recommendations.
2. **Transportation**: Simplifies booking for Grab Bike and Grab Car.
3. **Route Recommendations**: Provides suggestions for optimal travel routes.
4. **Conversational Assistant**: Answers user questions about Grab services.
5. **Location Integration**: Utilizes location data to provide an enhanced experience.

## Project Structure

```
geniva-artificial-intelligence/
├── core/
│   ├── db/
│   ├── models/
│   ├── temporary-data/
│   ├── tools/
│   ├── app.py
│   ├── config.py
│   ├── Dockerfile
│   ├── prompt.py
│   └── requirements.txt
├── documentation/
├── images/
│   ├──Dockerfile
├── tests/
├── .env (not uploaded)
├── .gitignore
├── docker-compose-database.yml
├── docker-compose-service.yml
├── ingest_direct.py
├── README.md
```

## Installation and Usage

This project uses Docker Compose to manage its services. The `docker-compose-database.yml` and `docker-compose-service.yml` files are not included in the public repository for security reasons.

To run the project:

1. Ensure Docker and Docker Compose are installed on your system.

2. Clone this repository:
   ```
   https://github.com/GeniVA-HackJakarta/geniva-artificial-intelligence.git
   ```

3. Navigate to the project directory:
   ```
   cd geniva-artificial-intelligence
   ```

4. Copy the `.env.example` file to `.env` and fill it with the appropriate configuration:
   ```
   cp .env.example .env
   ```

5. Contact the project administrator at alif.datascientist@gmail.com to obtain the `docker-compose-database.yml` and `docker-compose-service.yml` files.

6. Run the services using Docker Compose:
   ```
   docker-compose -f docker-compose-database.yml -f docker-compose-service.yml up -d
   ```

Note: Ensure not to upload Docker Compose files to public repositories if they contain sensitive information.

## API Endpoints

Based on the project structure, specific endpoints are likely defined in `core/app.py`. For more information on API usage, please refer to the documentation located in the `documentation/` folder.

## Contributing

We welcome contributions! Please read `CONTRIBUTING.md` (if available) for details on the process for submitting pull requests.

## License

This project is licensed under the [MIT License](LICENSE) (or adjust according to the license used).