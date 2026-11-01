export const WS_BASE_URL = "ws://127.0.0.1:8000/ws";

export function createWebSocketConnection(onMessage: (data: any) => void) {
  const ws = new WebSocket(WS_BASE_URL);

  ws.onopen = () => {
    console.log("Connected to WebSocket");
  };

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch (e) {
      console.error("Failed to parse websocket message", e);
    }
  };

  ws.onerror = (error) => {
    console.error("WebSocket error", error);
  };

  ws.onclose = () => {
    console.log("Disconnected from WebSocket");
  };

  return ws;
}
