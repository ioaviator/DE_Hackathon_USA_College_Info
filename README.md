## Data Engineering Hackathon - USA Top 1000 College 

### Background Story
Among the biggest challenges for university aspirants in the United States is finding accurate, up-to-date, and relevant information about colleges and universities. 

With thousands of schools nationwide, students often struggle to compare institutions based on critical factors such as tuition costs, graduation rates, admission requirements, and available programs.

### Overview
A data engineer have being called upon to a data pipeline that automates the extraction, transformation, and storage of university-related information from the [USA College Scorecard API.](https://collegescorecard.ed.gov/data/api-documentation/)

The data pipeline  is expected to retrieve data for the top 1000 schools in the U.S.A based on ranking and store the data in a structured format suitable for analytics

### Project Usage
This section walks  through setting up the project, including repository setup, Astro CLI configuration, and credential management in Azure Cloud, Terraform and Github Actions.

### Prerequisites
- Python 3.10 or higher
- Git
- Terraform
- Azure Cloud ( Blob Storage, Azure PostgreSQL, Container Registry, Azure Entra ID )
- Docker Desktop
- Apache Airflow via [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli)


#### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/ioaviator/DE_Hackathon_USA_College_Info.git

# Navigate to project directory
cd DE_Hackathon_USA_College_Info
```
#### Step 2: Download Azure CLI and the Login to Azure from the command line (Bash)

```bash 
  az login 
```
Take note of the subscription id and keep it safe
![az login](./img/az_login.png)

#### Step 3: Provision Azure  resource with Terraform
<br>

Login to [Azure Portal](https://portal.azure.com)  
Manually create a resource group, storage account and container, which will be used to store terraform state file remotely

```bash
  backend "azurerm" {
    resource_group_name  = "backend_tf"
    storage_account_name = "hackathonstatebackend"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
```

Navigate to the terraform directory. Create a file `credentials.txt` and paste your Azure subscription id. Add this file to `.gitignore` file. <br >
In the `providers.tf`, reference the `credentials.txt` file

**N.B: Always comment out the subscription_id line before pushing to GitHub. This is to prevent Github Actions from throwing an error**


```bash
  # Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}

  subscription_id = file("credentials.txt")
}
```

`change directory (cd)` into the terraform directory from the terminal. Run the following commands

- Initialize: `terraform init`
- Plan: `terraform plan`
- Apply: `terraform apply`

#### Step 4: Create and Configure environment variables

Create a `.env` file at the project root directory. Add this file to `.gitignore`

Visit the [Score card website](https://collegescorecard.ed.gov/data/api-documentation/) and generate an API key

Generate Azure blob `Account Key` and `Connection String`

Acount Key: `az storage account keys list -g <ResourceGroupName> -n <StorageAccountName>`

Connection String: `az storage account show-connection-string --name <StorageAccountName> --resource-group <ResourceGroupName> --subscription <SubscriptionID>`

Add database username and password credentials
```bash
API_KEY=LP3PqxbWKk
URL=<score-card-api-url>

## Azure blob storage account key
ACCOUNT_KEY="STAZ3hyCEMLaETuw=="
## Azure blob storage connection string
CONN_STRING="DefaultEndpointsProtocol=https;AccountName=<storage_account_name>;AccountKey=<blob_storage_account_key>;EndpointSuffix=core.windows.net"

## Azure postgres db username and password
DB_USERNAME=adminadmin
DB_PASSWORD=1e3q98q
```

#### Step 5: Virtual Environment Configuration

  Create a python virtual environment
  `python -m venv venv`

------------------------------------------
  *Activate virtual environment*

  Windows: `source venv\Scripts\activate`

  Linux: `source venv/bin/activate`

-------------------------------------

  *Install Project Requirements*
```bash
# Install Python packages
astro dev python package-install <package-name>

# Install packages in your Astro project
astro dev python package-install requirements.txt
```

#### Step 6: Start Project
```bash
astro dev start
```
To run the pipeline maually without orchestration.
From the project root directory
```bash
python main.py
```
<br>
============================================

## Data Pipeline Architecture

![data pipeline](./_img/data_pipeline.gif)

### Key Components

- Data Ingestion: API data extraction

- Storage Layers:
  - Raw Layer: Azure Blob Storage (Parquet format)
  - Processed Layer: Azure PostgreSQL

- Orchestration: Apache Airflow [Astronomer]
- Data Transformation: Python
- Infrastructure as Code: Terraform
- CI/CD: GitHub Actions
- Container Registry: Azure Container Registry

<br>

==================================
## Choice of Tools

**Cloud Service (Azure)**

  - **Azure Blob Storage**: Serves as the data lake for storing raw data in Parquet format, offering durability and cost-effectiveness for data storage.
  
  - **Azure PostgreSQL**: Serves as the data warehouse where transformed data is loaded. Analysts can connect to the warehouse and build visualizations
  
  - **Azure Container Registry**: Hosts our Docker containers

**Orchestration (Apache Airflow)**

  - Manages data pipeline dependencies and orchestration.

**Infrastructure as Code (Terraform)**
  - Automation of infrastructure provisioning, updates, and management. 
  - Manage infrastructure across different providers, simplifying management and orchestration

**Version Control & CI/CD (GitHub & GitHub Actions)**

  - **GitHub:** Maintains code versions and enables collaboration among teams.
  - **GitHub Actions:** Automates testing, building, and deployment processes.
  - Implements automated cloud  infrastructure deployment, code quality checks and image builds.

**Data Visualization (Power BI)**
  - Creates interactive dashboards for data analysis.
  - Connects directly to Azure PostgreSQL for data visualization.
  - Provides easy-to-use data visuals for business users to interpret data and understand data.
------------------------------

#### **Code Formatting and Style**

**black**
  - Automatically formats code to meet PEP 8 standards
  - Enforces consistent Python code formatting

**flake8**
  - Lints Python code for potential errors
  - Checks for style guide violations
  - Ensures code quality standards

 **isort**
  - Automatically sorts Python imports
  - Organizes imports into sections (standard library, third-party, local)
  - Maintains consistent import ordering
  - Improves code readability