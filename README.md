# Tony Di Fabbio — Personal & LINERFUN Project Website

Personal academic website and dissemination hub for the **LINERFUN** MSCA Global Fellowship (Grant 101206371).

**Live site:** https://difabbiot.github.io/

## Structure

```
website/
├── index.html        Landing — LINERFUN splash + quick nav
├── project.html      LINERFUN project detail (status bar, objectives, partners)
├── about.html        Biography, experience, education, skills, CV
├── research.html     Expertise, publications, awards & funding
├── blog.html         Blog / news feed (CDEP dissemination)
├── news.html         Legacy URL — instant redirect to blog.html
├── 404.html          Custom GitHub Pages error page
├── sitemap.xml       Search-engine sitemap (update <lastmod> when pages change)
├── robots.txt        Crawler rules + sitemap pointer
├── css/style.css     All styles (no frameworks, no build tools)
├── js/main.js        Active nav link, mobile menu, footer year
└── img/              Site logo, institution logos, photo
```

## Development

No build step. Open the HTML files directly, or run `python3 -m http.server` from the project root and visit http://localhost:8000.

## Deployment

GitHub Pages from the `main` branch, root `/`. Push to `main` and the site updates within a minute or two. The `.nojekyll` file disables Jekyll processing — keep it.

## SEO

- Every page carries a canonical URL, Open Graph/Twitter tags and JSON-LD structured data (`Person` on the landing page, `ProfilePage` on the bio, `ResearchProject` on the project page).
- `sitemap.xml` and `robots.txt` are in place — update the `<lastmod>` dates when a page changes, and re-submit the sitemap in Google Search Console after significant changes.
- For the site to rank for "Tony Di Fabbio", keep the site linked from ORCID, Google Scholar, LinkedIn, ResearchGate and the GitHub profile.

## Logo policy

Only two institutional logos may be displayed: **MSCA / EU** (`img/logoMSCA.png`) and **DIMEAS — Politecnico di Torino** (`img/logoDIMEAS.jpg`). There is **no permission** to use the University of Melbourne or ONERA logos — those partners appear as text wordmarks (`.inst-wordmark`) on the landing page. Do not re-add their image logos.

## EU acknowledgment

The EU banner at the top of every page and the EU/MSCA attribution in every footer are required by the MSCA grant conditions. Do not remove them.

---

**Funded by the European Union — MSCA Grant Agreement No. 101206371**
Views and opinions expressed are those of the author only and do not necessarily reflect those of the European Union or the REA.
