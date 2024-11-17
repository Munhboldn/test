import streamlit as st
import random
from fuzzywuzzy import process

# Dictionary with irregular verbs (base, past, and past participle forms)
verb_dict = {
    "arise": {"past": "arose", "participle": "arisen"},
    "be": {"past": "was/were", "participle": "been"},
    "bear": {"past": "bore", "participle": "born"},
    "become": {"past": "became", "participle": "become"},
    "begin": {"past": "began", "participle": "begun"},
    "bend": {"past": "bent", "participle": "bent"},
    "bet": {"past": "bet", "participle": "bet"},
    "bite": {"past": "bit", "participle": "bitten"},
    "bleed": {"past": "bled", "participle": "bled"},
    "blow": {"past": "blew", "participle": "blown"},
    "break": {"past": "broke", "participle": "broken"},
    "bring": {"past": "brought", "participle": "brought"},
    "build": {"past": "built", "participle": "built"},
    "burn": {"past": "burned/burnt", "participle": "burned/burnt"},
    "buy": {"past": "bought", "participle": "bought"},
    "catch": {"past": "caught", "participle": "caught"},
    "choose": {"past": "chose", "participle": "chosen"},
    "come": {"past": "came", "participle": "come"},
    "cost": {"past": "cost", "participle": "cost"},
    "creep": {"past": "crept", "participle": "crept"},
    "cut": {"past": "cut", "participle": "cut"},
    "do": {"past": "did", "participle": "done"},
    "draw": {"past": "drew", "participle": "drawn"},
    "drink": {"past": "drank", "participle": "drunk"},
    "drive": {"past": "drove", "participle": "driven"},
    "eat": {"past": "ate", "participle": "eaten"},
    "fall": {"past": "fell", "participle": "fallen"},
    "feel": {"past": "felt", "participle": "felt"},
    "fight": {"past": "fought", "participle": "fought"},
    "find": {"past": "found", "participle": "found"},
    "fly": {"past": "flew", "participle": "flown"},
    "forget": {"past": "forgot", "participle": "forgotten"},
    "forgive": {"past": "forgave", "participle": "forgiven"},
    "freeze": {"past": "froze", "participle": "frozen"},
    "get": {"past": "got", "participle": "gotten/got"},
    "give": {"past": "gave", "participle": "given"},
    "go": {"past": "went", "participle": "gone"},
    "grow": {"past": "grew", "participle": "grown"},
    "hang": {"past": "hung", "participle": "hung"},
    "have": {"past": "had", "participle": "had"},
    "hear": {"past": "heard", "participle": "heard"},
    "hide": {"past": "hid", "participle": "hidden"},
    "hit": {"past": "hit", "participle": "hit"},
    "hold": {"past": "held", "participle": "held"},
    "hurt": {"past": "hurt", "participle": "hurt"},
    "keep": {"past": "kept", "participle": "kept"},
    "kneel": {"past": "knelt", "participle": "knelt"},
    "know": {"past": "knew", "participle": "known"},
    "lay": {"past": "laid", "participle": "laid"},
    "lead": {"past": "led", "participle": "led"},
    "leave": {"past": "left", "participle": "left"},
    "lend": {"past": "lent", "participle": "lent"},
    "let": {"past": "let", "participle": "let"},
    "lie": {"past": "lay", "participle": "lain"},
    "light": {"past": "lit/lighted", "participle": "lit/lighted"},
    "lose": {"past": "lost", "participle": "lost"},
    "make": {"past": "made", "participle": "made"},
    "mean": {"past": "meant", "participle": "meant"},
    "meet": {"past": "met", "participle": "met"},
    "pay": {"past": "paid", "participle": "paid"},
    "put": {"past": "put", "participle": "put"},
    "quit": {"past": "quit", "participle": "quit"},
    "read": {"past": "read", "participle": "read", "pronunciation": "/red/"},
    "ride": {"past": "rode", "participle": "ridden"},
    "ring": {"past": "rang", "participle": "rung"},
    "rise": {"past": "rose", "participle": "risen"},
    "run": {"past": "ran", "participle": "run"},
    "say": {"past": "said", "participle": "said"},
    "see": {"past": "saw", "participle": "seen"},
    "sell": {"past": "sold", "participle": "sold"},
    "send": {"past": "sent", "participle": "sent"},
    "set": {"past": "set", "participle": "set"},
    "sew": {"past": "sewed", "participle": "sewn/sewed"},
    "shake": {"past": "shook", "participle": "shaken"},
    "shine": {"past": "shone", "participle": "shone"},
    "shoot": {"past": "shot", "participle": "shot"},
    "show": {"past": "showed", "participle": "shown"},
    "shrink": {"past": "shrank", "participle": "shrunk"},
    "shut": {"past": "shut", "participle": "shut"},
    "sing": {"past": "sang", "participle": "sung"},
    "sink": {"past": "sank", "participle": "sunk"},
    "sit": {"past": "sat", "participle": "sat"},
    "sleep": {"past": "slept", "participle": "slept"},
    "slide": {"past": "slid", "participle": "slid"},
    "sling": {"past": "slung", "participle": "slung"},
    "slink": {"past": "slunk", "participle": "slunk"},
    "speak": {"past": "spoke", "participle": "spoken"},
    "spend": {"past": "spent", "participle": "spent"},
    "spill": {"past": "spilt/spilled", "participle": "spilt/spilled"},
    "spin": {"past": "spun", "participle": "spun"},
    "spit": {"past": "spat", "participle": "spat"},
    "spread": {"past": "spread", "participle": "spread"},
    "spring": {"past": "sprang", "participle": "sprung"},
    "stand": {"past": "stood", "participle": "stood"},
    "steal": {"past": "stole", "participle": "stolen"},
    "stick": {"past": "stuck", "participle": "stuck"},
    "sting": {"past": "stung", "participle": "stung"},
    "stink": {"past": "stank", "participle": "stunk"},
    "strike": {"past": "struck", "participle": "struck"},
    "swear": {"past": "swore", "participle": "sworn"},
    "sweep": {"past": "swept", "participle": "swept"},
    "swim": {"past": "swam", "participle": "swum"},
    "take": {"past": "took", "participle": "taken"},
    "teach": {"past": "taught", "participle": "taught"},
    "tear": {"past": "tore", "participle": "torn"},
    "tell": {"past": "told", "participle": "told"},
    "think": {"past": "thought", "participle": "thought"},
    "throw": {"past": "threw", "participle": "thrown"},
    "understand": {"past": "understood", "participle": "understood"},
    "wake": {"past": "woke", "participle": "woken"},
    "wear": {"past": "wore", "participle": "worn"},
    "win": {"past": "won", "participle": "won"},
    "write": {"past": "wrote", "participle": "written"},
    "behold": {"past": "beheld", "participle": "beheld"},
    "bind": {"past": "bound", "participle": "bound"},
    "breed": {"past": "bred", "participle": "bred"},
    "cling": {"past": "clung", "participle": "clung"},
    "deal": {"past": "dealt", "participle": "dealt"},
    "dwell": {"past": "dwelt/dwelled", "participle": "dwelt/dwelled"},
    "fit": {"past": "fit/fitted", "participle": "fit/fitted"},
    "flee": {"past": "fled", "participle": "fled"},
    "grind": {"past": "ground", "participle": "ground"},
    "leap": {"past": "leapt/leaped", "participle": "leapt/leaped"},
    "plead": {"past": "pled/pleaded", "participle": "pled/pleaded"},
    "prove": {"past": "proved", "participle": "proven/proved"},
    "smell": {"past": "smelt/smelled", "participle": "smelt/smelled"},
    "spell": {"past": "spelt/spelled", "participle": "spelt/spelled"},
    "spoil": {"past": "spoilt/spoiled", "participle": "spoilt/spoiled"},
    "strive": {"past": "strove", "participle": "striven"},
    "thrust": {"past": "thrust", "participle": "thrust"},
    "weep": {"past": "wept", "participle": "wept"},
    "wind": {"past": "wound", "participle": "wound"}
}

