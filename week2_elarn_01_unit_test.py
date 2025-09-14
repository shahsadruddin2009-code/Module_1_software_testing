import os

def calculate_discount(loyalty_points):
    """
    Calculate the discount percentage based on customer loyalty points.

    Parameters:
    -----------
    loyalty_points : int
        The number of loyalty points accumulated by the customer.

    Returns:
    --------
    int
        The discount percentage:
        - 20% if loyalty_points >= 1000
        - 10% if loyalty_points >= 500 and < 1000
        - 0% if loyalty_points < 500

    Examples:
    ---------
    >>> calculate_discount(1500)
    20
    >>> calculate_discount(750)
    10
    >>> calculate_discount(200)
    0
    """
    if loyalty_points >= 1000:
        return 20  # 20% discount
    elif loyalty_points >= 500:
        return 10  # 10% discount
    else:
        return 0

os.system('cls')
while True:
    loyalty_points = input("Enter your loyalty points: ")
    if loyalty_points.isdigit() and int(loyalty_points) >= 0:
        discount = int(loyalty_points)
        break
    else:
        continue
calculate_discount(discount)