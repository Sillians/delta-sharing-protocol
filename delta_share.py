from __future__ import print_function
import delta_sharing
import os
import logging

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)
logger.info("Delta Sharing log information...")


logger.info(
    "Pointing to the Profile file in the local file system or a file on a remote storage..."
)
profile_file = os.path.dirname(__file__) + "docai-datasets.share"


logger.info("Creating a SharingClient...")
client = delta_sharing.SharingClient(profile_file)


client.list_all_tables()
logger.info("list of documentai tablename, share and schema...")
print(client.list_all_tables())


logger.info("Creating a url to access a shared table...")
table_url = profile_file + "#docaishare.docaischema.docaitable"
logger.info("Loading a table as a Pandas DataFrame...")
data = delta_sharing.load_as_pandas(table_url)


logger.info("outputing first 10 rows of the data...")
print(data.head(10))
