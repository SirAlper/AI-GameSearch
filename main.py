from langchain.messages import HumanMessage
from src.graph import graph_app

def main():
    print("🎮 Steam İndirim Avcısı Agent Başlatılıyor...")
    print("------------------------------------------------")

    while True:
        user_input = input("\n Soru sor (Cikis icin q): ")
        if user_input.lower() in ["q", "exit"]:
            print("Bay bay")
            break
        inital_state = {"messages": [HumanMessage(content=user_input)]}

        result = graph_app.invoke(inital_state)

        print("\n🤖 AI Cevabı:")
        print(result["messages"][-1].content)
        print("-" * 50)


if __name__ == "__main__":
    main()