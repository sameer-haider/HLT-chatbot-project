import aiml
import xml.etree.ElementTree as ET
from nlp import best_match, named_entity_recognition

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

# Set the bot's name
kernel.setBotPredicate("name", "TARS")

# Enter the main interaction loop
while True:
    # Get user input
    message = input("> ").upper()
    match = best_match(message, patterns)
    # print(match)

    ner = named_entity_recognition(message)
    # print(ner)

    # Get bot response
    response = kernel.respond(match)

    # Print the bot's response
    print(response)
