# One-shot rebuild: tiles + tasks + daily log + compact duration. Preserves <script>.
from pathlib import Path
import re

PATH = Path(__file__).resolve().parent / "Acai timer.html"
t = PATH.read_text(encoding="utf-8")

head = t[: t.index("<style>") + len("<style>")]
script_part = t[t.index("<script>") :]

marker = '<div class="app">'
inner = t[t.index(marker) + len(marker) : t.index("<script>")]
cup_i = inner.index('<div class="cup-scene"')
svg_e = inner.index("</svg>", cup_i) + len("</svg>")
cup_e = inner.index("</div>", svg_e) + len("</div>")
cup = inner[cup_i:cup_e]

dot3 = inner.index('id="dot3"')
sess_e = inner.index("</div>", inner.index("</div>", dot3) + 1) + len("</div>")
prog_i = inner.index('<div class="progress-wrap"')
prog_sessions = inner[prog_i:sess_e]

COMPACT = (
    '<div class="dur-section compact-duration"><div class="dur-label-row">Focus length</div>'
    '<div class="custom-row compact-time-row"><div class="time-field"><label>hr</label>'
    '<input class="time-input" id="customHr" type="number" min="0" max="23" value="0"/></div><span class="time-sep">:</span>'
    '<div class="time-field"><label>min</label><input class="time-input" id="customMin" type="number" min="0" max="59" value="25"/></div><span class="time-sep">:</span>'
    '<div class="time-field"><label>sec</label><input class="time-input" id="customSec" type="number" min="0" max="59" value="0"/></div>'
    '<button type="button" class="set-btn" id="setCustomBtn">Apply</button></div></div>'
    '<div class="controls"><button type="button" class="btn btn-icon" id="resetBtn" title="Reset">↺</button>'
    '<button type="button" class="btn btn-main" id="startBtn">Start Sipping</button>'
    '<button type="button" class="btn btn-icon" id="skipBtn" title="Skip Break">⏭</button></div>'
    '<div class="complete-msg" id="completeMsg">Session complete. Breathe and reset.</div>'
)

TODO = (
    '<div class="tile tile-tasks"><div class="todo-panel" id="todoPanel">'
    '<div class="todo-panel-head"><span class="custom-title" style="margin:0">Tasks</span>'
    '<button type="button" class="btn-text" id="todoClearDoneBtn">Clear finished</button></div>'
    '<div class="todo-add-row"><input type="text" id="todoNewInput" class="todo-input" placeholder="Add a task…" maxlength="500" autocomplete="off"/>'
    '<button type="button" class="btn btn-main" id="todoAddBtn" style="margin:0;padding:11px 18px;font-size:.82rem">Add</button></div>'
    '<div class="todo-remind-row"><label class="todo-inline"><input type="checkbox" id="todoRemindTomorrow"/> Remind tomorrow</label>'
    '<label class="todo-inline">Pick date <input type="date" id="todoRemindDate" class="todo-date-input"/></label></div>'
    '<p class="todo-hint">Tasks with a date appear under Tomorrow or Later until that day. Then they show in Today. Check off when done; open Finished to review or remove.</p>'
    '<div class="todo-section-title dur-label-row">Today</div><div id="todoListToday" class="todo-list"></div>'
    '<div class="todo-section-title dur-label-row">Tomorrow</div><div id="todoListTomorrow" class="todo-list"></div>'
    '<div class="todo-section-title dur-label-row">Later</div><div id="todoListLater" class="todo-list"></div>'
    '<div class="todo-done-wrap"><details class="todo-details"><summary class="todo-summary">Finished</summary>'
    '<div id="todoListDone" class="todo-list"></div></details></div></div></div>'
)

