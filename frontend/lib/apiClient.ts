export const API_BASE_URL = "http://127.0.0.1:8000";

export async function fetchEvents() {
  const response = await fetch(`${API_BASE_URL}/events/`);
  if (!response.ok) {
    throw new Error('Failed to fetch events');
  }
  return response.json();
}

export async function triggerNmapScan() {
  const response = await fetch(`${API_BASE_URL}/attack/nmap-scan`, {
    method: 'POST',
  });
  if (!response.ok) {
    throw new Error('Failed to trigger Nmap scan');
  }
  return response.json();
}

export async function triggerSshBruteforce(port: number = 2222) {
  const response = await fetch(`${API_BASE_URL}/attack/ssh-bruteforce?port=${port}`, {
    method: 'POST',
  });
  if (!response.ok) {
    throw new Error('Failed to trigger SSH brute-force');
  }
  return response.json();
}