# Function to set a background image from a URL
def add_bg_from_url(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Function to find the closest match using FuzzyWuzzy
def find_closest_match(input_word, choices):
    match, score = process.extractOne(input_word, choices)
    return match, score

# Function to display a verb's forms in a table
def display_verb_table(base, past, participle):
    st.markdown(
        """
        <style>
        .table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            border-radius: 8px;
            overflow: hidden;
        }
        .table th, .table td {
            padding: 12px;
            text-align: center;
            border: 1px solid #444;
            font-size: 16px;
            font-family: 'Arial', sans-serif;
            color: white;
        }
        .table th {
            background-color: #333;
            font-weight: bold;
        }
        .table tr:nth-child(odd) {
            background-color: #444;
        }
        .table tr:nth-child(even) {
            background-color: #555;
        }
        .table tr:hover {
            background-color: #666;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f"""
        <table class="table">
            <tr>
                <th>Base Form</th>
                <th>Past Tense</th>
                <th>Past Participle</th>
            </tr>
            <tr>
                <td>{base}</td>
                <td>{past}</td>
                <td>{participle}</td>
            </tr>
        </table>
    """, unsafe_allow_html=True)

# Initialize session states
if "random_verb" not in st.session_state:
    st.session_state.random_verb = None

if "search_term" not in st.session_state:
    st.session_state.search_term = None

if "quiz_verb" not in st.session_state:
    st.session_state.quiz_verb = None

if "favorites" not in st.session_state:
    st.session_state.favorites = []

# Set background image
image_url = "https://github.com/Munhboldn/test/blob/main/dark%20academia.jpg?raw=true"
add_bg_from_url(image_url)

# Title and description
st.title("✨ Irregular Verb Form Finder ✨")
st.write("""
Enter an irregular verb to see its **past tense** and **past participle** forms. 
Use the random verb button for inspiration, add verbs to your favorites, or test yourself with the quiz!
""")

# Sidebar for Favorites
st.sidebar.header("Your Favorites")
if st.session_state.favorites:
    for verb in st.session_state.favorites:
        st.sidebar.write(f"- {verb.capitalize()}")
    if st.sidebar.button("Clear Favorites"):
        st.session_state.favorites.clear()
        st.sidebar.success("Favorites cleared.")

# Random Verb Button
if st.button("🔄 Show Me a Random Verb"):
    st.session_state.random_verb = random.choice(list(verb_dict.keys()))
    st.session_state.search_term = ""  # Clear search input when random button is clicked

# Text input for user to search a verb
search_input = st.text_input("Search for a verb:")

# Update the session state with the user's search term
if search_input.strip():
    st.session_state.search_term = search_input.strip().lower()
    st.session_state.random_verb = None  # Clear random verb if user types something

# Determine which verb to display based on user input or random verb
if st.session_state.search_term:
    current_verb = st.session_state.search_term
elif st.session_state.random_verb:
    current_verb = st.session_state.random_verb
else:
    current_verb = None

# Display verb forms or suggestions if a verb is selected
if current_verb:
    if current_verb in verb_dict:
        st.write(f"### Forms for **{current_verb.capitalize()}**")
        display_verb_table(
            current_verb.capitalize(),
            verb_dict[current_verb]["past"],
            verb_dict[current_verb]["participle"]
        )
        # Add to Favorites Button
        if st.button(f"⭐ Add {current_verb.capitalize()} to Favorites"):
            if current_verb not in st.session_state.favorites:
                st.session_state.favorites.append(current_verb)
                st.success(f"Added **{current_verb.capitalize()}** to favorites!")
            else:
                st.info(f"**{current_verb.capitalize()}** is already in your favorites.")
    else:
        # Use FuzzyWuzzy to find the closest match
        closest_match, score = find_closest_match(current_verb, list(verb_dict.keys()))
        if score >= 80:  # Set a threshold for matching accuracy
            st.warning(f"No exact match found for **{current_verb}**. Did you mean **{closest_match.capitalize()}**? (Match Score: {score})")
            if st.button(f"⭐ Add {closest_match.capitalize()} to Favorites"):
                if closest_match not in st.session_state.favorites:
                    st.session_state.favorites.append(closest_match)
                    st.success(f"Added **{closest_match.capitalize()}** to favorites!")
                else:
                    st.info(f"**{closest_match.capitalize()}** is already in your favorites.")
            display_verb_table(
                closest_match.capitalize(),
                verb_dict[closest_match]["past"],
                verb_dict[closest_match]["participle"]
            )
        else:
            st.warning("No close matches found. Try another verb or check your spelling.")

# Initialize session state variables if they don't exist
if 'quiz_verb' not in st.session_state:
    st.session_state.quiz_verb = None
if 'quiz_past' not in st.session_state:
    st.session_state.quiz_past = ""
if 'quiz_participle' not in st.session_state:
    st.session_state.quiz_participle = ""

# Quiz Section
st.title("🎯 Irregular Verb Quiz")

# Button to trigger quiz
if st.button("🎲 Quiz Me!"):
    # Set up or reset the quiz state before rendering the quiz widget
    st.session_state.quiz_verb = random.choice(list(verb_dict.keys()))
    st.session_state.quiz_past = ""  # Reset past tense answer
    st.session_state.quiz_participle = ""  # Reset participle answer

# Render quiz if quiz verb is selected
if st.session_state.quiz_verb:
    st.write(f"What is the **past tense** and **past participle** of **{st.session_state.quiz_verb.capitalize()}**?")
    
    # Create text input fields for past tense and past participle
    # Use the current session state value for past and participle inputs
    answer_past = st.text_input("Past Tense:", key="quiz_past", value=st.session_state.quiz_past)
    answer_participle = st.text_input("Past Participle:", key="quiz_participle", value=st.session_state.quiz_participle)

    # Button to submit answers
    if st.button("Submit Answers"):
        correct_past = verb_dict[st.session_state.quiz_verb]["past"].lower()
        correct_participle = verb_dict[st.session_state.quiz_verb]["participle"].lower()

        # Function to handle multiple correct answers separated by '/'
        def check_answer(user_ans, correct_ans):
            correct_options = [ans.strip().lower() for ans in correct_ans.split('/')]
            return user_ans.strip().lower() in correct_options

        past_correct = check_answer(answer_past, correct_past)
        participle_correct = check_answer(answer_participle, correct_participle)

        # Display feedback
        if past_correct and participle_correct:
            st.success("✅ Both past tense and past participle are correct!")
        else:
            if not past_correct:
                st.error(f"❌ Wrong past tense! The correct answer(s): **{verb_dict[st.session_state.quiz_verb]['past']}**.")
            else:
                st.success("✅ Correct past tense!")
            
            if not participle_correct:
                st.error(f"❌ Wrong past participle! The correct answer(s): **{verb_dict[st.session_state.quiz_verb]['participle']}**.")
            else:
                st.success("✅ Correct past participle!")

        # Clear quiz state after submission
        st.session_state.quiz_verb = None

# Option to restart the quiz
if not st.session_state.quiz_verb and st.button("Start a New Quiz"):
    # Reset the quiz state for a new round
    st.session_state.quiz_verb = random.choice(list(verb_dict.keys()))
    st.session_state.quiz_past = ""
    st.session_state.quiz_participle = ""
