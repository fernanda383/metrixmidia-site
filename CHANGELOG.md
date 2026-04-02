# Changelog — metrixmidia.com.br

Registro de todas as alterações no site da Metrix Mídia. Atualizar a cada sessão de trabalho.

---

## [2026-03-30] — UX/Usabilidade global: nav mobile, acessibilidade, correções estruturais

### Acessibilidade (todo o site — 28 páginas)
- Skip link "Ir para o conteúdo" adicionado em todas as páginas
- `aria-label="Navegação principal"` adicionado em todos os `<nav>`
- `aria-current="page"` no link ativo por página
- `aria-label`, `aria-expanded`, `aria-controls` no botão hamburger

### Nav mobile (todo o site — 28 páginas)
- Hamburger button adicionado em todas as páginas (visível apenas em mobile)
- Overlay de navegação mobile com foco gerenciado (focus trap, Escape para fechar, body scroll locked)
- 3 artigos antigos (`instagram-reels`, `linkedin`, `prompt-library`) completamente sem navbar — navbar + footer adicionados

### Homepage (`index.html`)
- Logo href corrigido: `#` → `/`
- Footer: links Cases e Blog adicionados (antes só tinha Instagram + Privacidade)
- Planos: botões "Selecionar X" agora abrem WhatsApp com contexto pré-preenchido (antes eram `href="#"` mortos)
- Seção "Só trabalhamos com quem está disposto a:" removida a pedido
- `id="navbar"` adicionado ao `<nav>` (necessário para scroll effect do main.js)
- URL absoluta `metrixmidia.com.br/case/` → `/case/`

### Cases hub (`case/index.html`)
- CTA "E o seu próximo case?" → "Quer ser o próximo case?"
- `id="navbar"` adicionado
- `id="main-content"` adicionado ao `<main>`

### Blog hub (`blog/index.html`)
- `id="navbar"` adicionado
- `id="main-content"` adicionado ao `<main>`

### Case detail pages — labtem, academia, victor-azevedo
- Hero full-width restaurado: `.case-header` removida do seletor `max-width: 800px` (bug herdado do template)
- h3 → h2 nas seções do `<main>` (hierarquia semântica: h1 no header, h2 nas seções)
- Import duplicado de Inter removido
- Caption `color: #666` → `#999` (reprovava WCAG 4.5:1)
- URL absoluta Cases corrigida

### Case `editora-recriar` (corrigido em sessão anterior, deploy hoje)
- Mesmas correções aplicadas: hero, captions, headings, ARIA, hamburger, skip link

### Blog articles (21 arquivos com template padrão)
- Import duplicado de Inter removido
- `.case-header` removida do seletor `max-width: 800px`
- Caption e breadcrumb `#666` → `#999`
- URL absoluta Cases → `/case/`
- `aria-label` no nav, hamburger adicionado

---

## [2026-03-29] — Blog UX fixes + novos artigos e cases março 2026

### Novos arquivos
- `blog/case-editora-recriar-roas-5x-meta-google-ads-update/index.html` — Artigo update Recriar: ROAS 3.89x → 5.95x Meta, 9.15x Google Desktop. 6 otimizações documentadas. JSON-LD Article + BreadcrumbList + FAQPage.
- `blog/case-labtem-roas-4x-meta-ads-cursos/index.html` — Primeiro artigo dedicado Labtem: ROAS 2.16x → 4.05x, 5 ad sets por curso, budget flex. JSON-LD completo.
- `blog/case-academia-tenis-de-mesa-matriculas-meta-ads-pindamonhangaba/index.html` — Artigo Academia: R$4,85 custo/conversa (7d), 128 conversas, CTR 2,12%, 5 matrículas. JSON-LD completo.

### Cases atualizados
- `case/editora-recriar/index.html` — Badges e métricas atualizados para março 2026 (5.95x · 9.15x · 4.50x). Seção "Update março 2026" adicionada com link para artigo do blog.
- `case/labtem/index.html` — Badges e métricas atualizados para março 2026 (4.05x · +87% · 85% acima mediana). Seção "Update março 2026" adicionada.
- `case/academia-de-tenis-de-mesa/index.html` — Badges e métricas atualizados (R$4,85 · 128 conversas · 5 matrículas). Seção "Update março 2026" adicionada.

