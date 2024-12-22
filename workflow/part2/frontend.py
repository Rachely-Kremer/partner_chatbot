from partner_chatbot.workflow.part2.backend import stream_graph_update

if __name__=='__main__':
    while True:
        user_input= input("User:")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_update(user_input)