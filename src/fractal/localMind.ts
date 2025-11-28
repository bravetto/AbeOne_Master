/**
 * L-Mind: Local Mind (Edge Intelligence + Memory)
 * 
 * Pattern: LOCAL × INTELLIGENCE × MEMORY × ONE
 * Guardian: AEYON (999 Hz) - Atomic Execution
 */

export interface Hypervector {
  readonly id: string;
  readonly vector: Float32Array;
  readonly dimension: number;
  readonly metadata?: Record<string, unknown>;
  readonly timestamp: number;
}

export interface ResonancePattern {
  readonly patternId: string;
  readonly strength: number;
  readonly frequency: number;
  readonly hypervectors: string[];
  readonly timestamp: number;
}

export interface IntentState {
  readonly intentId: string;
  readonly content: string;
  readonly priority: number;
  readonly progress: number;
  readonly timestamp: number;
}

export class LocalHypervectorStore {
  private readonly dimension: number;
  private readonly capacity: number;
  private readonly vectors: Map<string, Hypervector>;

  constructor(dimension: number = 1024, capacity: number = 10000) {
    if (dimension <= 0 || !Number.isInteger(dimension)) {
      throw new Error(`Invalid dimension: ${dimension}`);
    }
    if (capacity <= 0 || !Number.isInteger(capacity)) {
      throw new Error(`Invalid capacity: ${capacity}`);
    }
    this.dimension = dimension;
    this.capacity = capacity;
    this.vectors = new Map();
  }

  encode(event: unknown): Hypervector {
    if (event === null || event === undefined) {
      throw new Error("Event cannot be null or undefined");
    }
    if (this.vectors.size >= this.capacity) {
      throw new Error(`Storage at capacity (${this.capacity})`);
    }

    const vector = this._generateVector(event);
    if (vector.length !== this.dimension) {
      throw new Error(`Vector dimension mismatch: ${vector.length} != ${this.dimension}`);
    }

    const normalized = this._normalize(vector);
    const hv: Hypervector = {
      id: this._generateId(),
      vector: normalized,
      dimension: this.dimension,
      metadata: this._extractMetadata(event),
      timestamp: Date.now()
    };

    this.vectors.set(hv.id, hv);
    return hv;
  }

  get(id: string): Hypervector | undefined {
    return this.vectors.get(id);
  }

  search(queryVector: Float32Array, topK: number = 10): Hypervector[] {
    if (!queryVector || queryVector.length !== this.dimension) {
      throw new Error(`Query vector dimension mismatch`);
    }
    const normalizedQuery = this._normalize(queryVector);
    const similarities: Array<{ hv: Hypervector; similarity: number }> = [];

    for (const hv of this.vectors.values()) {
      const similarity = this._cosineSimilarity(normalizedQuery, hv.vector);
      similarities.push({ hv, similarity });
    }

    similarities.sort((a, b) => b.similarity - a.similarity);
    return similarities.slice(0, topK).map(item => item.hv);
  }

  count(): number {
    return this.vectors.size;
  }

  private _generateVector(event: unknown): Float32Array {
    const eventStr = JSON.stringify(event);
    const vector = new Float32Array(this.dimension);
    for (let i = 0; i < this.dimension; i++) {
      const hash = this._hash(eventStr + i);
      vector[i] = (hash % 2000 - 1000) / 1000;
    }
    return vector;
  }

  private _normalize(vector: Float32Array): Float32Array {
    const magnitude = Math.sqrt(
      Array.from(vector).reduce((sum, val) => sum + val * val, 0)
    );
    if (magnitude === 0) {
      const unit = new Float32Array(vector.length);
      unit[0] = 1.0;
      return unit;
    }
    return new Float32Array(vector.map(val => val / magnitude));
  }

  private _cosineSimilarity(a: Float32Array, b: Float32Array): number {
    let dotProduct = 0;
    for (let i = 0; i < a.length; i++) {
      dotProduct += a[i] * b[i];
    }
    return dotProduct;
  }

  private _extractMetadata(event: unknown): Record<string, unknown> {
    if (typeof event === 'object' && event !== null) {
      const obj = event as Record<string, unknown>;
      const metadata: Record<string, unknown> = {};
      for (const [key, value] of Object.entries(obj)) {
        if (typeof value !== 'object' || value === null) {
          metadata[key] = value;
        }
      }
      return metadata;
    }
    return { type: typeof event, value: String(event) };
  }

  private _generateId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private _hash(str: string): number {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return Math.abs(hash);
  }
}

export class ResonanceEngine {
  private readonly patterns: Map<string, ResonancePattern>;
  private readonly resonanceThreshold: number = 0.7;

  constructor() {
    this.patterns = new Map();
  }

  observe(hypervector: Hypervector): void {
    if (!hypervector || !hypervector.id || !hypervector.vector) {
      throw new Error("Invalid hypervector");
    }

    const resonantPatterns = this._findResonantPatterns(hypervector);
    for (const pattern of resonantPatterns) {
      this._updatePattern(pattern.patternId, hypervector.id, pattern.strength);
    }

    if (resonantPatterns.length === 0) {
      this._createNewPattern(hypervector);
    }
  }

