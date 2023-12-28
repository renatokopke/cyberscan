CyberScan: Dynamic Web Defender!
======

## Introduction

CyberScan is a robust and flexible API, developed using Django Rest Framework, designed to integrate and simplify the security scanning process for web applications. It offers a convenient interface for executing security scans, facilitating integration with existing systems and automating the security workflow.

## Project Status

This project is currently under development. I am working on it in my free time as a form of fun and to contribute to the community. New features and improvements will be added progressively.

## Key Features

- **Integration with OWASP ZAP:** CyberScan utilizes the renowned OWASP Zed Attack Proxy (ZAP) in the backend, ensuring deep and reliable security analyses.
- **Simplified API Calls:** Facilitates the execution of security scans through clear and well-documented API calls.
- **Detailed Report Generation:** Provides comprehensive reports, allowing developers to identify and fix vulnerabilities efficiently.

## Configuration

### Docker Installation
Before you begin, make sure Docker is installed on your Linux operating system. For Docker installation instructions, refer to the official Docker documentation.

### Cloning the Repository
Clone the GitHub repository to obtain the necessary files to configure and run the service:

```bash
git clone https://github.com/renatokopke/cyberscan/cyberscan.git
cd cyberscan
```

### Environment Configuration
Copy the environment variable example file and adjust it as needed:

```bash
cp env-default .env
```
Note: Modify the variables in the .env file according to your needs. This file contains essential configurations for the service to function.

### Running the Service

To start the container, navigate to the docker directory and run docker-compose:

```bash
cd docker
docker-compose up -d
```

## Creating an Admin Account in Django

To set up a superuser (admin) account in Django, follow these steps:

### Access the Docker Container:
Run the following command to enter the container where Django is running:

```bash
docker exec -it cyberscan_app bash
```

### Navigate to the Application Directory:
1. Once inside the container, navigate to the application directory:
3. Execute the createsuperuser command to start the process of creating a new superuser:

```bash
cd /app
python manage.py createsuperuser
```

During the process, you will be prompted to provide a username, email address, and a secure password for the superuser:
- **Username:** Choose a username for the admin (e.g., admin).
- **Email Address:** Provide a valid email address for the account (e.g., admin@local.com).
- **Password:** Enter a secure password and then enter it again for confirmation.

### Exit the Container:
After creating the superuser, exit the container and return to the host environment by executing:
```bash
exit
```


## Acknowledgements

This project utilizes [OWASP Zed Attack Proxy (ZAP)](https://www.zaproxy.org/), one of the world's most popular security tools, used to find security vulnerabilities in web applications.

We extend our thanks to the contributors and maintainers of OWASP ZAP for making such a powerful and open tool available, significantly contributing to the web community's security.

## Author

- [Renato Kopke](https://www.linkedin.com/in/renatokopke/) - *Principal Developer*
