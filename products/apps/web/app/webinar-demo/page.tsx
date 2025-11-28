'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

/**
 * Webinar Demo Page
 * 
 * Pattern: DEMO × WEBINAR × SEAMLESS × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Simple, beautiful UI to test webinar system RIGHT NOW.
 * NO RABBIT HOLES - Clear errors, clear success.
 */

interface Webinar {
  id: string
  topic: string
  scheduled_time: string
  zoom_join_url?: string
}

export default function WebinarDemoPage() {
  const [webinars, setWebinars] = useState<Webinar[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [testStatus, setTestStatus] = useState<any>(null)
  
  // Registration form
  const [webinarId, setWebinarId] = useState('')
  const [email, setEmail] = useState('')
  const [name, setName] = useState('')
  const [registering, setRegistering] = useState(false)

  // Load webinars
  useEffect(() => {
    loadWebinars()
    runTest()
  }, [])

  async function runTest() {
    try {
      const response = await fetch('/api/webinar/test')
      const data = await response.json()
      setTestStatus(data)
    } catch (error) {
      console.error('Test failed:', error)
    }
  }

  async function loadWebinars() {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch('/api/webinar/list?limit=10')
      const data = await response.json()
      
      if (data.success) {
        setWebinars(data.webinars || [])
      } else {
        setError(data.error || 'Failed to load webinars')
      }
    } catch (error: any) {
      setError(error.message || 'Failed to load webinars')
    } finally {
      setLoading(false)
    }
  }

  async function handleRegister(e: React.FormEvent) {
    e.preventDefault()
    setRegistering(true)
    setError(null)
    setSuccess(null)

    try {
      const response = await fetch('/api/webinar/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          webinarId,
          email,
          name
        })
      })

      const data = await response.json()

      if (data.success) {
        setSuccess(`✅ Successfully registered! Registration ID: ${data.registrationId}`)
        setWebinarId('')
        setEmail('')
        setName('')
        loadWebinars() // Refresh list
      } else {
        setError(data.error || 'Registration failed')
      }
    } catch (error: any) {
      setError(error.message || 'Registration failed')
    } finally {
      setRegistering(false)
    }
  }

  return (
    <div className="container mx-auto py-8 px-4 max-w-4xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">🎉 Webinar System Demo</h1>
        <p className="text-muted-foreground">
          Test the webinar system RIGHT NOW. No rabbit holes, just results.
        </p>
      </div>

      {/* System Test Status */}
      {testStatus && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>System Status</CardTitle>
            <CardDescription>Quick health check</CardDescription>
          </CardHeader>
          <CardContent>
            {testStatus.ready ? (
              <Alert className="border-green-500 bg-green-50">
                <AlertDescription className="text-green-800">
                  ✅ {testStatus.message}
                </AlertDescription>
              </Alert>
            ) : (
              <Alert className="border-red-500 bg-red-50">
                <AlertDescription className="text-red-800">
                  ❌ {testStatus.message}
                </AlertDescription>
              </Alert>
            )}
            {testStatus.nextSteps && testStatus.nextSteps.length > 0 && (
              <div className="mt-4">
                <p className="text-sm font-semibold mb-2">Next Steps:</p>
                <ul className="list-disc list-inside text-sm space-y-1">
                  {testStatus.nextSteps.map((step: string, i: number) => (
                    <li key={i}>{step}</li>
                  ))}
                </ul>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Registration Form */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Register for Webinar</CardTitle>
          <CardDescription>Test registration flow</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleRegister} className="space-y-4">
            <div>
              <label htmlFor="webinarId" className="block text-sm font-medium mb-2">
                Webinar ID
              </label>
              <input
                id="webinarId"
                type="text"
                value={webinarId}
                onChange={(e) => setWebinarId(e.target.value)}
                placeholder="webinar_123"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label htmlFor="email" className="block text-sm font-medium mb-2">
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="user@example.com"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label htmlFor="name" className="block text-sm font-medium mb-2">
                Name
              </label>
              <input
                id="name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Your Name"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <Button type="submit" disabled={registering} className="w-full">
              {registering ? 'Registering...' : 'Register'}
            </Button>
          </form>

          {error && (
            <Alert className="mt-4 border-red-500 bg-red-50">
              <AlertDescription className="text-red-800">{error}</AlertDescription>
            </Alert>
          )}

          {success && (
            <Alert className="mt-4 border-green-500 bg-green-50">
              <AlertDescription className="text-green-800">{success}</AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Webinars List */}
      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle>Available Webinars</CardTitle>
              <CardDescription>All webinars in the system</CardDescription>
            </div>
            <Button onClick={loadWebinars} variant="outline" size="sm">
              Refresh
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {loading ? (
            <p className="text-muted-foreground">Loading webinars...</p>
          ) : webinars.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-muted-foreground mb-4">No webinars found</p>
              <p className="text-sm text-muted-foreground">
                Create one: <code className="bg-muted px-2 py-1 rounded">python3 scripts/webinar/master_orchestrator.py --create --topic "Test"</code>
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {webinars.map((webinar) => (
                <Card key={webinar.id} className="border">
                  <CardContent className="pt-6">
                    <h3 className="font-semibold text-lg mb-2">{webinar.topic || 'Untitled Webinar'}</h3>
                    <p className="text-sm text-muted-foreground mb-2">
                      <strong>ID:</strong> {webinar.id}
                    </p>
                    {webinar.scheduled_time && (
                      <p className="text-sm text-muted-foreground mb-2">
                        <strong>Scheduled:</strong> {new Date(webinar.scheduled_time).toLocaleString()}
                      </p>
                    )}
                    {webinar.zoom_join_url && (
                      <a
                        href={webinar.zoom_join_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline text-sm"
                      >
                        Join Zoom Meeting →
                      </a>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

