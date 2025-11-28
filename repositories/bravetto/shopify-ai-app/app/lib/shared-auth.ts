import { createHmac, createHash, timingSafeEqual } from "crypto";
import { config } from "./config";

export function validateStorefrontShopDomain(shopDomain: string): boolean {
  return /^[a-zA-Z0-9-]+\.myshopify\.com$/.test(shopDomain);
}

export function validateShopifyProxySignature(url: URL): boolean {
  const secret = config.shopify.apiSecret;
  if (!secret) return false;

  const rawQuery = url.search.startsWith('?') ? url.search.slice(1) : url.search;
  if (!rawQuery) return false;

  const pairs = rawQuery
    .split('&')
    .filter(Boolean)
    .map((kv) => {
      const eqIdx = kv.indexOf('=');
      if (eqIdx === -1) return { key: kv, value: '' };
      return { key: kv.slice(0, eqIdx), value: kv.slice(eqIdx + 1) };
    });

  const hmacParam = pairs.find((p) => p.key === 'hmac');
  const signatureParam = pairs.find((p) => p.key === 'signature');

  const canonical = pairs
    .filter((p) => p.key !== 'hmac' && p.key !== 'signature')
    .sort((a, b) => a.key.localeCompare(b.key))
    .map((p) => `${p.key}=${p.value}`)
    .join('&');

  // If an HMAC is present, validate strictly with HMAC-SHA256 and do NOT fall back
  if (hmacParam) {
    // Reject empty HMAC to prevent downgrade
    if (!hmacParam.value) return false;
    const computedHmacHex = createHmac('sha256', secret).update(canonical).digest('hex');
    try {
      const expected = Buffer.from(computedHmacHex, 'hex');
      const actual = Buffer.from(hmacParam.value, 'hex');
      return expected.length > 0 && expected.length === actual.length && timingSafeEqual(expected, actual);
    } catch {
      return false;
    }
  }

  // Otherwise, optionally support legacy 'signature' parameter via MD5 (DISABLED by default)
  if (signatureParam && signatureParam.value) {
    if (process.env.ALLOW_LEGACY_APP_PROXY_MD5 !== 'true') {
      // Block legacy MD5 unless explicitly allowed
      return false;
    }
    // Use a single canonical construction to reduce ambiguity: secret + canonical
    const md5Hex = createHash('md5').update(`${secret}${canonical}`).digest('hex');
    try {
      const expected = Buffer.from(md5Hex, 'hex');
      const actual = Buffer.from(signatureParam.value, 'hex');
      return expected.length > 0 && expected.length === actual.length && timingSafeEqual(expected, actual);
    } catch {
      return false;
    }
  }

  return false;
}

export function isFresh(url: URL, maxSkewSec = 300): boolean {
  const tsStr = url.searchParams.get("timestamp") || "";
  const ts = Number(tsStr);
  if (!Number.isFinite(ts)) return false;
  const now = Math.floor(Date.now() / 1000);
  return Math.abs(now - ts) <= maxSkewSec;
}

export async function mintInternalServiceJWT(shopDomain: string): Promise<string | null> {
  try {
    const secret = process.env.INTERNAL_JWT_SECRET;
    if (!secret) return null;
    const { SignJWT } = await import("jose");
    const now = Math.floor(Date.now() / 1000);
    return await new SignJWT({ shopDomain })
      .setProtectedHeader({ alg: "HS256", typ: "JWT" })
      .setIssuer("shopify-ai-app")
      .setAudience("bravetto-ai")
      .setIssuedAt(now)
      .setExpirationTime(now + 60)
      .setJti(`${now}-${Math.random().toString(36).slice(2)}`)
      .sign(new TextEncoder().encode(secret));
  } catch (e) {
    console.error('Failed to mint internal JWT', e);
    return null;
  }
}


