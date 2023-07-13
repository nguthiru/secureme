# Criminal mapping platform: <br /> Secure Me

## A web based platform aimed at easening the process of analysis and relationship detection in the current criminal system.

This project is django based and utilizes neo4js gragh database capability to establish seamless co relations between crime data across a specified geographical location.


### Abstract
The aim of this project is to examine data regarding the spatial distribution of crimes committed within a specified geographical location- in this case the country kenya.Here data is collected from all spawning registered crimes from each police station and sent to one unified database.

Therefore, we intend to apply algorithms and methods of analysis; geospatial , temporal and network analysis to compile and visualize the relations in the antecedent of the crime, the present and help show via patterns the types of crime that are more likely to manifest.


## Functional Requirements

For the above mentioned project to run seamlessly and effectively one should have the following:


1. **Python**: Install Python on your system. Django and the required libraries will be installed using Python's package manager, pip.

2. **Django**: Install Django using pip. You can use the command `pip install django` to install the latest version.

3. **Neo4j**: Download and install Neo4j, the graph database management system, on your machine. Follow the installation instructions provided by Neo4j for your specific operating system.

4. **Neo4j Driver**: Install the appropriate Neo4j driver library for Python, depending on the version of Neo4j you are using. You can use libraries like `py2neo` or `neo4j-driver` to establish the connection between Django and Neo4j.

5. **Project Dependencies**: Install any additional dependencies required by your Django project. This could include libraries for mapping, authentication, API development, or any other functionality specific to your project. You can manage these dependencies by creating a `requirements.txt` file and installing them using `pip`.

6. **Configuration**: In your Django project's settings, configure the connection details for Neo4j. This includes specifying the Neo4j database URL, username, password, and any other relevant parameters. Refer to the documentation of your chosen Neo4j driver library for specific configuration instructions.

7. **Modeling**: Define Django models that correspond to the entities you want to store in Neo4j. These models will specify the structure and relationships of your data.

8. **Data Ingestion**: Implement the logic to ingest crime data into your project. This could involve parsing existing datasets, integrating with APIs, or providing a user interface for manual data entry. Convert the data into the appropriate format and use the Neo4j driver library to save it to the Neo4j database.

9. **Development Server**: Start the Django development server using the command `python manage.py runserver`. This will run the Django project locally, allowing you to access it through a web browser.

* IDE
   * Visual Studio (with python setup) 
   
### Tools used

 * [Neo4js](https://neo4j.com/)
 * [Neo4jBloom](https://neo4j.com/product/bloom/)
 * [VueJS](https://vuejs.org/)
 * [FastApi](https://fastapi.tiangolo.com/)
 

#### Platform buildup:

This platform has:

1.An administrators side.
2.An arresting officers entry side.

The two sides contain the following:

1.Admin side.

* Registration and athentication module
* Mapping module
* Visualization module
* Registration Approval module
* Network and Hotspot analysis

2.Officers side.

* Registration and athentication module
* Criminal data entry module


### How the project works

The crime mapping Django project incorporates Neo4j as the graph database and Django as the framework. It enables users to explore and analyze crime data through interactive maps. Crime data is ingested, converted, and stored in Neo4j using Django models. The project offers robust search capabilities and statistical analysis using Django's querying and Neo4j's Cypher query language. User authentication and authorization ensure secure access control. Overall, the project provides an efficient solution for visualizing, analyzing, and managing crime data.


### Setup

1. Navigate to the project directory and create a virtual environment using the command

   ```python3 -m venv env```

3. Activate the virtual environment using `source env/bin/activate` on macOS/Linux or

  ```env\Scripts\activate```  on Windows.

3. Install the project dependencies using
   
   ```pip install -r requirements.txt.```

4. Create a `.env file in the project root directory and add the following environment variables:

- SECRET_KEY: a secret key for the Django project.

- `DEBUG`: set to `True` for development, `False` for production.

-`ALLOWED_HOSTS: a comma-separated list of allowed hostnames for the Django project.

- `DATABASE_URL': a URL to connect to your database. For example, `sqlite:///db.sqlite3` for SQLite or postgres://user:password@localhost /dbname' for PostgreSQL

- To set the Neo4j URL for the "Secure Me" Django project, add a new environment variable to the `.env` file with the following format:

`NEO4J_URL=bolt://localhost:7687`

- Replace `localhost` with the hostname or IP address of your Neo4j server, and `7687` with the port number used by your Neo4j instance.

- Then, in your Django project's settings file (`settings.py`), add the following line:
  
  ```NEO4J_URL = os.environ.get('NEO4J_URL')```


- This will read the `NEO4J_URL` environment variable and store it in the `NEO4J_URL` variable in your Django project's settings. You can then use this variable to connect to your Neo4j database.

5. Run database migrations using

   ```python manage.py migrate```

6. Create a superuser account using `python

   ```manage.py createsuperuser```

7. Run the development server using

   ```python manage.py runserver```

After completing this steps, you should be able to access the "Secure Me" Django project by opening your web browser and navigating to http://localhost:8000/
 

### Relevant Sources.

In order for the project to be complete, extensive research was done from articles of related works and youtube tutorials.This include;
 
* Related works.

[ArcGIS Enterprise SDK Developer Guide](https://developers.arcgis.com/enterprise-sdk/)
[ArcGIS Server - Extending services](https://enterprise.arcgis.com/en/server/latest/develop/windows/about-extending-services.htm)

* Youtube tutorials.
  
[Django setup in vs code](https://youtu.be/f1NQnhFFV-E)
[neo4j tutorial](https://youtu.be/_IgbB24scLI)

### Resources.

[Docker](https://www.docker.com/)
[Django](https://www.djangoproject.com/)
[Neo4js](https://neo4j.com/)






