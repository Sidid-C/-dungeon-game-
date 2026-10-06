# Dungeon game: story files and a public web link

**Start with:** your audio + web dungeon demo from last time. The enclosed `web_text_adventure/` is a completed reference version. This directory itself will become the Git repository. Keep a copy of your earlier version so you can compare them.

**Goals:** let writing teammates revise descriptions in plain text, and publish a playable link that anyone with a browser can open. The game still has typed commands, four rooms, a wolf, a dragon, an axe, two treasures, and the four sound effects.

## 1. Trace the old design

Open your previous `main.py`. Find the descriptions supplied to `Room`, `Monster`, `Treasure`, and `Weapon` inside `TextAdventure.__init__`. What must happen when the writer wants to change the description of the hall? Which parts of a room, such as exits, are game logic rather than prose?

## 2. Move descriptions into files

1. Make `text/`. Create `entrance.txt`, `hall.txt`, `armory.txt`, `lair.txt`, `wolf.txt`, `dragon.txt`, `diamond.txt`, `chalice.txt`, and `axe.txt`. Copy the corresponding descriptions into them. Save as UTF-8 plain text. Keep these files inside the folder that pygbag packages.
2. At the top of `main.py`, alongside `ASSET_DIR`, add:

   ```python
   TEXT_DIR = BASE_DIR / "text"

   def story(filename):
       return (TEXT_DIR / filename).read_text(encoding="utf-8").strip()
   ```

3. Replace each description string with a call such as `Room("hall", story("hall.txt"))` or `Monster("wolf", 2, story("wolf.txt"))`. Keep names, armor, damage, values, room links, commands, and sounds in Python. `BASE_DIR` makes the path relative to `main.py`, even if you launch from a different directory.
4. `look()` already displays each object's `.description`; trace how the text from `wolf.txt` reaches the screen. The reference version also extends `wrap_text()` to preserve line breaks in a story file. Try two paragraphs and decide whether they display well in the last 20 visible lines.
5. Ask the writing teammate to change only `text/hall.txt`. Run the game locally, enter the hall, type `look`, and check the change. If a room file is missing or misspelled, the game will report `FileNotFoundError`; check spelling and capitalization.

**Discuss:** Which revisions can the writer make independently now? Which changes still require Python (for example, a new exit or different monster behavior)? Each description file is a fragment inserted into a sentence: room text follows “You are in …”; object text follows “There is … here.” Write accordingly. Agree on a naming convention and commit text changes alongside code changes.

## 3. Test in the browser locally

In a terminal **inside `web_text_adventure/`** (the folder containing `main.py`), run:

```bash
python -m pygbag .
```

Open the localhost address pygbag prints; click the game and type `look`, `go north`, and `attack wolf`. Play through the axe and dragon to the win. Verify the changed prose and move, pickup, danger, and win sounds. Browsers often require a click or key press before playing audio. 

The async loop and `await asyncio.sleep(0)` in `main.py` allow the browser to redraw while the program runs. All text and WAV files must remain inside this game directory to be included in the build.

## 4. Set up Git and GitHub (one time)

**Git** tracks changes on your computer; **GitHub** stores a copy online; **GitHub Pages** publishes the browser build. One teammate can own the repository for this exercise. Everyone can help edit and test; team members who push from their own computers will need GitHub accounts and repository access.

1. If you do not have a GitHub account, sign up at [github.com/signup](https://github.com/signup) and verify your email. Record your username. You can use the free plan.
2. Check whether Git is installed by running `git --version` in a terminal. If it is missing, install it from [git-scm.com/install](https://git-scm.com/install). On macOS, `xcode-select --install` supplies Git through Apple's Command Line Tools. On Windows, Git for Windows includes Git Bash; open Git Bash for the commands below. Restart your terminal and check `git --version` again.
3. Set your commit identity once on each computer. Use your own name and an email associated with your GitHub account (or your GitHub no-reply address if you prefer):

   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```

   These values label commits; they do not sign you in. GitHub may open a browser for sign-in on your first push. 

## 5. Make the first push

1. On GitHub, click **+ → New repository**. Name it `dungeon-game` (or choose another name), choose **Public**, and leave **Add a README**, `.gitignore`, and license unchecked, because the project already has its own files. Select **Create repository**. GitHub Free Pages needs a public repo. Use only text and sound your team can publish.
2. In a terminal, **change into the `web_text_adventure` folder containing `main.py`**. Confirm the location before creating the repository:

   ```bash
   pwd
   ls -a
   ```

   You should see `main.py`, `assets`, `text`, `.gitignore`, and `.github` together. On Windows Git Bash, `pwd` and `ls -a` also work. GitHub will recognize the workflow only if `.github/workflows/pages.yml` is at the top of this repository. Do not initialize Git in the folder *containing* `web_text_adventure`.
3. From inside `web_text_adventure`, enter the following, replacing `YOUR-USERNAME` with your GitHub username:

   ```bash
   git init
   git branch -M main
   git status
   git add .
   git commit -m "Add dungeon game with story files"
   git remote add origin https://github.com/YOUR-USERNAME/dungeon-game.git
   git push -u origin main
   ```

   `git add .` selects files; `git commit` saves a local snapshot; `git push` sends it to GitHub. The `-u` in the first push sets the destination so later pushes can simply say `git push`. If you chose another repository name, adjust the URL. If `git remote add origin` says it already exists, run `git remote -v` and ask for help rather than adding another remote.
4. Refresh your GitHub repository's **Code** tab. Verify that `main.py` and `.github/workflows/pages.yml` appear directly at the repository root. `build/`, `.venv/`, and generated archives should not appear. If Git reports that there is nothing to commit, use `git status` to check whether you are in an already initialized repository.

## 6. Publish and update the site

1. On GitHub, choose **Settings → Pages → Build and deployment → Source → GitHub Actions**. Open **Actions**, select **Build and publish dungeon game** in the left sidebar, and inspect its newest run. If Pages was enabled after your initial push, click **Run workflow**. The supplied workflow builds from `main.py` at the repository root and publishes `build/web`. It runs on each push to `main`.
2. When the run succeeds, choose **Settings → Pages → Visit site**. The address should resemble `https://YOUR-USERNAME.github.io/dungeon-game/`. Open it in a separate browser tab and test `look`, navigation, combat, treasure, and audio. Ask a writing or music teammate to test it too.
3. Make a real revision in `text/hall.txt` and save it. From the same `web_text_adventure` directory run:

   ```bash
   git status
   git add text/hall.txt
   git commit -m "Revise hall description"
   git push
   ```

   Refresh **Actions**; a new build should start. When it succeeds, reload the public game (hard refresh if needed), enter the hall, and type `look`. Check that the revised sentence appears. For later work, follow the same **edit → save → `git status` → `git add` → `git commit` → `git push`** cycle. The live site changes only after the push and successful build, not when a local file is saved or committed.

**Troubleshooting:** If the workflow is absent from Actions, check that `.github/workflows/pages.yml` is on GitHub at the **repository root** on `main`, not inside another `web_text_adventure/` folder. Open a failed Actions run to read its log. Check exact filename capitalization, whether `text/` and `assets/` were committed, and whether `build/web/index.html` was produced. A 404 can mean Pages is not configured or the deployment has not finished. For a blank canvas, inspect the browser console and compare with the local pygbag run. Audio may require clicking the page first.

**Extension:** Add a new room text file and corresponding `Room` and neighbor links in Python. Explain why the prose can be separate while the new map connection still requires code.
