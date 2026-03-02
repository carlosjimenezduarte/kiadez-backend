<script>
  import { onMount } from "svelte";

  onMount(() => {
    /**
         * MVP: "One thing at a time"
         * - Entry 1: takes out 5 and breaks -> 3 remain -> FAIL
         * - Entry 2: takes out 7 and breaks -> 1 remains -> FAIL
         * - Entry 3: takes out 1 by 1 until 8 -> SUCCESS
         */
    
        const TOTAL = 8;
    
        const boardGroup = document.getElementById("boardGroup");
        const ballsGroup = document.getElementById("ballsGroup");
        const starGroup = document.getElementById("starGroup");
        const starUI = document.getElementById("starUI");
    
        const msgBig = document.getElementById("msgBig");
        const msgSmall = document.getElementById("msgSmall");
    
        const controlsGame = document.getElementById("controlsGame");
        const btnRestart = document.getElementById("btnRestart");
        const btnExit = document.getElementById("btnExit");
    
        const btnDonate = document.getElementById("btnDonate");
        const btnSave = document.getElementById("btnSave");
        const btnStarExit = document.getElementById("btnStarExit");
    
        const entryEls = [
          document.getElementById("entry1"),
          document.getElementById("entry2"),
          document.getElementById("entry3"),
        ];
    
        const state = {
          status: "idle", // idle | pulling | fail | success
          extracted: 0,
          activeEntry: null,
          timers: [],
          balls: [], // {el, x, y, outX, outY, isOut}
        };
    
        function clearTimers() {
          state.timers.forEach(t => clearTimeout(t));
          state.timers = [];
        }
    
        function setMessage(big = "", small = "") {
          msgBig.textContent = big;
          msgSmall.textContent = small;
        }
    
        function lockEntries(lock = true) {
          entryEls.forEach(el => {
            el.style.pointerEvents = lock ? "none" : "auto";
            el.style.opacity = lock ? "0.6" : "1";
          });
        }
    
        function resetGame() {
          clearTimers();
          state.status = "idle";
          state.extracted = 0;
          state.activeEntry = null;
    
          // UI
          boardGroup.classList.remove("hidden");
          starGroup.classList.add("hidden");
          starUI.classList.add("hidden");
          controlsGame.classList.remove("hidden");
          setMessage("", "");
    
          // Rebuild balls
          ballsGroup.innerHTML = "";
          state.balls = [];
    
          // Internal positions (simple necklace)
          // (You can switch to a perfect ring later; for now this is clear and clean)
          const inner = [
            {x: 145, y: 170},
            {x: 175, y: 150},
            {x: 205, y: 140},
            {x: 235, y: 150},
            {x: 265, y: 170},
            {x: 255, y: 210},
            {x: 225, y: 235},
            {x: 185, y: 225},
          ];
    
          // Exit positions (outside the box) by entry
          // Entry 1: exits up/left
          // Entry 2: exits up/right
          // Entry 3: exits right/down (one by one)
          const outByEntry = {
            1: inner.map((_, i) => ({x: 70 - i*18, y: 70})),
            2: inner.map((_, i) => ({x: 350 + i*18, y: 70})),
            3: inner.map((_, i) => ({x: 350 + i*18, y: 350})),
          };
    
          for (let i = 0; i < TOTAL; i++) {
            const c = document.createElementNS("http://www.w3.org/2000/svg", "circle");
            c.setAttribute("r", "10");
            c.setAttribute("fill", "#333333");
            c.setAttribute("cx", inner[i].x);
            c.setAttribute("cy", inner[i].y);
            ballsGroup.appendChild(c);
    
            state.balls.push({
              el: c,
              x: inner[i].x,
              y: inner[i].y,
              out: outByEntry, // reference
              isOut: false,
            });
          }
    
          lockEntries(false);
        }
    
        function moveBallTo(ball, x, y, durationMs = 280) {
          // Simple animation via timeouts + attribute tween
          const startX = parseFloat(ball.el.getAttribute("cx"));
          const startY = parseFloat(ball.el.getAttribute("cy"));
          const start = performance.now();
    
          function tick(now) {
            const t = Math.min(1, (now - start) / durationMs);
            const ease = t * (2 - t); // easeOutQuad
            const cx = startX + (x - startX) * ease;
            const cy = startY + (y - startY) * ease;
            ball.el.setAttribute("cx", cx.toFixed(2));
            ball.el.setAttribute("cy", cy.toFixed(2));
            if (t < 1) requestAnimationFrame(tick);
          }
          requestAnimationFrame(tick);
        }
    
        function fail(remainingCount) {
          state.status = "fail";
          lockEntries(true);
          setMessage("That did not work", "Try a different way.");
          // Remaining balls stay inside and do not move.
        }
    
        function success() {
          state.status = "success";
          lockEntries(true);
    
          // Transition: hide board, show star
          setMessage("", "");
          controlsGame.classList.add("hidden");
    
          // Conceptual fade: direct hidden toggle for MVP (simple)
          boardGroup.classList.add("hidden");
          starGroup.classList.remove("hidden");
          starUI.classList.remove("hidden");
        }
    
        function pullFromEntry(entry) {
          if (state.status !== "idle") return;
    
          state.status = "pulling";
          state.activeEntry = entry;
          lockEntries(true);
    
          // Rules:
          // entry 1: salen 5, quedan 3 -> fail
          // entry 2: salen 7, queda 1 -> fail
          // entry 3: salen 8 de 1 a 1 -> success
          const breakAt = (entry === 1) ? 5 : (entry === 2) ? 7 : 8;
    
          if (entry === 1 || entry === 2) {
            // They come out "all at once", but we break at breakAt
            // Animate the first breakAt to the exit point
            for (let i = 0; i < breakAt; i++) {
              const ball = state.balls[i];
              const target = ball.out[entry][i];
              state.timers.push(setTimeout(() => {
                moveBallTo(ball, target.x, target.y, 260);
                ball.isOut = true;
              }, 40));
            }
    
            // Then it "breaks"
            state.timers.push(setTimeout(() => {
              const remaining = TOTAL - breakAt;
              fail(remaining);
            }, 380));
          } else {
            // entry 3: one by one until 8
            let delay = 0;
            for (let i = 0; i < TOTAL; i++) {
              const ball = state.balls[i];
              const target = ball.out[3][i];
              state.timers.push(setTimeout(() => {
                moveBallTo(ball, target.x, target.y, 260);
                ball.isOut = true;
                state.extracted++;
                if (state.extracted === TOTAL) {
                  // short pause and victory
                  setTimeout(success, 260);
                }
              }, delay));
              delay += 260; // ritmo constante
            }
          }
        }
    
        // UI hooks
        entryEls.forEach(el => {
          el.addEventListener("click", () => {
            const entry = Number(el.dataset.entry);
            pullFromEntry(entry);
          });
        });
    
        btnRestart.addEventListener("click", resetGame);
    
        btnExit.addEventListener("click", () => {
          // TODO: redirect to the game article/landing within Kiadez
          alert("Exit: this would take you back to Kiadez.com (game landing).");
        });

        btnStarExit.addEventListener("click", () => {
          alert("Exit: this would take you back to Kiadez.com (game landing).");
        });

        btnDonate.addEventListener("click", () => {
          // TODO: integrate with backend (donation to Guardian 0)
          // - if no session: modal (guest donation vs login)
          // - if session exists: POST /stars/donate (future)
          alert("Donate star (MVP): donation to Guardian 0 would be recorded here.");
        });

        btnSave.addEventListener("click", () => {
          // TODO: integrate with backend
          // - if no session: redirect to login/register and return here
          // - if session exists: POST /stars/save
          alert("Save to my profile (MVP): the star would be credited to the user here.");
        });
    
        // Init
        resetGame();
  });
