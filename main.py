import os

from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, StorageContext, load_index_from_storage

from Chatbot import Chatbot


def get_index(load_from_memory):
    global index
    if load_from_memory:
        storage_context = StorageContext.from_defaults(persist_dir='/home/kornel/PycharmProjects/chatbot/data/index')
        # load index
        index = load_index_from_storage(storage_context)
    else:
        index = GPTVectorStoreIndex.from_documents(documents)
        index.storage_context.persist('/home/kornel/PycharmProjects/chatbot/data/index')

    return index


if __name__ == '__main__':
    os.environ["OPENAI_API_KEY"] = 'XXX'
    documents = SimpleDirectoryReader('/home/kornel/PycharmProjects/chatbot/data/').load_data()
    print(documents)

    index = get_index(load_from_memory=True)
    bot = Chatbot("Add your API Key here ", index=index)
    bot.load_chat_history("chat_history.json")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["bye", "goodbye"]:
            print("Bot: Goodbye!")
            bot.save_chat_history("chat_history.json")
            break
        response = bot.generate_response(user_input)
        print(f"Bot: {response['content']}")
