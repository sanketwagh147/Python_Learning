# This works too 
"""
Explore typer library
"""
# def main(name: str):
    # print(f"Hello {name}")

import typer
from icecream import ic


app = typer.Typer()



# Using typer find GCD of two number

@app.command()
def find_gcd(num_1:int, num_2:int):
    """Generates GCD

    Args:
        num_1 (int): first number
        num_2 (int): second number

    Returns:
        _type_: int
    """
    while num_2 !=0:
        # 1 liner
        # num_1, num_2 = num_2, num_1 % num_2

        # Euclidean 
        temp = num_2
        num_2 = num_1 % num_2
        num_1 = temp

    print(f"GCD is {num_1}")
    return num_1

@app.command()
def find_gcd_factor(num_1:int, num_2:int):
    """Generates GCD

    Args:
        num_1 (int): first number
        num_2 (int): second number

    Returns:
        _type_: int
    """
    fact_1 = [ i for i in range(1, num_1 + 1) if num_1 % i == 0]
    fact_2 = [ i for i in range(1, num_2 + 1) if num_2 % i == 0]

    s1 = set(fact_1)   
    s2 = set(fact_2)   
    ic(s1)
    ic(s2)

    common_set = s1.intersection(s2)
    max_f = max(list(common_set))

    print(f"GCD is {max_f}")
    return num_1


if __name__ == "__main__":
    # print(find_gcd(48,64))
    app()