</script>

<svelte:head>
<meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>One thing at a time — Kiadez</title>
  <style>
    :root {
      --bg: #ffffff;
      --text: #111111;
      --muted: #6b7280;
      --border: #cfcfcf;
      --shape: #333333;
      --btn: #111111;
      --btnText: #ffffff;
      --btnBorder: #111111;
      --soft: #f6f6f6;
    }

    body {
      margin: 0;
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, "Helvetica Neue", Arial;
      background: var(--bg);
      color: var(--text);
      display: grid;
      place-items: center;
      min-height: 100vh;
    }

    .wrap {
      width: min(560px, 92vw);
      display: grid;
      gap: 18px;
    }

    .title {
      display: grid;
      gap: 6px;
      text-align: center;
      margin-top: 6px;
    }
    .title h1 {
      margin: 0;
      font-size: 18px;
      font-weight: 650;
      letter-spacing: .2px;
    }
    .title p {
      margin: 0;
      font-size: 13px;
      color: var(--muted);
    }

    .panel {
      display: grid;
      place-items: center;
      padding: 16px 0 6px;
    }

    .controls {
      display: flex;
      justify-content: center;
      gap: 10px;
      flex-wrap: wrap;
      padding-bottom: 2px;
    }

    button {
      border-radius: 10px;
      padding: 10px 14px;
      border: 1px solid var(--btnBorder);
      background: var(--bg);
      color: var(--btnBorder);
      font-weight: 600;
      cursor: pointer;
      font-size: 14px;
      transition: transform .04s ease;
      user-select: none;
    }
    button:active { transform: translateY(1px); }
    button.primary {
      background: var(--btn);
      color: var(--btnText);
      border-color: var(--btn);
    }
    button.ghost {
      background: transparent;
      border-color: transparent;
      color: var(--muted);
      font-weight: 600;
      padding: 10px 10px;
    }

    .message {
      text-align: center;
      min-height: 56px;
      display: grid;
      place-items: center;
      gap: 6px;
    }
    .message .big {
      font-weight: 700;
      font-size: 16px;
      margin: 0;
    }
    .message .small {
      margin: 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.3;
    }

    /* SVG */
    svg {
      width: min(420px, 86vw);
      height: auto;
    }

    .entry {
      cursor: pointer;
    }
    .entry:hover .slot {
      opacity: .9;
    }

    .hidden { display: none !important; }

    .starCard {
      display: grid;
      justify-items: center;
      gap: 12px;
      padding: 6px 0 2px;
    }

    .choice {
      display: grid;
      gap: 10px;
      justify-items: center;
    }
    .choice .question {
      font-size: 13px;
      color: var(--muted);
      margin: 0;
    }
    .choice .row {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      justify-content: center;
    }
  </style>
