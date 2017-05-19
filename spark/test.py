"""SimpleApp"""


from pyspark import SparkContext

logFile = "test"
sc = SparkContext("local","Simple A``pp")
logData = sc.textFile(logFile).cache()

numAs = logData.filter(lambda s: 'a' in s).count()
numBs = logData.filter(lambda s: 'b' in s).count()

print("Lines with a: %i, lines with b: %i"%(numAs, numBs))
