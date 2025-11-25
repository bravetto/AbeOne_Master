import { useState, useCallback } from "react";
import type { LoaderFunction, ActionFunction } from "@remix-run/node";
import { json } from "@remix-run/node";
import { useLoaderData, useActionData, Form, useNavigation } from "@remix-run/react";
import {
  Card,
  Page,
  Layout,
  Text,
  BlockStack,
  Button,
  Banner,
  InlineStack,
  Checkbox,
  TextField,
  Spinner,
  Badge,
  List,
} from "@shopify/polaris";
import { TitleBar } from "@shopify/app-bridge-react";
import { authenticate } from "../shopify.server";
import { KnowledgeSeeder } from "../lib/seed-knowledge";
import type { SeedKnowledgeConfig } from "../lib/seed-knowledge";

interface LoaderData {
  shop: string;
}

interface ActionData {
  success?: boolean;
  message?: string;
  error?: string;
  result?: {
    documentsProcessed?: number;
    summary?: {
      sources: Record<string, number>;
      types: Record<string, number>;
    };
  };
}

export const loader: LoaderFunction = async ({ request }) => {
  const { session } = await authenticate.admin(request);
  
  return json<LoaderData>({
    shop: session.shop,
  });
};

export const action: ActionFunction = async ({ request }) => {
  const { session } = await authenticate.admin(request);
  const formData = await request.formData();
  
  const intent = formData.get("intent");
  
  if (intent === "seed") {
    try {
      const bravettoConfig = {
        apiUrl: process.env.BRAVETTO_API_URL || 'https://www.bravetto.ai',
        defaultSystemPromptId: process.env.DEFAULT_SYSTEM_PROMPT_ID || '',
        defaultOrgId: process.env.DEFAULT_ORG_ID || 'shopify_integration',
      };
      
      const seeder = new KnowledgeSeeder(bravettoConfig);
      
      const resourceTypes = JSON.parse(formData.get("resourceTypes") as string || '["products"]');
      const includeWebCrawl = formData.get("includeWebCrawl") === "true";
      const webCrawlUrl = formData.get("webCrawlUrl") as string;
      const maxPages = parseInt(formData.get("maxPages") as string || "10");
      
                   // Get the Admin API access token from the session
      const adminAccessToken = session.accessToken;
      
      if (!adminAccessToken) {
        throw new Error('No access token available in session');
      }
      
      const seedConfig: SeedKnowledgeConfig = {
         shopDomain: session.shop,
         accessToken: adminAccessToken,
         resourceTypes,
         includeWebCrawl,
         webCrawlUrl: includeWebCrawl ? webCrawlUrl : undefined,
         maxPages,
         chunkSize: 1000,
         chunkOverlap: 200,
         namespace: session.shop.replace('.myshopify.com', ''),
       };
      
      const result = await seeder.seedShopifyData(seedConfig);
      
      // Enhanced result validation
      let enhancedMessage = result.message;
      if (result.success && result.documentsProcessed === 0) {
        enhancedMessage = 'Warning: No documents were processed. Check that your store has the selected content types and verify app permissions.';
      } else if (result.success) {
        enhancedMessage = `Successfully processed ${result.documentsProcessed} documents into your knowledge base.`;
      }
      
      return json<ActionData>({
        success: result.success,
        message: enhancedMessage,
        error: result.error,
        result: {
          documentsProcessed: result.documentsProcessed,
          summary: result.summary,
        },
      });
    } catch (error) {
      return json<ActionData>({
        success: false,
        error: error instanceof Error ? error.message : "Unknown error occurred",
      });
    }
  }
  
  return json<ActionData>({ error: "Invalid action" });
};

