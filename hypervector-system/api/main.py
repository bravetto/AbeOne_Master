"""
HyperVector API Main

FastAPI application entry point.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import vectors, health
from .routes.vectors import set_storage
from ..src.hypervector.storage import HyperVectorStorage

# Initialize FastAPI app
app = FastAPI(
    title="HyperVector API",
    description="REST API for 10K hyperdimensional vector storage",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(vectors.router)

# Initialize storage
storage = HyperVectorStorage(
    dimension=int(os.getenv("VECTOR_DIMENSION", "1024")),
    capacity=int(os.getenv("VECTOR_CAPACITY", "10000")),
    storage_path=os.getenv("STORAGE_PATH", ".hypervector")
)

# Set storage instance for routes
set_storage(storage)


@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    print(" HyperVector API starting up...")
    print(f" Storage initialized: {storage.count()} vectors")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    print(" HyperVector API shutting down...")

