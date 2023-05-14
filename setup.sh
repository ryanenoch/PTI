mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[browser]\n\
gatherUsageStats = false\n\
" > ~/.streamlit/config.toml
