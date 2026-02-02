/* ================= CANONICAL LESSON LIST ================= */
/* THIS IS THE SINGLE SOURCE OF TRUTH */
const REQUIRED_TOOLS = [
  "reconnaissance",      // nmap
  "enumeration",         // netcat
  "exploitation",        // sqlmap + metasploit
  "credential_attacks",  // hydra + john
  "password_cracking"
];


/* ================= CURRENT PAGE ================= */
const LESSON_ID = document.body.dataset.lesson;

/* ================= TRACK COMPLETION ================= */
if (LESSON_ID && REQUIRED_TOOLS.includes(LESSON_ID)) {

  let completed = false;

  window.addEventListener("scroll", () => {
    const scrollTop = window.scrollY;
    const winHeight = window.innerHeight;
    const docHeight = document.documentElement.scrollHeight;

    if (scrollTop + winHeight >= docHeight - 5 && !completed) {
      completed = true;

      localStorage.setItem(`lesson:${LESSON_ID}`, "done");

      /* 🔎 DEBUG (keep for now) */
      console.log("Completed:", LESSON_ID);
      console.log(
        "Progress:",
        REQUIRED_TOOLS.map(t => ({
          tool: t,
          status: localStorage.getItem(`lesson:${t}`)
        }))
      );

      const allDone = REQUIRED_TOOLS.every(
        id => localStorage.getItem(`lesson:${id}`) === "done"
      );

      if (allDone) {
        setTimeout(() => {
          window.location.href = "/";
        }, 800);
      }
    }
  });
}
