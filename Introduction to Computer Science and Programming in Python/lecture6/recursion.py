def factorial(n):
    if (n == 1):
        return 1
    else:
        return n * factorial(n - 1)

print(factorial(4))

def printMove(fr, to):
    print('move from ' + str(fr) + ' to ' + str(to))

def Towers(n, fr, to, spare):
 if n == 1:
    printMove(fr, to)
 else:
    Towers(n-1,    fr, spare,    to)
    Towers(1,      fr,    to, spare)
    Towers(n-1, spare,    to,    fr)

Towers(2, 1, 2, 3)

def fibonacci(x):
    '''
    assumes x an int >= 0
    returns Fibonacci of x
    '''
    if x == 0 or x == 1:
        return 1
    else:
        return fibonacci(x - 1) + fibonacci(x - 2)

print(fibonacci(30))

def isPalindrome(s):
    
    def toChars(s):
        s = s.lower()
        ans = ''
        for c in s:
            if c in 'abcdefghijklmnopqrstuvwxyz':
                ans = ans + c
        return ans

    def isPal(s):
        if len(s) <= 1:
            return True
        else:
            return s[0] == s[-1] and isPal(s[1:-1])
        
    return isPal(toChars(s))


print(isPalindrome("Able was I, ere I saw Elba"))


def fibonacci_efficient(n, d):
    if n in d:
        return d[n]
    else:
        ans = fibonacci_efficient(n-1, d) + fibonacci_efficient(n-2, d)
        d[n] = ans
        return ans

d = {1:1, 2:2}
print(fibonacci_efficient(100, d))