DAILY = (
    '<div class="tile tile-daily"><div class="day-log-panel" id="dayLogPanel">'
    '<div class="day-log-head"><span class="custom-title" style="margin:0">Today\'s focus log</span>'
    '<button type="button" class="btn-text" id="copyReportBtn">Copy day report</button></div>'
    '<div class="sheet-sync-section">'
    '<div class="dur-label-row" style="margin-bottom:6px">Google Sheet sync</div>'
    '<p class="sheet-hint">Paste the <strong>Web app URL</strong> from Apps Script (open <code>GoogleAppsScript.gs</code> in this folder for setup). Each saved focus log appends a row.</p>'
    '<div class="sheet-url-row"><input type="url" id="sheetWebhookInput" class="sheet-url-input" placeholder="https://script.google.com/macros/s/.../exec" autocomplete="off"/>'
    '<button type="button" class="btn btn-main sheet-save-btn" id="sheetSaveUrlBtn">Save URL</button></div>'
    '<p class="sheet-sync-status" id="sheetSyncStatus" aria-live="polite"></p></div>'
    '<div class="day-log-content" id="dayLogContent"></div></div>'
    '<div class="log-modal" id="logModal" aria-hidden="true"><div class="log-modal-card" role="dialog" aria-labelledby="logModalTitle">'
    '<h2 class="log-modal-title" id="logModalTitle">What did you get done?</h2>'
    '<p class="log-modal-meta" id="logTimeRange"></p>'
    '<p class="log-modal-sub">Adds to today\'s log above for end-of-day meetings and notes.</p>'
    '<label for="logNoteInput" class="dur-label-row" style="display:block;margin-bottom:6px">This focus block</label>'
    '<textarea id="logNoteInput" maxlength="2000" placeholder="e.g. Sprint planning, deep work, 1:1 with Alex…"></textarea>'
    '<div class="log-modal-actions"><button type="button" class="btn-ghost" id="logSkipBtn">Skip</button>'
    '<button type="button" class="btn btn-main" id="logSaveBtn" style="margin:0">Save to log</button></div></div></div></div>'
)

body_inner = (
    '<body><div class="berry-bg" id="berryBg"></div><div class="app">'
    '<header class="tile tile-header"><div><div class="title">Trey\'s Focus <span>Flow</span></div>'
    '<div class="subtitle">Focus timer, tasks, and daily log</div></div></header>'
    '<div class="tile tile-visual">' + cup + '</div>'
    '<div class="tile tile-focus">' + prog_sessions + COMPACT + '</div>'
    + TODO + DAILY
    + '</div>'
)

old_css = t[t.index("<style>") + 7 : t.index("</style>")]
old_css = re.sub(
    r"\.dur-tabs\{[^}]+\}\.dur-btn\{[^}]+\}\.dur-btn:focus-visible\{[^}]+\}\.dur-btn:hover,\.dur-btn\.active\{[^}]+\}",
    "",
    old_css,
    count=1,
)
old_css = old_css.replace(
    "body{min-height:100vh;min-height:100dvh;background:linear-gradient(145deg,#d8e2ec 0%,#e8eef6 48%,#dde8e4 100%);font-family:'DM Sans',sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;overflow-x:hidden;overflow-y:auto;position:relative;padding:20px 16px 28px;box-sizing:border-box;}",
    "body{min-height:100vh;min-height:100dvh;background:linear-gradient(145deg,#d8e2ec 0%,#e8eef6 48%,#dde8e4 100%);font-family:'DM Sans',sans-serif;display:block;overflow-x:hidden;overflow-y:auto;position:relative;padding:clamp(20px,3vh,36px) clamp(16px,3.5vw,56px) clamp(32px,4vh,56px);box-sizing:border-box;}",
    1,
)
old_css = old_css.replace(
    ".app{position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;gap:16px;padding:12px 0;width:100%;max-width:420px;margin:0 auto;}",
    ".app{position:relative;z-index:1;width:100%;max-width:min(1720px,calc(100vw - 32px));margin:0 auto;display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:clamp(24px,2.8vw,40px);align-items:start;}",
    1,
)
APP_RULE = ".app{position:relative;z-index:1;width:100%;max-width:min(1720px,calc(100vw - 32px));margin:0 auto;display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:clamp(24px,2.8vw,40px);align-items:start;}"
TILE_CSS = (
    ".tile{background:rgba(255,255,255,.82);border:1px solid rgba(184,199,214,.75);border-radius:22px;"
    "box-shadow:0 10px 40px rgba(26,40,54,.09);padding:clamp(22px,2.5vw,38px);box-sizing:border-box;min-height:0;}"
    ".tile-header{grid-column:1/-1;text-align:center;padding:clamp(22px,2.5vw,36px) clamp(24px,3.5vw,52px);"
    "background:linear-gradient(180deg,rgba(245,248,252,.96) 0%,rgba(236,242,249,.9) 100%);}"
    ".tile-visual{grid-column:1/span 6;display:flex;justify-content:center;align-items:flex-start;padding-top:clamp(8px,1.5vw,20px);}"
    ".tile-focus{grid-column:7/span 6;display:flex;flex-direction:column;align-items:center;gap:clamp(20px,2.2vw,32px);}"
    ".tile-tasks{grid-column:1/-1;grid-row:3;align-self:stretch;}"
    ".tile-daily{grid-column:1/-1;grid-row:4;align-self:stretch;display:flex;flex-direction:column;gap:clamp(14px,1.5vw,22px);}"
    ".tile-focus .sessions{margin-top:4px;}"
    ".tile-focus .dur-section{width:100%;max-width:min(620px,100%);background:rgba(255,255,255,.55);border-radius:16px;"
    "padding:clamp(12px,1.4vw,20px);border:1px solid rgba(184,199,214,.55);}"
    ".tile-focus .controls{width:100%;max-width:min(620px,100%);}"
    ".tile-focus .complete-msg.show{margin-top:8px;}"
    ".tile-daily .day-log-panel{background:transparent;border:none;box-shadow:none;padding:0;margin:0;width:100%;}"
    "@media (max-width:960px){.tile-header,.tile-visual,.tile-focus,.tile-tasks,.tile-daily{grid-column:1/-1;grid-row:auto;}"
    ".tile-visual{order:1;}.tile-focus{order:2;}.tile-tasks{order:3;}.tile-daily{order:4;}.app{display:flex;flex-direction:column;}}"
)
if APP_RULE in old_css and ".tile-daily{" not in old_css:
    old_css = old_css.replace(APP_RULE, APP_RULE + TILE_CSS, 1)