export default function KnowledgePage() {
  const { shop } = useLoaderData<LoaderData>();
  const actionData = useActionData<ActionData>();
  const navigation = useNavigation();
  const isSeeding = navigation.formData?.get("intent") === "seed";
  
  const [resourceTypes, setResourceTypes] = useState({
    products: true,
    collections: true,
    pages: true,
    articles: true,
  });
  
  const [includeWebCrawl, setIncludeWebCrawl] = useState(false);
  const [webCrawlUrl, setWebCrawlUrl] = useState(`https://${shop}`);
  const [maxPages, setMaxPages] = useState("25");
  
  const handleResourceTypeChange = useCallback((key: string, value: boolean) => {
    setResourceTypes(prev => ({ ...prev, [key]: value }));
  }, []);
  
  const selectedResourceTypes = Object.entries(resourceTypes)
    .filter(([_, selected]) => selected)
    .map(([type, _]) => type);
  
  return (
    <Page>
      <TitleBar title="Knowledge Base Management" />
      <Layout>
        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <Text as="h1" variant="headingLg">
                AI Knowledge Base for {shop}
              </Text>
              <Text as="p" variant="bodyMd">
                Seed your store's data into the AI knowledge base to provide better customer support. 
                This will crawl your products, pages, and other content to train the AI assistant.
              </Text>
              
              {actionData?.success && (
                <Banner tone="success">
                  ✅ Knowledge base updated successfully!
                  Processed {actionData.result?.documentsProcessed} items.
                </Banner>
              )}
              
              {actionData?.error && (
                <Banner tone="critical">
                  ❌ Error: {actionData.error}
                </Banner>
              )}
            </BlockStack>
          </Card>
        </Layout.Section>
        
        <Layout.Section>
          <Card>
            <Form method="post">
              <input type="hidden" name="intent" value="seed" />
              <input type="hidden" name="resourceTypes" value={JSON.stringify(selectedResourceTypes)} />
              <input type="hidden" name="includeWebCrawl" value={includeWebCrawl.toString()} />
              <input type="hidden" name="webCrawlUrl" value={webCrawlUrl} />
              <input type="hidden" name="maxPages" value={maxPages} />
              
              <BlockStack gap="400">
                <Text as="h2" variant="headingMd">
                  Configure Knowledge Sources
                </Text>
                
                <BlockStack gap="300">
                  <Text as="h3" variant="headingSm">
                    Shopify Data to Include:
                  </Text>
                  <BlockStack gap="200">
                    {Object.entries(resourceTypes).map(([type, selected]) => (
                      <Checkbox
                        key={type}
                        label={`${type.charAt(0).toUpperCase() + type.slice(1)}`}
                        checked={selected}
                        onChange={(value) => handleResourceTypeChange(type, value)}
                      />
                    ))}
                  </BlockStack>
                </BlockStack>
                
                <BlockStack gap="300">
                  <Checkbox
                    label="Include website crawling"
                    checked={includeWebCrawl}
                    onChange={setIncludeWebCrawl}
                    helpText="Crawl your public website for additional content"
                  />
                  
                  {includeWebCrawl && (
                    <BlockStack gap="200">
                                             <TextField
                         label="Website URL to crawl"
                         value={webCrawlUrl}
                         onChange={setWebCrawlUrl}
                         placeholder="https://your-store.com"
                         autoComplete="url"
                       />
                       <TextField
                         label="Max pages to crawl"
                         type="number"
                         value={maxPages}
                         onChange={setMaxPages}
                         helpText="Higher numbers take longer but capture more content"
                         autoComplete="off"
                       />
                    </BlockStack>
                  )}
                </BlockStack>
                
                <InlineStack gap="200">
                  <Button
                    variant="primary"
                    submit
                    loading={isSeeding}
                    disabled={selectedResourceTypes.length === 0}
                  >
                    {isSeeding ? 'Seeding Knowledge Base...' : 'Update Knowledge Base'}
                  </Button>
                  
                  {isSeeding && (
                    <InlineStack gap="200" align="center">
                      <Spinner size="small" />
                      <Text as="span" variant="bodySm" tone="subdued">
                        This may take a few minutes...
                      </Text>
                    </InlineStack>
                  )}
                </InlineStack>
              </BlockStack>
            </Form>
          </Card>
        </Layout.Section>
        
        {actionData?.result?.summary && (
          <Layout.Section>
            <Card>
              <BlockStack gap="300">
                <Text as="h2" variant="headingMd">
                  Last Seeding Results
                </Text>
                
                <BlockStack gap="200">
                  <Text as="h3" variant="headingSm">Sources:</Text>
                  <List>
                                         {Object.entries(actionData.result.summary.sources).map(([source, count]) => (
                       <List.Item key={source}>
                         <InlineStack gap="200" align="space-between">
                           <Text as="span">{source}</Text>
                           <Badge>{`${count} items`}</Badge>
                         </InlineStack>
                       </List.Item>
                     ))}
                   </List>
                   
                   <Text as="h3" variant="headingSm">Content Types:</Text>
                   <List>
                     {Object.entries(actionData.result.summary.types).map(([type, count]) => (
                       <List.Item key={type}>
                         <InlineStack gap="200" align="space-between">
                           <Text as="span">{type}</Text>
                           <Badge>{`${count} items`}</Badge>
                         </InlineStack>
                       </List.Item>
                     ))}
                  </List>
                </BlockStack>
              </BlockStack>
            </Card>
          </Layout.Section>
        )}
        
        <Layout.Section variant="oneThird">
          <Card>
            <BlockStack gap="300">
              <Text as="h2" variant="headingMd">
                Knowledge Base Tips
              </Text>
              <List>
                <List.Item>Include products for better product recommendations</List.Item>
                <List.Item>Add pages for FAQ and policy information</List.Item>
                <List.Item>Enable web crawling to capture blog posts and guides</List.Item>
                <List.Item>Re-run seeding when you add new products or content</List.Item>
              </List>
            </BlockStack>
          </Card>
        </Layout.Section>
      </Layout>
    </Page>
  );
} 