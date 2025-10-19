// server.js
const express = require("express");
const cors = require("cors");
const fs = require("fs/promises");
const fssync = require("fs");
const path = require("path");
require('dotenv').config();

const app = express();
app.use(cors());

const REPO_PATH = process.env.REPO_PATH || "/app/notes";
const TODO_FILE = process.env.TODO_FILE || "TODO.md";

const MARKDOWN_PATH = path.join(REPO_PATH, TODO_FILE);

function iso(dt) {
    return dt ? new Date(dt).toISOString() : null;
}

async function parseChecklist(filePath = MARKDOWN_PATH) {
    try {
        const raw = await fs.readFile(filePath, "utf8");
        const lines = raw.split(/\r?\n/);

        const checklist = [];
        const re = /^- \[( |x)\] (.+)$/;

        for (const line of lines) {
            const m = line.match(re);
            if (m) {
                const done = m[1] === "x";
                const text = m[2].trim();
                checklist.push({ done, text });
            }
        }

        const total = checklist.length;
        const completed = checklist.filter(i => i.done).length;
        const nextItem = (checklist.find(i => !i.done) || {}).text || null;

        // mtime / age
        let lastUpdated = null;
        let ageHours = null;
        try {
            const stat = fssync.statSync(filePath);
            lastUpdated = stat.mtime;
            ageHours = (Date.now() - stat.mtime.getTime()) / (1000 * 60 * 60);
        } catch { /* leave nulls */ }

        return {
            status: "ok",
            total,
            completed,
            percent: total ? Math.floor((completed / total) * 100) : 0,
            next: nextItem || "well done!",
            last_updated: lastUpdated ? iso(lastUpdated) : null,
            age_hours: ageHours
        };
    } catch (e) {
        return { status: "error", message: `Could not read markdown: ${e.message}` };
    }
}

app.get("/", (_req, res) => {
    res.json({ ok: true, version: "0.1.0-a", hint: "use /focus or /healthz" });
});

app.get("/healthz", (_req, res) => {
    res.json({ ok: true });
});

app.get("/focus", async (_req, res) => {
    const data = await parseChecklist();
    res.json(data);
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log(`focus-api (node) listening on :${PORT}`);
});