old_css = old_css.replace(
    ".title{font-family:'Playfair Display',serif;font-size:1.9rem;font-weight:900;color:var(--berry);letter-spacing:-.5px;text-align:center;line-height:1.1;}",
    ".title{font-family:'Playfair Display',serif;font-size:clamp(1.85rem,3.2vw,2.55rem);font-weight:900;color:var(--berry);letter-spacing:-.5px;text-align:center;line-height:1.1;}",
    1,
)
old_css = old_css.replace(
    ".cup-scene{position:relative;width:200px;height:340px;cursor:pointer;filter:drop-shadow(0 18px 36px rgba(30,58,90,.22));transition:filter .3s;}",
    ".cup-scene{position:relative;width:clamp(200px,18vw,280px);height:auto;aspect-ratio:200/340;cursor:pointer;filter:drop-shadow(0 18px 36px rgba(30,58,90,.22));transition:filter .3s;}",
    1,
)
old_css = old_css.replace(
    ".progress-wrap{position:relative;width:186px;height:186px;display:flex;align-items:center;justify-content:center;}",
    ".progress-wrap{position:relative;width:min(300px,32vw);height:min(300px,32vw);max-width:100%;aspect-ratio:1;display:flex;align-items:center;justify-content:center;}",
    1,
)
old_css = old_css.replace(
    ".timer-display{font-family:'Playfair Display',serif;font-size:3.6rem;font-weight:900;color:var(--berry);letter-spacing:-2px;line-height:1;text-align:center;}",
    ".timer-display{font-family:'Playfair Display',serif;font-size:clamp(2.75rem,5.5vw,4.35rem);font-weight:900;color:var(--berry);letter-spacing:-2px;line-height:1;text-align:center;}",
    1,
)

if ".compact-duration" not in old_css:
    old_css = old_css.replace(
        ".dur-section{display:flex;flex-direction:column;align-items:center;gap:7px;}",
        ".dur-section{display:flex;flex-direction:column;align-items:center;gap:7px;}"
        ".compact-duration{gap:4px;}"
        ".compact-duration .custom-row{align-items:flex-end;flex-wrap:wrap;justify-content:center;gap:6px 10px;}"
        ".compact-duration .time-field{gap:1px;}"
        ".compact-duration .time-field label{font-size:.52rem;}"
        ".compact-duration .time-input{width:40px;padding:4px 2px;font-size:.8rem;border-radius:8px;}"
        ".compact-duration .time-sep{margin-top:0;align-self:center;padding-bottom:8px;font-size:.9rem;}"
        ".compact-duration .set-btn{margin-top:0;padding:7px 16px;font-size:.74rem;align-self:center;}",
        1,
    )

