const REQUIRED_TOOLS = [
  "/nmap",
  "/sqlmap",
  "/netcat",
  "/metasploit",
  "/password_cracking",
  "/john",
  "/hydra"
];

const CURRENT_PAGE = location.pathname;

// ❌ Do nothing on security_features.html
if (CURRENT_PAGE !== "/") {

  let completed = false;

  window.addEventListener("scroll", () => {
    const scrollTop = window.scrollY;
    const winHeight = window.innerHeight;
    const docHeight = document.documentElement.scrollHeight;

    if (scrollTop + winHeight >= docHeight - 5 && !completed) {
      completed = true;

      // mark this lesson complete
      localStorage.setItem(`lesson:${CURRENT_PAGE}`, "done");

      // check if all lessons are completed
      const allDone = REQUIRED_TOOLS.every(
        p => localStorage.getItem(`lesson:${p}`) === "done"
      );

      if (allDone) {
        // redirect to home after short delay
        setTimeout(() => {
          window.location.href = "/";
        }, 800);
      }
    }
  });

}
