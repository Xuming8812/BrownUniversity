import numpy as np

def fibonacci(n):
    #check corner case
    if n < 0:
        raise Exception('negative input')
    #define the matrix
    matrix = np.matrix([[1, 1],[1, 0]])
    #call the helper function
    return helper(matrix,n)[0,1]

def helper(matrix,n):
    #check corner case
    if n < 0:
        raise Exception('negative input')
    #define the matrix
    result = np.matrix([[1, 0], [0, 1]])
    #loop until n = 0
    while(n!=0):
        #update result matrix
        if(n%2!=0):
            result = np.matmul(result, matrix)
        #divide n by 2 each iteration
        n = n//2
        #update the matrix each iteration
        matrix = np.matmul(matrix, matrix)
    
    return result

print(fibonacci(6))