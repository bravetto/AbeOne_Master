import { useEffect, useState, useCallback } from "react";
import { json, type LoaderFunction, type ActionFunction } from "@remix-run/node";
import { useLoaderData, useFetcher } from "@remix-run/react";
import { authenticate } from "../shopify.server";
import {
  Page,
  Layout,
  Card,
  BlockStack,
  Text,
  TextField,
  Button,
  Banner,
  Divider,
} from "@shopify/polaris";

interface LoaderData {
  shop: string;
  apiUrl: string;
  isConnected: boolean;
  connectionDetails?: {
    shopName: string;
    orgId: string;
    systemPromptId?: string;
  };
}

// Prompt selection is managed in Bravetto AI dashboard; no local options here.

export const loader: LoaderFunction = async ({ request }) => {
  const { session } = await authenticate.admin(request);
  const apiUrl = process.env.BRAVETTO_API_URL || "https://www.bravetto.ai";
  
  // Check if already connected
  let isConnected = false;
  let connectionDetails = undefined;
  
  try {
    const settingsRes = await fetch(`${apiUrl}/api/shopify/settings`, {
      method: "GET",
              headers: {
          "Content-Type": "application/json",
          "X-Shopify-Shop-Domain": session.shop,
          ...(process.env.SHOPIFY_APP_URL ? { "Origin": process.env.SHOPIFY_APP_URL } : {}),
        },
    });
    
    if (settingsRes.ok) {
      const data = await settingsRes.json();
      if (data.orgId) {
        isConnected = true;
        connectionDetails = {
          shopName: session.shop,
          orgId: data.orgId,
          systemPromptId: data.systemPromptId,
        };
      }
    }
  } catch (error) {
    // Ignore connection check errors
  }
  
  return json<LoaderData>({ 
    shop: session.shop, 
    apiUrl,
    isConnected,
    connectionDetails,
  });
};

export const action: ActionFunction = async ({ request }) => {
  const { session } = await authenticate.admin(request);
  const formData = await request.formData();
  const actionType = formData.get("actionType");
  
  const apiUrl = process.env.BRAVETTO_API_URL || "https://www.bravetto.ai";
  const shopifyAppUrl = process.env.SHOPIFY_APP_URL || "https://shopify-ai-app.vercel.app";

  // Ensure we have a valid Shopify shop in session
  if (!session || !session.shop) {
    return json({ error: "Missing Shopify session. Please reload the app or reauthorize." }, { status: 401 });
  }
  
  if (actionType === "connect") {
    const rawApiKey = formData.get("apiKey");
    const apiKey = typeof rawApiKey === "string" ? rawApiKey.trim() : "";
    
    if (!apiKey) {
      return json({ error: "API key is required." }, { status: 400 });
    }
    
    try {
      // Validate API key with bravetto.ai
      const authRes = await fetch(`${apiUrl}/api/shopify/auth`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          apiKey,
          shopDomain: session.shop,
        }),
      });

      // Parse response safely
      const authContentType = authRes.headers.get("content-type") || "";
      let authBody: any = null;
      if (authContentType.includes("application/json")) {
        try {
          authBody = await authRes.json();
        } catch {
          authBody = null;
        }
      } else {
        const text = await authRes.text();
        authBody = { error: text };
      }

      if (!authRes.ok) {
        const message = (authBody && authBody.error) || `Authentication failed (HTTP ${authRes.status})`;
        return json({ error: message }, { status: 401 });
      }

      if (!authContentType.includes("application/json") || !authBody) {
        return json({ error: "Unexpected response from Bravetto API during authentication." }, { status: 502 });
      }

      const authData = authBody;
      
      // Save connection in bravetto.ai
      const res = await fetch(`${apiUrl}/api/shopify/settings`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Shopify-Shop-Domain": session.shop,
          ...(shopifyAppUrl ? { "Origin": shopifyAppUrl } : {}),
        },
        body: JSON.stringify({
          systemPromptId: authData.integration?.systemPromptId || "",
          orgId: authData.integration?.orgId,
          apiKey: apiKey,
          accessToken: session.accessToken,
        }),
      });

      const settingsContentType = res.headers.get("content-type") || "";
      let settingsBody: any = null;
      if (settingsContentType.includes("application/json")) {
        try {
          settingsBody = await res.json();
        } catch {
          settingsBody = null;
        }
      } else {
        const txt = await res.text();
        settingsBody = { error: txt };
      }

      if (!res.ok) {
        const message = (settingsBody && settingsBody.error) || `Connection failed (HTTP ${res.status})`;
        return json({ error: message }, { status: res.status });
      }
      
      return json({ 
        success: true, 
        message: "Successfully connected to Bravetto AI!",
        orgId: authData.integration?.orgId,
      });
    } catch (error: any) {
      console.error("Error connecting to Bravetto AI:", error);
      return json({ error: "Unable to connect. Please try again." }, { status: 500 });
    }
  } else if (actionType === "updatePrompt") {
    const rawSystemPromptId = formData.get("systemPromptId");
    const rawOrgId = formData.get("orgId");
    const systemPromptId = typeof rawSystemPromptId === "string" ? rawSystemPromptId.trim() : "";
    const orgId = typeof rawOrgId === "string" ? rawOrgId.trim() : "";
    
    if (!systemPromptId || !orgId) {
      return json({ error: "Both organization ID and system prompt ID are required." }, { status: 400 });
    }
    
    try {
      const res = await fetch(`${apiUrl}/api/shopify/settings`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Shopify-Shop-Domain": session.shop,
          ...(shopifyAppUrl ? { "Origin": shopifyAppUrl } : {}),
        },
        body: JSON.stringify({
          systemPromptId,
          orgId,
          accessToken: session.accessToken,
        }),
      });

      const settingsContentType = res.headers.get("content-type") || "";
      let settingsBody: any = null;
      if (settingsContentType.includes("application/json")) {
        try {
          settingsBody = await res.json();
        } catch {
          settingsBody = null;
        }
      } else {
        const txt = await res.text();
        settingsBody = { error: txt };
      }

      if (!res.ok) {
        const message = (settingsBody && settingsBody.error) || "Save failed";
        return json({ error: message }, { status: res.status });
      }

      return json({ success: true, message: "System prompt updated successfully." });
    } catch (error: any) {
      console.error("Error updating prompt:", error);
      return json({ error: "Unable to update prompt. Please try again." }, { status: 500 });
    }
  }
  
  return json({ error: "Invalid action type" }, { status: 400 });
};

