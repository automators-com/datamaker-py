#!/usr/bin/env python3
"""Demo script showing DataMaker client usage and testing."""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))

from datamaker.main import DataMaker
from datamaker.error import DataMakerError


def demo_client_usage():
    """Demonstrate basic DataMaker client usage."""
    print("DataMaker Python Client Demo")
    print("=" * 40)

    # Initialize client with API key
    api_key = "dm-36f19f0a3528686ee6686d5304a1b72869c4c7a99e736ff0d45b47705be86ba4"
    client = DataMaker(api_key=api_key)

    print(f"✅ Client initialized successfully")
    print(f"📡 Base URL: {client.base_url}")
    print(f"🔑 API Key: {client.api_key[:20]}...")
    print()

    # Test basic functionality
    print("Testing basic functionality...")

    try:
        # Test API key validation
        print("🔍 Testing API key validation...")
        result = client.validate_api_key()
        print(f"✅ API key is valid: {result}")
    except DataMakerError as e:
        print(f"❌ API key validation failed: {e}")
        print("   This is expected if the API key is invalid or expired.")

    try:
        # Test getting current user
        print("👤 Testing get current user...")
        user = client.get_current_user()
        print(f"✅ Current user: {user}")
    except DataMakerError as e:
        print(f"❌ Get current user failed: {e}")

    try:
        # Test getting templates
        print("📋 Testing get templates...")
        templates = client.get_templates()
        print(f"✅ Found {len(templates)} templates")
        if templates:
            print(f"   Sample template: {templates[0]['name']}")
    except DataMakerError as e:
        print(f"❌ Get templates failed: {e}")

    try:
        # Test getting projects
        print("📁 Testing get projects...")
        projects = client.get_projects()
        print(f"✅ Found {len(projects)} projects")
        if projects:
            print(f"   Sample project: {projects[0]['name']}")
    except DataMakerError as e:
        print(f"❌ Get projects failed: {e}")

    print()
    print("Demo completed!")


def demo_template_creation():
    """Demonstrate template creation and data generation."""
    print("\nTemplate Creation and Data Generation Demo")
    print("=" * 50)

    api_key = "dm-36f19f0a3528686ee6686d5304a1b72869c4c7a99e736ff0d45b47705be86ba4"
    client = DataMaker(api_key=api_key)

    # Create a sample template
    template_data = {
        "name": "Demo Template",
        "fields": [
            {"name": "firstName", "type": "firstName"},
            {"name": "lastName", "type": "lastName"},
            {"name": "email", "type": "email"},
            {"name": "company", "type": "companyName"},
            {"name": "phone", "type": "phoneNumber"},
        ],
        "quantity": 3,
    }

    try:
        print("📝 Creating template...")
        created_template = client.create_template(template_data)
        print(f"✅ Template created with ID: {created_template['id']}")

        # Generate data from the template
        print("🎲 Generating data...")
        generated_data = client.generate(created_template)
        print(f"✅ Generated {len(generated_data)} records")

        # Display sample data
        if generated_data:
            print("\nSample generated data:")
            for i, record in enumerate(generated_data[:2], 1):
                print(f"  Record {i}: {record}")

        # Clean up - delete the template
        print("\n🧹 Cleaning up...")
        delete_result = client.delete_template(created_template["id"])
        print(f"✅ Template deleted successfully")

    except DataMakerError as e:
        print(f"❌ Template operations failed: {e}")
        print("   This is expected if the API key is invalid or expired.")


if __name__ == "__main__":
    demo_client_usage()
    demo_template_creation()
