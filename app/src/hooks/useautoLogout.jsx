import { useEffect } from "react";

export default function useAutoLogout(sessionId, handleLogout, timeout) {
  useEffect(() => {
    if (!sessionId) return;

    let timer;

    const resetTimer = () => {
      clearTimeout(timer);
      timer = setTimeout(() => {
        console.log("Auto logout: inactive for 5 mins");
        handleLogout();
      }, timeout);
    };

    window.addEventListener("mousemove", resetTimer);
    window.addEventListener("keydown", resetTimer);
    window.addEventListener("click", resetTimer);
    window.addEventListener("scroll", resetTimer);

    const handleUnload = () => handleLogout();
    window.addEventListener("beforeunload", handleUnload);

    resetTimer(); 

    return () => {
      clearTimeout(timer);
      window.removeEventListener("mousemove", resetTimer);
      window.removeEventListener("keydown", resetTimer);
      window.removeEventListener("click", resetTimer);
      window.removeEventListener("scroll", resetTimer);
      window.removeEventListener("beforeunload", handleUnload);
    };
  }, [sessionId, handleLogout, timeout]);
}
