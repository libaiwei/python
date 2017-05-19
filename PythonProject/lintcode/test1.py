class solution:
    def fizzbuzz(self,n):
        results = []
        for i in range(1,n):
            if i % 3 == 0:
                results.append('fizz')
            elif i % 5 == 0:
                results.append('buzz')
            else:
                results.append(str(i))
        return results
results = solution().fizzbuzz(15)
print results
