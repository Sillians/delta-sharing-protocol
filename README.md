## DocumentAI Delta Sharing

Delta Sharing is an open protocol for secure data sharing, making it simple to share data with other organizations regardless of which computing platforms they use. It makes it easy to share live data in your Delta lake without copying it to another system, thereby, Data Recipients can directly connect to the Delta Shares from Pandas, Apache Spark, etc, without having to first deploy a specific compute pattern. 

Delta Sharing allows us to share `terabytes-scale` of our `10K-data` dataset stored in `delta-lake`, reliably and efficiently by leveraging cloud systems like `S3`, `ADLS`, and `GCS`. In our use-case the `ADLS`.


## Concepts

* `Share:` A share is a logical grouping to share with recipients. A share can be shared with one or multiple recipients. A recipient can access all resources in a share. A share may contain multiple schemas.
* `Schema:` A schema is a logical grouping of tables. A schema may contain multiple tables.
* `Table:` A table is a Delta Lake table or a view on top of a Delta Lake table.
* `Recipient:` A principal that has a bearer token to access shared tables.
* `Sharing Server:` A server that implements this protocol.


## File Structure
```
├── delta-sharing-server-0.4.0
│   ├── delta-sharing-server-0.4.4
│   │   ├── bin
│   │   │   ├── delta-sharing-server
│   │   │   ├── delta-sharing-server.bat
│   │   ├── conf
│   │   │   ├── core-site.xml
│   │   │   ├── delta-sharing-server.yaml
│   │   │   ├── delta-sharing-server.yaml.template
│   │   ├── lib
│   │   │   ├── jar files
│   │   │   ├── jar files
│   │   │   ├── jar files
│   │   │   ├── jar files
│   │   │   ├── jar files
├── delta_share.py
├── delta-datasets.share
├── README.md
├── requirements.txt
├── Dockerfile
├── .gitignore
└── 
```

## File Contents and Configurations

* delta-sharing-server-0.4.0 ; This is the `pre-built package`, which is the delta sharing server.
    * `conf/core-site.xml`; The server is using `hadoop-azure` to read `Azure Data Lake Storage Gen2`. In this file, we specify `the Shared key Authentication`. `cd` into the directory and specify the following changes;

    `YOUR-ACCOUNT-NAME` is your Azure storage account and `YOUR-ACCOUNT-KEY` is your account key.

    ```
    <?xml version="1.0"?>
    <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
    <configuration>
    <property>
        <name>fs.azure.account.auth.type.YOUR-ACCOUNT-NAME.dfs.core.windows.net</name>
        <value>SharedKey</value>
        <description>
        </description>
    </property>
    <property>
        <name>fs.azure.account.key.YOUR-ACCOUNT-NAME.dfs.core.windows.net</name>
        <value>YOUR-ACCOUNT-KEY</value>
        <description>
        The secret password. Never share these.
        </description>
    </property>
    </configuration>

    ```

    
    * `conf/delta-sharing-server.yaml`; this contains the `server yaml` files, containing the server configs for special requirements. To add shared data, reference to the Delta lake tables you would like to share from this server is specified in this config file.

    This is a link to the full template : https://github.com/delta-io/delta-sharing/blob/main/server/src/universal/conf/delta-sharing-server.yaml.template , were it contains format for different Cloud Storage.

    But this we are using the `Azure Data Lake Storage Gen2`, I had to limit the template for `ADLS Gen2` only.
    Make changes to the following;
    - `share2` ; change this to any name you wish to call your share.
    - `schema2` ; change this to any name you wish to assign to your schema.
    - `table3` ; change this to what you wish to name your table.
    - Locate this ; `location: "abfss://<container-name>@<account-name}.dfs.core.windows.net/<the-table-path>"` and change the 
        - `<container-name>` to the container were your delta-table resides(sink container),
        - `<account-name>` to your storage account name,
        - `<the-table-path>` to the name of your Delta-lake table.
     - `bearerToken` ; a number of digits/characters you'd like to use as a token for authorization.
     - `port` ; you can change the port number to your desired port number.
     - `host`; you can change the host to any desired `ipv4 address` of your choice. Here we are using the localhost. 


    ``` 
    # The format version of this config file
    version: 1
    # Config shares/schemas/tables to share
    shares:
    - name: "share2"
    schemas:
    - name: "schema2"
        tables:
        - name: "table3"
        # Azure Data Lake Storage Gen2. See https://github.com/delta-io/delta-sharing#azure-data-lake-storage-gen2 for how to config the credentials
        location: "abfss://<container-name>@<account-name}.dfs.core.windows.net/<the-table-path>"
        cdfEnabled: true
    # Set the host name that the server will use
    host: "localhost"
    # server authentication
    authorization:
        bearerToken: <token>
    # Set the port that the server will listen on. Note: using ports below 1024 
    # may require a privileged user in some operating systems.
    port: 8080
    # Set the url prefix for the REST APIs
    endpoint: "/delta-sharing"
    # Set the timeout of S3 presigned url in seconds
    preSignedUrlTimeoutSeconds: 3600
    # How many tables to cache in the server
    deltaTableCacheSize: 10
    # Whether we can accept working with a stale version of the table. This is useful when sharing
    # static tables that will never be changed.
    stalenessAcceptable: false
    # Whether to evaluate user provided `predicateHints`
    evaluatePredicateHints: false
    
    ```


### Profile File Format

A profile file is a JSON file that contains the information for a recipient to access shared data on a Delta Sharing server.
- `shareCredentialsVersion`; The file format version of the profile file. 
- `endpoint`; The url of the sharing server.
- `bearerToken`; The bearer token to access the server.

If you should make changes to the `endpoint`, and the `bearerToken`, please do well to update such changes in the profile, that is `docai-datasets.share`.


## How to run the program
 - install the packages in the `requirements.txt` file.
    `pip3 install -r requirements.txt`

- Start the server by Running the following shell command:
    - `cd` into delta-sharing-server-0.4.0 folder
    - Run the code in terminal `bin/delta-sharing-server -- --config <the-server-config-yaml-file>`
    <the-server-config-yaml-file> should be the absolute path of the yaml file, which is in the `conf/delta-sharing-server.yaml`
    - You will see the event logs and your Serving `ipv4 address`, if run is successful

- Spilt your terminal, `cd` back to the root directory and Run the python script `python3 delta_share.py`. If successful, you should see the list of table name, schema, share and first 10 rows of the data. 
