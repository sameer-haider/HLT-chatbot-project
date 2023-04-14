import aiml
import xml.etree.ElementTree as ET
import nlp


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

# Enter the main interaction loop
while True:
    # Get user input
    message = input("> ").upper()
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
    print(response)
