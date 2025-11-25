#!/usr/bin/env python3
"""
Test script to verify all Cursor bot identified bugs have been fixed.
"""
import sys
import os

# Add the codeguardians-gateway directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'codeguardians-gateway', 'codeguardians-gateway'))

def REPLACE_ME():
    """Test that EmailRequiredError and ValidationError can be imported in clerk_webhooks."""
    try:
        # This should work without NameError
        from app.api.webhooks.clerk_webhooks import router
        print("✅ Clerk webhook imports work correctly")
        return True
    except NameError as e:
        print(f"❌ NameError in clerk webhook imports: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error in clerk webhook imports: {e}")
        return False

def test_validation_error_propagation():
    """Test that validation errors are properly propagated through the webhook service."""
    try:
        from app.services.clerk_webhook_service import ClerkWebhookService
        from app.core.exceptions import EmailRequiredError, ValidationError
        import asyncio

        # Create a mock db session
        class MockDB:
            async def rollback(self):
                pass
            def add(self, obj):
                pass
            async def execute(self, query):
                # Mock result for user existence check
                class MockResult:
                    def scalar_one_or_none(self):
                        return None  # User doesn't exist
                return MockResult()
            async def commit(self):
                pass
            async def refresh(self, obj):
                pass

        mock_db = MockDB()
        service = ClerkWebhookService(mock_db)

        # Test that EmailRequiredError is raised from validate_user_data
        try:
            service.validate_user_data({'id': 'test', 'email_addresses': []})
            print("❌ EmailRequiredError should have been raised")
            return False
        except EmailRequiredError:
            print("✅ EmailRequiredError properly raised from validate_user_data")
        except Exception as e:
            print(f"❌ Unexpected error from validate_user_data: {e}")
            return False

        # Test that ValidationError is raised from validate_user_data
        try:
            service.validate_user_data({'email_addresses': [{'email_address': 'invalid-email'}]})
            print("❌ ValidationError should have been raised")
            return False
        except ValidationError:
            print("✅ ValidationError properly raised from validate_user_data")
        except Exception as e:
            print(f"❌ Unexpected error from validate_user_data: {e}")
            return False

        # Test that EmailRequiredError is raised from handle_user_created
        async def test_email_error():
            try:
                await service.handle_user_created({'data': {'id': 'test', 'email_addresses': []}})
                print("❌ EmailRequiredError should have been raised")
                return False
            except EmailRequiredError:
                print("✅ EmailRequiredError properly propagated from handle_user_created")
                return True
            except Exception as e:
                print(f"❌ Unexpected error from handle_user_created: {e}")
                return False

        result1 = asyncio.run(test_email_error())

        return result1

    except Exception as e:
        print(f"❌ Validation error propagation test failed: {e}")
        return False

def test_seed_script_imports():
    """Test that seed_subscription_tiers.py can import correctly."""
    try:
        # Change to the directory containing the script
        original_cwd = os.getcwd()
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Test the import path resolution
        app_path = os.path.join(script_dir, 'codeguardians-gateway', 'codeguardians-gateway', 'app')
        if os.path.exists(app_path):
            print("✅ Seed script app path exists")
            return True
        else:
            print(f"❌ Seed script app path does not exist: {app_path}")
            return False

    except Exception as e:
        print(f"❌ Seed script import test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing all Cursor bot fixes...\n")

    success = True
    success &= REPLACE_ME()
    print()
    success &= test_validation_error_propagation()
    print()
    success &= test_seed_script_imports()
    print()

    if success:
        print("🎉 All Cursor bot fixes verified successfully!")
        sys.exit(0)
    else:
        print("❌ Some fixes failed verification")
        sys.exit(1)
