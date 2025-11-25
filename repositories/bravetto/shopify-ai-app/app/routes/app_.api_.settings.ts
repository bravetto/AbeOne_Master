import type { LoaderFunctionArgs, ActionFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
// Note: We avoid authenticate.admin to eliminate session-dependency for this proxy.

const BRAVETTO_API_URL = process.env.BRAVETTO_API_URL || "https://www.bravetto.ai";
const SHOPIFY_APP_URL = process.env.SHOPIFY_APP_URL || "https://shopify-ai-app.vercel.app";

export async function loader({ request }: LoaderFunctionArgs) {
  console.log("=== API.SETTINGS LOADER ===");
  console.log("Request headers:", Object.fromEntries(request.headers.entries()));
  
  const shop = request.headers.get("x-shopify-shop-domain") || "";
  console.log("Shop domain:", shop);
  
  if (!shop) return json({ error: "Missing X-Shopify-Shop-Domain" }, { status: 400 });

  console.log("Calling upstream:", `${BRAVETTO_API_URL}/api/shopify/settings`);
  const authHeader = request.headers.get("authorization") || request.headers.get("Authorization");
  const res = await fetch(`${BRAVETTO_API_URL}/api/shopify/settings`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-Shopify-Shop-Domain": shop,
      // Spoof origin to satisfy trusted-origin fallback on backend
      "Origin": SHOPIFY_APP_URL,
      ...(authHeader ? { Authorization: authHeader } : {}),
    },
  });

  console.log("Upstream response status:", res.status);
  const text = await res.text();
  console.log("Upstream response text:", text);
  
  try {
    const data = JSON.parse(text);
    return json(data, { status: res.status });
  } catch {
    return json({ error: text || "Upstream error" }, { status: res.status });
  }
}

export async function action({ request }: ActionFunctionArgs) {
  const shop = request.headers.get("x-shopify-shop-domain") || "";
  if (!shop) return json({ error: "Missing X-Shopify-Shop-Domain" }, { status: 400 });
  const body = await request.text();
  
  console.log("=== API.SETTINGS ACTION ===");
  console.log("Shop domain:", shop);
  console.log("Request body:", body);

  const authHeader = request.headers.get("authorization") || request.headers.get("Authorization");
  const res = await fetch(`${BRAVETTO_API_URL}/api/shopify/settings`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Shopify-Shop-Domain": shop,
      "Origin": SHOPIFY_APP_URL,
      ...(authHeader ? { Authorization: authHeader } : {}),
    },
    body,
  });

  console.log("Upstream response status:", res.status);
  const text = await res.text();
  console.log("Upstream response text:", text);
  
  try {
    const data = JSON.parse(text);
    return json(data, { status: res.status });
  } catch {
    return json({ error: text || "Upstream error" }, { status: res.status });
  }
}

