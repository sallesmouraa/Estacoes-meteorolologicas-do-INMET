# 🌦️ Estações Meteorológicas do INMET (BDMEP)

Metadados das estações meteorológicas brasileiras do INMET (BDMEP), com pipeline simples para **limpeza**, **validação** e **relatório de qualidade**.

---

## 📌 Visão geral

Este repositório contém o arquivo bruto `br_inmet_bdmep_estacao.csv` e scripts em Python para:

- normalizar dados
- derivar latitude/longitude
- validar regras de qualidade
- gerar relatório em Markdown

---

## 📁 Estrutura do projeto

| Caminho | Descrição |
|---|---|
| `br_inmet_bdmep_estacao.csv` | Base original (raw) |
| `scripts/clean_data.py` | Limpeza e enriquecimento (`latitude`, `longitude`) |
| `scripts/validate_data.py` | Regras de validação e geração de relatório |
| `reports/data_quality_report.md` | Relatório de qualidade gerado automaticamente |

---

## ⚙️ Requisitos

- Python **3.10+**
- Sem dependências externas (apenas biblioteca padrão)

---

## ▶️ Como executar

Na raiz do projeto:

```bash
python scripts/clean_data.py
python scripts/validate_data.py
```

---

## 🧹 Etapa 1 — Limpeza (`scripts/clean_data.py`)

A rotina de limpeza:

- lê `br_inmet_bdmep_estacao.csv`
- normaliza `altitude` vazia para `NA`
- extrai `latitude` e `longitude` de `geolocalizacao` no formato `POINT(x y)`
- gera `br_inmet_bdmep_estacao_clean.csv`

> ℹ️ **Observação:** neste projeto, o parser assume o primeiro valor de `POINT(...)` como `latitude` e o segundo como `longitude`, seguindo o padrão adotado na base utilizada.

---

## ✅ Etapa 2 — Validação (`scripts/validate_data.py`)

Valida no arquivo limpo:

- campos obrigatórios vazios (`id_municipio`, `id_estacao`, `estacao`, `data_fundacao`, `geolocalizacao`)
- `altitude == NA`
- datas inválidas (`YYYY-MM-DD`)
- geolocalizações inválidas (`POINT(...)` malformado)
- coordenadas fora de faixa (lat: `-90..90`, lon: `-180..180`)
- IDs de estação duplicados

Ao final, gera automaticamente `reports/data_quality_report.md`.

---

## 📤 Saídas geradas

- `br_inmet_bdmep_estacao_clean.csv`
- `reports/data_quality_report.md`

---

## 📄 Licença

Este projeto está sob a licença **GNU GPL v3**.
Consulte o arquivo [LICENSE](LICENSE).
