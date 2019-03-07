# -- FILE: features/environment.py,

def before_all(context):
    print("-------------------")
    print("|   BEFORE ALL    |")
    print("-------------------")

def before_scenario(context, scenario):
    print("-------------------")
    print("| BEFORE SCENARIO |")
    print("-------------------")
    print("-------------------")
    print("|    SCENARIO     |")
    print("-------------------")
    
def after_scenario(context, scenario):
    print("\n-------------------")
    print("| AFTER SCENARIO  |")
    print("-------------------\n")
    print("----------------------------------------\n")

def after_all(context):
    print("-------------------")
    print("|    AFTER ALL    |")
    print("-------------------\n")
    print("========================================\n")