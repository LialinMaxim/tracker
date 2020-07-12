# Traker

## Local launch

## Development to Azure with cloud Shell

According to the [Azure manual](https://docs.microsoft.com/en-us/azure/app-service/containers/tutorial-python-postgresql-app#use-azure-cloud-shell)

### Create the Azure PostgreSQL database

1. Create a resource group
```shell
az group create --name myResourceGroup --location "West Europe"
```

2. Create PostgreSQL server
```shell
az postgres server create --resource-group <resourcegroup-name> --name <postgresql-name> --location "<region>" --admin-user <admin-username> --admin-password <admin-password> --sku-name B_Gen5_1
```

3. Create firewall rules
```shell
az postgres server firewall-rule create --resource-group <resourcegroup-name> --server-name <postgresql-name> --start-ip-address=0.0.0.0 --end-ip-address=0.0.0.0 --name AllowAllAzureIPs
```

```shell
az postgres server firewall-rule create --resource-group <resourcegroup-name> --server-name <postgresql-name> --start-ip-address=<your-ip-address> --end-ip-address=<your-ip-address> --name AllowLocalClient
```

4. Create Database
```shell
psql -h <postgresql-name>.postgres.database.azure.com -U <admin-username>@<postgresql-name> postgres
```

```sql
CREATE DATABASE helitackdb;
CREATE USER dbmanager WITH PASSWORD 'your-db-password';
GRANT ALL PRIVILEGES ON DATABASE helitackdb TO dbmanager;
```

Type `\q` to exit the PostgreSQL client.


### Run migration and create superuser from local server

1. Set local environment variables
```bash
export DBHOST="<postgresql-name>.postgres.database.azure.com"
export DBUSER="dbmanager@<postgresql-name>"
export DBNAME="heritrackdb"
export DBPASS="your-db-password"
export DJANGO_SETTINGS_MODULE="helitrack.settings.azure"
```

2. Run Django migration to the Azure database
```shell
python manage.py migrate
```
3. Load default data from `initial_inspections.json` to Azure database.
```shell
python manage.py loaddata initial_inspections.json
```

4. Create superuser
```shell
python manage.py createsuperuser
```

5. Run the Django server and check Django admin
```shell
python manage.py runserver
```

### Deploy web app

1. Configure a deployment user
```shell
az webapp deployment user set --user-name <username> --password <password>
```

2. Create App Service plan
The following example creates an App Service plan in the Free pricing `--sku F1`.

```shell
az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku F1 --is-linux
```

3. Create a web app in Bash mode
```bash
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name <app-name> --runtime "PYTHON|3.7" --deployment-local-git
```
Save `deploymentLocalGitUrl` URL as you need it later.

4. Configure environment variables
```shell
az webapp config appsettings set --name <app-name> --resource-group <resourcegroup-name> --settings DBHOST="<postgresql-name>.postgres.database.azure.com" DBUSER="dbmanager@<postgresql-name>" DBPASS="<your-db-password>" DBNAME="helitrackdb" DJANGO_SETTINGS_MODULE="helitrack.settings.azure"
```

5. Change `helitrack.settings.azure.py` as you need it
```python
CORS_ORIGIN_WHITELIST = [
    'https://helitrack-angular.azurewebsites.net',
    'https://helitrack-frontend.azurewebsites.net',
    'https://helitrack-svelte.azurewebsites.net',
]
```

6. Push to Azure from Git
```shell
git remote add azure <deploymentLocalGitUrl-from-create-step>
```

```shell
git push azure <your-local-branch>:master
```

Browse to the deployed app with URL `http://<app-name>.azurewebsites.net/api/swagger/`.

### Stream diagnostic logs

1. Turn on container logging
```shell
az webapp log config --name <app-name> --resource-group myResourceGroup --docker-container-logging filesystem
```

2. See the log stream
```shell
az webapp log tail --name <app-name> --resource-group myResourceGroup
```

To stop log streaming at any time, type `Ctrl+C`.


## Loading default data

Default data contains:
- inspection statuses
- inspection types with schemes
- permission groups
- permission group levels

Load default data from `initial_inspections.json` to database.

```shell
python manage.py loaddata initial_inspections.json
```

Loading of default data from `initial_permissions.json` will be apply with database migrations in
`helitrack-backend\accounts\migrations\0009_load_intial_data.py`

### Creating fresh dump form current database

Inspection statuses and types
```shell
python manage.py dumpdata inspections.status inspections.inspectiontype --indent 2 > initial_inspections.json
```

Permissions
```shell
python manage.py dumpdata contenttypes auth.permission auth.group accounts.grouplevel --indent 2 > initial_permissions.json
```
