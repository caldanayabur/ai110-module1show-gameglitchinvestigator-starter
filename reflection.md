# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

The game looked like a number guessing game, but it didn't work correctly.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

First, the game was giving me wrong hints, so I was getting farther away from the secret number instead of closer.
Second, the "hard" mode was easier than normal mode.
Third, the "easy" mode had fewer attempts than normal mode.
Fourth, the game ignored difficulty level and always gave the same number of attempts.
Five, the game didn't prevent me from entering invalid inputs such as an out of range number. 

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used Claude as a VS Code extension.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

The AI helped me separate the game logic from the UI code by moving the functions get_range_for_difficulty, parse_guess, check_guess, and update_score from app.py (UI logic) to logic_utils.py (game logic).

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

The AI deleted the replies I made on the reflection.md file, I assumed because it already fixed the bugs.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I played the game multiples times to see if the bugs I identified before were actually fixed. The AI also wrote several pytest cases.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.

The AI created a test case where it checked if the hint that was given to the user was correct. For example, if the secret number was 80 and the user guessed 50, the hint should say "Too low". I ran this test using pytest and it passed successfully.

- Did AI help you design or understand any tests? How?

One test that the AI helped me with was to test that the game rewards you for guessing faster the correct number. The test checked if the score was higher when the user guessed the number in fewer attempts.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

The secret number kept changing because the script was being rerun multiple times, and the secret number was generated inside the script.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit reruns the entire script every time you interact with the app, such as clicking a button or entering input.

- What change did you make that finally gave the game a stable secret number?

I wrapped the secret number generation in a guard check, preventing a new number from being generated on every rerun. I also used Streamlit's session state to store the secret number, so it would persist across interactions.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

I found useful the tests, as normally I don't write tests for my code, and I just check if it works by running it and trying different inputs. I also never use Git, but I found it an useful habit to commit my changes in small steps, so I can easily go back if something breaks.

- What is one thing you would do differently next time you work with AI on a coding task?

Nex time I would identify the bugs myself before asking the AI for help, as the AI uses that information to give me better suggestions.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

This project made me realize the importance of testing AI generated code and also checking more carefully the suggestions that the AI gives.

## Challenge 5: AI Model Comparison

I told ChatGPT and Gemini that the hints in the game were backwards, and I asked them to fix the code.

Both models gave me a similar fix. However, Gemini went a step further by fixing the section of the code that randomly converts the secret number into a string on even-numbered attempts. It then provided a final solution for the bug I reported, along with an extra piece of code to ensure both the guess and the secret number are integers before comparing them.

Overall, I think Gemini’s fix is more complete.
