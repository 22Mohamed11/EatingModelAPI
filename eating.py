import json
from flask import Flask, request, jsonify
import pickle

#model_url = "https://firebasestorage.googleapis.com/v0/b/workshop1-87b4b.appspot.com/o/meal_planner_model.pk1?alt=media&token=b555f559-6e9d-4cc0-ac99-f4712fdad8e5"
app = Flask(__name__)

class Food:
    def __init__(self, name, category, serve, meal, calories):
        self.name = name
        self.category = category
        self.serve = serve
        self.meal = meal
        self.calories = calories

def calculate_bmi(weight, height):
    return weight / ((height/100) ** 2)

def calculate_daily_calories(bmi, weight, age, gender):
    if bmi < 18.5:
        response_msg = "You are underweight."
        if gender == 'male' and 65 <= age <= 75:
            daily_calories = 2800
        elif gender == 'male' and age >= 75:
            daily_calories = 2000
        elif gender == 'female' and 65 <= age <= 75:
            daily_calories = 2200
        elif gender == 'female' and age >= 75:
            daily_calories = 1800
        else:
            daily_calories = weight * 40
    elif 18.5 <= bmi <= 24.9:
        response_msg = "Your weight is ideal."
        if gender == 'male' and 65 <= age <= 75:
            daily_calories = 2600
        elif gender == 'male' and age >= 75:
            daily_calories = 1800
        elif gender == 'female' and 65 <= age <= 75:
            daily_calories = 2000
        elif gender == 'female' and age >= 75:
            daily_calories = 1600
        else:
            daily_calories = weight * 30
    elif 25 <= bmi <= 29.9:
        response_msg = "You are overweight."
        if gender == 'male' and 65 <= age <= 75:
            daily_calories = 2200
        elif gender == 'male' and age >= 75:
            daily_calories = 1600
        elif gender == 'female' and 65 <= age <= 75:
            daily_calories = 1600
        elif gender == 'female' and age >= 75:
            daily_calories = 1400
        else:
            daily_calories = weight * 20
    else:
        response_msg = "You are obese."
        if gender == 'male' and 65 <= age <= 75:
            daily_calories = 2000
        elif gender == 'male' and age >= 75:
            daily_calories = 1400
        elif gender == 'female' and 65 <= age <= 75:
            daily_calories = 1400
        elif gender == 'female' and age >= 75:
            daily_calories = 1200
        else:
            daily_calories = weight * 10

    return response_msg, daily_calories

def suggest_meals(food_dataset):
    breakfast_meal = [food for food in food_dataset if food.meal == "Breakfast"]
    lunch_meal = [food for food in food_dataset if food.meal == "Lunch"]
    dinner_meal = [food for food in food_dataset if food.meal == "Dinner"]
    snacks = [food for food in food_dataset if food.category == "Snack"]

    return breakfast_meal, lunch_meal, dinner_meal, snacks

# Load the model
with open("G:/EatingAPI/meal_planner_model.pk1", "rb") as model_file:
    model = pickle.load(model_file)
    
food_data = [
    Food("Oat", "Whole Grains", "1 cup", "Breakfast", 150),
    Food("Cherries", "Fruit", "1 cup", "Breakfast", 50),
    Food("Meat", "Protein", "4 oz", "Lunch", 250),
    Food("Rice", "Carbs", "1 cup", "Lunch", 200),
    Food("Avocado", "Fat", "1/2", "Lunch", 160),
    Food("Carrots", "Vegetables", "1 cup", "Lunch", 50),
]

@app.route('/calculate_bmi', methods=['POST'])
def calculate_bmi_route():
    data = request.get_json()
    weight = data['weight']
    height = data['height']
    bmi = model['calculate_bmi'](weight, height)
    return jsonify({"bmi": bmi})

@app.route('/calculate_daily_calories', methods=['POST'])
def calculate_daily_calories_route():
    data = request.get_json()
    bmi = data['bmi']
    weight = data['weight']
    age = data['age']
    gender = data['gender']
    response_msg, daily_calories = calculate_daily_calories(bmi, weight, age, gender)
    return jsonify({"response_msg": response_msg, "daily_calories": daily_calories})

@app.route('/suggest_meals', methods=['GET'])
def suggest_meals_route():
    breakfast, lunch, dinner, snacks = model['suggest_meals'](food_data)
    breakfast_table = [["Category", "Food", "Serve"]]
    for food in breakfast:
        breakfast_table.append([food.category, food.name, food.serve])
    lunch_table = [["Category", "Food", "Serve"]]
    for food in lunch:
        lunch_table.append([food.category, food.name, food.serve])
    dinner_table = [["Category", "Food", "Serve"]]
    for food in dinner:
        dinner_table.append([food.category, food.name, food.serve])
    snacks_table = [["Category", "Food", "Serve"]]
    for food in snacks:
        snacks_table.append([food.category, food.name, food.serve])
    return jsonify({
        "breakfast": breakfast_table[1:],
        "lunch": lunch_table[1:],
        "dinner": dinner_table[1:],
        "snacks": snacks_table[1:]
    })

if __name__ == "__main__":
    app.run(debug=True)