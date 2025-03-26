#!/bin/bash

# Error handling
trap 'echo "[post-install] Error on line $LINENO. Exit code: $?" >&2' ERR

echo "[post-install] Starting post-install script..."

# Determine the correct home directory
export HOME="/home/vscode"

# Source bashrc to load pyenv and nvm
source $HOME/.bashrc

# Initialize pyenv
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Install Python version from .python-version
PYTHON_VERSION=$(cat /workspaces/ai-learning/.python-version)
pyenv install "$PYTHON_VERSION"
pyenv global "$PYTHON_VERSION"

# Install poetry
pipx install poetry --python "$PYTHON_VERSION"

# Install and set default Node.js version from .nvmrc
NODE_VERSION=$(cat /workspaces/ai-learning/.nvmrc)
nvm install "$NODE_VERSION"
nvm alias default "$NODE_VERSION"
node --version

# Install yq for YAML processing
VERSION=v4.40.5
BINARY=yq_linux_arm64
wget https://github.com/mikefarah/yq/releases/download/${VERSION}/${BINARY} -O /usr/local/bin/yq && chmod +x /usr/local/bin/yq

# ===== Keycloak Configuration =====
echo "[post-install] Setting up Keycloak realm and user..."

# Keycloak setup variables
# Use service name from docker-compose since app shares network with db
KEYCLOAK_URL="http://keycloak:8080"
KEYCLOAK_ADMIN="admin"
KEYCLOAK_ADMIN_PASSWORD="admin"
REALM_NAME="local"
CLIENT_ID="openid-client"
CLIENT_SECRET=$(openssl rand -hex 16)
USER_NAME="user"
USER_PASSWORD="password"

# Wait for Keycloak to be ready
echo "[post-install] Waiting for Keycloak to be ready at $KEYCLOAK_URL"

# Keycloak 22.0.0 doesn't use the /auth path prefix anymore
# Try both with and without /auth to be sure
PATHS_TO_TRY=("/" "/admin/" "/realms/master/" "/auth/")
WORKING_PATH=""
connected=false

for path in "${PATHS_TO_TRY[@]}"; do
    echo "[post-install] Trying to connect to Keycloak at $KEYCLOAK_URL$path"
    if curl -s --max-time 5 --head --fail "$KEYCLOAK_URL$path" > /dev/null 2>&1; then
        connected=true
        WORKING_PATH="$path"
        echo "[post-install] Successfully connected to Keycloak at $KEYCLOAK_URL$path"
        break
    fi
    echo "[post-install] Path $path not accessible"
done

if [ "$connected" = false ]; then
    echo "[post-install] ERROR: Could not connect to Keycloak. Network diagnostics:"
    echo "[post-install] Current network connectivity:"
    ip addr show
    echo "[post-install] Network routes:"
    ip route
    echo "[post-install] DNS resolution for keycloak:"
    getent hosts keycloak || echo "Could not resolve keycloak"
    echo "[post-install] Trying a direct connection with verbose output:"
    curl -v --max-time 10 "$KEYCLOAK_URL"
    echo "[post-install] WARNING: Skipping Keycloak setup due to connection issues."
    echo "[post-install] Script completed successfully (without Keycloak setup)!"
    exit 0
fi

# Determine the correct token endpoint based on working path
if [[ "$WORKING_PATH" == "/auth/"* ]]; then
    # Old style with /auth prefix
    TOKEN_ENDPOINT="$KEYCLOAK_URL/auth/realms/master/protocol/openid-connect/token"
    ADMIN_ENDPOINT="$KEYCLOAK_URL/auth/admin"
else
    # New style without /auth prefix (Keycloak 17+)
    TOKEN_ENDPOINT="$KEYCLOAK_URL/realms/master/protocol/openid-connect/token"
    ADMIN_ENDPOINT="$KEYCLOAK_URL/admin"
fi

# Get admin token
echo "[post-install] Getting admin token from $TOKEN_ENDPOINT..."
AUTH_RESPONSE=$(curl -s -X POST "$TOKEN_ENDPOINT" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=$KEYCLOAK_ADMIN" \
    -d "password=$KEYCLOAK_ADMIN_PASSWORD" \
    -d "grant_type=password" \
    -d "client_id=admin-cli")

echo "[post-install] Auth response: $AUTH_RESPONSE"
ADMIN_TOKEN=$(echo "$AUTH_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$ADMIN_TOKEN" ]; then
    echo "[post-install] Failed to get admin token. Verbose response:"
    curl -v -X POST "$TOKEN_ENDPOINT" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=$KEYCLOAK_ADMIN" \
        -d "password=$KEYCLOAK_ADMIN_PASSWORD" \
        -d "grant_type=password" \
        -d "client_id=admin-cli"
    echo "[post-install] Check Keycloak credentials and endpoint."
    echo "[post-install] Script completed successfully (without Keycloak setup)!"
    exit 0
fi

echo "[post-install] Successfully obtained admin token!"

# Create realm
echo "[post-install] Creating realm '$REALM_NAME'..."
REALM_RESPONSE=$(curl -s -X POST "$ADMIN_ENDPOINT/realms" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"realm\":\"$REALM_NAME\",\"enabled\":true}")

echo "[post-install] Realm creation response: $REALM_RESPONSE"

# Create client
echo "[post-install] Creating client '$CLIENT_ID'..."
CLIENT_RESPONSE=$(curl -s -X POST "$ADMIN_ENDPOINT/realms/$REALM_NAME/clients" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
        \"clientId\": \"$CLIENT_ID\",
        \"enabled\": true,
        \"protocol\": \"openid-connect\",
        \"redirectUris\": [\"*\"],
        \"publicClient\": false,
        \"clientAuthenticatorType\": \"client-secret\",
        \"secret\": \"$CLIENT_SECRET\",
        \"standardFlowEnabled\": true,
        \"directAccessGrantsEnabled\": true
    }")

echo "[post-install] Client creation response: $CLIENT_RESPONSE"

# Create user
echo "[post-install] Creating user '$USER_NAME'..."
USER_RESPONSE=$(curl -s -X POST "$ADMIN_ENDPOINT/realms/$REALM_NAME/users" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
        \"username\": \"$USER_NAME\",
        \"enabled\": true,
        \"emailVerified\": true,
        \"credentials\": [{
            \"type\": \"password\",
            \"value\": \"$USER_PASSWORD\",
            \"temporary\": false
        }]
    }")

echo "[post-install] User creation response: $USER_RESPONSE"

echo "[post-install] Keycloak configuration completed!"
echo "[post-install] Realm: $REALM_NAME"
echo "[post-install] Client: $CLIENT_ID"
echo "[post-install] Client Secret: $CLIENT_SECRET"
echo "[post-install] User: $USER_NAME / $USER_PASSWORD"

echo "[post-install] Script completed successfully!"
