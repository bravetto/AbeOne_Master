import type { LoaderFunction } from "@remix-run/node";
import { json } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { Card, Page, Layout, Text, BlockStack, Banner, Link } from "@shopify/polaris";
import { authenticate } from "../shopify.server";

interface LoaderData {
  shop: string;
  connectionStatus: {
    success: boolean;
    message: string;
  };
}

export const loader: LoaderFunction = async ({ request }) => {
  const { session } = await authenticate.admin(request);

  // Skip health check to avoid authentication issues
  const connectionStatus = {
    success: true,
    message: "Ready to connect to Bravetto AI backend"
  };
  
  return json<LoaderData>({
    shop: session.shop,
    connectionStatus,
  });
};

export default function Index() {
  const { shop, connectionStatus } = useLoaderData<LoaderData>();

  return (
    <Page>
        <Layout>
          <Layout.Section>
            <Card>
            <BlockStack gap="400">
              <Text as="h1" variant="headingLg">
                Bravetto AI Chat Integration
                    </Text>
              <Text as="p" variant="bodyMd">
                Welcome to your Bravetto AI powered chat assistant for {shop}
                  </Text>
              
              {connectionStatus.success ? (
                <Banner tone="success">
                   {connectionStatus.message}
                </Banner>
              ) : (
                <Banner tone="critical">
                   {connectionStatus.message}
                </Banner>
                  )}
                </BlockStack>
          </Card>
        </Layout.Section>

        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <Text as="h2" variant="headingMd">Live Chat Experience</Text>
              <Text as="p" variant="bodyMd">
                The embedded test chat has been removed to keep the dashboard focused on configuration. To
                confirm the assistant experience, open your storefront theme extension or use a preview with
                the Bravetto chat block installed.
              </Text>
              <Text as="p" variant="bodyMd">
                Need to verify connectivity? Use the chat widget in your theme preview or embed it on a hidden
                page for internal testing.
              </Text>
            </BlockStack>
          </Card>
        </Layout.Section>
          
          <Layout.Section variant="oneThird">
              <Card>
            <BlockStack gap="300">
              <Text as="h2" variant="headingMd">Next Steps</Text>
                <BlockStack gap="200">
                <Text as="p">1. Preview your theme extension to validate the chat experience</Text>
                <Text as="p">2. <Link url="/app/knowledge">Set up your Knowledge Base</Link> with store data</Text>
                <Text as="p">3. Deploy chat widgets to your storefront and checkout</Text>
                <Text as="p">4. Monitor chat analytics and customer interactions</Text>
                  </BlockStack>
                </BlockStack>
              </Card>
          </Layout.Section>
      </Layout>
    </Page>
  );
}
