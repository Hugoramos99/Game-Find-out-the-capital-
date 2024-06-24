#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 13:30:44 2024

@author: hugoramos
"""
import streamlit as st
import requests
import random
import pycountry

# Function to get country data from API
def get_country_data():
    response = requests.get("https://restcountries.com/v3.1/all")
    if response.status_code == 200:
        return response.json()
    return []

# Function to get a random country and its capital
def get_random_country_and_capitals(countries):
    country = random.choice(countries)
    country_name = country['name']['common']
    capital = country['capital'][0] if 'capital' in country and country['capital'] else "Unknown"
    
    # Get 3 other random capitals
    capitals = [capital]
    while len(capitals) < 4:
        random_country = random.choice(countries)
        random_capital = random_country['capital'][0] if 'capital' in random_country and random_country['capital'] else None
        if random_capital and random_capital not in capitals:
            capitals.append(random_capital)
    
    random.shuffle(capitals)
    return country_name, capital, capitals

# Function to get country flag URL
def get_country_flag_url(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        if country:
            code = country.alpha_2.lower()
            return f"https://flagcdn.com/{code}.svg"
    except Exception as e:
        return None
    return None

# Function to update progress line for attempts
def update_attempts_progress(wrong_attempts):
    attempts_left = 3 - wrong_attempts
    return attempts_left / 3

# Streamlit UI setup
st.title("🌍 Guess the Capital Game 🎉")
st.write("Guess the capital of the randomly selected country. You have 3 lives!")

# Initialize session state
if 'countries' not in st.session_state:
    st.session_state.countries = get_country_data()
if 'country' not in st.session_state:
    st.session_state.country, st.session_state.correct_capital, st.session_state.options = get_random_country_and_capitals(st.session_state.countries)
if 'correct_attempts' not in st.session_state:
    st.session_state.correct_attempts = 0
if 'wrong_attempts' not in st.session_state:
    st.session_state.wrong_attempts = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'best_score' not in st.session_state:
    st.session_state.best_score = 0
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Function to reset game state
def reset_game():
    st.session_state.correct_attempts = 0
    st.session_state.wrong_attempts = 0
    st.session_state.country, st.session_state.correct_capital, st.session_state.options = get_random_country_and_capitals(st.session_state.countries)
    st.session_state.game_over = False
    st.session_state.dark_mode = False

# Function to check and update best score
def check_best_score():
    if st.session_state.correct_attempts > st.session_state.best_score:
        st.session_state.best_score = st.session_state.correct_attempts
        st.balloons()

# Display game over message
if st.session_state.game_over:
    if st.session_state.correct_attempts < st.session_state.best_score:
        st.session_state.dark_mode = True
    if st.session_state.dark_mode:
        st.markdown("""
            <style>
                body {
                    background: linear-gradient(45deg, #232526, #414345);
                    color: #ffffff;
                }
            </style>
        """, unsafe_allow_html=True)
    st.write("## 💀 Game Over!")
    st.write(f"Total correct answers: {st.session_state.correct_attempts}")
    check_best_score()
    st.write(f"Best score: {st.session_state.best_score}")
    st.success("Time to study!", icon="📚")
    if st.button("Play Again"):
        reset_game()
        st.experimental_rerun()
else:
    # Display the current country
    st.write(f"**Country:** {st.session_state.country}")
    flag_url = get_country_flag_url(st.session_state.country)
    if flag_url:
        st.image(flag_url, width=150)
    
    # Display the options as buttons
    for option in st.session_state.options:
        if st.button(option):
            if option == st.session_state.correct_capital:
                st.session_state.correct_attempts += 1
                st.write("Correct! 🎉")
            else:
                st.session_state.wrong_attempts += 1
                st.write("Wrong! 😞")
            
            # Check if game should continue or end
            if st.session_state.wrong_attempts >= 3:
                st.session_state.game_over = True
            else:
                st.session_state.country, st.session_state.correct_capital, st.session_state.options = get_random_country_and_capitals(st.session_state.countries)
            st.experimental_rerun()

    # Display the score
    st.write(f"Correct attempts: {st.session_state.correct_attempts}")
    
    # Display the progress line for wrong attempts
    attempts_progress = update_attempts_progress(st.session_state.wrong_attempts)
    st.write("Left Attempts:")
    st.progress(attempts_progress)

    # Crazy effect when 1 attempt is left
    if st.session_state.wrong_attempts == 2:
        st.markdown("""
            <style>
                body {
                    background: linear-gradient(45deg, #ff0000, #ff8000);
                    color: #ffffff;
                }
                .stButton>button {
                    animation: shake 0.5s;
                    animation-iteration-count: infinite;
                }
                @keyframes shake {
                    0% { transform: translate(1px, 1px) rotate(0deg); }
                    10% { transform: translate(-1px, -2px) rotate(-1deg); }
                    20% { transform: translate(-3px, 0px) rotate(1deg); }
                    30% { transform: translate(3px, 2px) rotate(0deg); }
                    40% { transform: translate(1px, -1px) rotate(1deg); }
                    50% { transform: translate(-1px, 2px) rotate(-1deg); }
                    60% { transform: translate(-3px, 1px) rotate(0deg); }
                    70% { transform: translate(3px, 1px) rotate(-1deg); }
                    80% { transform: translate(-1px, -1px) rotate(1deg); }
                    90% { transform: translate(1px, 2px) rotate(0deg); }
                    100% { transform: translate(1px, -2px) rotate(-1deg); }
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                body {
                    background: linear-gradient(135deg, #ff9a9e, #fad0c4);
                    color: #333;
                    font-family: 'Comic Sans MS', cursive, sans-serif;
                }
            </style>
        """, unsafe_allow_html=True)

# Custom CSS for cool styling
st.markdown("""
    <style>
        .stButton>button {
            background-color: #8e44ad;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #6c3483;
        }
        .stTextInput>div>div>input {
            background-color: #dcdcdc;
            color: #333;
            border: 2px solid #8e44ad;
            border-radius: 5px;
            padding: 10px;
        }
        h1, h4 {
            color: #8e44ad;
            text-shadow: 2px 2px #dcdcdc;
        }
    </style>
""", unsafe_allow_html=True)

# Display the best score
st.markdown(f"### 🏆 Best score: {st.session_state.best_score}")