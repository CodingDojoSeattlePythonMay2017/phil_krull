sq = 10
for num in range(100, 1001):
    f = 'Foo'
    b = 'Bar'
    # perfect square
    if num == sq * sq:
        f = ''
        # print num, 'Bar'
        sq += 1
    # find prime
    is_prime = True
    i = 2
    while is_prime and i < num:
        if num % i == 0:
            is_prime = False
        i += 1

    if is_prime:
        b = ''
        # print num, 'Foo'

    print num, f+b
