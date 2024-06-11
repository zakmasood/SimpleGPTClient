import tkinter as tk
from tkinter import scrolledtext
import openai
import tiktoken

# Set your OpenAI API key here
openai.api_key = "YOUR API KEY HERE"

# Function to count the tokens in a message
def count_tokens(message, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(message))

# Function to handle sending messages to the OpenAI API
def send_message():
    user_message = user_input.get("1.0", tk.END).strip()
    if user_message:
        # Count the tokens in the user's message
        user_tokens = count_tokens(user_message)

        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, "You: " + user_message + " (Tokens used: ")
        token_start_index = chat_history.index(tk.END) # Get the current position
        chat_history.insert(tk.END, str(user_tokens))
        token_end_index = chat_history.index(tk.END) # Get the position after inserting token count
        chat_history.insert(tk.END, ")\n\n")

        # Highlight the token count in red
        chat_history.tag_add("token_highlight", token_start_index, token_end_index)
        chat_history.tag_configure("token_highlight", foreground="red")

        chat_history.config(state=tk.DISABLED)
        user_input.delete("1.0", tk.END)

        # Append user message to conversation history
        conversation_history.append({"role": "user", "content": user_message})

        # OpenAI API call using gpt-4-turbo
        response = openai.ChatCompletion.create(
            model="gpt-4o-2024-05-13",
	    #Add your own model!
            messages=conversation_history,
            max_tokens=4096,
            temperature=0.9,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6
        )

        ai_message = response.choices[0].message['content'].strip()

        # Append AI response to conversation history
        conversation_history.append({"role": "assistant", "content": ai_message})

        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, "AI: " + ai_message + "\n\n")
        chat_history.config(state=tk.DISABLED)

# Initialize conversation history
conversation_history = [
    {"role": "system", "content": "You are an AI assistant. The assistant is helpful, creative, clever, and very friendly."}
]

# GUI setup
root = tk.Tk()
root.title("Chatbot")
root.configure(bg='black')

# Apply font settings
font_family = "Comfortaa"
font_size = 20

chat_history = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD, bg='black', fg='lime', font=(font_family, font_size))
chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

user_input = tk.Text(root, height=3, bg='black', fg='lime', insertbackground='white', font=(font_family, font_size))
user_input.pack(padx=10, pady=(0, 10), fill=tk.X)

send_button = tk.Button(root, text="Send", command=send_message, bg='black', fg='white', font=(font_family, font_size))
send_button.pack(pady=(0, 10))

root.mainloop()