import { spawn } from "node:child_process";

function readStdin() {
  return new Promise((resolve, reject) => {
    let input = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => {
      input += chunk;
    });
    process.stdin.on("end", () => {
      try {
        resolve(JSON.parse(input || "{}"));
      } catch (error) {
        reject(error);
      }
    });
    process.stdin.on("error", reject);
  });
}

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function withTimeout(promise, ms, label) {
  let timer;
  const timeout = new Promise((_, reject) => {
    timer = setTimeout(() => reject(new Error(`timeout: ${label}`)), ms);
  });
  return Promise.race([promise, timeout]).finally(() => clearTimeout(timer));
}

class RpcClient {
  constructor(ws) {
    this.ws = ws;
    this.nextId = 1;
    this.pending = new Map();
    this.events = [];
    this.reply = "";
    this.finalReply = "";
    this.turnStatus = null;
    ws.onmessage = (event) => this.handleMessage(event);
  }

  request(method, params = {}, timeoutMs = 120000) {
    const id = this.nextId++;
    this.ws.send(JSON.stringify({ jsonrpc: "2.0", id, method, params }));
    return withTimeout(
      new Promise((resolve, reject) => {
        this.pending.set(id, { resolve, reject });
      }),
      timeoutMs,
      method,
    );
  }

  handleMessage(event) {
    const message = JSON.parse(event.data);
    if (message.id && this.pending.has(message.id)) {
      const pending = this.pending.get(message.id);
      this.pending.delete(message.id);
      if (message.error) {
        pending.reject(new Error(JSON.stringify(message.error)));
      } else {
        pending.resolve(message.result);
      }
      return;
    }
    if (!message.method) {
      return;
    }
    this.events.push(message);
    const params = message.params || {};
    if (message.method === "item/agentMessage/delta") {
      this.reply += params.delta || "";
      return;
    }
    const item = params.item;
    if (item && item.type === "agentMessage" && typeof item.text === "string" && item.text.trim()) {
      this.finalReply = item.text.trim();
      return;
    }
    if (message.method === "turn/completed") {
      this.turnStatus = params.turn?.status || "completed";
    }
  }

  async waitForTurn(timeoutMs) {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      if (this.turnStatus) {
        return this.turnStatus;
      }
      await wait(250);
    }
    throw new Error("timeout: turn/completed");
  }
}

async function openWebSocket(url, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  let lastError;
  while (Date.now() < deadline) {
    try {
      const ws = new WebSocket(url);
      await new Promise((resolve, reject) => {
        ws.onopen = resolve;
        ws.onerror = reject;
      });
      return ws;
    } catch (error) {
      lastError = error;
      await wait(250);
    }
  }
  throw lastError || new Error("Codex app-server did not open");
}

async function ensureThread(rpc, payload, timeoutMs) {
  const resumeParams = {
    threadId: payload.threadId,
    model: payload.model || null,
    developerInstructions: payload.developerInstructions || null,
  };
  if (payload.threadId) {
    try {
      const resumed = await rpc.request("thread/resume", resumeParams, timeoutMs);
      return resumed.thread?.id || payload.threadId;
    } catch (error) {
      if (!payload.allowCreateOnResumeFailure) {
        throw error;
      }
    }
  }

  const startParams = {
    cwd: payload.cwd || null,
    model: payload.model || null,
    developerInstructions: payload.developerInstructions || null,
  };
  const started = await rpc.request("thread/start", startParams, timeoutMs);
  const threadId = started.thread?.id;
  if (!threadId) {
    throw new Error("thread/start returned no thread id");
  }
  if (payload.threadName) {
    await rpc.request("thread/name/set", { threadId, name: payload.threadName }, 15000).catch(() => null);
  }
  return threadId;
}

async function main() {
  const payload = await readStdin();
  if (!payload.question || !String(payload.question).trim()) {
    throw new Error("question is required");
  }
  const timeoutMs = Number(payload.timeoutMs || 120000);
  const port = 22000 + Math.floor(Math.random() * 20000);
  const url = `ws://127.0.0.1:${port}`;
  const codexExe = payload.codexExe || "codex";
  const startupTier = payload.startupServiceTier || "fast";
  const server = spawn(
    codexExe,
    ["-c", `service_tier="${startupTier}"`, "app-server", "--listen", url],
    { stdio: ["ignore", "ignore", "pipe"] },
  );
  let stderr = "";
  server.stderr.on("data", (chunk) => {
    stderr += String(chunk);
  });

  let ws;
  try {
    ws = await openWebSocket(url, 15000);
    const rpc = new RpcClient(ws);
    await rpc.request(
      "initialize",
      {
        clientInfo: { name: "fujie-desktop-pet", version: "0.1.0" },
        capabilities: { experimentalApi: true },
      },
      15000,
    );
    const threadId = await ensureThread(rpc, payload, timeoutMs);
    await rpc.request(
      "turn/start",
      {
        threadId,
        input: [{ type: "text", text: String(payload.question).trim() }],
        model: payload.model || null,
      },
      timeoutMs,
    );
    const status = await rpc.waitForTurn(timeoutMs);
    if (status !== "completed") {
      throw new Error(`turn failed: ${status}`);
    }
    const text = (rpc.finalReply || rpc.reply).trim();
    if (!text) {
      throw new Error("empty assistant reply");
    }
    process.stdout.write(JSON.stringify({ ok: true, text, threadId }));
  } catch (error) {
    process.stdout.write(
      JSON.stringify({
        ok: false,
        error: error instanceof Error ? error.message : String(error),
        stderr: stderr.slice(-4000),
      }),
    );
    process.exitCode = 1;
  } finally {
    try {
      ws?.close();
    } catch {
      // ignore cleanup errors
    }
    server.kill();
  }
}

main();