</svelte:head>

<div class="wrap">
    <div class="title">
      <h1>One thing at a time</h1>
      <p>No rush. No clues. Just one decision.</p>
    </div>

    <div class="panel">
      <!-- TABLERO -->
      <svg viewBox="0 0 420 420" aria-label="One thing at a time game">
        <!-- Group: board -->
        <g id="boardGroup">
          <!-- Box -->
          <rect x="80" y="80" width="260" height="260" rx="6" fill="#FAFAFA" stroke="#CFCFCF" stroke-width="2"/>

          <!-- Entries (slots) -->
          <!-- Entry 1: top-left -->
          <g class="entry" id="entry1" data-entry="1">
            <rect class="slot" x="78" y="78" width="34" height="10" rx="4" fill="#CFCFCF" opacity="0.7"/>
          </g>

          <!-- Entry 2: top-right -->
          <g class="entry" id="entry2" data-entry="2">
            <rect class="slot" x="308" y="78" width="34" height="10" rx="4" fill="#CFCFCF" opacity="0.7"/>
          </g>

          <!-- Entry 3: bottom-right -->
          <g class="entry" id="entry3" data-entry="3">
            <rect class="slot" x="308" y="332" width="34" height="10" rx="4" fill="#CFCFCF" opacity="0.7"/>
          </g>

          <!-- Spheres (8) -->
          <g id="ballsGroup"></g>
        </g>

        <!-- Group: star -->
        <g id="starGroup" class="hidden">
          <!-- Simple star (you can replace with your SVG later) -->
          <path d="M210 90
                   L240 170
                   L325 170
                   L255 220
                   L280 305
                   L210 255
                   L140 305
                   L165 220
                   L95 170
                   L180 170 Z"
                fill="#D6B35F" opacity="0.95"/>
          <circle cx="210" cy="210" r="4" fill="#ffffff" opacity="0.25"/>
        </g>
      </svg>
    </div>

    <!-- MESSAGES -->
    <div class="message" id="message">
      <p class="big" id="msgBig"></p>
      <p class="small" id="msgSmall"></p>
    </div>

    <!-- CONTROLS -->
    <div class="controls" id="controlsGame">
      <button id="btnRestart">Restart</button>
      <button class="ghost" id="btnExit">Exit</button>
    </div>

    <!-- POST-VICTORY -->
    <div class="starCard hidden" id="starUI">
      <div class="title" style="margin-top:0;">
        <h1 style="font-size:18px;">You won a star</h1>
        <p style="margin-top:2px; font-size:13px;">
          <strong>One thing at a time.</strong><br/>
          Patience is power.
        </p>
      </div>

      <div class="choice">
        <p class="question">What do you want to do with this star?</p>
        <div class="row">
          <button class="primary" id="btnDonate">Donate star</button>
          <button id="btnSave">Save to my profile</button>
          <button class="ghost" id="btnStarExit">Exit</button>
        </div>
      </div>
    </div>
  </div>
