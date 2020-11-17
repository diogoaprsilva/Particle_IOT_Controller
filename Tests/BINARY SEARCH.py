def search (numbers, x):
    for number in numbers:
        if number == x:
            return True
    return False


def binary_search(numbers2, items):
    first = 0
    last = len(numbers2) - 1
    found = False
    while (first <= last and not found):
        mid = (first + last) // 2
        if numbers2[mid] == items:
            found = True
        else:
            if items < numbers2[mid]:
                last = mid - 1
            else:
                first = mid + 1
    return found



x = 200
numbers = [2,4,5,6,7,8,9,10,11,100]
print("Searching for %s" % x)
print(search(numbers, x))
print("Binary searching for %s" % x)
print(binary_search(numbers, x))
print('-------------')

x = 200
numbers = [2,4,5,6,7,8,9,10,11,100, 123, 145, 167, 168, 178, 179, 182, 184, 186, 188, 190, 200, 205, 216, 228, 256]
print("Searching for %s" % x)
print(search(numbers, x))
print("Binary searching for %s" % x)
print(binary_search(numbers, x))
print('-------------')

x = 200
numbers = [1, 200]
print("Searching for %s" % x)
print(search(numbers, x))
print("Binary searching for %s" % x)
print(binary_search(numbers, x))
print('-------------')

x = 200
numbers = []
print("Searching for %s" % x)
print(search(numbers, x))
print("Binary searching for %s" % x)
print(binary_search(numbers, x))
print('-------------')