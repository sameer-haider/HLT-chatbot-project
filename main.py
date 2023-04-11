import aiml

# Create kernel and load aiml
kernel = aiml.Kernel()
kernel.learn("brain.xml")

# Set the bot's name
kernel.setBotPredicate("name", "Interstellar_Bot")

# Enter the main interaction loop
while True:
    # Get user input
    message = input("> ").upper()
    print(message)

    # Get bot response
    response = kernel.respond(message)

    # Print the bot's response
    print(response)
