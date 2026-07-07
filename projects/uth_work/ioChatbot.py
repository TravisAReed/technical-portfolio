from ollama import chat

#global vars
model1 = "medgemma1.5:4b"











def unloadModel(model):
    chat(
        model=model,
        messages=[],
        keep_alive=0,
    )

def runChatbot(model):
    # inp = 'not blank'
    # aiOut = "Enter your response and hit enter. Hit enter without content to end chat:\n"
    inp = input("Enter your response and hit enter. Hit enter without content to end chat at anytime. What would you like to know?\n")    
    response = None

    while inp != '': #each response "stateless" so it won't remember previous answers at all
        print('-------------------------------------------') #seperates each qa pair from each other
        response = chat(
        model=model, #had to first run "ollama pull medgemma1.5:4b" then checked with "ollama list"
        messages=[
            {
                "role": "user",
                "content": inp
            }
        ],
        # messages=[
        #     {
        #         "role": "user",
        #         "content": "Explain in simple terms what high fasting glucose can indicate."
        #     }
        # ],
        #keep_alive time updates to parameter's value each call so as long as being actively used it wont end
        # keep_alive=-1 #indefinitely
        # keep_alive=5 #default        
        )
        inp = input("AI Response:\n"+response.message.content+"\n\nPatient Answer:\n")
        

    
    #handling end of chat
    if (response == None):
        print("chat exited immediatly")
    else:
        # print(response.message.content)
        unloadModel(model)

runChatbot(model1)

unloadModel(model1) #here for safety but shouldn't be needed