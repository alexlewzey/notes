# Import SparkSession from pyspark.sql
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

spark = SparkSession.builder \
    .appName("MockDataFrameExample") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Create a mock DataFrame
data = [("James", "Smith", "USA", "CA"),
        ("Michael", "Rose", "USA", "NY"),
        ("Robert", "Williams", "USA", "CA"),
        ("Maria", "Jones", "USA", "FL")]
columns = ["firstname", "lastname", "country", "state"]

df = spark.createDataFrame(data, columns)

# Show the DataFrame
print("Original DataFrame:")
df.show()

# Add a new column
df = df.withColumn("age", lit(None))

# Show the DataFrame with the new column
print("DataFrame with new column 'age':")
df.show()

# Stop the SparkSession
spark.stop()
