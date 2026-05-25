# Tony Di Fabbio — Personal & LINERFUN Project Website

Personal academic website and project communication hub for the **LINERFUN** MSCA Global Fellowship (Grant 101206371).

## Structure

```
website/
├── index.html        Homepage — LINERFUN spotlight + quick nav
├── project.html      LINERFUN project detail page
├── research.html     Publications & research areas
├── about.html        Biography, experience, education, awards
├── news.html         News/blog for CDEP activities
├── css/
│   └── style.css     All styles (no frameworks, no build tools)
├── js/
│   └── main.js       Minimal JS (active nav, mobile menu, footer year)
└── README.md         This file
```

## Deploy on GitHub Pages

1. Create a GitHub repo named `<your-username>.github.io` (or any name for a project page)
2. Push this folder's contents to the `main` branch:

```bash
cd website/
git init
git add .
git commit -m "Initial website"
git remote add origin https://github.com/<your-username>/<your-username>.github.io.git
git push -u origin main
```

3. Go to **Settings → Pages** in your GitHub repo and set Source to `main` branch, root `/`
4. Your site will be live at `https://<your-username>.github.io` within a few minutes

## Customisation

### Add your photo
Replace the placeholder emoji `👤` in `index.html` and `about.html` with an `<img>` tag:
```html
<img src="img/tony.jpg" alt="Tony Di Fabbio" class="hero-photo">
```
Drop your photo as `img/tony.jpg`.

### Add a profile photo to About page
Same pattern — replace the `<div class="about-photo">👤</div>` with:
```html
<img src="img/tony.jpg" alt="Tony Di Fabbio" class="about-photo" style="object-fit:cover;">
```

### Update DOI links
In `research.html`, each `<div class="pub-links">` is ready for DOI/PDF links — just add:
```html
<a href="https://doi.org/..." class="pub-link" target="_blank">DOI</a>
<a href="..." class="pub-link" target="_blank">PDF</a>
```

### Add news posts
In `news.html`, copy a `.news-post` block and fill in date, badge, title, and text.

### EU acknowledgment
The EU banner and footer acknowledgment texts are required by MSCA grant conditions.
Do not remove them.

## Technical Notes

- Pure HTML/CSS/JS — no build tools, no npm, no frameworks
- No external CSS frameworks (no Bootstrap, no Tailwind)
- No external fonts (uses system font stack)
- Fully mobile responsive
- GitHub Pages compatible out of the box (no Jekyll config needed — add `.nojekyll` file if needed)

## To add `.nojekyll` (prevents Jekyll processing)

```bash
touch .nojekyll
```

---

**Funded by the European Union — MSCA Grant Agreement No. 101206371**  
Views and opinions expressed are those of the author only and do not necessarily reflect those of the European Union or the REA.
