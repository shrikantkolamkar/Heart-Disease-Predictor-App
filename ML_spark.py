from pyspark.sql import SparkSession

data = [('James','','Smith','1991-04-01','M',3000),
        ('Michael','Rose','','2000-05-19','M',4000),
        ('Robert','','Williams','1978-09-05','M',4000),
        ('Maria','Anne','Jones','1967-12-01','F',4000),
        ('Jen','Mary','Brown','1980-02-17','F',-1)]

columns = ["firstname","middlename","lastname","dob","gender","salary"]
df = SparkSession.builder.appName("PySparkExample").getOrCreate().createDataFrame(data=data, schema = columns)

# Display the contents of the DataFrame
df.show()

# Select only the firstname and salary columns
df_subset = df.select(["firstname", "salary"])
df_subset.show()

# Filter the DataFrame to only include rows where salary is greater than 0
df_filtered = df.filter(df.salary > 0)
df_filtered.show()

# Group the DataFrame by the gender column and calculate the average salary for each group
df_grouped = df.groupBy("gender").mean("salary")
df_grouped.show()

# Stop the SparkSession
SparkSession.getActiveSession().stop()