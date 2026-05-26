import os
from pysus.online_data import SINAN
import pandas as pd
from google.cloud import storage

def run_oda_pipeline():
    # 1. Configurações
    BUCKET_NAME = "dados_alagoinhas_bronze"
    DESTINATION_FOLDER = "saude/violencia"
    COD_ALAGOINHAS = "290070"
    
    print("Conectando ao SINAN...")
    sinan = SINAN.SINAN().load()
    
    # Instanciamos o client do Storage apenas uma vez
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    
    # 2. Busca Histórica (2000 até 2030)
    for ano in range(2000, 2031):
        print(f"\n--- Processando ano: {ano} ---")
        
        try:
            # O código para Violência Interpessoal/Autoprovocada geralmente é VIOL
            arquivos = sinan.get_files(dis_code="VIOL", year=ano)
        except Exception as e:
            print(f"Erro ao acessar dados de {ano} no servidor: {e}")
            continue
        
        if not arquivos:
            print(f"Nenhum arquivo de {ano} encontrado no servidor.")
            continue

        # 3. Download e Filtro
        # O SINAN pode retornar mais de um arquivo por ano (ex: dados preliminares e consolidados)
        for arquivo in arquivos:
            print(f"Baixando {arquivo.name}...")
            arquivo_baixado = arquivo.download()
            df = arquivo_baixado.to_dataframe()
            
            # Garante que a coluna existe antes de filtrar
            if 'ID_MN_RESI' not in df.columns:
                print(f"Atenção: Coluna 'ID_MN_RESI' não encontrada em {arquivo.name}. Pulando arquivo.")
                continue

            df_alagoinhas = df[df['ID_MN_RESI'] == COD_ALAGOINHAS]
            
            if df_alagoinhas.empty:
                print(f"Nenhum dado de Alagoinhas encontrado no arquivo {arquivo.name}.")
                continue

            # 4. Preparação do arquivo para o Storage
            # Usamos o ano e o nome original do arquivo para garantir unicidade no Data Lake
            nome_base = arquivo.name.split('.')[0]
            local_filename = f"violencia_alagoinhas_{ano}_{nome_base}.csv"
            
            df_alagoinhas.to_csv(local_filename, index=False, sep=';', encoding='utf-8')
            
            # 5. Upload para o Cloud Storage
            print(f"Subindo {local_filename} para o bucket {BUCKET_NAME}...")
            blob = bucket.blob(f"{DESTINATION_FOLDER}/{local_filename}")
            blob.upload_from_filename(local_filename)
            
            # Limpa o arquivo local para não encher o disco de quem está rodando (Cloud Run/Compute)
            os.remove(local_filename)
            print(f"Sucesso! Arquivo disponível em {DESTINATION_FOLDER}/{local_filename}")

if __name__ == "__main__":
    run_oda_pipeline()