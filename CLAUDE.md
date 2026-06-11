# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Personal academic website and EU MSCA dissemination hub for the LINERFUN project (Grant 101206371). Pure static site — no build tools, no npm, no frameworks, no external CSS libraries. Live at https://difabbiot.github.io/.

## Development

Open any HTML file directly in a browser — there is no build step or dev server. For live reload, use `python3 -m http.server` from the project root, then visit `http://localhost:8000`.

Deployment is via GitHub Pages (`main` branch, root `/`). The `.nojekyll` file prevents Jekyll processing — do not remove it.

## Architecture

**Landing page vs inner pages:** `index.html` uses `.landing-body` / `.landing-main` / `.splash` layout classes and a minimal footer. Every other page (`about.html`, `project.html`, `research.html`, `blog.html`) follows the inner-page pattern: sticky `<nav>` with `.nav-inner`, a `.page-hero` block, then `<div class="col">` sections.

**CSS** (`css/style.css`): single file, no preprocessor. All design tokens are CSS custom properties in `:root` (`--navy`, `--blue`, `--col: 660px`, etc.). Content width is 660 px. Page-specific overrides are written in `<style>` blocks inside the `<head>` of the relevant HTML file.

**JS** (`js/main.js`): three responsibilities — mark the current page's nav link `.active`, handle mobile nav toggle (`#nav-toggle` / `#nav-links`), and write the current year into `#footer-year`.

## Content patterns

| Element | Class |
|---|---|
| Timeline row | `.tl-item` (two-col grid: date + body) |
| Publication entry | `.pub` → `.pub-title`, `.pub-authors`, `.pub-venue`, `.pub-links` |
| Blog/news post | `.post` (add `.pinned` for highlighted) |
| Post badge | `.post-tag` + `.tag-msca` / `.tag-paper` / `.tag-news` / `.tag-talk` |
| Skills chips | `.chips` > `.chip` |
| Awards list | `.award-list` > `li` with `.award-amount` span |
| DOI/PDF button | `<a class="pub-link">` inside `.pub-links` |

## SEO conventions

Every page `<head>` carries: name-first `<title>`, meta description, canonical URL (`https://difabbiot.github.io/...`), Open Graph/Twitter tags (og:image = `img/tony.jpg` absolute URL), favicon, and theme-color. JSON-LD lives on three pages: `Person`+`WebSite` (index), `ProfilePage` (about), `ResearchProject` (project). When adding or significantly changing a page, update `sitemap.xml` `<lastmod>` dates. `news.html` is a legacy redirect to `blog.html` — do not link to it or add content there.

## Logo policy

Only two institutional logos may be displayed: **MSCA** (`img/logoMSCA.png`) and **DIMEAS — Politecnico di Torino** (`img/logoDIMEAS.jpg`). There is **no permission** for University of Melbourne or ONERA logos — those partners are named as plain text links (`.inst-partners`, under the logo row on the landing page). Never re-add their image logos.

## EU acknowledgment requirement

The `.eu-banner` at the top of every page and the EU/MSCA attribution in every footer are **legally required** by the MSCA grant conditions. Do not remove or substantially alter them.
