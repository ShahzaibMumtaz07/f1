# Formula One (F1) Project

F1 is a Django project designed for visualizing Formula One data on an orthographic map projection (globe). The project is currently being developed and welcomes contributions from interested individuals.

## Objective

The primary objective of the F1 project is to provide a visually engaging and interactive platform for exploring Formula One data. The platform is designed to help users easily visualize and understand the rich history of Formula One, as well as current season data.

## Data Source

The F1 project utilizes the Formula 1 World Championship dataset, which can be downloaded from [Kaggle](https://www.kaggle.com/rohanrao/formula-1-world-championship-1950-2020). The dataset contains detailed information on every driver, team, and race from 1950 to 2022. This data is updated every season to ensure that F1 users have access to the latest information on the sport.

## Technologies Used

The F1 project is built using the Django web framework and utilizes a range of web technologies including HTML, CSS, and JavaScript. The data is hosted on a PostgreSQL database to ensure efficient and reliable data storage. To create the orthographic map projection, the project uses Globe.gl, a JavaScript library for creating 3D globes and maps, which can be found at [GitHub](https://github.com/vasturiano/globe.gl).

For containerization, Docker and docker-compose are being used to ensure easy deployment of the application on different systems. Additionally, this project can be seen as a basic template for setting up Django for production ready applications.

## Usage
- Rename `.sample_env` as `.env`
- In the command line run: 

	`docker-compose up --build -d`

- Navigate to http://localhost:8000/api/world/ for accessing the page.

## Contributing

Contributions to the F1 project are welcome from interested individuals. Whether you are a developer, designer, or simply a fan of Formula One, there are many ways to get involved with the project. You can help by improving the code, adding new features, or simply testing the platform and providing feedback.

To get started with contributing, you can fork the project on GitHub and submit a pull request. 

## Conclusion

The F1 project is an exciting platform for exploring Formula One data in a visually engaging and interactive way. With regular updates to the data, the platform provides a comprehensive view of the sport's rich history and current season standings. With contributions from interested individuals, the F1 project can continue to grow and improve, providing a valuable resource for Formula One fans around the world.
