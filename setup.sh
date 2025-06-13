echo "mkdir -p ~/.streamlit/" > setup.sh
echo "echo \"[server]\nheadless = true\nport = \$PORT\nenableCORS = false\n\" > ~/.streamlit/config.toml" >> setup.sh
chmod +x setup.sh