export default function SettingsPage() {
  const { shop, apiUrl, isConnected, connectionDetails } = useLoaderData<LoaderData>();
  const fetcher = useFetcher();
  const [apiKey, setApiKey] = useState("");
  // Prompt selection is read-only in Shopify UI
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  // No prompt list or loading state needed

  // No prompt fetching; prompt is managed in Bravetto AI dashboard.

  // Handle fetcher updates
  useEffect(() => {
    if (fetcher.state === "idle" && fetcher.data) {
      const data = fetcher.data as any;
      if (data.success) {
        setMessage(data.message);
        setError(null);
        if (data.orgId) {
          // Reload the page to update connection status
          window.location.reload();
        }
      } else if (data.error) {
        setError(data.error);
        setMessage(null);
      }
    }
  }, [fetcher.state, fetcher.data]);

  const handleConnect = useCallback(() => {
    setMessage(null);
    setError(null);
    
    const formData = new FormData();
    formData.append("actionType", "connect");
    formData.append("apiKey", apiKey.trim());
    
    fetcher.submit(formData, { method: "POST" });
  }, [apiKey, fetcher]);

  // No update handler; prompt updates occur in Bravetto AI dashboard

  return (
    <Page>
      <Layout>
        <Layout.Section>
          {!isConnected ? (
            <Card>
              <BlockStack gap="400">
                <Text as="h1" variant="headingLg">Connect to Bravetto AI</Text>
                <Text as="p" variant="bodyMd">Shop: {shop}</Text>
                {message && <Banner tone="success">{message}</Banner>}
                {error && <Banner tone="critical">{error}</Banner>}
                
                <Text as="p" variant="bodyMd">
                  To connect your Shopify store to Bravetto AI, you'll need an API key.
                </Text>
                
                <Text as="h2" variant="headingMd">How to get your API key:</Text>
                <BlockStack gap="200">
                  <Text as="p" variant="bodyMd">
                    1. Log in to your Bravetto AI account at {apiUrl}
                  </Text>
                  <Text as="p" variant="bodyMd">
                    2. Navigate to your team/organization page
                  </Text>
                  <Text as="p" variant="bodyMd">
                    3. Go to Integrations → Shopify
                  </Text>
                  <Text as="p" variant="bodyMd">
                    4. Click "Add Shopify Store" and enter your store details
                  </Text>
                  <Text as="p" variant="bodyMd">
                    5. Copy the generated API key
                  </Text>
                </BlockStack>
                
                <Divider />
                
                <TextField
                  label="Bravetto AI API Key"
                  value={apiKey}
                  onChange={setApiKey}
                  helpText="Enter the API key from your Bravetto AI account"
                  autoComplete="off"
                  placeholder="sk_shopify_..."
                  monospaced
                />
                
                <Button 
                  variant="primary" 
                  onClick={handleConnect} 
                  loading={fetcher.state !== "idle"} 
                  disabled={fetcher.state !== "idle" || !apiKey.trim()}
                >
                  Connect to Bravetto AI
                </Button>
              </BlockStack>
            </Card>
          ) : (
            <BlockStack gap="400">
              <Card>
                <BlockStack gap="400">
                  <Text as="h1" variant="headingLg">Bravetto AI Connection</Text>
                  <Text as="p" variant="bodyMd">Shop: {shop}</Text>
                  <Banner tone="success">
                    Connected to Bravetto AI organization: <strong>{connectionDetails?.orgId}</strong>
                  </Banner>
                  {message && <Banner tone="success">{message}</Banner>}
                  {error && <Banner tone="critical">{error}</Banner>}
                </BlockStack>
              </Card>
              
              <Card>
                <BlockStack gap="400">
                  <Text as="h2" variant="headingMd">AI System Prompt</Text>
                  <Text as="p" variant="bodyMd">
                    Configure how the AI assistant responds to customers in your store.
                  </Text>
                  
                  {/* Current Status Banner */}
                  {connectionDetails?.systemPromptId ? (
                    <Banner tone="success">
                      <Text as="p" variant="bodyMd">
                        <strong>✅ Active Prompt:</strong> A custom system prompt is currently assigned to this store (ID: {connectionDetails.systemPromptId.substring(0, 8)}...).
                        Your AI assistant is using this custom prompt for all customer interactions.
                      </Text>
                    </Banner>
                  ) : (
                    <Banner tone="warning">
                      <Text as="p" variant="bodyMd">
                        <strong>⚠️ No Custom Prompt:</strong> This store is using the default Shopify guidelines only. 
                        Set a custom prompt in your Bravetto AI dashboard for better, more personalized customer interactions.
                      </Text>
                    </Banner>
                  )}
                  
                  <Text as="p" variant="bodyMd">
                    <strong>Selected Prompt (read-only):</strong> {connectionDetails?.systemPromptId ? (
                      <code>{connectionDetails.systemPromptId}</code>
                    ) : (
                      <em>None</em>
                    )}
                  </Text>
                  
                  <Banner tone="info">
                    <Text as="p" variant="bodyMd">
                      <strong>Manage prompts:</strong> Visit your{' '}
                      <a href={`${apiUrl}/team/${connectionDetails?.orgId}/studio/prompts`} target="_blank" rel="noopener noreferrer" style={{textDecoration: 'underline'}}>
                        Bravetto AI dashboard
                      </a>{' '}
                      to create, edit, or delete system prompts for your organization.
                    </Text>
                  </Banner>
                </BlockStack>
              </Card>
              
              <Card>
                <BlockStack gap="400">
                  <Text as="h2" variant="headingMd">Next Steps</Text>
                  <Text as="p" variant="bodyMd">
                    1. Set your default system prompt in the Bravetto AI dashboard
                  </Text>
                  <Text as="p" variant="bodyMd">
                    2. Enable the Bravetto AI chat widget in your store's theme editor
                  </Text>
                  <Text as="p" variant="bodyMd">
                    3. Test the chat widget on your storefront - it will automatically use the prompt set in your Bravetto AI dashboard
                  </Text>
                  <Text as="p" variant="bodyMd">
                    4. Monitor chat conversations and improve prompts in your Bravetto AI dashboard
                  </Text>
                </BlockStack>
              </Card>
            </BlockStack>
          )}
        </Layout.Section>
      </Layout>
    </Page>
  );
}


