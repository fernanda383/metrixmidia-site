# Metrix Mídia Site

Site estático da Metrix Mídia com hub de cases e primeiro case (Academia de Tênis de Mesa).

## Como rodar local
```bash
npm install -g serve   # se não tiver
serve .
```
Abra http://localhost:3000 (ou porta indicada).

## Estrutura
- `index.html` – home.
- `case/` – hub `/case` e página detalhada `/case/academia-de-tenis-de-mesa`.
- `data/cases.json` – dados dos cards.
- `static/cases/academia-tenis-de-mesa/` – assets do case (substitua os placeholders).
- `docs/case-academia-tenis.pdf` – PDF de 10 lâminas do case.

## Deploy
Repo preparado para Vercel (estático). Basta conectar o projeto e publicar a branch `main`.
