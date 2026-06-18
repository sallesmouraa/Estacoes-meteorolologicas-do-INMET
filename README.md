# Estacoes-meteorolologicas-do-INMET

Metadados das estações meteorológicas do INMET (BDMEP).

Este repositório contém o arquivo `br_inmet_bdmep_estacao.csv` e scripts para **limpeza** e **validação** dos dados, gerando um relatório de qualidade.

## Estrutura do projeto

- `br_inmet_bdmep_estacao.csv` — base original (raw)
- `scripts/clean_data.py` — limpeza e enriquecimento (latitude/longitude)
- `scripts/validate_data.py` — validações de qualidade
- `reports/data_quality_report.md` — relatório gerado automaticamente

## Requisitos

- Python **3.10+**
- Sem dependências externas (apenas biblioteca padrão)

## Como executar

Na raiz do projeto:

```bash
python scripts/clean_data.py
python scripts/validate_data.py
```

## O que cada etapa faz

### 1) Limpeza (`scripts/clean_data.py`)

- Lê `br_inmet_bdmep_estacao.csv`
- Normaliza `altitude` vazia para `NA`
- Extrai `latitude` e `longitude` do campo `geolocalizacao` no formato `POINT(x y)`
- Gera `br_inmet_bdmep_estacao_clean.csv`

> Observação: neste projeto, o parser assume o primeiro valor de `POINT(...)` como `latitude` e o segundo como `longitude`, seguindo o padrão já presente na base utilizada.

### 2) Validação (`scripts/validate_data.py`)

Valida no arquivo limpo:

- Campos obrigatórios vazios (`id_municipio`, `id_estacao`, `estacao`, `data_fundacao`, `geolocalizacao`)
- `altitude == NA`
- Datas inválidas (formato `YYYY-MM-DD`)
- Geolocalizações inválidas (`POINT(...)` malformado)
- Coordenadas fora de faixa (lat: -90..90, lon: -180..180)
- IDs de estação duplicados

Ao final, gera `reports/data_quality_report.md`.

## Saídas geradas

- `br_inmet_bdmep_estacao_clean.csv`
- `reports/data_quality_report.md`

## Licença

Este projeto está sob a licença GNU GPL v3. Veja o arquivo [LICENSE](LICENSE).