  express(intent: IntentState): Hypervector[] {
    if (!intent || !intent.intentId) {
      throw new Error("Invalid intent");
    }

    const resonantPatterns = Array.from(this.patterns.values())
      .filter(pattern => pattern.strength >= this.resonanceThreshold)
      .sort((a, b) => b.strength - a.strength);

    const result: Hypervector[] = [];
    for (const pattern of resonantPatterns.slice(0, 10)) {
      result.push({
        id: pattern.patternId,
        vector: new Float32Array(1024),
        dimension: 1024,
        metadata: { pattern: pattern.patternId, strength: pattern.strength },
        timestamp: pattern.timestamp
      });
    }

    return result;

  wantsGlobalSupport(hypervector: Hypervector): boolean {
    if (!hypervector || !hypervector.id) {
      return false;
    }

    // Check if hypervector resonates with patterns requiring global support
    const resonantPatterns = this._findResonantPatterns(hypervector);
    
    // Require global support if:
    // 1. Multiple strong resonant patterns (complexity)
    // 2. Pattern strength exceeds threshold significantly
    // 3. Frequency indicates global coordination needed
    const strongPatterns = resonantPatterns.filter(p => p.strength > 0.85);
    const needsGlobal = strongPatterns.length > 1 || 
                       resonantPatterns.some(p => p.strength > 0.9) || 
                       (hypervector.metadata && typeof hypervector.metadata.frequency === 'number' && hypervector.metadata.frequency >= 777);

    return needsGlobal;

  }

  private _findResonantPatterns(hypervector: Hypervector): Array<{ patternId: string; strength: number }> {
    const resonant: Array<{ patternId: string; strength: number }> = [];
    for (const [patternId, pattern] of this.patterns.entries()) {
      const strength = this._calculateResonance(hypervector, pattern);
      if (strength >= this.resonanceThreshold) {
        resonant.push({ patternId, strength });
      }
    }
    return resonant;
  }

  private _calculateResonance(hv: Hypervector, pattern: ResonancePattern): number {
    return Math.random() * 0.3 + 0.7;
  }

  private _updatePattern(patternId: string, vectorId: string, strength: number): void {
    const pattern = this.patterns.get(patternId);
    if (!pattern) return;

    const updatedPattern: ResonancePattern = {
      ...pattern,
      strength: Math.max(pattern.strength, strength),
      hypervectors: [...new Set([...pattern.hypervectors, vectorId])],
      timestamp: Date.now()
    };
    this.patterns.set(patternId, updatedPattern);
  }

  private _createNewPattern(hypervector: Hypervector): void {
    const patternId = `pattern-${hypervector.id}`;
    const pattern: ResonancePattern = {
      patternId,
      strength: 0.5,
      frequency: 530.0,
      hypervectors: [hypervector.id],
      timestamp: Date.now()
    };
    this.patterns.set(patternId, pattern);
  }
}

export class IntentState {
  private readonly intents: Map<string, IntentState>;
  private currentIntent: IntentState | null = null;

  constructor() {
    this.intents = new Map();
  }

  update(event: unknown): void {
    if (event === null || event === undefined) {
      return;
    }

    const intent = this._extractIntent(event);
    if (!intent) {
      return;
    }

    const existing = this.intents.get(intent.intentId);
    if (existing) {
      this._updateIntent(existing, intent);
    } else {
      this.intents.set(intent.intentId, intent);
    }

    this.currentIntent = intent;
  }

  getCurrentIntent(): IntentState | null {
    return this.currentIntent;
  }

  get state(): IntentState | null {
    return this.currentIntent;
  }

  getIntent(intentId: string): IntentState | undefined {
    return this.intents.get(intentId);
  }

  private _extractIntent(event: unknown): IntentState | null {
    if (typeof event === 'object' && event !== null) {
      const obj = event as Record<string, unknown>;
      if (obj.intent || obj.intentId || obj.goal) {
        return {
          intentId: String(obj.intentId || obj.intent || this._generateIntentId()),
          content: String(obj.intent || obj.goal || obj.content || ''),
          priority: typeof obj.priority === 'number' ? obj.priority : 0.5,
          progress: typeof obj.progress === 'number' ? obj.progress : 0.0,
          timestamp: Date.now()
        };
      }
    }
    return null;
  }

  private _updateIntent(existing: IntentState, update: IntentState): void {
    const updated: IntentState = {
      ...existing,
      content: update.content || existing.content,
      priority: Math.max(existing.priority, update.priority),
      progress: Math.max(existing.progress, update.progress),
      timestamp: Date.now()
    };
    this.intents.set(existing.intentId, updated);
  }

  private _generateIntentId(): string {
    return `intent-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}

export class LocalMind {
  public readonly hypervectors: LocalHypervectorStore;
  public readonly resonance: ResonanceEngine;
  public readonly intent: IntentState;

  constructor(dimension: number = 1024) {
    this.hypervectors = new LocalHypervectorStore(dimension);
    this.resonance = new ResonanceEngine();
    this.intent = new IntentState();
  }

  perceive(event: unknown): Hypervector {
    if (event === null || event === undefined) {
      throw new Error("Cannot perceive null or undefined event");
    }

    const hv = this.hypervectors.encode(event);
    this.resonance.observe(hv);
    this.intent.update(event);
    return hv;
  }

  act(intent: IntentState): Hypervector[] {
    if (!intent || !intent.intentId) {
      throw new Error("Invalid intent: missing intentId");
    }
    return this.resonance.express(intent);
  }
}

// Add wantsGlobalSupport method to ResonanceEngine class
// This will be inserted after the express method

// Note: This is a placeholder - the actual method should be added to the ResonanceEngine class
// For now, we'll add it via sed or manual edit

