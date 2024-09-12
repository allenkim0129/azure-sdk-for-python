This document currently details Python commands for building Azure Cosmos SDK.

### Fork and clone the repository
To build and develop locally, it is strongly recommended to fork and clone the repository: https://github.com/Azure/azure-sdk-for-python

**<u>NOTE:</u>** All of the below commands need to be ran from the following directory from the home directory of `azure-sdk-for-python` repository.

```shell
sdk/cosmos/azure-cosmos
```

### Prerequisites
* Azure subscription - [Create a free account][azure_sub]
* Azure [Cosmos DB account][cosmos_account] - SQL API
* [Python 3.6+][python]

If you need a Cosmos DB SQL API account, you can create one with this [Azure CLI][azure_cli] command:

```Bash
az cosmosdb create --resource-group <resource-group-name> --name <cosmos-account-name>
```

### Install the packages

```shell
pip install azure-cosmos
pip install -r dev_requirements.txt 
```

**<u>NOTE:</u>** For Mac users, `pip` might not work automatically, try with `pip3` instead. Alternately, adding an alias of `pip3` to `pip` in `~/.zprofile` file will also work([How to add alias][pip_alias]).
```shell
pip3 install azure-cosmos
pip3 install -r dev_requirements.txt 
```

### Use Pycharm IDE for Python SDK on MAC

#### Setting Pycharm IDE for Python SDK

[//]: # (TODO: Add screenshots)
Your Python interpreter might not be the right version(**Python 3.6+**). Change the Python versions in Pycharm.
1. Add local interpreter
![Screenshot 2024-09-11 at 1 28 42 PM](https://github.com/user-attachments/assets/93b0815b-72e7-40ac-b865-c4f00c7627fa)

3. Select the right interpreter version
![Screenshot 2024-09-11 at 1 32 13 PM](https://github.com/user-attachments/assets/a4a881df-6e37-4a09-884c-dcece4daeefd)


#### Running unit tests

Install public dependent packages by search
- pytest

Install python sdk packages from disk
- Choose home directory


Since MAC does not support emulator yet, test configs manually updated to run unit tests.
1. Get `ACCOUNT_KEY` and `ACCOUNT_HOST` from your Azure Cosmos DB account
    - `ACCOUNT_KEY`: Primary key from the keys from Settings from Azure Cosmos DB account
    - `ACCOUNT_HOST`: URL from the overview page of Azure Cosmos DB account
2. Replace default values of `ACCOUNT_KEY` and `ACCOUNT_HOST` in `test_config.py` file in `azure-sdk-for-python/sdk/cosmos/azure-cosmos/test` 
3. 

Open azure-sdk-for-python/sdk/cosmos/azure-cosmos/test/test_config.py in Pycharm IDE as project to update the default value `ACCOUNT_KEY` and `ACCOUNT_HOST`:
![Screenshot 2022-12-19 at 1 51 17 PM](https://user-images.githubusercontent.com/14034156/208549832-9edf00d6-613a-4efd-a410-eaeb7abe86cd.png)


### Defining Project Structure

Open project structure through project settings for azure-cosmos project and set the SDK and Language Level to JDK 11 under Project tab:
![Screenshot 2022-12-19 at 1 54 08 PM](https://user-images.githubusercontent.com/14034156/208549843-4824a467-9d21-4ffa-bc56-7f14da9d573c.png)

Open Modules tab in the same settings and set the Language level to match project default, which should be JDK 11:
![Screenshot 2022-12-19 at 1 58 27 PM](https://user-images.githubusercontent.com/14034156/208549863-d541c174-c7a3-48d6-b186-e19b78153cff.png)


Set target bytecode version for the project azure-cosmos in IntelliJ Preferences for Java Compiler as JDK 11: 
![Screenshot 2022-12-19 at 2 23 22 PM](https://user-images.githubusercontent.com/14034156/208549894-39804c35-9f4c-4b74-b076-aeaf24edd847.png)

### Installing the Cosmos DB emulator

Setup Azure Cosmos DB Emulator by following [this instruction](https://docs.microsoft.com/azure/cosmos-db/local-emulator). Then please export the emulator's SSL certificates and install them in the JVM trust stores on your development machine following [this instruction](https://learn.microsoft.com/azure/cosmos-db/local-emulator-export-ssl-certificates).

For running the SDK unit tests use follogwing start options for the emulator:
PS C:\Program Files\Azure Cosmos DB Emulator> .\CosmosDB.Emulator.exe /enablepreview /EnableSqlComputeEndpoint /disableratelimiting /partitioncount=50 /consistency=Strong

For installing the keys on windows following power shell script (running as administrator) can be used:
```
Push-Location -Path $env:JAVA_HOME

gci -recurse cert:\LocalMachine\My | ? FriendlyName -eq DocumentDbEmulatorCertificate | Export-Certificate -Type cer -FilePath cosmos_emulator.cer
keytool -cacerts -delete -alias cosmos_emulator -storepass changeit
keytool -cacerts -importcert -alias cosmos_emulator -storepass changeit -file cosmos_emulator.cer
del cosmos_emulator.cer

Pop-Location
```

### Running Unit Tests

Unit tests are tests with group "unit" and can be run from IntelliJ directly without needing any Azure Cosmos DB Account or Emulator support. To run them, right click on any unit test class and run them. To test this, run `ClientConfigDiagnosticsTest` from IntelliJ IDE directly. 

Note: When running the Azure Cosmos DB Emulator in a virtual machine you may receive timeouts. If that happens increase the number of cores and improve the I/O performance of the VM.

### Running Integration Tests

Azure Cosmos Java SDK has different Integration tests which can be run with Azure Cosmos Emulator or Azure Cosmos DB production Account. 

Emulator Integration tests are with test group `emulator`, labeled in the code as `groups = { "emulator" }` and can be run from IntelliJ after starting Azure Cosmos DB Emulator on the local development machine. For example, `DocumentCrudTest` is of group emulator.

Latest version of Azure Cosmos DB Emulator can be downloaded and installed from [here](https://learn.microsoft.com/azure/cosmos-db/local-emulator)
Our CI pipelines start Azure Cosmos DB Emulator with these parameters. It is highly recommended to use these for local development and testing.
```shell
/enablepreview /EnableSqlComputeEndpoint /disableratelimiting /partitioncount=50 /consistency=Strong
```

Other test groups are meant to be tested against Azure Cosmos DB production account, but can also be tested against Emulator. There are multiple different test groups like `groups = {"fast", "long", "direct", "multi-region", "multi-master"}`. For example, `CosmosItemTest` is a simple group test which can be run against Azure Cosmos DB production account, as well as against emulator.

To run any test against Azure Cosmos DB production account, it is required to update `TestConfigurations.java` class with account host and key. 
NOTE: When creating a PR, make sure to remove any account key and account host information from the PR. To avoid security breaches, never commit and push any keys and host information related to Azure Cosmos DB Account.



<!-- LINKS -->
[azure_sub]: https://azure.microsoft.com/free/
[cosmos_account]: https://docs.microsoft.com/azure/cosmos-db/account-overview
[python]: https://www.python.org/downloads/
[azure_cli]: https://docs.microsoft.com/cli/azure
[pip_alias]: https://stackoverflow.com/questions/44455001/how-to-change-pip3-command-to-be-pip#:~:text=You%20can%20use%20pip3%20using%20the%20alias%20pip,in%20your%20~%2F.zprofile%20file%20has%20the%20same%20effect.
