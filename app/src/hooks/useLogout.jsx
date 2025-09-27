import { useCallback } from "react";

export default function useLogout(sessionId, setUser, setSessionId, setImageUrl) {
  return useCallback(async () => {
    if (!sessionId) return;

    try {
      await fetch("http://localhost:8001/logout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId }),
      });
    } catch (err) {
      console.error("Logout error:", err);
    }

    setUser(null);
    setSessionId(null);
    setImageUrl(null);
  }, [sessionId, setUser, setSessionId, setImageUrl]);
}
