import timeit

def exchangeable_value1(budget, exchange_rate, spread, denomination):
    tospread = 1 + spread/100
    torate = exchange_rate * tospread
    tochange = budget / torate
    return (tochange - ((tochange % denomination)))

def exchangeable_value2(budget, exchange_rate, spread, denomination):
    # 1. Calculate the actual rate (base rate + spread percentage)
    actual_rate = exchange_rate * (1 + spread / 100)
    
    # 2. Calculate the total amount of new currency we can buy
    total_new_currency = budget / actual_rate
    
    # 3. Calculate how many WHOLE bills we can get, and multiply by their denomination
    return int((total_new_currency // denomination) * denomination)


t1 = timeit.timeit("exchangeable_value1(127.25, 1.20, 10, 20)", globals=globals(), number=1000000)
# 80.0

t2 = timeit.timeit("exchangeable_value2(127.25, 1.20, 10, 20)", globals=globals(), number=1000000)
# 80

print(f"Function 1 (Humanoid): {t1:.3f} seconds (per 1M calls)")
print(f"Function 2 (Siliconoid): {t2:.3f} seconds (per 1M calls)")