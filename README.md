

<p align="center">
  <img src=".github/image.png" alt="Cook CLI Banner" width="100%" style="border-radius:12px"">
</p>

<h1 align="center">Cook – The All-in-One CLI for Lazy Devs</h1>

<p align="center">
  <b>Like npm, but for everything – without the npm and better.</b><br>
  Automate your dev workflow, organize your codebase, and streamline commands – all from one CLI.
</p>

<p align="center">
  <a href="https://github.com/thealphaones/cook/releases"><img src="https://img.shields.io/github/v/release/thenormvg/cook?style=flat-square" /></a>
  <a href="https://github.com/thealphaones/cook/blob/main/LICENSE"><img src="https://img.shields.io/github/license/thenormvg/cook?style=flat-square" /></a>
  <a href="https://yourpublicplatform.com"><img src="https://img.shields.io/badge/Templates%20Hub-online-blue?style=flat-square" /></a>
</p>

<!-- ---

## 🚀 Install

```bash
curl -fsSL https://raw.githubusercontent.com/thenormvg/cook/main/install.sh | bash
````

This will install the `cook` binary globally.
You can also manually clone and build it if needed. -->

---

## 🎯 Features in v1

* **📦 Code Templates with Online Sync**
  Create and reuse full project templates. Sync them via our public hub.

* **⚙️ Global & Local Custom Commands**
  Automate your routine commands per project or system-wide.

* **📜 License Generator**
  Generate open-source licenses for your projects instantly.

* **📊 Lines of Code Counter**
  Analyze your project code stats, respecting `.gitignore`.

* **🌲 Directory Tree Viewer**
  Visually explore your folder structure in the terminal.

* **🔁 Hot Reload & Cleanup**
  Instantly apply config changes and clean unused files.

---

## 🧠 CLI Command Tree

```bash
cook
├── auth                # Authentication
│   ├── log-in           # Log in to your account
│   ├── log-out          # Log out
│   └── now             # Show current session
├── mold                # Template (Mold) management
│   ├── add             # Add a new template
│   ├── list            # List templates
│   ├── use             # Use a template
│   ├── show            # Show template details
│   └── update          # Update a template
├── cmd                 # Custom command management
│   ├── add_global      # Add global command
│   ├── add_local       # Add project command
│   ├── list            # List all commands
│   └── remove          # Remove a command
├── licence             # License handling
│   ├── gen             # Generate license
│   ├── list            # List available licenses
│   └── show            # View license text
├── loc                 # Show LOC stats
├── tree                # Render folder structure
├── version             # Show CLI version
└── .                   # Ping/default action
```

---

## 🧾 Example: `cook.config.json`

Here’s a sample project config using Cook:

```json
{
  "name": "nuxt-awesome-app",
  "author": "thenormvg",
  "cmd": {
    "serve":  ["pnpm i", "npm run dev"], 
    "build": ["pnpm run build"]
  },
  "template": {
    "name": "nuxt-fullstack-template",
    "category": "nuxt",
    "version": "1.0.0",
    "stack": [
      "nuxt",
      "vue 3",
      "typescript",
      "pinia",
      "drizzle ORM",
      "postgresql",
      "tailwindcss",
      "framer motion"
    ],
    "github": "https://github.com/thenormvg/nuxt-fullstack-template",
    "readme": "README.md"
  }
}
```

---

## 🧭 Architecture

```
Cook CLI Ecosystem
├── 🧠 Core CLI Tool
│   └── Handles all local automation, commands, and templates
├── ☁️ Public Platform (hub)
│   └── Online template/snippet repo
└── 🔌 MCP Server (Soon..)
    └── Discoverable services, shared workflows, and plugins
```

---

## 💡 Who Is It For?

* Developers juggling multiple side-projects
* Teams standardizing workflows and setups
* OSS contributors creating repeatable project layouts
* Builders who just want things done fast ⚡

---

## 🌍 Join the Early Access

We're actively building **Cook v1** and accepting early adopters.
Join the waitlist and get access to:

* 🔒 Internal beta builds
* 📦 Plugin dev tools
* 🧠 Influence over future features

👉 [**Join Early Access »**](https://yourwebsite.com/waitlist)

---

## 📄 License

Licensed under the [MIT License](./LICENSE).

---

<p align="center">
  Made with ❤️ for lazy devs by <a href="https://github.com/thealphaones">TheAlphaOnes</a>
</p>


