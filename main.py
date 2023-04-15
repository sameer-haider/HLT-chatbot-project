import aiml
import xml.etree.ElementTree as ET
import nlp
import user

# Load the XML file
tree = ET.parse("brain.xml")

# Find all patterns in the XML
root = tree.getroot()
patterns = []
for category in root.findall("category"):
    pattern = category.find("pattern").text
    patterns.append(str(pattern))

# Create kernel and load aiml
kernel = aiml.Kernel()
kernel.learn("brain.xml")
kernel.setBotPredicate("name", "TARS")

# Make new user or pick previous user
username = input('Enter a username, or enter "new" if you want to make a new user: ')
if username == "new":
    username = input("Choose a username (chatbot will address you by this): ")
    age = input("State your age: ")
    like_1_str = input(
        "Do you like space science. Interstellar talks a lot about space. Enter (y/n):"
    )
    like_1 = 0
    if like_1_str == "y":
        like_1 = 1
    like_2_str = input("Do you like Matthew McConaughey? Enter (y/n):")
    like_2 = 0
    if like_2_str == "y":
        like_2 = 1
    user.create_user(username=username, age=age, like_1=like_1, like_2=like_2)
    print("TARS: " + kernel.respond("NEW USER " + username))
else:
    print("TARS: " + kernel.respond("RETURNING USER " + username))

info = user.get_user_by_username(username)
like_1 = info[3]
if like_1 == 1:
    kernel.respond("SET LIKE 1 YES")
else:
    kernel.respond("SET LIKE 1 NO")
like_2 = info[4]
if like_2 == 1:
    kernel.respond("SET LIKE 2 YES")
else:
    kernel.respond("SET LIKE 2 NO")

# Enter the main interaction loop
while True:
    # Get user input
    message = input("USER: ").upper()
    match = nlp.best_match(message, patterns)
    # print(match)

    # NER for pattern asking "who played * in movie"
    ner = nlp.named_entity_recognition(message)
    actor = nlp.extract_person(ner)
    if "*" in match:
        match = match.replace("*", actor)

    # Get bot response
    response = kernel.respond(match)

    # Print the bot's response
    print("TARS: " + response)

    if "Goodbye" in response:
        break