PANEL_CSS = (
    ".btn-text{background:none;border:none;font-family:inherit;font-size:.72rem;font-weight:500;color:var(--berry);"
    "cursor:pointer;padding:6px 10px;border-radius:8px;text-decoration:underline;text-underline-offset:3px;}"
    ".btn-text:hover{color:var(--pink);background:rgba(228,235,244,.65);}"
    ".btn-text:focus-visible{outline:2px solid var(--berry);outline-offset:2px;}"
    ".day-log-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap;margin-bottom:12px;}"
    ".day-log-content{max-height:min(480px,50vh);overflow-y:auto;padding-right:6px;margin-top:4px;}"
    ".day-log-content::-webkit-scrollbar{width:8px;}"
    ".day-log-content::-webkit-scrollbar-thumb{background:rgba(61,111,163,.35);border-radius:8px;}"
    ".day-log-empty{font-size:.8rem;color:#5d6f82;line-height:1.4;margin:8px 0;}"
    ".hour-block{margin-bottom:16px;padding-bottom:14px;border-bottom:1px solid rgba(184,199,214,.6);}"
    ".hour-block:last-child{border-bottom:none;margin-bottom:0;padding-bottom:0;}"
    ".hour-label{font-size:.68rem;font-weight:600;color:var(--berry);letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;}"
    ".log-entry{background:rgba(255,255,255,.65);border:1px solid rgba(184,199,214,.45);border-radius:12px;padding:10px 12px;margin-bottom:8px;}"
    ".log-entry-time{font-size:.78rem;font-weight:600;color:#2c3d4f;display:inline-block;margin-right:10px;}"
    ".log-entry-dur{font-size:.72rem;color:#b07090;}"
    ".log-entry-note{font-size:.8rem;color:#2a3544;margin:8px 0 0;line-height:1.4;}"
    ".log-entry-note .muted{color:#7a8795;font-style:italic;}"
    ".sheet-sync-section{margin-top:8px;padding:14px 16px;background:rgba(255,255,255,.55);border:1px solid rgba(184,199,214,.55);border-radius:14px;}"
    ".sheet-hint{font-size:.72rem;color:#4d5d6e;line-height:1.45;margin:0 0 10px;}"
    ".sheet-hint code{font-size:.68rem;background:rgba(228,235,244,.92);padding:2px 6px;border-radius:6px;}"
    ".sheet-url-row{display:flex;flex-wrap:wrap;gap:10px;align-items:center;}"
    ".sheet-url-input{flex:1;min-width:200px;padding:10px 12px;border:1.5px solid #b8c7d6;border-radius:12px;font-family:inherit;font-size:.78rem;color:var(--berry);}"
    ".sheet-url-input:focus{outline:none;border-color:var(--pink);}"
    ".sheet-save-btn{padding:11px 18px!important;font-size:.82rem!important;}"
    ".log-modal{position:fixed;inset:0;background:rgba(22,32,44,.48);display:flex;align-items:center;justify-content:center;"
    "padding:20px;z-index:100;opacity:0;visibility:hidden;pointer-events:none;transition:opacity .2s,visibility .2s;}"
    ".log-modal.show{opacity:1;visibility:visible;pointer-events:auto;}"
    ".log-modal-card{width:100%;max-width:min(520px,100%);background:#fff;border-radius:20px;padding:clamp(22px,3vw,32px);"
    "box-shadow:0 24px 60px rgba(20,35,52,.22);border:1px solid rgba(184,199,214,.65);}"
    ".log-modal-title{font-family:'Playfair Display',serif;font-size:1.35rem;color:var(--berry);margin:0 0 8px;}"
    ".log-modal-meta{font-size:.8rem;color:#4d5d6e;margin:0 0 8px;line-height:1.4;}"
    ".log-modal-sub{font-size:.74rem;color:#5a6b78;line-height:1.45;margin:0 0 14px;}"
    "#logNoteInput{width:100%;min-height:100px;resize:vertical;padding:12px 14px;border:1.5px solid #b8c7d6;border-radius:12px;"
    "font-family:inherit;font-size:.88rem;color:#2a3544;margin-bottom:16px;}"
    "#logNoteInput:focus{outline:none;border-color:var(--pink);}"
    ".log-modal-actions{display:flex;justify-content:flex-end;gap:12px;flex-wrap:wrap;}"
    ".btn-ghost{background:white;border:1.5px solid #b8c7d6;color:var(--berry);font-family:'DM Sans',sans-serif;font-size:.88rem;"
    "font-weight:500;padding:11px 22px;border-radius:50px;cursor:pointer;transition:all .18s;}"
    ".btn-ghost:hover{background:var(--blush);border-color:var(--pink);}"
    ".btn-ghost:focus-visible{outline:2px solid var(--berry);outline-offset:2px;}"
    ".todo-panel{width:100%;margin-top:0;background:rgba(255,255,255,.75);border:1.5px solid #b8c7d6;border-radius:16px;padding:14px 16px;}"
    ".todo-panel-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;flex-wrap:wrap;gap:8px;}"
    ".todo-add-row{display:flex;gap:8px;margin-bottom:8px;width:100%;align-items:center;}"
    ".todo-input{flex:1;min-width:0;padding:10px 12px;border:1.5px solid #b8c7d6;border-radius:12px;font-family:'DM Sans',sans-serif;font-size:.85rem;color:var(--berry);}"
    ".todo-input:focus{outline:none;border-color:var(--pink);}"
    ".todo-remind-row{display:flex;flex-wrap:wrap;gap:12px;align-items:center;font-size:.72rem;color:#5d6f82;margin-bottom:6px;}"
    ".todo-inline{display:flex;align-items:center;gap:6px;cursor:pointer;}"
    ".todo-date-input{padding:4px 8px;border:1.5px solid #b8c7d6;border-radius:8px;font-family:inherit;font-size:.72rem;color:var(--berry);}"
    ".todo-hint{font-size:.65rem;color:#5d6f82;line-height:1.35;margin-bottom:10px;}"
    ".todo-section-title{margin-top:10px;margin-bottom:6px;}"
    ".todo-list{min-height:4px;}"
    ".todo-empty{font-size:.72rem;color:#7a8795;font-style:italic;padding:6px 0;margin:0;}"
    ".todo-item{display:flex;flex-wrap:wrap;align-items:flex-start;gap:8px;padding:8px 10px;background:rgba(255,255,255,.5);"
    "border-radius:10px;margin-bottom:6px;border:1px solid rgba(184,199,214,.4);}"
    ".todo-row-label{display:flex;align-items:flex-start;gap:8px;flex:1;min-width:0;cursor:pointer;margin:0;}"
    ".todo-cb{margin-top:3px;flex-shrink:0;}"
    ".todo-text{flex:1;word-break:break-word;font-size:.82rem;color:#2c3d4f;}"
    ".todo-text-done{text-decoration:line-through;opacity:.65;}"
    ".todo-badge{font-size:.62rem;background:var(--blush);color:var(--berry);padding:2px 8px;border-radius:50px;white-space:nowrap;align-self:center;}"
    ".todo-actions{display:flex;flex-wrap:wrap;gap:2px 8px;align-items:center;margin-left:auto;}"
    ".todo-done-wrap{margin-top:12px;border-top:1px solid rgba(184,199,214,.55);padding-top:10px;}"
    ".todo-summary{cursor:pointer;font-size:.67rem;color:#b07090;letter-spacing:1px;text-transform:uppercase;list-style:none;}"
    ".todo-summary::-webkit-details-marker{display:none;}"
    ".todo-del{color:#2d5a78!important;}"
)
if ".log-modal{" not in old_css or ".todo-panel{" not in old_css:
    old_css += PANEL_CSS

out = head + old_css + "</style></head>" + body_inner + script_part
PATH.write_text(out, encoding="utf-8")
print("Wrote", PATH, "bytes", len(out))
