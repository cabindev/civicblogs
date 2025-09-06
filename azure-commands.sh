#!/bin/bash

# Azure Cloud Shell Commands for GitHub Actions Setup
echo "🚀 Setting up Azure for GitHub Actions Auto-Deployment"

# 1. Get current subscription info
echo "📋 Current subscription information:"
az account show --output table

# 2. Get subscription ID
SUBSCRIPTION_ID=$(az account show --query id --output tsv)
echo "📋 Subscription ID: $SUBSCRIPTION_ID"

# 3. Get tenant ID  
TENANT_ID=$(az account show --query tenantId --output tsv)
echo "📋 Tenant ID: $TENANT_ID"

# 4. Create resource group (if not exists)
echo "📦 Creating resource group..."
az group create \
  --name civicblogs-rg \
  --location "Southeast Asia" \
  --output table

# 5. Create service principal for GitHub Actions
echo "🔐 Creating service principal for GitHub Actions..."
az ad sp create-for-rbac \
  --name "civicblogs-github-actions" \
  --role contributor \
  --scopes /subscriptions/$SUBSCRIPTION_ID/resourceGroups/civicblogs-rg \
  --json-auth

echo ""
echo "✅ Setup completed!"
echo ""
echo "📝 Next steps:"
echo "1. Copy the JSON output above"
echo "2. Go to GitHub Repository → Settings → Secrets and variables → Actions"
echo "3. Add these 4 secrets:"
echo "   - AZURE_CLIENT_ID (from clientId)"
echo "   - AZURE_CLIENT_SECRET (from clientSecret)"  
echo "   - AZURE_SUBSCRIPTION_ID (from subscriptionId)"
echo "   - AZURE_TENANT_ID (from tenantId)"
echo ""
echo "4. Create Azure Web App:"
echo "   az webapp create --resource-group civicblogs-rg --plan civicblogs-plan --name civicspace --runtime 'PYTHON|3.11' --deployment-source-url https://github.com/cabindev/civicblogs.git"