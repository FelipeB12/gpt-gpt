from openai import OpenAI
import typer # to be able to add styles to the app -> pip install "typer[all]"
from rich import print # Nicer prints
from rich.table import Table # Easily fix a table


#funtion to be able typer to call all the program
def main():

  #conection to OpenAI server 
  client = OpenAI(api_key="you key")

  # greeting 
  print("[bold green]Chat GPT Juan[/bold green]")
  
  # Add table of commands
  table = Table("Command","Description")
  table.add_row("exit","Leave the app")
  table.add_row("new","Start a new convertation")
  print(table)

  # Here you will be able to set the inputs and alter the behavior of the bot, who it is and what it has to do
  context = [
      #role = system, it is the behavior/training we want the bot answer with
      {"role": "system", "content": "You are a very helpful assistant."} 
  ]
  messages = context


  while True:# We start the loop so we can ask several times run the program only once 

    # The content-prompt we will work with will be gotten with the funtion __prompt()
    content = __prompt()
    
    if content == "new":
      # Message to open new conversation
      print("New conversation")
      # If the user needs a new conversartion, the convertation will be restored to context
      messages = [context]
      # If the use has started a new chat we now call the funtion to get a prompt and validate exit or continue
      content = __prompt()


    # With append we will add to the array messages the next message so the model will have context of the convesation 
    messages.append(
        #role = user, is the input we provide to the model, what we want the model to do
        {"role": "user", "content": content}
        )

    responce = client.chat.completions.create(
      #here you choose the modelk you want to use or have access to 
      model="gpt-3.5-turbo",
      #the message sent will be the array we have on line 11
      messages=messages 
    )

    # We can get the answer bellow with all the parameters and id this comes with, and to be able to access to only the messages we need to take the message from the array responce
    # print(responce)
    # The answer is save it to be sabed on the role of assistant
    responce_content = responce.choices[0].message.content

    # At this point we have the answer of the model that now we will save to have more context in the conversation 
    messages.append(
        #role = assistant, is the context of the model where we now add the response so the are also saved
        {"role": "assistant", "content": responce_content}
        )

    print(f"[bold green]>  [/bold green][green]{responce_content}[/green]")


# Funtion that will manage the promt from the user, and we specify wewill get and string
def __prompt() -> str:
  # prompt will take the message written on terminal to send it to the request with typer
  prompt = typer.prompt("\n¿What is your question? ")
  # In case we need to stop the loop we create a comand 
  if prompt == "exit":
    # Confirmation of leaving the app with typer ans save it on a boolean variable
    exit=typer.confirm("¿Are you sure?")
    if exit: 
      # Say bye
      print("Have a good day!")
      # As the program is managed by typer, we stop it with typer
      raise typer.Abort()
    # If the person do not confirm we call the funtion again it will ask again
    return __prompt()
  return prompt


# This will call the funtion that will contain the entire proyect to be able to manage it with typer
if __name__ == "__main__":
  typer.run(main)


# el programa se ejecuta en terminal con "python -u main.py"