# **Protocol vs ABC Overview**

# | Aspect | **Protocol** | **abc.ABC** |
# |--------|-------------|-------------|
# | **Type** | Structural typing (duck typing) | Nominal typing (inheritance) |
# | **Enforcement** | Static type checking only | Runtime enforcement |
# | **Inheritance** | No inheritance required | Must inherit from ABC |
# | **When checked** | Type checker (mypy, etc.) | Runtime when methods called |
# | **Flexibility** | Very flexible | More rigid |

## **Protocol (Structural Typing)**

## **What it is:**
# - Defines an interface based on **structure** (what methods/attributes exist)
# - No inheritance required - if it "looks like a duck and quacks like a duck"
# - Only enforced by static type checkers (mypy, PyCharm, VS Code)
