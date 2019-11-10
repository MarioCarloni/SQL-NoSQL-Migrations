# Python Multi-DB Seeders

> This project is designed and built to instantiate, migrate, seed, and query from SQL/NoSQL databases automatically. Directions to start the containers are provided below.


## Start-up
Make sure you've updated to the lastest version of Docker
```bash
# Navigate to the project directory
cd project/dir

# Create services
docker-compose up --build

# Destroy services
docker-compose down -v 
```

## Troubleshooting
```bash
ERROR: for container-name  Cannot start service container-name: error while creating mount source path '/host_mnt/c/Users/user/Documents/projectDir/dir': mkdir /host_mnt/c: file exists
```
Remove all services and volumes, including orphan containers, and rebuild. Also try resetting credentials on shared drives in Docker settings.
```bash
docker-compose down -v --remove-orphans
docker-compose up --build
```

## Section 1: Databases
1. PostgreSQL
    * See postgres_db service in `docker-compose.yml` 
1. MongoDB 
    * See mongo_db service in `docker-compose.yml` 
1. Neo4J
    * See neo4j_db service in `docker-compose.yml` 
1. Data
    * See `/src/import/users.csv`

## Section 2: Python ORMs
1. PostgreSQL (SQLAlchemy)
    * See SQLAlchemy ORM + Pandas usage in `/src/seed_postgres.py` 
1. MongoDB (MongoEngine)
    * See MongoEngine ORM + Pandas usage in `/src/seed_mongo.py` 
1. Neo4J (py2neo)
    * See py2neo OGM + Pandas usage in `/src/seed_neo4j.py` 

## Section 3: AWS Data Lakes
1. If existing data needed to be migrated to a lake, I would first use Lake Formation to catalog all data, migrate to S3, and secure data access. I would then use CloudFormation to manage all lake resource deployments. In those deployments, depending on the project, I would specify DynamoDB for low-volume, small-object NoSQL data management, S3 for large-object high-volume SQL/NoSQL data management, along with either Athena or Redshift for querying depending on data storage type. I would deploy Glue to manage automatic data cataloging in the lake. If a project called for a data pipeline, I would deploy Lambda to manage REST endpoints, and secure each endpoint through an API Gateway. I would deploy Cognito to manage user data access, and either kinesis or elasticsearch to visualize real-time data dashboards. Regardless of the project,  I would deploy CloudWatch to visualize resource logs and take automated action during particular events.
1. A Data Lake is a central repository for all structured and unstructured data, and allows for the storage, monitoring, data access, and management of services which can communicate with the repository.
1. [Template script](https://github.com/awslabs/aws-data-lake-solution/blob/master/deployment/data-lake-deploy.template) 

## Section 4: Kafka/Spark
1. Kafka is a distributed streaming platform to publish, subscribe, store, and process real-time streaming data. It’s used mainly for real-time streaming data pipelines and applications. It’s run as a cluster, where the cluster stores streams of records called topics, and each topic contains a key/value pair as well as a timestamp.
1. The Producer API publishes record streams to topics, the Consumer API subscribes to topics and processes record streams, the Streams API transforms incoming and outgoing topic streams, and the Connector API builds producers/consumers that connect topics to existing applications and systems.
1. See kafka/zookeeper services in `docker-compose.yml`
    1. Test topic created through environment variables within the service, see kafka service
1. See spark-master/spark-worker services in `docker-compose.yml`

## Section 5: Docker/Kubernetes
1. Deployed Cassandra, Spark, and Kafka as microservices, see `docker-compose.yml`
1. Wrote deployments, services, persistent volumes, persistent volume claims, cluster issuers, tls certificates, and an ingress controller to manage service endpoints. See `kubernetes-deployment.yml` 