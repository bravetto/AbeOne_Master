import type { LoaderFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";

const BRAVETTO_API_URL = process.env.BRAVETTO_API_URL || "https://www.bravetto.ai";
const SHOPIFY_APP_URL = process.env.SHOPIFY_APP_URL || "https://shopify-ai-app.vercel.app";

export async function loader({ request }: LoaderFunctionArgs) {
  console.log("=== API.PROMPTS LOADER ===");
  const url = new URL(request.url);
  const orgId = url.searchParams.get("orgId");
  const shop = request.headers.get("x-shopify-shop-domain") || "";
  
  console.log("OrgId:", orgId);
  console.log("Shop domain:", shop);
  
  if (!orgId) return json({ error: "Missing orgId" }, { status: 400 });
  if (!shop) return json({ error: "Missing X-Shopify-Shop-Domain" }, { status: 400 });

  console.log("Calling upstream:", `${BRAVETTO_API_URL}/api/shopify/prompts?orgId=${encodeURIComponent(orgId)}`);
  const authHeader = request.headers.get("authorization") || request.headers.get("Authorization");
  const res = await fetch(`${BRAVETTO_API_URL}/api/shopify/prompts?orgId=${encodeURIComponent(orgId)}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-Shopify-Shop-Domain": shop,
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
