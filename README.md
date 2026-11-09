<div align="center">
  <img src="icon.svg" alt="Jarvis Logo" width="112" height="112">

  <h1>Jarvis</h1>

  <p><b>Dein persönlicher KI-Assistent im Browser.</b><br>
  Eine leuchtende Kugel, die zuhört, nachdenkt und antwortet – per Text oder Stimme.</p>

  <p>
    <a href="https://jannickspielt.github.io/jarvis/"><b>▶&nbsp; Jarvis öffnen</b></a>
  </p>

  <img src="screenshot.jpg" alt="Jarvis: orange Kugel mit Antwortzeile und Eingabefeld" width="800">
</div>

## Was Jarvis kann

- 💬 **Chatten** – Antworten erscheinen live, während das Modell schreibt
- 🎙️ **Sprechen** – Klick auf die Kugel und frag einfach los, auf Deutsch
- 🔊 **Antworten vorlesen** – Satz für Satz, mit einer deutschen Stimme deiner Wahl
- 👋 **„Hey Jarvis“** – Auf Wunsch hört Jarvis zu und reagiert auf sein Weckwort
- 🕘 **Verlauf** – Gespräche bleiben gespeichert und lassen sich wieder öffnen
- 🧠 **Viele Anbieter** – OpenRouter, Requesty, Vercel AI Gateway, Eden AI, Hugging Face, OpenAI, Anthropic, Gemini, Groq, Mistral, DeepSeek und xAI, jeweils mit eigenem Key
- 💻 **Lokal & privat** – Am Computer mit Ollama, LM Studio, Jan, llama.cpp, vLLM oder LocalAI – Jarvis erkennt sie von selbst

Die Kugel zeigt dabei, was gerade passiert: Sie atmet ruhig, reagiert beim Zuhören auf deine Lautstärke, wirbelt beim Nachdenken und pulsiert beim Antworten.

## Loslegen

1. **[Jarvis öffnen](https://jannickspielt.github.io/jarvis/)**
2. Oben rechts auf den Modellnamen tippen und deinen [OpenRouter-Key](https://openrouter.ai/keys) eintragen
3. Lostippen oder auf die Kugel tippen und sprechen

**Als App installieren**
- **iPhone / iPad:** in Safari *Teilen › Zum Home-Bildschirm*
- **Mac:** in Safari *Ablage › Zum Dock hinzufügen*
- **Chrome:** *⋮ › Streamen, speichern und teilen › Seite als App installieren*

## Desktop-App (Mac & Windows)

**[Download: neueste Version](https://github.com/JannickSpielt/jarvis/releases/latest)** – `.dmg` für den Mac, `-setup.exe` für Windows.

Die App lädt beim Start immer die aktuelle Jarvis-Version und erreicht Ollama direkt, ohne Hintergrund-Dienst.

- **Mac:** Die App ist nicht von Apple signiert. Wenn macOS „beschädigt“ oder „kann nicht geöffnet werden“ meldet, einmal im Terminal ausführen:
  `xattr -dr com.apple.quarantine /Applications/Jarvis.app`
- **Windows:** Bei der SmartScreen-Warnung *Weitere Informationen › Trotzdem ausführen*. Die Spracheingabe funktioniert in der Windows-App möglicherweise nicht; Vorlesen und Chat schon.

## Am Mac mit Ollama (ohne App)

Safari lässt die Online-Version nicht auf [Ollama](https://ollama.com) zugreifen. Dafür gibt es die Mac-Version: ein winziger Hintergrund-Dienst, der Jarvis unter `http://localhost:4180` bereitstellt – immer aktuell von GitHub, offline mit der zuletzt geladenen Kopie.

**Einrichten** (einmal im Terminal):

```bash
curl -fsSL https://jannickspielt.github.io/jarvis/mac/install.sh | bash
```

Danach öffnet sich Jarvis in Safari. Über *Ablage › Zum Dock hinzufügen* wird daraus die Mac-App, in den Einstellungen *Ollama (lokal)* wählen. Auf Handy und Tablet steht nur OpenRouter zur Wahl, weil Ollama dort nicht läuft.

**Entfernen:**

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.jannick.jarvis-local.plist
rm -rf ~/Library/LaunchAgents/com.jannick.jarvis-local.plist "$HOME/Library/Application Support/Jarvis"
```

## Datenschutz

- Dein OpenRouter-Key bleibt in deinem Browser und geht nur direkt an OpenRouter, nie an diese Seite.
- Gespräche und Einstellungen liegen ebenfalls nur lokal im Browser.
- Spracheingabe nutzt die Spracherkennung des Browsers (Safari: Apple, Chrome: Google). Vorlesen läuft mit den Stimmen deines Geräts.

## Technik

Eine einzige Datei, [`index.html`](index.html): HTML, CSS und JavaScript ohne Abhängigkeiten oder Build-Schritt. Die Kugel wird live auf einem Canvas gezeichnet, Sprache läuft über die Web Speech API.
