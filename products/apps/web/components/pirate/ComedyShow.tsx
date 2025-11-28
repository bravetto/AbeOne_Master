'use client'

import { useState } from 'react'

export function ComedyShow() {
  const [ticketCount, setTicketCount] = useState(2) // Two drink minimum, remember?

  return (
    <section id="comedy" className="py-24 px-4 md:px-8 lg:px-24 bg-gradient-to-b from-purple-900 via-purple-800 to-indigo-900">
      <div className="max-w-6xl mx-auto text-center">
        <div className="mb-12">
          <h2 className="text-4xl md:text-6xl font-display font-bold text-white mb-4">
             Stand-Up Comedy Show 
          </h2>
          <p className="text-2xl md:text-3xl text-purple-200 mb-6">
            Where 20% of our customers discover us (and hopefully buy stuff)
          </p>
          <p className="text-lg text-purple-300 max-w-3xl mx-auto">
            Come for the laughs, stay for the merch. Or come for the merch, stay for the laughs. 
            Either way, you&apos;re buying tickets and tipping. Because duhhh.
          </p>
        </div>

        {/* Show Details */}
        <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 mb-12 border-2 border-purple-400/50">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div>
              <div className="text-4xl mb-2"></div>
              <h3 className="font-bold text-white text-xl mb-2">Every Week</h3>
              <p className="text-purple-200">Open mic night at the club</p>
            </div>
            <div>
              <div className="text-4xl mb-2"></div>
              <h3 className="font-bold text-white text-xl mb-2">Two Drink Minimum</h3>
              <p className="text-purple-200">Because we need to pay rent</p>
            </div>
            <div>
              <div className="text-4xl mb-2"></div>
              <h3 className="font-bold text-white text-xl mb-2">Tip Your Comedians</h3>
              <p className="text-purple-200">It&apos;s the pirate way</p>
            </div>
          </div>
        </div>

        {/* Ticket Purchase */}
        <div className="bg-white rounded-2xl p-8 shadow-2xl max-w-2xl mx-auto">
          <h3 className="text-3xl font-display font-bold text-purple-900 mb-6">
            Get Your Tickets
          </h3>
          
          <div className="space-y-6">
            <div className="flex items-center justify-between p-4 bg-purple-50 rounded-lg">
              <div>
                <p className="font-bold text-purple-900">Number of Tickets</p>
                <p className="text-sm text-purple-700">(Two drink minimum per person)</p>
              </div>
              <div className="flex items-center gap-4">
                <button
                  onClick={() => setTicketCount(Math.max(2, ticketCount - 1))}
                  className="w-10 h-10 rounded-full bg-purple-600 text-white font-bold hover:bg-purple-700 transition-colors"
                >
                  -
                </button>
                <span className="text-2xl font-bold text-purple-900 w-12 text-center">
                  {ticketCount}
                </span>
                <button
                  onClick={() => setTicketCount(ticketCount + 1)}
                  className="w-10 h-10 rounded-full bg-purple-600 text-white font-bold hover:bg-purple-700 transition-colors"
                >
                  +
                </button>
              </div>
            </div>

            <div className="border-t-2 border-purple-200 pt-6 space-y-3">
              <div className="flex justify-between text-lg">
                <span className="text-purple-700">Tickets ({ticketCount})</span>
                <span className="font-bold text-purple-900">${(ticketCount * 15).toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-lg">
                <span className="text-purple-700">Two Drink Minimum ({ticketCount} × $12)</span>
                <span className="font-bold text-purple-900">${(ticketCount * 12).toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-xl font-bold pt-3 border-t-2 border-purple-300">
                <span className="text-purple-900">Total</span>
                <span className="text-purple-900">${(ticketCount * 27).toFixed(2)}</span>
              </div>
            </div>

            <button className="w-full py-4 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200">
              Buy Tickets Now 
            </button>

            <p className="text-sm text-purple-600 text-center">
              * Tips for comedians not included (but highly encouraged)
            </p>
          </div>
        </div>

        {/* Why Come */}
        <div className="mt-12 text-left max-w-3xl mx-auto">
          <h4 className="text-2xl font-bold text-white mb-4">Why You Should Come:</h4>
          <ul className="space-y-2 text-purple-200">
            <li className="flex items-start gap-2">
              <span className="text-yellow-400"></span>
              <span>Laughs so hard you&apos;ll forget you&apos;re in Tampa</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-yellow-400"></span>
              <span>Drinks that&apos;ll make you forget you&apos;re in Tampa</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-yellow-400"></span>
              <span>Buy our merch and look cool (or at least cooler)</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-yellow-400"></span>
              <span>Support local comedy (we need it)</span>
            </li>
          </ul>
        </div>
      </div>
    </section>
  )
}

