import time
import os
from create_functions import *

def process_data_from_unified_files(data_directory):
    """
    Processa os dados de locais, coordenadas e imagens a partir de arquivos TXT unificados.
    """
    locais_file_path = os.path.join(data_directory, "locais.txt")
    coordenadas_file_path = os.path.join(data_directory, "coordenadas.txt")
    imagens_file_path = os.path.join(data_directory, "imagens.txt")

    if not os.path.exists(locais_file_path):
        print(f"Erro: Arquivo '{locais_file_path}' não encontrado. Certifique-se de que ele existe.")
        return

    # 1. Criar todos os locais e mapear nomes para IDs
    local_name_to_id = {}
    print("\n--- Criando Locais ---")
    with open(locais_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            local_nome = line.strip()
            if not local_nome:
                continue
            
            local_id = create_local(local_nome)
            if local_id:
                local_name_to_id[local_nome] = local_id
            time.sleep(0.1)

    # 2. Processar todas as coordenadas usando o mapeamento de IDs
    print("\n--- Processando Coordenadas ---")
    if os.path.exists(coordenadas_file_path):
        with open(coordenadas_file_path, 'r', encoding='utf-8') as cf:
            for coord_line in cf:
                parts = coord_line.strip().split(',')
                if len(parts) == 3:
                    local_nome = parts[0].strip()
                    lat_str = parts[1].strip()
                    lng_str = parts[2].strip()

                    if local_nome in local_name_to_id:
                        local_id = local_name_to_id[local_nome]
                        try:
                            lat = float(lat_str)
                            lng = float(lng_str)
                            create_coordenada(lat, lng, local_id)
                        except ValueError:
                            print(f"Aviso: Coordenada inválida para '{local_nome}': '{lat_str},{lng_str}'. Ignorando.")
                    else:
                        print(f"Aviso: Local '{local_nome}' não encontrado na lista de locais criados para a coordenada '{lat_str},{lng_str}'.")
                else:
                    print(f"Aviso: Formato de linha de coordenada inválido: '{coord_line.strip()}'. Esperado 'NomeLocal,lat,lng'.")
                time.sleep(0.05) # Pequeno atraso

    else:
        print(f"Aviso: Arquivo de coordenadas '{coordenadas_file_path}' não encontrado.")

    # 3. Processar todas as imagens usando o mapeamento de IDs
    print("\n--- Processando Imagens ---")
    if os.path.exists(imagens_file_path):
        with open(imagens_file_path, 'r', encoding='utf-8') as imf:
            for img_line in imf:
                parts = img_line.strip().split(',')
                if len(parts) == 2:
                    local_nome = parts[0].strip()
                    image_path = parts[1].strip()

                    if local_nome in local_name_to_id:
                        local_id = local_name_to_id[local_nome]
                        if image_path:
                            create_imagem(image_path, local_id)
                    else:
                        print(f"Aviso: Local '{local_nome}' não encontrado na lista de locais criados para a imagem '{image_path}'.")
                else:
                    print(f"Aviso: Formato de linha de imagem inválido: '{img_line.strip()}'. Esperado 'NomeLocal,caminho/da/imagem'.")
                time.sleep(0.05) # Pequeno atraso
    else:
        print(f"Aviso: Arquivo de imagens '{imagens_file_path}' não encontrado.")

if __name__ == "__main__":
    
    print(f"Iniciando o processamento de dados do diretório: {DATA_DIR}")
    process_data_from_unified_files(DATA_DIR)
    print("\nProcessamento concluído!")