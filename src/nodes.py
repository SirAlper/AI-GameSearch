from langchain.messages import SystemMessage, ToolMessage
from src.state import AgentState
from src.model import model_with_tools
from src.tools import TOOLS_BY_NAME

SYSTEM_PROMPT = """
Sen uzman bir oyun öneri ajanısı amacın içeriğindeki toolları kullanarak kullanıcılara oyun önerilerinde bulunmak.
Tabi bu oyunlar öyle herkesin bildiği AAA oyunlar olmamalı (Witcher 3, RDR2, GTA5, Assasin's Creed düzeyinde oyunlar 
olmamalı)

Eğer kullanıcı indirimde olan oyunları merak ettiyse gerekli ajanı kullanarak steamde indirimde olan oyunları sırala ve bunları
aynı formatta öner

Öncelikle kullanıcı sana bana oyun öner gibi bir istemde bulunduğu zaman tavily üzerinden web search yapacak ve "Best indie game 2025" 
gibi aramalar gerçekleştireceksin aramalar yaparken bunu referans kullanıp kendi arama kriterlerini oluştur
eger tür belirtmişse aramanı o türe göre özelleştireceksin. Ardından tavily kullanarak sadece oyun isimleri bul bu oyunların steamden fiyatına bakacaksın sonrasında da steamden toollar yardımıyla
yorumlarına bakacaksın her oyun için bunu gerçekleştir ve maksimum 5 oyun bul.Sonra tüm bilgileri bir araya topla düşün iyi oy almış oyunları önermeni istiyorum önerirken oyunun açıklamasını ve neden önerdiğini de
eklersen çok iyi olur.

Ardindan cevap olarak oyunun adini aciklamasini fiyatini ve puanini ekle oyle cevap ver cevaplar mumkunse
maddeler halinde duzgun yazilmis bicimde olsun ve tek oyunla sinirla kalma bir kac oyun oner ve aldigin sayisal verileri kullan
yani olumlu oy almıs kac tane almıs onları yaz

Sonra bulduklarını kullanıcıyla paylaş ve ardından yeni istek geldiğinde bu dongüyü sürekli tekrarla konuşma boyunca bu ilkeyi uygula ve konuşmada daha önce cevabında kullandığın bir oyunu
2. kere kullanma bu sana yasak örneğin kullanıcı senden oyun istedi sen listende peake yer verdin başka oyunlar önerdi araştırdın
peake denk geldin geri dönüp konuşmaya bak ben bu oyunu önerdim mi önerdiysen başka oyunlar ara
"""

def llm_node(state: AgentState):
    """Yapay Zeka'nın düşündüğü ve karar verdiği düğüm"""

    recent_messages = state["messages"]

    messages = [SystemMessage(content=SYSTEM_PROMPT)] + recent_messages
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

def tool_node(state: AgentState):
    """Araçların çalıştırıldığı düğüm"""
    result = []
    last_message = state["messages"][-1]

    if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
        return {"messages": []}

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool = TOOLS_BY_NAME.get(tool_name)

        if tool:
            print("Tool suan calisiyor")
            try:
                observation = tool.invoke(tool_call["args"])
                print(f"📄 TOOL CEVABI (İlk 300 karakter): {str(observation)[:300]}...")
                print("-" * 50)

                content = str(observation)[:2000]

                result.append(ToolMessage(
                content=content,
                tool_call_id = tool_call["id"],
                name=tool_name
                ))
            except Exception as e:
                result.append(ToolMessage(
                    content=f"Hata {str(e)}",
                    tool_call_id=tool_call["id"],
                    name=tool_name
                ))
    print(result)
    return {"messages": result}