/* ================= CANONICAL PHASE LIST ================= */
/* SINGLE SOURCE OF TRUTH */
const REQUIRED_PHASES = [
  "reconnaissance",     // nmap
  "enumeration",        // netcat
  "exploitation",       // sqlmap + metasploit
  "credential_attacks"  // password_cracking + hydra + john
];

/* ================= CURRENT PAGE ================= */
const LESSON_ID = document.body.dataset.lesson;

/* ================= TRACK COMPLETION ================= */
if (LESSON_ID && REQUIRED_PHASES.includes(LESSON_ID)) {

  let completed = false;

  window.addEventListener("scroll", () => {
    const scrollTop = window.scrollY;
    const winHeight = window.innerHeight;
    const docHeight = document.documentElement.scrollHeight;

    if (scrollTop + winHeight >= docHeight - 5 && !completed) {
      completed = true;

      localStorage.setItem(`lesson:${LESSON_ID}`, "done");

      /* DEBUG */
      console.table(
        REQUIRED_PHASES.map(p => ({
          phase: p,
          status: localStorage.getItem(`lesson:${p}`)
        }))
      );

      const allDone = REQUIRED_PHASES.every(
        p => localStorage.getItem(`lesson:${p}`) === "done"
      );

      if (allDone) {
        setTimeout(() => {
          window.location.href = "/";
        }, 800);
      }
    }
  });
}
