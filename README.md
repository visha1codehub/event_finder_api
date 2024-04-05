# Event Finder API

This is an Event Finder API built with Django, Django Rest Framework, Docker, Docker Compose, PostgreSQL for database storage, and Redis for caching. The application integrates with an external API in three different ways: synchronously, asynchronously, and using threading.

## Features

- **Event Search**: Users can search for events based on two required parameters such as latitude and longitude.
- **Synchronous External API Integration**: Utilizes synchronous calls to fetch data from an external API.
- **Asynchronous External API Integration**: Incorporates asynchronous calls to fetch data from an external API, improving performance and scalability.
- **Threading for External API Calls**: Implements threading to handle external API calls concurrently, enhancing responsiveness.

## Technologies Used

- Django: A high-level Python web framework for rapid development.
- Django Rest Framework: A powerful and flexible toolkit for building Web APIs.
- Docker: A platform for developing, shipping, and running applications in containers.
- Docker Compose: A tool for defining and running multi-container Docker applications.
- PostgreSQL: A powerful, open-source object-relational database system.
- Redis: An open-source, in-memory data structure store used as a cache, message broker, and queue.
- Python Threading: Allows concurrent execution of tasks to improve performance.

# API Documentation:

### Create Event

- **Description:** This endpoint allows users to create a new event.

- **URL:** `/api/event/create`

- **Method:** `POST`

- **Request Body:**

```json
{
  "event_name": "Sample Event",
  "city_name": "Sample City",
  "date": "2024-03-01",
  "time": "10:00:00",
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

- **Response:**

```json
{
    "success": true,
    "message": "Event created successfully!",
    "status": 201,
    "data": {
        "event_name": "Sample Event2",
        "city_name": "Sample City",
        "date": "2024-03-01",
        "time": "10:00:00",
        "latitude": "40.712800000000000",
        "longitude": "-74.006000000000000"
    }
}
```

### Get Events

Endpoints allow users to retrieve events based on location and date.
Following three ways:

#### (1) Synchronously

- **Description:** This endpoint allows synchronous calls and slowest.

- **URL:** `api/event/sync`

- **Method:** `GET`

- **Query Parameters:**

  - `latitude` (required): Latitude of the user's location.
  - `longitude` (required): Longitude of the user's location.
  <!-- - `date` (required): Date in YYYY-MM-DD format. -->
#### (2) Asynchronously

- **Description:** This endpoint allows asynchronous parallel calls and fastest.

- **URL:** `api/event/async`

- **Method:** `GET`

- **Query Parameters:**

  - `latitude` (required): Latitude of the user's location.
  - `longitude` (required): Longitude of the user's location.
  <!-- - `date` (required): Date in YYYY-MM-DD format. -->

  #### (3) Theading

- **Description:** This endpoint implements python threading to handle external API calls concurrently. It is little bit slower than asynchronous endpoint.

- **URL:** `api/event/thread`

- **Method:** `GET`

- **Query Parameters:**

  - `latitude` (required): Latitude of the user's location.
  - `longitude` (required): Longitude of the user's location.
  <!-- - `date` (required): Date in YYYY-MM-DD format. -->

- **Response:**

```json
{
    "events": [
        {
            "event_name": "Whole source",
            "city_name": "Vaughnfurt",
            "date": "2024-04-05",
            "weather": "Windy 1C",
            "distance_km": "8885.932011998337"
        },
        {
            "event_name": "Per",
            "city_name": "New Joyce",
            "date": "2024-04-06",
            "weather": "Sunny 14C",
            "distance_km": "8859.361769842482"
        },
        {
            "event_name": "Mind able magazine",
            "city_name": "Lake Katherine",
            "date": "2024-04-05",
            "weather": "Snowy 25C",
            "distance_km": "13788.949581463812"
        },
        {
            "event_name": "Tough group",
            "city_name": "Ewingtown",
            "date": "2024-04-05",
            "weather": "Cloudy 31C",
            "distance_km": "10872.89585463272"
        },
        {
            "event_name": "Fire ball technology",
            "city_name": "Murphymouth",
            "date": "2024-04-05",
            "weather": "Windy 7C",
            "distance_km": "6393.095843075413"
        },
        {
            "event_name": "Down model manager several",
            "city_name": "South Bryanland",
            "date": "2024-04-06",
            "weather": "Sunny 28C",
            "distance_km": "11053.845347584442"
        },
        {
            "event_name": "Test Event before",
            "city_name": "Test City2",
            "date": "2024-04-06",
            "weather": "Sunny, 18C",
            "distance_km": "11940.462776237671"
        },
        {
            "event_name": "Right newspaper behavior",
            "city_name": "Lake Johnbury",
            "date": "2024-04-06",
            "weather": "Windy 27C",
            "distance_km": "10619.72488015569"
        },
        {
            "event_name": "Thousand by",
            "city_name": "Schmidtfort",
            "date": "2024-04-07",
            "weather": "Sunny 16C",
            "distance_km": "9148.375988952124"
        },
        {
            "event_name": "Girl require important",
            "city_name": "New Matthew",
            "date": "2024-04-07",
            "weather": "Cloudy 22C",
            "distance_km": "4509.825463992096"
        }
    ],
    "page": 1,
    "pageSize": 10,
    "totalEvents": 54,
    "totalPages": 6,
    "next": "http://127.0.0.1:8000/api/event/thread/?latitude=23.3232&longitude=-65.42342&page=2",
    "previous": null
}
```

### Get OpenAPI Documentation

- **Description:** This is a format for describing RESTful APIs, which includes endpoints, request/response formats, parameters, authentication methods, and more.

- **URL:** `/api/docs`

- **Method:** `GET`

- **Request Body:**

![Alt text](https://github.com/visha1codehub/Learn_Github_Action/blob/master/swagger_screenshot.png?raw=true "Screeshot")

## Setup Instructions

Follow these steps to set up and run the project locally on your machine:

### Prerequisites

1. **docker-desktop:** Make sure you have docker-desktop installed on your system. You can download it from [docker-desktop.org](https://www.docker.com/products/docker-desktop/).

2. **docker-compose:** Ensure that docker-compose is installed and running on your machine. You can download it from [docker-compose.org](https://docs.docker.com/compose/install/).

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/event_finder_api.git
    ```

2. Navigate to the project directory:

   ```bash
   cd event_finder_api
   ```

### Running the Server

1. Start the server using npm or yarn:

   ```bash
   docker-compose up
   ```

2. Once the server is running, you can access the API endpoints locally at `http://localhost:8000`.
