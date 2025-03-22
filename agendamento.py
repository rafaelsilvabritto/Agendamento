import requests

API_URL = "https://api.cal.com/v2"
API_VERSION = "2024-08-13"
TOKEN = "SEU_TOKEN"
EVENT_TYPE_ID = "ID_DO_EVENTO"

HEADERS = {
    "cal-api-version": API_VERSION,
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

def buscar_horarios(data_inicial, data_final):
    url = f"{API_URL}/schedules/get-all-schedules"
    
    params = {
        "eventTypeId": EVENT_TYPE_ID,
        "startDate": data_inicial,
        "endDate": data_final
    }
    
    resposta = requests.get(url, headers=HEADERS, params=params)
    
    if resposta.status_code == 200:
        data = resposta.json()
        return data.get("data", [])
    else:
        print("Erro ao buscar horários disponíveis:", resposta.json())
        return None

def agendamento(data_inicial, data_final, cliente_email, cliente_nome):
    url = f"{API_URL}/bookings"
    
    dados = {
        "eventTypeId": EVENT_TYPE_ID,
        "start": data_inicial,
        "end": data_final,
        "attendeeEmail": cliente_email,
        "attendeeName": cliente_nome,
    }
    
    resposta = requests.post(url, headers=HEADERS, json=dados) 
    
    if resposta.status_code != 200 and resposta.status_code != 201:
        print("Erro ao agendar:", resposta.json())
        return None
    return resposta.json()

data_inicial = input("Digite a data inicial: ")
data_final = input("Digite a data final: ")

horarios_disponiveis = buscar_horarios(data_inicial, data_final)

if horarios_disponiveis:
    print("\nHorários disponíveis:")
    for i, slot in enumerate(horarios_disponiveis):
        print(f"{i + 1}. Início: {slot['start']}, Fim: {slot['end']}")

    while True:
        try:
            escolha = int(input("\nEscolha um horário pelo número: ")) - 1
            if 0 <= escolha < len(horarios_disponiveis):
                op_selecionada = horarios_disponiveis[escolha]
                data_inicial = op_selecionada["start"]
                data_final = op_selecionada["end"]
                break
            else:
                print("Número inválido! Escolha um número da lista.")
        except ValueError:
            print("Entrada inválida! Digite um número.")

    cliente_email = input("Digite seu e-mail: ")
    cliente_nome = input("Digite seu nome: ")

    reserva = agendamento(data_inicial, data_final, cliente_email, cliente_nome)

    if reserva:
        print("Agendamento confirmado:", reserva)
else:
    print("Nenhum horário disponível encontrado.")