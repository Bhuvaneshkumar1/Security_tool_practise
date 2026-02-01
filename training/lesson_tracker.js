const REQUIRED_TOOLS = [
  "nmap",
  "sqlmap",
  "netcat",
  "metasploit",
  "password_cracking",
  "john",
  "hydra"
];

/* 👇 SET THIS MANUALLY PER PAGE */
const LESSON_ID = document.body.dataset.lesson;

/* ❌ Do nothing on home page */
if (LESSON_ID) {

  let completed = false;

  window.addEventListener("scroll", () => {
    const scrollTop = window.scrollY;
    const winHeight = window.innerHeight;
    const docHeight = document.documentElement.scrollHeight;

    if (scrollTop + winHeight >= docHeight - 5 && !completed) {
      completed = true;

      localStorage.setItem(`lesson:${LESSON_ID}`, "done");

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
