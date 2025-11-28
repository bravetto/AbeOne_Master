import type { LoaderFunctionArgs, ActionFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
import { config } from "../lib/config";
import { validateShopifyProxySignature, isFresh, mintInternalServiceJWT, validateStorefrontShopDomain } from "../lib/shared-auth";

// Replaced local helpers with shared-auth module

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const url = new URL(request.url);
  if (!validateShopifyProxySignature(url)) {
    console.warn('[AppProxy] Unauthorized: invalid signature', {
      shop: url.searchParams.get('shop') || null,
      hasSignature: !!(url.searchParams.get('hmac') || url.searchParams.get('signature')),
      ts: url.searchParams.get('timestamp') || null,
    });
    return new Response("Unauthorized", { status: 401 });
  }
  const hasTimestamp = !!url.searchParams.get('timestamp');
  if (hasTimestamp && !isFresh(url)) {
    console.warn('[AppProxy] Unauthorized: timestamp not fresh', {
      ts: url.searchParams.get('timestamp') || null,
    });
    return new Response("Unauthorized", { status: 401 });
  }

  const shop = url.searchParams.get("shop") || "";
  if (!validateStorefrontShopDomain(shop)) {
    return new Response("Bad shop", { status: 400 });
  }

  const message = url.searchParams.get("message") || "";
  const token = await mintInternalServiceJWT(shop);
  if (!token) {
    return json({ error: "Internal auth not configured: missing INTERNAL_JWT_SECRET" }, { status: 500 });
  }

  const wantsStreaming = config.chat.enableStreaming === true;
  const shopifySessionToken = request.headers.get("authorization");

  const res = await fetch(`${config.bravetto.apiUrl}/api/shopify/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Shopify-Shop-Domain": shop,
      "Authorization": `Bearer ${token}`,
      ...(shopifySessionToken ? { "X-Shopify-Session-Token": shopifySessionToken } : {}),
    },
    body: JSON.stringify({
      message,
      shopDomain: shop,
      streaming: wantsStreaming,
      context: { platform: "shopify_storefront" },
    }),
  });

  const contentType = res.headers.get("content-type") || "application/json";
  const headers = new Headers();
  res.headers.forEach((value, key) => {
    if (key === "transfer-encoding" || key === "content-length") {
      return;
    }
    headers.set(key, value);
  });

  if (!headers.has("Content-Type")) {
    headers.set("Content-Type", contentType);
  }

  const isSseResponse = wantsStreaming && contentType.includes("text/event-stream") && res.body;

  if (isSseResponse && res.body) {
    if (!headers.has("Cache-Control")) {
      headers.set("Cache-Control", "no-cache, no-transform");
    }
    headers.set("Connection", "keep-alive");
    headers.set("X-Accel-Buffering", "no");

    return new Response(res.body, {
      status: res.status,
      headers,
    });
  }

  const text = await res.text();
  return new Response(text, {
    status: res.status,
    headers,
  });
};

export const action = async ({ request }: ActionFunctionArgs) => {
  const url = new URL(request.url);
  if (!validateShopifyProxySignature(url)) {
    console.warn('[AppProxy] Unauthorized: invalid signature (POST)', {
      shop: url.searchParams.get('shop') || null,
      hasSignature: !!(url.searchParams.get('hmac') || url.searchParams.get('signature')),
      ts: url.searchParams.get('timestamp') || null,
    });
    return new Response("Unauthorized", { status: 401 });
  }
  const hasTimestamp = !!url.searchParams.get('timestamp');
  if (hasTimestamp && !isFresh(url)) {
    console.warn('[AppProxy] Unauthorized: timestamp not fresh (POST)', {
      ts: url.searchParams.get('timestamp') || null,
    });
    return new Response("Unauthorized", { status: 401 });
  }

  const shop = url.searchParams.get("shop") || "";
  if (!validateStorefrontShopDomain(shop)) {
    return new Response("Bad shop", { status: 400 });
  }

  // Prefer JSON body for POST requests, fallback to URL param
  let message = "";
  let systemPromptId: string | null = null;
  let context: any = { platform: "shopify_storefront" };
  let wantsStreaming = config.chat.enableStreaming === true;
  let history: any[] | undefined;
  try {
    const contentType = request.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
      const body = await request.json();
      message = (body && typeof body.message === "string") ? body.message : "";
      if (typeof body.systemPromptId === "string") systemPromptId = body.systemPromptId;
      if (body && typeof body.streaming === "boolean") wantsStreaming = body.streaming;
      if (body && body.context && typeof body.context === "object") {
        context = { platform: "shopify_storefront", ...body.context };
      }
      if (body && Array.isArray(body.history)) {
        history = body.history;
      }
    }
  } catch (_) {
    // ignore JSON parse errors and fallback to query param
  }
  if (!message) {
    message = url.searchParams.get("message") || "";
  }

  const token = await mintInternalServiceJWT(shop);
  if (!token) {
    return json({ error: "Internal auth not configured: missing INTERNAL_JWT_SECRET" }, { status: 500 });
  }

  const shopifySessionToken = request.headers.get("authorization");

  const res = await fetch(`${config.bravetto.apiUrl}/api/shopify/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Shopify-Shop-Domain": shop,
      "Authorization": `Bearer ${token}`,
      ...(shopifySessionToken ? { "X-Shopify-Session-Token": shopifySessionToken } : {}),
    },
    body: JSON.stringify({
      message,
      shopDomain: shop,
      streaming: wantsStreaming,
      systemPromptId,
      context,
      history,
    }),
  });

  const contentType = res.headers.get("content-type") || "application/json";
  const headers = new Headers();
  res.headers.forEach((value, key) => {
    if (key === "transfer-encoding" || key === "content-length") {
      return;
    }
    headers.set(key, value);
  });

  if (!headers.has("Content-Type")) {
    headers.set("Content-Type", contentType);
  }

  const isSseResponse = wantsStreaming && contentType.includes("text/event-stream") && res.body;

  if (isSseResponse && res.body) {
    if (!headers.has("Cache-Control")) {
      headers.set("Cache-Control", "no-cache, no-transform");
    }
    headers.set("Connection", "keep-alive");
    headers.set("X-Accel-Buffering", "no");

    return new Response(res.body, {
      status: res.status,
      headers,
    });
  }

  const text = await res.text();
  return new Response(text, {
    status: res.status,
    headers,
  });
};