### Dados
- `data/cases.json` — Resultados dos 3 cases atualizados para março 2026. Thumbnails da Recriar e Labtem apontando para novos screenshots `.png`.

### Blog index
- `blog/index.html` — 3 cards novos adicionados no topo (Recriar update em destaque full-width, Academia, Labtem). Card duplicado do artigo original Recriar (3.89x) removido do final.
- `blog/case-editora-recriar-roas-meta-ads/index.html` — Nota editorial de atualização adicionada ao final + link para o artigo update.

### Navbar
- `blog/como-escolher-agencia-trafego-pago/index.html` — Navbar antiga substituída pelo padrão Apple-style.
- `blog/como-melhorar-roas-meta-ads/index.html` — Navbar atualizada.
- `blog/gestao-redes-sociais-pequenos-negocios/index.html` — Navbar atualizada.
- `blog/o-que-e-narrativa-autentica-marketing/index.html` — Navbar atualizada.

### Correções UX/UI
- `blog/blog.css`
  - `.blog-inline-cta` restruturado: `display: inline-flex` → `display: block`. Adicionado `.blog-inline-cta p { color: rgba(255,255,255,0.85) }` para corrigir texto amarelo ilegível em parágrafos. Seletor `.blog-inline-cta a` alterado para `:not([class])` para não sobrepor cor de botões `.btn-whatsapp` / `.btn-primary`.
  - `.blog-stats-block` adicionado: grid 4 colunas (2 colunas em mobile ≤640px). Classe estava em uso nos artigos mas ausente no CSS.
- `index.html` — Typo `point-events-none` → `pointer-events-none` (2 ocorrências).
- `blog/index.html` — Typo `point-events-none` → `pointer-events-none`.
- `case/index.html` — Typo `point-events-none` → `pointer-events-none`.
- `politica-de-privacidade.html` — Typo `point-events-none` → `pointer-events-none`.

### Assets adicionados
- `static/cases/editora-recriar/roas-7dias-mar2026.png` — Dashboard ROAS 5.95x (7 dias, mar/26)
- `static/cases/editora-recriar/dashboard-mar2026.png` — Dashboard ROAS 4.26x (mês completo mar/26)
- `static/cases/labtem/roas-7dias-mar2026.png` — Dashboard ROAS 4.05x (7 dias, mar/26)
- `static/cases/labtem/dashboard-mar2026.png` — Dashboard ROAS 3.70x (mês completo mar/26)
- `static/cases/academia-tenis-de-mesa/roas-7dias-mar2026.png` — Dashboard R$4,85/conversa (7 dias, mar/26)
- `static/cases/academia-tenis-de-mesa/dashboard-mar2026.png` — Dashboard R$9,26 (mês completo mar/26)

---

## [2026-03-09] — Implementação inicial do blog GEO

### Novos arquivos
- `blog/blog.css` — Todas as classes `.blog-*` prefixadas
- `blog/index.html` — Index do blog com cards hardcoded (sem fetch — requisito GEO)
- `blog/meta-ads-mais-caro-2026-como-proteger-roas/index.html`
- `blog/o-que-e-trafego-pago/index.html`
- `blog/como-melhorar-roas-meta-ads/index.html`
- `blog/como-escolher-agencia-trafego-pago/index.html`
- `blog/gestao-redes-sociais-pequenos-negocios/index.html`
- `blog/o-que-e-narrativa-autentica-marketing/index.html`
- `blog/case-editora-recriar-roas-meta-ads/index.html`
- `sitemap.xml` — Todas as URLs do site
- `robots.txt` — Com referência ao sitemap

### Arquivos atualizados
- `index.html` — Cases e Blog adicionados à nav. Seção teaser do blog (3 artigos). Schema JSON-LD Organization.
